# 第15章：最佳实践与反模式

> "经验是你犯错后给它起的名字。" —— Oscar Wilde

在前14章中，我们从零构建了完整的Agent系统：从单一Agent到Multi-Agent Team，从简单的定时任务到复杂的自主决策，从本地实验到生产部署。

但知道"怎么做"不等于"做得好"。这一章将总结真实项目中的血泪教训，告诉你什么该做（Do's）、什么不该做（Don'ts），以及如何让你的Agent系统持续演进。

---

## 15.1 Do's：七条最佳实践

### 1. ✅ 从简单开始，渐进复杂

**原则**：先让一个Agent在一个任务上工作良好，再考虑Multi-Agent。

**反例**：直接上来设计7个Agent的复杂系统，结果3个月后还在调试协调逻辑。

**正例**：

```
第1周：单Agent实现Morning Briefing（手动触发）
第2周：添加Cron自动运行
第3周：优化输出格式，添加个性化
第4周：考虑是否需要拆分成多Agent（研究+总结）
```

**为什么有效**：
- 快速获得可用的成果（正反馈）
- 每个阶段的问题都可控
- 容易回滚（最多损失一周的工作）

**案例**：Self-healing Server（第1章、第6章、第11章多次讨论）

```
迭代路径：
v1.0：单个Cron job，检查一个服务，重启它（1天完成）
v1.5：添加5个服务的检查（1周完成）
v2.0：Agent分析日志，生成诊断（2周完成）
v2.5：Agent自动生成修复命令（1周完成）
v3.0：15个Cron job覆盖全栈（1周完成）

总计：6周，每周都有可用版本
```

如果一开始就设计v3.0，可能需要3个月，且中间无可用版本。

> 💡 **AI辅助提示**
> 不确定你的想法是否太复杂？问AI：
> "我想实现[你的想法]，如何分解成5个渐进的版本？每个版本应该实现什么核心功能？"

### 2. ✅ 文件作为接口，Git作为真相源

**原则**：Agent之间通过文件通信，所有配置和状态都在Git中。

**为什么**：
- **可审计**：Git历史记录了所有改动
- **可回滚**：任何时候都能回到之前的状态
- **可协作**：多人可以同时改进Agent
- **可复现**：新环境只需git clone + 配置凭证

**标准目录结构**：

```
~/agents/
├── .git/                    # Git仓库
├── README.md                # 项目文档
├── config/
│   ├── agents.yaml          # Agent配置
│   ├── cron.yaml            # 定时任务
│   └── credentials.yaml.example  # 凭证模板（不含真实值）
├── prompts/
│   ├── system/
│   │   ├── research.md
│   │   └── writer.md
│   └── templates/
│       └── morning-briefing.md
├── skills/
│   ├── search/
│   │   ├── SKILL.md
│   │   └── search.py
│   └── summarize/
├── state/
│   ├── tasks/
│   │   └── task-{id}.yaml
│   └── memory/
│       └── {date}.jsonl
└── logs/
    └── agent-{name}.jsonl
```

**Git工作流**：

```bash
# 每次改动Agent配置
$ git add config/agents.yaml
$ git commit -m "chore: 将research agent切换到gemini-flash以降低成本"

# 部署到生产
$ git push origin main
$ ssh prod-server "cd ~/agents && git pull && ./reload.sh"

# 出问题？立即回滚
$ git revert HEAD
$ git push origin main
```

**案例**：Autonomous PM（第5章、第10章深入）

```
状态文件：state/project-{id}.yaml

# v1: 纯手工维护
status: in-progress
tasks:
  - "实现用户登录"
  - "设计数据库"

# v2: Agent自动更新（每次运行后commit）
status: in-progress
tasks:
  - id: task-001
    title: "实现用户登录"
    status: completed
    completed_at: 2024-01-15T10:30:00Z
  - id: task-002
    title: "设计数据库"
    status: in-progress
    assigned_to: dev-agent

# Git历史自动记录了项目进展
$ git log --oneline state/project-alpha.yaml
abc1234 chore(pm): task-001 completed
def5678 chore(pm): task-002 started
...
```

