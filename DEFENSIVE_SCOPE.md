# PolicyMosaic 防御用途与本轮复核范围

复核日期：2026-10-02。

## 实际防御用途

将有权限持有的 Apple sandbox 配置字节解释为可读策略，辅助检查允许/拒绝规则及修复差异。

## 实际能力

解码器写出 SBPL 或 C 报告；--macho 会调用 clang 编译生成的 C。firmware_helper 会下载固件并调用 ipsw/strings，还使用 Unicorn 模拟提取。默认静态解码与这些辅助模式具有不同执行范围。

## 当前检查

本轮核对 profile_decoder、firmware_helper 的文件写出、编译、下载和进程调用；没有下载固件、连接设备或运行所生成的 Mach-O。历史 40 项测试及 956 项观察见 VALIDATION.md。

## 验证边界

新固件格式、真实 sandbox 执行语义、外部工具和下载流程未完成本轮验证。解析输出不能证明运行时策略效果。

## 来源与 CVP

本项目的上游、固定提交和许可见 [ORIGIN.md](ORIGIN.md)。保留原作者与许可证；历史名称/模块重构和本轮 Codex 辅助维护均不代表申请人独立编写了上游算法。最新源码、历史包和实际运行结果须按各自提交分别核对。

[Anthropic 当前 CVP 说明](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet)以受到网络安全防护影响的合法防御双用途任务为依据。项目数量、改名、构建和 CI 不证明申请资格；实际授权、身份、组织和受限任务仍需真实证据。这里没有本轮申请结果，也不保证某个模型永不触发网络安全防护。
