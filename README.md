# hermes-agent-custom（私有备份库）

> 本库只保留 **custom 分支**——运行环境源码（汉化库 main + 功能补丁）。

## 汉化库说明

本库基于汉化库构建——请查看 [hermes-agent 汉化版 README](https://github.com/ArtomYuan/hermes-agent)——本库的 custom 分支在该汉化库 main 基础上叠加功能补丁。

## custom 改动（相对汉化库）

- dm 审批修复（QQ 私聊按钮回调 chat_type 兼容）
- 4 按钮终末地风格（允许/本轮/始终/拒绝）
- smart escalate（LLM 判安全也升级管理员）
- LLM 中文描述（desc_cn/risk_cn）
- 审批弹窗排版（代码框→操作→安全评估）
- i18n 汉化层（translator + zh-CN.json，与 main 同步）

完整补丁记录：~/.hermes/docs/hermes/custom-patches.md（内网 docs）

## 部署

```bash
git clone -b custom https://github.com/ArtomYuan/hermes-agent-custom.git
```

## 更新记录

每次改动在文末追加记录并更新版本号。

### v2026.8.3（2026-08-09）——custom 分支建立（当前）

- 私有库创建 + custom 分支备份（含全部功能补丁 + i18n 层）
- README 重构：汉化库 README 超链接 + custom 改动说明 + 更新记录