> 🔧 **遇到错误？**
> Git历史混乱了？试试这个清理策略：
> "我的Agent系统的Git历史有大量自动commit，如何清理和压缩？需要保留哪些信息？"

### 3. ✅ 安全纵深防御

**原则**：永远假设某一层会被攻破，设计多层防护。

**最小安全清单**：

```yaml
# 1. 凭证隔离（第7章深入讨论）
credentials:
  storage: external_service  # Vault, 1Password, AWS Secrets Manager
  access: per-agent          # 每个Agent只能访问必要的凭证
  rotation: automatic        # 定期自动轮换

# 2. 权限最小化
agents:
  research:
    permissions:
      - read:web
      - read:files:/data/public/*
    denied:
      - write:*
      - execute:*
  
  deployment:
    permissions:
      - execute:ssh:prod-server-1
      - write:files:/deploy/*
    denied:
      - read:credentials
      - execute:sudo

# 3. 审计日志
audit:
  log_all_actions: true
  alert_on:
    - permission_denied
    - credential_access
    - sudo_execution
    - sensitive_file_access
  retention_days: 90

# 4. 沙箱执行
execution:
  sandbox: docker  # 或Firecracker, gVisor
  network: restricted
  filesystem: read-only (except /tmp)
```

**真实案例**：API Key泄露事件（多个团队遇到）

```
事故经过：
1. 开发者在Agent prompt中硬编码了API Key
2. Agent的输出被记录到公开的Discord频道
3. 输出中包含了原始prompt（debug模式）
4. API Key泄露 → 被滥用 → $2000账单

防御层（应该有的）：
第1层：凭证应该在环境变量或Vault中 ✅
第2层：Prompt不应该包含敏感信息 ✅
第3层：输出应该过滤敏感内容 ✅
第4层：API应该有支出限额 ✅
第5层：监控异常调用模式 ✅

任何一层生效都能避免损失
```

> 📚 **深入学习**
> 想系统学习Agent安全？问AI：
> "AI Agent系统有哪些独特的安全风险？如何设计威胁模型？"

### 4. ✅ 可观测优先（Observability-First）

**原则**：从第一行代码开始就添加日志、Metrics、Traces，不要等到出问题。

**代码模板**：

```python
# 每个Agent的标准框架
class ObservableAgent:
    def __init__(self, name):
        self.name = name
        self.logger = AgentLogger(name)
        self.metrics = AgentMetrics(name)
        self.tracer = get_tracer(name)
        
    def execute(self, task):
        task_id = generate_task_id()
        
        with self.tracer.start_span("execute") as span:
            self.metrics.invocations.inc()
            self.logger.log_invocation(task_id, task)
            
            try:
                result = self._do_work(task)
                self.metrics.success.inc()
                self.logger.log_completion(task_id, result)
                return result
            except Exception as e:
                self.metrics.failure.inc()
                self.logger.log_error(task_id, e)
                raise
```

这样即使是新Agent，第一次运行就有完整的可观测性。

**对比**：

| 方式 | 可观测性后加 | 可观测性先行 |
|------|--------------|--------------|
| 第1次出问题 | "日志在哪？" | 立即定位 |
| 调试时间 | 2-4小时 | 10-30分钟 |
| 线索完整度 | 50% | 95% |
| 团队信心 | 低（不敢改） | 高（有数据支撑） |

> 💡 **AI辅助提示**
> 不确定该记录什么日志？问AI：
> "对于[你的Agent类型]，应该记录哪些关键事件和指标？给我一个最佳实践的checklist。"

### 5. ✅ 定期审查和优化

**原则**：每月或每季度Review你的Agent系统，删除不用的、优化低效的。

**审查清单**：

