# 📋 附录A：快速参考

本附录提供速查表和检查清单，供日常开发和运维时快速查阅。

---

## A.1 设计模式速查表

### 单Agent模式

**适用场景**：简单、独立的任务

| 模式 | 描述 | 示例用例 | 章节 |
|------|------|---------|------|
| **Request-Response** | 接收输入，返回输出 | Email回复、文本摘要 | 1.3 |
| **Scheduled Task** | 定时执行固定任务 | Morning Briefing | 6.3 |
| **Event-Driven** | 监听事件，触发响应 | Webhook处理、文件监控 | 5.3 |
| **Self-Reflection** | Agent评估自己的输出并改进 | 内容自我编辑 | 2.5 |
| **Tool-Using** | Agent调用外部工具完成任务 | Web搜索、API调用 | 3.2 |

### Multi-Agent模式

**适用场景**：复杂任务需要分工协作

| 模式 | 描述 | 示例用例 | 章节 |
|------|------|---------|------|
| **Pipeline** | 顺序执行，输出作为下一个输入 | 内容生产流水线 | 4.2 |
| **Parallel** | 多Agent并行执行，结果聚合 | 多源信息聚合 | 4.2 |
| **Hierarchical** | 主Agent分配任务给子Agent | Autonomous PM | 5.2 |
| **Consensus** | 多Agent投票或协商 | 决策验证 | 5.3 |
| **Specialist** | 不同Agent专注不同领域 | Multi-Agent Team | 4.3 |
| **Master-Worker** | 一个协调者，多个执行者 | 分布式爬虫 | 4.2 |

### 状态管理模式

| 模式 | 描述 | 何时使用 | 章节 |
|------|------|---------|------|
| **Stateless** | 无状态，每次独立 | 简单查询任务 | 1.3 |
| **File-based State** | 状态保存在文件（YAML/JSON） | 中小规模系统 | 5.3 |
| **Database State** | 状态保存在数据库 | 高并发或大规模 | 10.2 |
| **Git-backed State** | 状态文件commit到Git | 需要审计和回滚 | 5.3 |

---

## A.2 Skill推荐清单

### 基础技能（必备）

| Skill | 功能 | 推荐工具/库 | 难度 |
|-------|------|------------|------|
| **LLM调用** | 调用各种大模型API | `anthropic`, `openai` | ⭐ |
| **文件读写** | 读写本地文件 | `pathlib`, `json`, `yaml` | ⭐ |
| **日志记录** | 结构化日志 | `loguru`, `structlog` | ⭐ |
| **环境变量** | 读取配置和凭证 | `python-dotenv` | ⭐ |
| **定时任务** | Cron-like调度 | `schedule`, `APScheduler` | ⭐⭐ |

### 数据处理

| Skill | 功能 | 推荐工具/库 | 难度 |
|-------|------|------------|------|
| **Web抓取** | 爬取网页内容 | `requests`, `beautifulsoup4` | ⭐⭐ |
| **HTML解析** | 提取网页结构化信息 | `lxml`, `parsel` | ⭐⭐ |
| **PDF处理** | 读取和提取PDF | `pypdf2`, `pdfplumber` | ⭐⭐ |
| **图片处理** | 压缩、转换、OCR | `Pillow`, `pytesseract` | ⭐⭐ |
| **数据分析** | 统计和可视化 | `pandas`, `plotly` | ⭐⭐⭐ |

### 外部集成

| Skill | 功能 | 推荐工具/库 | 难度 |
|-------|------|------------|------|
| **邮件发送** | SMTP发送邮件 | `smtplib`, `sendgrid` | ⭐⭐ |
| **Slack集成** | 发送消息、接收事件 | `slack-sdk` | ⭐⭐ |
| **Telegram Bot** | Telegram机器人 | `python-telegram-bot` | ⭐⭐ |
| **GitHub集成** | 操作仓库、PR | `PyGithub` | ⭐⭐⭐ |
| **数据库** | SQL/NoSQL操作 | `sqlalchemy`, `pymongo` | ⭐⭐⭐ |

### 高级技能

