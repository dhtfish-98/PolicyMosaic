"""Explicit limits for local profile inspection and optional helper processes."""
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
import io
import functools
import math
import os
from pathlib import Path
import selectors
import signal
import stat
import struct
import subprocess
import time


class PolicyFormatError(ValueError, struct.error):
    """Unsupported, incomplete, or over-limit input; no policy result implied."""


INPUT_BYTES = 64 * 1024 * 1024
OUTPUT_BYTES = 16 * 1024 * 1024
MAX_NODES = 4096
MAX_DEPTH = 128
MAX_PROFILES = 1024
MAX_STEPS = 2_000_000
MAX_ITEMS = 65536
TOTAL_REPORT_BYTES = 64 * 1024 * 1024


def _fdopen_owned(descriptor, mode):
    """Transfer ownership only after fdopen succeeds; close on construction failure."""
    try:
        return os.fdopen(descriptor, mode)
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            # Some fdopen implementations may already close on failure.
            pass
        raise


def read_exact(stream, count):
    if type(count) is not int or not 0 <= count <= INPUT_BYTES:
        raise PolicyFormatError('invalid or over-limit read length')
    pieces = []
    remaining = count
    while remaining:
        piece = stream.read(remaining)
        if not isinstance(piece, bytes) or not piece or len(piece) > remaining:
            raise PolicyFormatError('truncated binary field')
        pieces.append(piece)
        remaining -= len(piece)
    return b''.join(pieces)


def read_local(path, maximum=INPUT_BYTES):
    flags = os.O_RDONLY | os.O_NONBLOCK | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_CLOEXEC', 0)
    descriptor = os.open(os.fspath(path), flags)
    with _fdopen_owned(descriptor, 'rb') as source:
        before = os.fstat(source.fileno())
        if not stat.S_ISREG(before.st_mode) or not 0 <= before.st_size <= maximum:
            raise PolicyFormatError('input must be a regular file within the size limit')
        data = source.read(maximum + 1)
        after = os.fstat(source.fileno())
        identity = lambda value: (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns, value.st_ctime_ns)
        if len(data) > maximum or len(data) != before.st_size or identity(before) != identity(after):
            raise PolicyFormatError('input changed during reading or exceeds the size limit')
        return data


class ProfileReader(io.BytesIO):
    """Immutable caller-owned snapshot with exact finite reads and checked seeks."""
    def read(self, count=-1):
        if type(count) is not int or count < 0:
            raise PolicyFormatError('binary reads require a finite length')
        if count > len(self.getbuffer()) - self.tell():
            raise PolicyFormatError('truncated binary field')
        return super().read(count)

    def seek(self, offset, whence=0):
        end = len(self.getbuffer())
        if type(offset) is not int or whence not in (0, 1, 2):
            raise PolicyFormatError('invalid binary offset')
        position = offset + (0 if whence == 0 else self.tell() if whence == 1 else end)
        if not 0 <= position <= end:
            raise PolicyFormatError('binary offset outside input')
        return super().seek(position)


def safe_component(label):
    if not isinstance(label, str) or not label or len(label.encode('utf-8')) > 180:
        raise PolicyFormatError('invalid output name')
    # Preserve ordinary upstream names, while keeping every derived name one component.
    value = label.replace('/', '_').replace('\\', '_').replace(' ', '_')
    if value in ('.', '..') or any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise PolicyFormatError('invalid output name')
    return value


def write_exclusive(path, data, maximum=OUTPUT_BYTES):
    if type(maximum) is not int or not 0 < maximum <= INPUT_BYTES or not isinstance(data, bytes) or len(data) > maximum:
        raise PolicyFormatError('report exceeds output limit')
    active = _publication.get()
    if active is not None:
        if active[0] + len(data) > active[1]:
            raise PolicyFormatError('total report output limit reached')
        active[0] += len(data)
    destination = Path(path)
    directory = os.open(destination.parent, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0) | getattr(os, 'O_NOFOLLOW', 0))
    try:
        descriptor = os.open(destination.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600, dir_fd=directory)
        with _fdopen_owned(descriptor, 'wb') as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
    finally:
        os.close(directory)


class ReportBuffer(io.StringIO):
    def __init__(self):
        super().__init__()
        self.size = 0

    def write(self, text):
        encoded = text.encode('utf-8')
        if self.size + len(encoded) > OUTPUT_BYTES:
            raise PolicyFormatError('report exceeds output limit')
        self.size += len(encoded)
        return super().write(text)