```markdown
## 月度Agent健康检查

### 使用情况
- [ ] 哪些Agent使用频率最高？
- [ ] 哪些Agent超过30天未被调用？（考虑下线）
- [ ] 调用模式有变化吗？（早晚高峰、周末差异）

### 成本分析
- [ ] 哪个Agent成本最高？
- [ ] 是否有优化空间？（换模型、裁剪上下文）
- [ ] ROI是否合理？（价值 vs 成本）

### 质量评估
- [ ] 用户反馈如何？
- [ ] 成功率趋势（上升/下降）？
- [ ] 有没有重复性问题？

### 技术债务
- [ ] 哪些prompt需要重构？
- [ ] 哪些配置文件过于复杂？
- [ ] 有没有硬编码的临时修复？

### 安全审计
- [ ] 凭证是否定期轮换？
- [ ] 权限是否最小化？
- [ ] 审计日志是否异常？
```

**案例**：Content Factory优化（第4章、第5章、第9章多次提及）

```
初始设计（第1季度）：
- 5个Agent，全用Claude Opus
- 月成本：$2,000
- 产出：100篇文章
- ROI：694%

第一次审查（第2季度）：
发现：Research Agent消耗50%成本，但不需要推理
优化：切换到Gemini Flash
结果：成本降到$700，质量不变

第二次审查（第3季度）：
发现：30%的文章是重复主题
优化：添加主题去重Agent（用Haiku，仅$5/月）
结果：内容质量提升，用户投诉减少40%

第三次审查（第4季度）：
发现：Marketing Agent的SEO建议90%相同
优化：模板化+缓存，月调用减少80%
结果：成本进一步降到$450
```

三次优化后：**成本降77%，质量提升**。

### 6. ✅ 文档化设计决策

**原则**：用ADR（Architecture Decision Records）记录"为什么"。

**模板**：

```markdown
# ADR-005: 为什么Research Agent用Gemini而不是Claude

**日期**：2024-03-15
**状态**：已采纳
**决策者**：@修行人

## 背景
Research Agent每天调用2000+次，主要做信息检索和提取，成本占整个系统的50%。

## 考虑的方案

### 方案1：继续用Claude Opus
- 优点：质量最高
- 缺点：成本高（$960/月）

### 方案2：切换到Claude Haiku
- 优点：成本低（$24/月）
- 缺点：质量下降明显（A/B测试准确率-15%）

### 方案3：切换到Gemini Flash
- 优点：成本低（$24/月），速度快
- 缺点：需要适配新API

## 决策
选择方案3：Gemini Flash

## 理由
- A/B测试显示质量仅下降3%（可接受）
- 成本降低97%（$960 → $24）
- 响应速度提升50%
- Gemini的超长上下文（1M tokens）适合大规模检索

## 后果
- 需要重写API调用代码（预计2小时）
- 需要调整prompt以适配Gemini（预计1天）
- 节省成本可以用于其他实验

## 后续
- 监控切换后的质量指标
- 如果质量下降超过5%，回滚到Claude Sonnet（折中方案）
```

**为什么重要**：
- 6个月后你不会记得为什么这样设计
- 新团队成员能快速理解系统
- 避免重复犯错（"我们试过，不行"）

> 🔧 **遇到错误？**
> 不知道该记录哪些决策？问AI：
> "什么样的技术决策值得写ADR？给我5个真实项目的ADR示例。"

### 7. ✅ 主动监控和告警

**原则**：不要等用户报告问题，让系统主动告诉你。

**核心告警**：