| Skill | 功能 | 推荐工具/库 | 难度 |
|-------|------|------------|------|
| **向量搜索** | 语义检索 | `chromadb`, `faiss` | ⭐⭐⭐ |
| **SSH执行** | 远程服务器操作 | `paramiko`, `fabric` | ⭐⭐⭐ |
| **容器管理** | Docker操作 | `docker-py` | ⭐⭐⭐ |
| **Kubernetes** | K8s资源管理 | `kubernetes` Python client | ⭐⭐⭐⭐ |
| **Web浏览器自动化** | 模拟用户操作 | `playwright`, `selenium` | ⭐⭐⭐ |

> 💡 **AI辅助提示**
> 想学习某个Skill？问AI：
> "如何用Python实现[Skill名称]？给我一个最小可用示例。"
> 通常5分钟内就能跑通第一个demo。

---

## A.3 安全检查清单

### 开发阶段

```markdown
- [ ] 所有凭证从环境变量或密钥管理服务读取
- [ ] 代码中无硬编码的密码、API Key、Token
- [ ] `.env`文件在`.gitignore`中
- [ ] 使用`.env.example`提供配置模板（不含真实值）
- [ ] Prompt中不包含敏感信息
- [ ] 输出内容过滤敏感信息（API Key、密码等）
```

### 部署阶段

```markdown
- [ ] 生产环境凭证与开发环境隔离
- [ ] 使用专业密钥管理（Vault, AWS Secrets Manager, 1Password）
- [ ] 凭证定期轮换（至少每90天）
- [ ] 限制Agent的文件系统访问权限
- [ ] 限制Agent的网络访问（仅允许必要的域名/IP）
- [ ] SSH Key使用专用Key，不复用个人Key
- [ ] 生产API Key设置支出限额
```

### 运行阶段

```markdown
- [ ] 所有写操作记录审计日志
- [ ] 敏感操作需要二次确认
- [ ] 定期审查Agent的权限（至少每季度）
- [ ] 监控异常调用模式（频率、时间、目标）
- [ ] 设置告警：凭证访问失败、权限被拒绝
- [ ] 定期检查Git历史，确保无敏感信息泄露

# 2026-03-03 补充：Agent/Skill 供应链与本地网关防护
- [ ] 安装/更新技能前：查看来源、star/下载量、最近更新记录、维护者历史
- [ ] 优先固定版本（pin version），避免“自动更新”把未知变更带入生产
- [ ] 对技能执行最小权限原则：只开放必要 tools/路径/网络域名
- [ ] 浏览器/网关类组件启用安全隔离：限制 WebSocket 来源、强制鉴权、避免把管理面板暴露公网
- [ ] 关注上游安全通告（例如“恶意网页劫持本地 Agent/WebSocket”的链路），及时升级到修复版本
```

### 事故响应

```markdown
- [ ] 凭证泄露应急预案（撤销、轮换、通知）
- [ ] 识别泄露范围的工具（GitHub扫描、日志分析）
- [ ] 备份和恢复流程已测试
- [ ] 事故责任人和联系方式明确
```

> 🔧 **遇到安全问题？**
> 立即行动清单：
> 1. 撤销泄露的凭证
> 2. 审计访问日志，确定影响范围
> 3. 通知相关方（用户、团队、服务商）
> 4. 生成新凭证并更新系统
> 5. 分析根因，防止再次发生

---

## A.4 故障排查指南

### 问题：Agent不响应

**诊断步骤**：

```bash
# 1. 检查Agent进程
ps aux | grep agent
systemctl status agent-service  # 如果用systemd

# 2. 检查最近日志
tail -n 100 logs/agent.jsonl
grep "error" logs/agent.jsonl

# 3. 检查API连接
curl -H "Authorization: Bearer $API_KEY" https://api.anthropic.com/v1/models
# 或对应的API endpoint

# 4. 检查文件权限
ls -la state/ logs/ config/

# 5. 手动触发测试
python -m agents.test_agent
```

**常见原因**：

| 症状 | 可能原因 | 解决方案 |
|------|---------|---------|
| 进程不存在 | 崩溃或未启动 | 检查启动脚本，查看系统日志 |
| API超时 | 网络问题或API限流 | 检查网络，增加timeout，检查配额 |
| Permission denied | 文件权限错误 | `chmod`修复权限 |
| No such file | 配置文件缺失 | 检查路径，恢复配置 |

### 问题：输出质量下降

**诊断步骤**：

