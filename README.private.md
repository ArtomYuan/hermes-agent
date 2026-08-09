# hermes-agent-custom（私有备份库）

> 本库只保留 **custom 分支**——运行环境源码（汉化库 main + 功能补丁）。
> 汉化库 main 在公开仓库：github.com/ArtomYuan/hermes-agent

## 分支内容（custom）

基于汉化库 main 的功能补丁分支：

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

## 备份策略

- 本库 = 代码远程备份（无凭据/docs/skills——敏感数据在内网 unison）
- push 前 gitleaks 自动扫描（pre-push hook）
