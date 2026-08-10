# hermes-agent-custom

> 本库为 **Hermes 自定义版**——基于汉化库 main 深度定制。

## 汉化库说明

本库基于汉化库构建——请查看 [hermes-agent 汉化版 README](https://github.com/ArtomYuan/hermes-agent)——本库在汉化库基础上进行了个性化定制。

## 自定义改动（与汉化版差异）

- 4 按钮终末地风格（允许/本轮/始终/拒绝）
- smart escalate（LLM 判安全也升级管理员）
- LLM 中文描述（desc_cn/risk_cn）
- 审批弹窗排版（代码框→操作→安全评估）

## 部署

```bash
git clone -b custom https://github.com/ArtomYuan/hermes-agent-custom.git
```

## 更新记录

每次改动在文末追加记录并更新版本号。

### v2026.8.3（2026-08-09）——custom 分支建立（当前）

- 仓库创建 + custom 分支建立（含全部自定义改动）
- README 重构：汉化库 README 超链接 + 自定义改动说明 + 更新记录