```yaml
# alerts.yaml
alerts:
  # 成功率告警
  - name: agent_success_rate_low
    condition: success_rate < 0.95
    window: 1h
    severity: high
    action: notify_slack
    
  # 延迟告警
  - name: agent_latency_high
    condition: p95_latency > 10s
    window: 5m
    severity: medium
    action: notify_telegram
    
  # 成本告警
  - name: daily_cost_spike
    condition: daily_cost > avg(7d) * 1.5
    window: 1d
    severity: high
    action: notify_email + pause_non_critical_agents
    
  # 错误率告警
  - name: error_rate_spike
    condition: error_rate > 0.1
    window: 15m
    severity: critical
    action: page_oncall
    
  # 异常模式告警
  - name: unusual_invocation_pattern
    condition: hourly_invocations > avg(24h) * 3
    window: 1h
    severity: medium
    action: notify_slack
```

**真实案例**：凌晨API故障（Self-healing Server）

```
02:15 - API提供商故障，Agent开始失败
02:16 - 告警触发：error_rate_spike
02:17 - Telegram通知：⚠️ Agent失败率达到80%
02:18 - 查看Dashboard，发现API返回503
02:20 - 手动切换到备用API提供商
02:25 - 系统恢复正常

如果没有告警：
08:00 - 用户发现服务器宕机
08:30 - 开始调查（已经停机6小时）
```

**告警设计原则**：
- ✅ 可操作（告警应该说明"接下来该做什么"）
- ✅ 分级（不是所有问题都需要半夜叫醒你）
- ✅ 去重（同一问题不要连发10条告警）
- ❌ 避免"狼来了"（告警太多会被忽略）

---

## 15.2 Don'ts：七条反模式

### 1. ❌ 一开始就全自动化

**问题**：完全没有人工审查，Agent自主做所有决策。

**后果**：

```
案例：全自动发布Agent
- Agent每天生成内容并自动发布到社交媒体
- 某天Agent理解错误，发布了不当内容
- 用户大量投诉，品牌受损
- 需要手动删除+公开道歉

根本原因：
没有"人工审查"这一环节
```

**正确做法**：渐进式自动化

```
Level 1：Agent生成，人工审查后发布（100%人工）
Level 2：Agent生成+自评分，高分自动发布，低分人工审查（80%自动）
Level 3：运行3个月无问题后，全自动（95%自动，随机抽查5%）
```

**何时可以全自动**：
- ✅ 可逆操作（如发送通知，可以撤回）
- ✅ 低风险任务（如信息检索）
- ✅ 有多层校验（如Self-healing先诊断，再确认，再执行）
- ❌ 不可逆操作（如删除数据、资金转账）
- ❌ 涉及用户敏感信息
- ❌ 品牌形象相关

> 💡 **AI辅助提示**
> 不确定你的任务是否适合全自动？问AI：
> "我想让Agent自动[具体任务]，有哪些潜在风险？如何设计安全阀？"

### 2. ❌ 单Agent做所有事

**问题**："超级Agent"试图处理所有类型的任务。

**症状**：

```python
# 一个Agent的prompt长达5000字
You are a super agent that can:
1. Research information from the web
2. Write content in 10 different styles
3. Manage your calendar
4. Send emails
5. Analyze data
6. Generate code
7. ... (还有20项)
```

**后果**：
- 质量下降（模型难以专注）
- 难以调试（不知道哪个能力失效）
- 成本高（每次都加载全部能力）
- 难以优化（无法针对性改进）

**正确做法**：专业化Agent

```python
# 拆分成多个专家Agent
agents = {
    "research": ResearchAgent(),      # 专注检索
    "writer": WriterAgent(),          # 专注写作
    "analyst": AnalystAgent(),        # 专注分析
    "coordinator": CoordinatorAgent() # 编排调度
}

def handle_task(task):
    # Coordinator决定派给谁
    agent = coordinator.route(task)
    return agent.execute(task)
```

**案例**：Content Factory（第4章、第9章深入）

```
初版：单个ContentAgent（失败）
- 一个Agent负责选题、研究、写作、编辑
- prompt长达4000字
- 输出质量不稳定

重构：5个专业Agent（成功）
- Strategy Agent：选题和规划
- Research Agent：信息收集
- Writer Agent：内容创作
- Editor Agent：审查和优化
- Marketing Agent：SEO和分发

结果：质量提升30%，成本降低40%
```

