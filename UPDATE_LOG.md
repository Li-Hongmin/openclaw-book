# OpenClaw实战书籍更新日志

本文件记录书籍内容的自动更新历史和值得新增的主题。

---

## 2/24 18:40 - 功能更新与2026新特性

### 更新内容

**第3章（OpenClaw基础）- 新增2个小节**：

1. **3.5 Web Control UI - 浏览器控制面板** ✅
   - Control UI的启动和访问方式
   - 主要功能：实时聊天、会话管理、配置编辑、执行审批、节点管理
   - 安全配置：SSH隧道、Tailscale、Token认证
   - 实战场景：批量配置调试、敏感操作审批、多设备协作

2. **3.6 Mobile Nodes - iOS/Android 配对** ✅
   - 架构说明（Gateway ↔ Mobile Node）
   - Android/iOS配对步骤详解
   - 使用示例：动态报告显示、手机拍照、通知推送
   - Canvas实战：让Agent控制手机界面
   - 安全与隐私说明

**第4章（单Agent vs 多Agent）- 新增1个小节**：

3. **4.4 Per-Agent Security & Isolation（2026新特性）** ✅
   - Per-Agent配置的必要性和使用场景
   - Sandbox配置（mode, scope, docker.setupCommand）
   - Tools工具权限配置（allow/deny白黑名单）
   - 完整配置示例：三级权限架构（admin/family/public）
   - 调试技巧和安全最佳实践

### 发现的新功能（来自官方文档）

**已整合到书籍**：
- ✅ Web Control UI（浏览器控制面板）
- ✅ Mobile nodes配对（iOS & Android）
- ✅ Per-agent sandbox配置（v2026.1.6+）
- ✅ Per-agent tool restrictions（工具权限隔离）
- ✅ agent-to-agent messaging（需显式启用和白名单）

**可能需要补充的主题**（待后续更新）：
- [ ] **Broadcast groups**（广播群组）- 一条消息发送到多个Agent
- [ ] **Discord role-based routing**（Discord角色路由）- 根据用户角色分配Agent
- [ ] **MCP (Model Context Protocol) 集成** - 新的工具集成方式
- [ ] **Canvas A2UI** - Agent-to-UI动态界面系统深度讲解
- [ ] **Gateway Tailscale集成** - 远程访问最佳实践
- [ ] **Per-agent model overrides** - 动态切换模型

### 社区动态

- **社区规模**：OpenClaw Discord已有13,409名成员（截至2/24）
- **最新版本**：v2026.2.3（主要改进：Telegram类型安全、配置标签优化）
- **社区贡献**：
  - [Multimodal Multi-Agent System Proposal](https://medium.com/@gwrx2005/proposal-for-a-multimodal-multi-agent-system-using-openclaw-81f5e4488233)
  - [How to pair iOS & Android nodes](https://medium.com/@janaksenevirathne/how-to-pair-ios-android-nodes-with-openclaw-gateway-524cd055dd7e)
  - [OpenClaw Architecture Explained](https://ppaolo.substack.com/p/openclaw-system-architecture-overview)

### 需要关注的安全更新

- **CVE-2026-25253**：Gateway自动连接WebSocket时的Token泄露风险（已修复）
- **Session Isolation Failure**：多用户会话隔离问题（社区报告，需持续关注）
- **建议**：定期更新到最新版本，使用per-agent sandbox隔离不信任的Agent

---

## 待补充的章节主题

### 高优先级

1. **第6章（持久化与定时任务）** - 补充cron vs heartbeat的新用法
   - Cron的isolated session模式
   - Heartbeat的batch check策略
   - 定时任务的错误处理和重试机制

2. **第11章（基础设施与DevOps）** - 补充Mobile nodes在DevOps中的应用
   - 用手机Canvas显示服务器监控仪表盘
   - 手机通知集成（故障告警）
   - 远程截屏/拍照用于现场问题排查

3. **第13章（性能与成本优化）** - 补充per-agent model选择策略
   - 不同Agent使用不同模型降低成本
   - Sandbox模式对性能的影响
   - Scope: agent vs shared的资源消耗对比

### 中优先级

4. **附录A（快速参考）** - 补充新的配置选项
   - Per-agent sandbox配置速查表
   - Tools权限矩阵
   - Binding规则优先级

5. **第7章（安全边界与风险管理）** - 深化安全主题
   - Per-agent isolation实战案例
   - 多用户共享Gateway的安全架构
   - CVE案例分析和防护措施

### 低优先级（需求驱动）

6. **新章节候选**：《Canvas与动态UI》
   - Canvas系统深度讲解
   - A2UI协议详解
   - 实战：构建Agent控制的仪表盘

7. **新章节候选**：《MCP与外部工具集成》
   - Model Context Protocol介绍
   - 如何开发自定义MCP服务器
   - 与LangChain、AutoGPT等框架的集成

---

## 更新来源

- 官方文档：https://docs.openclaw.ai
- GitHub仓库：https://github.com/openclaw/openclaw
- 社区Discord：https://discord.com/invite/clawd
- Medium博客：搜索"OpenClaw"相关文章
- Brave Search：定期搜索"OpenClaw 2026 new features"

---

## 下次更新计划

**时间**：2-3天后（2/27左右）

**重点方向**：
1. 搜索OpenClaw Discord的#announcements和#showcase频道
2. 查看GitHub Issues/Discussions中的高赞话题
3. 更新第6章（Cron与Heartbeat新用法）
4. 补充Canvas相关的实战案例