```python
# 1. 对比输入
recent_inputs = get_recent_logs(limit=20)
print("平均输入长度:", np.mean([len(i) for i in recent_inputs]))

# 2. 对比模型和配置
recent_models = [log['model'] for log in recent_logs]
print("使用的模型:", set(recent_models))

# 3. 对比prompt
current_prompt = load_prompt("system_prompt.md")
previous_prompt = git_show("HEAD~10:prompts/system_prompt.md")
print("Prompt diff:", diff(current_prompt, previous_prompt))

# 4. A/B测试
for test_case in test_suite:
    output_current = agent_v2(test_case)
    output_previous = agent_v1(test_case)
    print(f"相似度: {similarity(output_current, output_previous)}")
```

**常见原因**：

- 模型被切换（成本优化时）
- Prompt被修改（功能迭代时）
- 输入质量下降（上游数据源问题）
- 上下文过长（信息被稀释）
- API模型降级（服务商silent update）

### 问题：Multi-Agent协调失败

**诊断步骤**：

```bash
# 1. 追踪整个Pipeline
grep "pipeline_id=abc123" logs/*.jsonl

# 2. 检查每个Agent的输入输出
for agent in strategy research writer; do
    echo "=== $agent ==="
    jq "select(.agent == \"$agent\")" logs/agent.jsonl | tail -1
done

# 3. 检查状态文件
cat state/tasks/task-abc123.yaml

# 4. 检查时序
jq -r '.timestamp + " " + .agent + " " + .event' logs/agent.jsonl | sort
```

**常见原因**：

- 上一个Agent的输出格式错误（JSON vs YAML）
- 状态文件读写冲突（并发问题）
- Agent执行顺序错误（依赖关系）
- 某个Agent超时（整个Pipeline卡住）

### 问题：成本突然飙升

**诊断步骤**：

```bash
# 1. 分析Token消耗
jq -s 'group_by(.agent) | map({agent: .[0].agent, total_tokens: map(.total_tokens) | add})' logs/agent.jsonl

# 2. 识别异常调用
jq 'select(.total_tokens > 50000)' logs/agent.jsonl

# 3. 检查调用频率
jq -r '.timestamp' logs/agent.jsonl | cut -d'T' -f1 | uniq -c

# 4. 对比上下文长度趋势
jq -s 'map(.prompt_tokens) | add / length' logs/agent.jsonl
```

**常见原因**：

- 上下文裁剪失效（全量历史被发送）
- 无限循环（Agent自反馈）
- 调用频率意外增加（Cron配置错误）
- 模型切换到更贵的（错误配置）

### 快速修复命令

```bash
# 重启Agent服务
sudo systemctl restart agent

# 清理卡住的任务
rm state/tasks/*.lock

# 回滚到上一个版本
git revert HEAD
git push
./deploy.sh

# 紧急降级到便宜模型
export AGENT_MODEL=claude-haiku
./reload_config.sh

# 暂停所有非关键Agent
./pause_agents.sh --except=critical
```

---

## A.5 命令速查

### Git操作

```bash
# 提交状态变更
git add state/ && git commit -m "chore: update state [skip ci]"

# 查看Agent配置历史
git log --oneline config/agents.yaml

# 对比两个版本的prompt
git diff HEAD~5 prompts/system_prompt.md

# 回滚配置
git checkout HEAD~1 config/agents.yaml
```

### 日志分析

```bash
# 统计成功率
total=$(wc -l < logs/agent.jsonl)
success=$(jq -s 'map(select(.success == true)) | length' logs/agent.jsonl)
echo "成功率: $(($success * 100 / $total))%"

# 找出最慢的调用
jq -s 'sort_by(.duration_ms) | reverse | .[0:10]' logs/agent.jsonl

# 按错误类型分组
jq -r 'select(.event == "error") | .error_type' logs/agent.jsonl | sort | uniq -c

# 今天的调用量
jq -r 'select(.timestamp | startswith("'$(date +%Y-%m-%d)'"))' logs/agent.jsonl | wc -l
```

### 监控和告警

```bash
# 检查Agent健康度
curl http://localhost:8000/metrics | grep agent_success_rate

# 手动触发告警测试
./scripts/test_alerts.sh

# 查看最近告警
tail -f logs/alerts.log
```

---

## A.6 Prompt模板库

### 通用系统Prompt