### 3. ❌ 硬编码凭证

**问题**：API Key、密码直接写在代码或配置文件里。

**为什么这是灾难**：

```python
# ❌ 绝对不要这样
OPENAI_API_KEY = "sk-proj-abc123..."  
DATABASE_PASSWORD = "SuperSecret123"

# 你以为安全，但：
1. Git历史永久记录（即使后来删除）
2. 代码分享/截图时容易泄露
3. 日志/错误信息可能包含
4. 多人协作时暴露给所有人
```

**真实事故**：

```
某团队将Agent代码上传到GitHub（private repo）
3个月后，repo设置误改为public
2小时内，API Key被扫描到
12小时内，$3000额度被刷光
```

**正确做法**：永远从环境变量或密钥管理服务读取

```python
# ✅ 正确方式
import os
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("缺少环境变量：OPENAI_API_KEY")
```

或使用专业工具（第7章深入讨论）：

```python
# 使用Vault
from hvac import Client
vault = Client(url='https://vault.example.com')
OPENAI_API_KEY = vault.read('secret/openai')['api_key']
```

> 🔧 **遇到错误？**
> 已经不小心提交了凭证到Git？立即：
> 1. 撤销该凭证（重新生成API Key）
> 2. 用`git filter-branch`或`BFG Repo-Cleaner`清理历史
> 问AI："如何从Git历史中完全删除敏感信息？"

### 4. ❌ 没有回滚机制

**问题**：Agent修改了状态，但出错后无法恢复。

**案例**：数据库自动清理Agent

```python
# ❌ 危险实现
def cleanup_old_records():
    records = db.query("SELECT * FROM logs WHERE created_at < '30 days ago'")
    for record in records:
        db.delete(record)  # 不可逆！
    
# 结果：误删除了重要数据，无法恢复
```

**正确做法**：先备份，再操作，可回滚

```python
# ✅ 安全实现
def cleanup_old_records():
    # 1. 先备份
    records = db.query("SELECT * FROM logs WHERE created_at < '30 days ago'")
    backup_file = f"backup_{datetime.now()}.json"
    save_json(backup_file, records)
    
    # 2. 软删除（标记）
    for record in records:
        db.update(record, {"deleted": True, "deleted_at": datetime.now()})
    
    # 3. 等待24小时确认
    # 4. 真正删除（在另一个定时任务中）
    
def permanent_delete():
    # 只删除24小时前标记的
    db.delete("WHERE deleted=True AND deleted_at < '24 hours ago'")
```

**回滚策略**：

| 操作类型 | 推荐策略 |
|---------|---------|
| 文件修改 | Git自动commit（可回滚） |
| 数据库写入 | 软删除+延迟删除 |
| API调用 | 幂等设计（可重试） |
| 发布内容 | 草稿模式+定时发布 |
| 系统配置 | 先备份+可切换 |

### 5. ❌ 忽略日志和审计

**问题**：Agent做了什么，完全没记录。

**后果**：

```
用户："为什么Agent删除了我的文件？"
你："呃...让我看看..."
（没有日志）
你："我也不知道...可能是误操作？"
用户：💢
```

**最小审计要求**：

```python
# 对于任何"写操作"，必须记录
audit_log = {
    "timestamp": "2024-03-15T10:30:00Z",
    "agent": "cleanup_agent",
    "action": "delete_file",
    "target": "/data/old_logs/2023-01.log",
    "reason": "file older than 90 days",
    "user": "system",
    "result": "success"
}
```

**关键原则**：
- ✅ 记录所有"写"操作（修改、删除、发送）
- ✅ 记录决策依据（"为什么"）
- ✅ 保留足够长时间（至少30天）
- ✅ 支持按时间/Agent/操作类型查询

### 6. ❌ 过度工程化简单任务