@dataclass
class WorkBudget:
    remaining: int = MAX_STEPS
    deadline: float = 0

    def __post_init__(self):
        self.deadline = time.monotonic() + 20

    def step(self):
        self.remaining -= 1
        if self.remaining < 0 or time.monotonic() > self.deadline:
            raise PolicyFormatError('profile analysis work limit reached')


_budget = ContextVar('policymosaic_work_budget', default=None)
_publication = ContextVar('policymosaic_publication_budget', default=None)


@contextmanager
def publication_scope(maximum=TOTAL_REPORT_BYTES):
    if type(maximum) is not int or not 0 < maximum <= TOTAL_REPORT_BYTES:
        raise PolicyFormatError('invalid total report output limit')
    current = _publication.get()
    token = _publication.set(current if current is not None else [0, maximum])
    try:
        yield
    finally:
        _publication.reset(token)


@contextmanager
def bounded_analysis():
    current = _budget.get()
    token = _budget.set(current or WorkBudget())
    try:
        yield
    finally:
        _budget.reset(token)


def analysis_step():
    current = _budget.get()
    if current is not None:
        current.step()


def checked_add(left, right):
    if isinstance(left, (str, bytes, list, tuple)) and isinstance(right, type(left)):
        limit = MAX_ITEMS if isinstance(left, (list, tuple)) else OUTPUT_BYTES
        if len(left) + len(right) > limit:
            raise PolicyFormatError('analysis expansion limit reached')
    return left + right


def checked_multiply(left, right):
    sequence, number = (left, right) if isinstance(left, (str, bytes, list, tuple)) else (right, left)
    if isinstance(sequence, (str, bytes, list, tuple)) and isinstance(number, int):
        limit = MAX_ITEMS if isinstance(sequence, (list, tuple)) else OUTPUT_BYTES
        if len(sequence) * max(0, number) > limit:
            raise PolicyFormatError('analysis expansion limit reached')
    return left * right


def c_content(text):
    """Encode data as a C string body, including control and UTF-8 bytes."""
    if not isinstance(text, str) or len(text.encode('utf-8')) > OUTPUT_BYTES:
        raise PolicyFormatError('invalid or over-limit C literal')
    parts = []
    for byte in text.encode('utf-8'):
        if byte in (34, 92):
            parts.append('\\' + chr(byte))
        elif 32 <= byte <= 126:
            parts.append(chr(byte))
        else:
            parts.append('\\%03o' % byte)
    value = ''.join(parts)
    if len(value) > OUTPUT_BYTES:
        raise PolicyFormatError('C literal expansion limit reached')
    return value


def analysis_guard(function):
    @functools.wraps(function)
    def guarded(*arguments, **keywords):
        with bounded_analysis():
            analysis_step()
            return function(*arguments, **keywords)
    return guarded


def run_tool(arguments, *, timeout=30, maximum=OUTPUT_BYTES, text=False, cwd=None):
    """No shell; bounded concurrent pipe reads; terminate the process group on failure."""
    if type(timeout) not in (int, float) or not math.isfinite(timeout) or not 0 < timeout <= 300 or type(maximum) is not int or not 0 < maximum <= INPUT_BYTES:
        raise PolicyFormatError('invalid helper resource limits')
    command = [os.fspath(value) for value in arguments]
    if not command or any('\0' in value for value in command):
        raise PolicyFormatError('invalid helper invocation')
    process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, cwd=cwd, start_new_session=True)
    output = bytearray()
    errors = bytearray()
    started = time.monotonic()
    completed = False
    try:
        with selectors.DefaultSelector() as pending:
            pending.register(process.stdout, selectors.EVENT_READ, output)
            pending.register(process.stderr, selectors.EVENT_READ, errors)
            while pending.get_map():
                if time.monotonic() - started > timeout:
                    raise PolicyFormatError('helper process timed out')
                for entry, _ in pending.select(min(0.1, timeout)):
                    piece = os.read(entry.fileobj.fileno(), min(65536, maximum + 1))
                    if not piece:
                        pending.unregister(entry.fileobj)
                        continue
                    entry.data.extend(piece)
                    if len(output) + len(errors) > maximum:
                        raise PolicyFormatError('helper process output limit reached')
            try:
                return_code = process.wait(timeout=max(0.01, timeout - (time.monotonic() - started)))
            except subprocess.TimeoutExpired as error:
                raise PolicyFormatError('helper process timed out') from error
            if return_code != 0:
                raise PolicyFormatError('helper process failed')
        result = bytes(output)
        if text:
            try:
                decoded = result.decode('utf-8')
                completed = True
                return decoded
            except UnicodeDecodeError as error:
                raise PolicyFormatError('helper returned invalid UTF-8') from error
        completed = True
        return result
    finally:
        if not completed:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()
        process.stdout.close()
        process.stderr.close()