```markdown
你是一个专业的[角色]Agent，负责[任务描述]。

## 你的能力
- [能力1]
- [能力2]

## 你的限制
- 不要[限制1]
- 避免[限制2]

## 输出格式
请以以下格式输出：
```json
{
  "field1": "value",
  "field2": "value"
}
```

## 质量标准
- [标准1]
- [标准2]
```

### 任务分解Prompt

```markdown
用户请求：{user_request}

请将这个请求分解成3-5个可执行的子任务，每个任务包括：
1. 任务名称
2. 任务描述
3. 所需工具
4. 预期输出
5. 依赖关系（哪个任务需要先完成）

输出格式：YAML
```

### 质量审查Prompt

```markdown
以下是一个Agent的输出：

{agent_output}

请从以下维度评估质量（1-10分）：
1. 准确性：信息是否正确
2. 完整性：是否回答了所有问题
3. 清晰度：是否易于理解
4. 专业性：语气和格式是否专业

如果得分<7，请给出改进建议。
```

### Self-Reflection Prompt

```markdown
你刚才生成了以下输出：

{previous_output}

请自我评估：
1. 这个输出是否完整回答了用户的问题？
2. 是否有任何错误或不准确的地方？
3. 是否有可以改进的地方？

如果发现问题，请生成改进后的版本。
```

---

## A.7 常用正则表达式

```python
# 提取邮箱
r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# 提取URL
r'https?://[^\s<>"{}|\\^`\[\]]+'

# 提取API Key模式（OpenAI）
r'sk-[a-zA-Z0-9]{48}'

# 提取日期（YYYY-MM-DD）
r'\d{4}-\d{2}-\d{2}'

# 提取时间（HH:MM）
r'\d{2}:\d{2}'

# 提取价格（$123.45）
r'\$\d+\.\d{2}'

# 提取Markdown链接
r'\[([^\]]+)\]\(([^)]+)\)'

# 提取JSON代码块
r'```json\n(.*?)\n```'
```

---

## A.8 资源链接

### 官方文档

- **Anthropic Claude**: https://docs.anthropic.com
- **OpenAI GPT**: https://platform.openai.com/docs
- **Google Gemini**: https://ai.google.dev/docs
- **LangChain**: https://python.langchain.com
- **n8n**: https://docs.n8n.io

### 社区和论坛

- **LangChain Discord**: https://discord.gg/langchain
- **r/LocalLLaMA**: https://reddit.com/r/LocalLLaMA
- **Anthropic Community**: https://community.anthropic.com

### 学习资源

- **Prompt Engineering Guide**: https://www.promptingguide.ai
- **OpenAI Cookbook**: https://github.com/openai/openai-cookbook
- **Awesome LLM**: https://github.com/Hannibal046/Awesome-LLM

### 工具和服务

- **Prompt管理**: https://promptlayer.com
- **Token计算**: https://platform.openai.com/tokenizer
- **向量数据库**: https://www.trychroma.com
- **密钥管理**: https://www.vaultproject.io

---

## A.9 速记卡

打印或保存到手机，日常开发时快速查阅。

```
┌─────────────────────────────────────────┐
│     Agent开发速记卡                      │
├─────────────────────────────────────────┤
│ 安全三问：                               │
│ 1. 凭证是否硬编码？                      │
│ 2. 输出是否过滤敏感信息？                │
│ 3. 权限是否最小化？                      │
├─────────────────────────────────────────┤
│ 可观测三要素：                           │
│ 1. 结构化日志（输入/决策/输出/错误）     │
│ 2. Metrics（成功率/延迟/Token）          │
│ 3. Trace（多Agent调用链）                │
├─────────────────────────────────────────┤
│ 部署前检查：                             │
│ ✓ 测试覆盖关键case                       │
│ ✓ 日志和监控已配置                       │
│ ✓ 告警规则已设置                         │
│ ✓ 回滚方案已准备                         │
├─────────────────────────────────────────┤
│ 出问题时：                               │
│ 1. 先看日志（最近100行）                 │
│ 2. 再看监控（成功率/延迟）               │
│ 3. 对比历史（是否有配置变更）             │
│ 4. 隔离问题（单Agent测试）               │
└─────────────────────────────────────────┘
```

---

**附录结束**。返回主目录继续学习，或直接开始你的Agent项目！ 🚀