**问题**：为只需运行5次的任务设计复杂的Multi-Agent系统。

**案例**：一次性数据迁移

```
任务：将100个Markdown文件转成HTML

❌ 过度设计：
- Orchestrator Agent（调度）
- Reader Agent（读取文件）
- Parser Agent（解析Markdown）
- Converter Agent（转换HTML）
- Writer Agent（写入文件）
- Validator Agent（验证）
开发时间：2周

✅ 简单方案：
import markdown
for file in glob("*.md"):
    html = markdown.markdown(open(file).read())
    open(file.replace(".md", ".html"), "w").write(html)
开发时间：10分钟
```

**判断标准**：

| 何时用Agent | 何时不用 |
|------------|---------|
| 需要自然语言理解 | 规则明确 |
| 长期运行/重复任务 | 一次性任务 |
| 需要自主决策 | 流程固定 |
| 上下文复杂 | 输入简单 |
| 质量>速度 | 速度>完美 |

**箴言**："不要用Agent去做cron + bash能搞定的事。"

> 📚 **深入学习**
> 不确定是否需要Agent？问AI：
> "对于[你的任务]，传统脚本 vs Agent系统，各有什么优劣？给我一个决策树。"

### 7. ❌ 不测试就部署到生产

**问题**：在生产环境直接实验新Agent或新prompt。

**案例**：营销邮件Agent直接上生产

```
场景：新开发的Email Agent，未测试就设置为自动发送
结果：
- 第1封：称呼错误（"Dear {{name}}"）
- 第2封：链接失效
- 第3封：语气过于随意（"Yo dude!"）
- 发送了200封才发现问题
- 取消订阅率暴增30%
```

**正确测试流程**：

```
1. 本地测试（开发环境）
   - 输入：5-10个手工case
   - 输出：人工检查质量
   
2. Staging环境（模拟真实数据）
   - 输入：100个真实样本
   - 输出：自动化检查+人工抽查
   
3. 灰度发布（小流量）
   - 5%流量走新Agent
   - 95%流量走旧Agent
   - 监控指标对比
   
4. 全量发布
   - 确认质量无退化
   - 逐步切量（5% → 25% → 50% → 100%）
```

**自动化测试示例**：

```python
# test_agent.py
def test_morning_briefing():
    # 固定输入
    mock_data = {
        "news": ["AI突破", "市场波动"],
        "calendar": ["10:00 团队会议"],
        "weather": "晴，18°C"
    }
    
    # 调用Agent
    result = morning_briefing_agent(mock_data)
    
    # 检查输出
    assert "AI" in result
    assert "10:00" in result
    assert len(result) < 1000  # 不能太长

# 回归测试
def test_regression():
    """确保新版本不会打破旧case"""
    for case in load_test_cases():
        result = agent(case.input)
        assert similarity(result, case.expected_output) > 0.8
```

---

## 15.3 持续演进

Agent系统不是"一次性项目"，而是**活的系统**，需要持续演进。

### 健康度评估框架

**每月评估清单**：

```markdown
## Agent系统健康度评分（100分制）

### 可用性（30分）
- [ ] 成功率 > 95%（10分）
- [ ] P95延迟 < 5s（10分）
- [ ] 无重大事故（10分）

### 成本效益（20分）
- [ ] ROI > 200%（10分）
- [ ] 月成本同比下降或持平（10分）

### 代码质量（20分）
- [ ] 测试覆盖率 > 60%（10分）
- [ ] 无硬编码凭证（5分）
- [ ] 所有配置在Git中（5分）

### 可观测性（15分）
- [ ] 所有Agent有结构化日志（5分）
- [ ] 关键指标有Dashboard（5分）
- [ ] 告警配置完整（5分）

### 安全性（15分）
- [ ] 凭证定期轮换（5分）
- [ ] 权限最小化（5分）
- [ ] 审计日志完整（5分）

**总分**：____/100

- 90-100：优秀，继续保持
- 70-89：良好，有改进空间
- 50-69：及格，需要重点优化
- <50：危险，建议重构
```

### 何时重构

**重构信号**：

```
🚨 立即重构：
- 成功率 < 90%持续1周
- 单个Agent prompt > 10,000字
- 无法解释的质量下降
- 维护成本 > 重构成本

⚠️ 计划重构：
- 添加新功能需要修改3+个Agent
- Prompt调整频繁（每周>2次）
- 技术债务积累（超过10个TODO）

✅ 可以缓一缓：
- 系统运行正常
- ROI健康
- 用户满意
```

**重构策略**：

```python
# 增量重构（推荐）
while True:
    # 1. 识别最痛的点
    pain_point = identify_biggest_issue()
    
    # 2. 制定小步计划
    plan = break_into_small_steps(pain_point)
    
    # 3. 逐步替换
    for step in plan:
        implement(step)
        test()
        if ok:
            deploy()
        else:
            rollback()
    
    # 4. 重复
    if system_health_score > 90:
        break
```

**案例**：Multi-Agent Team的渐进式重构（第4章、第5章）

```
初版问题：
- 5个Agent全用Opus，成本$2,000/月
- 协调通过共享文件，经常冲突
- 无监控，出问题靠猜

重构路径（6个月）：

月1：添加可观测性
  → 所有Agent加日志
  → 建立Dashboard
  → 识别瓶颈（Research Agent成本最高）

月2-3：优化成本
  → Research切换到Gemini（节省$900/月）
  → 启用Prompt Caching（节省$200/月）
  
月4：改进协调
  → 引入中央协调器
  → 状态从文件迁移到Redis
  → 冲突减少90%

月5-6：持续优化
  → 添加自动化测试
  → 优化其他Agent模型
  → 最终成本降到$450/月

结果：成本降78%，质量提升，可维护性提升
```

### 如何扩展

**扩展方向**：

1. **横向扩展**：增加更多Agent
   ```
   当前：5个Agent处理内容生产
   扩展：+3个Agent处理内容分发
   ```

2. **纵向扩展**：增强单个Agent能力
   ```
   当前：Research Agent只搜索文本
   扩展：+图片识别 +视频分析
   ```

3. **深度扩展**：增加自主程度
   ```
   当前：Agent执行明确任务
   扩展：Agent自主发现问题并解决
   ```

**扩展检查清单**：

- [ ] 现有系统健康度 > 80分
- [ ] 新功能有明确ROI预期
- [ ] 不破坏现有功能（回归测试）
- [ ] 监控和告警已就位
- [ ] 有回滚方案

---

## 本章小结

**Do's核心**：
1. 渐进复杂
2. 文件+Git
3. 安全纵深
4. 可观测优先
5. 定期审查
6. 文档决策
7. 主动监控

**Don'ts核心**：
1. 别立即全自动
2. 别单Agent包揽
3. 别硬编码凭证
4. 别无回滚机制
5. 别忽略日志
6. 别过度工程
7. 别跳过测试

**持续演进**：
- 每月评估健康度
- 痛点驱动重构
- 增量改进，避免大爆炸
- 始终保持可回滚

**终极原则**：

> "好的Agent系统不是设计出来的，是迭代出来的。"

从简单开始，持续优化，保持健康。你的Agent系统会越来越强大、越来越可靠。

**全书总结**：

恭喜！你已经完成了从零到一的Agent工程之旅：
- 第一部分：理解Agent基础和工作流设计
- 第二部分：掌握多Agent架构和安全部署
- 第三部分：实战各类生产力和内容自动化
- 第四部分：优化、调试和最佳实践

现在，轮到你去构建改变生活的Agent系统了。

**下一步**：

- 选择一个困扰你的重复性任务
- 用本书的方法从L1开始实现
- 分享你的成果和经验
- 加入社区，持续学习

**记住**：最好的学习方式是实践。开始动手吧！ 🚀
