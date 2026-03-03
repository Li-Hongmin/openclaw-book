# 🤖 第5.5章：Sub-agent模式深度解析（2026新功能）

> 📅 更新于 2/24  
> ⭐ OpenClaw 2026.2+ 原生支持

---

## 🌟 什么是Sub-agent模式

Sub-agent（子代理）是OpenClaw 2026.2版本引入的重大新功能，专门为Agent协作设计。它解决了传统多Agent架构的几个核心痛点：

**传统方式的问题**：
```python
# ❌ 传统方式：主Agent阻塞等待
主Agent: "请搜索最新AI论文"
  ↓ 等待... 等待... 等待...（5-10分钟）
  ↓ 主Agent的上下文一直占用，token持续消耗
  ↓
搜索完成: "找到12篇论文"
主Agent继续下一步
```

**Sub-agent方式**：
```python
# ✅ Sub-agent方式：非阻塞并行
主Agent: sessions_spawn("搜索最新AI论文")
  → 返回 runId
  ↓ 主Agent立即继续其他工作
  ↓ （可以spawn更多子任务）
  ↓
（5-10分钟后）
子Agent完成 → 自动announce结果 → 主Agent接收
```

**核心优势**：
1. **非阻塞**：spawn后立即返回，主Agent不等待
2. **并行**：可以同时运行多个子Agent（默认最多8个）
3. **独立上下文**：每个子Agent有自己的session，避免主Agent上下文膨胀
4. **成本优化**：可以为子Agent设置更便宜的模型
5. **自动汇报**：子Agent完成后自动announce结果，无需轮询

---

## 🎯 基础用法

### 简单示例：并行研究任务

假设你需要研究三个不同主题的AI技术：

```python
# 主Agent的逻辑
# 1. Spawn三个并行研究任务
sessions_spawn(
    task="研究LLM多模态能力最新进展，整理成摘要",
    label="multimodal-research"
)

sessions_spawn(
    task="研究AI Agent框架对比（LangChain vs AutoGPT vs OpenClaw），列出优缺点",
    label="framework-research"
)

sessions_spawn(
    task="研究Prompt Engineering最佳实践2026版，提炼10条核心原则",
    label="prompt-research"
)

# 2. 主Agent继续做其他事情
# 例如准备文档模板、设置GitHub仓库等

# 3. （10-15分钟后）子Agent们陆续完成并自动announce：
# ✅ multimodal-research完成: 多模态能力摘要已保存到 research/multimodal-2026.md
# ✅ framework-research完成: 框架对比表已生成，见 research/frameworks.md
# ✅ prompt-research完成: 10条原则已整理，见 research/prompts-best-practices.md

# 4. 主Agent汇总所有结果
# "收到三份研究报告，现在开始综合分析..."
```

### 配置参数详解

```python
sessions_spawn(
    task="任务描述（清晰、具体）",          # 必填
    label="subagent-label",               # 可选，用于识别子Agent
    model="openai/gpt-4o-mini",           # 可选，覆盖默认模型
    thinking="low",                       # 可选，覆盖思考级别
    runTimeoutSeconds=900,                # 可选，超时时间（秒）
    thread=False,                         # 可选，是否绑定Discord线程
    mode="run",                           # "run"一次性 | "session"持久会话
    cleanup="keep"                        # "keep"保留 | "delete"完成后删除
)
```

**参数说明**：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `task` | 必填 | 清晰的任务描述，子Agent的唯一指令 |
| `label` | 自动生成UUID | 用于识别子Agent，建议手动指定 |
| `model` | 继承主Agent | 可指定更便宜的模型节约成本 |
| `thinking` | 继承主Agent | "off", "low", "medium", "high" |
| `runTimeoutSeconds` | 0（无超时） | 超时后自动停止，避免失控 |
| `thread` | `false` | Discord专用，绑定专属线程 |
| `mode` | "run" | "run"=一次性任务，"session"=持久会话 |
| `cleanup` | "keep" | "keep"=保留日志，"delete"=完成后清理 |

### 返回值

```json
{
  "status": "accepted",
  "runId": "a3f2e1b...",
  "childSessionKey": "agent:main:subagent:a3f2e1b..."
}
```

- **非阻塞**：立即返回，不等待结果
- **runId**：用于后续查询状态
- **childSessionKey**：子Agent的session标识

---

## 🔧 高级模式：Orchestrator Pattern

当任务复杂到需要"项目经理"协调多个"工人"时，可以使用2层嵌套的orchestrator模式：

```
主Agent
  ↓
Orchestrator Sub-agent（项目经理）
  ↓
├─ Worker 1 (数据收集)
├─ Worker 2 (数据分析)
├─ Worker 3 (可视化)
└─ Worker 4 (报告生成)
  ↓
汇总结果 → announce → 主Agent
```

### 配置嵌套支持

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxSpawnDepth: 2,           // 允许2层嵌套
        maxChildrenPerAgent: 5,      // 每个Agent最多5个子Agent
        maxConcurrent: 8,            // 全局并发上限
        runTimeoutSeconds: 1800,     // 默认30分钟超时
        model: "openai/gpt-4o-mini", // 子Agent默认用便宜模型
        archiveAfterMinutes: 60      // 1小时后自动清理
      }
    }
  }
}
```

### Orchestrator示例

**主Agent**：
```python
# 主Agent只负责高层决策
sessions_spawn(
    task="""
    你是项目经理，负责协调完成一份AI市场分析报告。
    
    子任务：
    1. 收集50家AI公司的最新动态
    2. 分析它们的技术方向和融资情况
    3. 生成趋势图表
    4. 撰写10页综合报告
    
    你需要spawn 4个worker sub-agent分别完成这些任务，
    汇总后生成最终报告。
    
    工作流程由你自主决定，我不干预细节。
    完成后announce最终报告路径。
    """,
    label="market-analysis-orchestrator",
    model="anthropic/claude-sonnet-4-5",  # Orchestrator用强模型
    runTimeoutSeconds=3600  # 允许1小时
)

# 主Agent不管细节，等待最终报告
```

**Orchestrator Sub-agent内部逻辑**：
```python
# （这是Orchestrator自主决策的）
# 1. Spawn数据收集worker
sessions_spawn(
    task="收集50家AI公司（OpenAI, Anthropic, ...）的最新新闻、融资、产品发布",
    label="data-collector",
    model="openai/gpt-4o-mini"  # Worker用便宜模型
)

# 2. Spawn分析worker（依赖数据收集）
# ... 等待data-collector完成 ...
sessions_spawn(
    task="分析收集的数据，提取技术方向、融资规模、市场定位",
    label="data-analyzer"
)

# 3. Spawn可视化worker
sessions_spawn(
    task="根据分析结果生成融资趋势图、技术栈分布图、市场地图",
    label="visualizer"
)

# 4. Spawn报告writer
sessions_spawn(
    task="综合所有分析和图表，撰写10页PDF报告",
    label="report-writer"
)

# 5. 汇总所有结果
# "所有子任务完成，最终报告：reports/ai-market-2026.pdf"
```

**announce链**：
```
Worker 1-4完成 → announce到Orchestrator
Orchestrator汇总 → announce到主Agent
主Agent接收最终结果
```

### 深度限制

| 深度 | Session Key | 角色 | 能spawn子Agent吗？ |
|------|-------------|------|------------------|
| 0 | `agent:main:main` | 主Agent | ✅ 总是可以 |
| 1 | `agent:main:subagent:<uuid>` | 子Agent / Orchestrator | ✅ 如果 `maxSpawnDepth >= 2` |
| 2 | `agent:main:subagent:<uuid>:subagent:<uuid>` | Leaf Worker | ❌ 不能再spawn |

**为什么限制深度**？
- 避免无限递归导致失控
- 控制复杂度，2层足够大多数场景
- token成本指数增长

---

## 💰 成本优化策略

Sub-agent的一大优势是可以为不同任务设置不同模型，优化成本：

### 模型选择决策树

```
任务需要推理能力？
├─ 是：Claude Opus / GPT-4.5
│   └─ 需要长上下文？
│       ├─ 是：Claude Opus 4-6（200K）
│       └─ 否：GPT-4.5 Turbo
│
└─ 否：简单任务
    └─ GPT-4o-mini / Claude Haiku
```

### 实战案例：内容工厂

假设你运营一个内容工厂，每天生产10篇博客文章：

**任务拆分**：
1. **研究**（需要深度理解） → Claude Opus
2. **大纲**（需要结构化思维） → GPT-4.5
3. **撰写**（执行型任务） → GPT-4o-mini
4. **SEO优化**（模板化任务） → GPT-4o-mini
5. **校对**（细节检查） → Claude Haiku

**成本对比**：

| 方案 | 模型配置 | 每篇成本 | 10篇/天成本 |
|------|---------|---------|-----------|
| 全用Opus | 所有步骤都用Claude Opus 4-6 | $2.50 | $25.00 |
| 混合模型 | 研究用Opus，其他用mini/haiku | $0.80 | $8.00 |
| **节约** | **↓ 68%** | **↓ $1.70** | **↓ $17.00/天** |

**配置示例**：

```json5
{
  agents: {
    defaults: {
      model: "anthropic/claude-opus-4-6",  // 主Agent用强模型
      subagents: {
        model: "openai/gpt-4o-mini"  // 子Agent默认用便宜模型
      }
    }
  }
}
```

```python
# 主Agent根据任务性质选择模型
sessions_spawn(
    task="深度研究AI政策法规，找出10个关键风险点",
    model="anthropic/claude-opus-4-6"  # 研究用强模型
)

sessions_spawn(
    task="根据研究报告撰写1500字博客文章",
    model="openai/gpt-4o-mini"  # 写作用便宜模型
)

sessions_spawn(
    task="校对文章，修复语法和拼写错误",
    model="anthropic/claude-haiku-4"  # 校对用最便宜模型
)
```

### 思考级别（Thinking Level）优化

对于简单任务，降低thinking level也能节约成本：

```python
sessions_spawn(
    task="将这10篇文章的标题翻译成英文",
    model="openai/gpt-4o-mini",
    thinking="off"  # 翻译不需要思考，关闭thinking节约token
)

sessions_spawn(
    task="分析这100条用户评论，找出3个核心痛点",
    model="anthropic/claude-opus-4-6",
    thinking="high"  # 分析需要深度思考
)
```

---

## 🎛️ 并发控制与超时管理

### 并发上限

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxConcurrent: 8,           // 全局最多8个子Agent同时运行
        maxChildrenPerAgent: 5       // 每个Agent最多spawn 5个子Agent
      }
    }
  }
}
```

**为什么限制并发**？
- **资源保护**：避免过多Agent耗尽系统资源
- **成本控制**：并发越多，API费用越高
- **质量保证**：过多并发可能导致rate limit

**超过限制会发生什么**？
- 新spawn请求会进入队列等待
- 队列满了会返回错误
- 建议设置超时避免永久等待

### 超时策略

```python
# 短任务：严格超时
sessions_spawn(
    task="搜索Hacker News首页，返回前10条标题",
    runTimeoutSeconds=120  # 2分钟内必须完成
)

# 长任务：宽松超时
sessions_spawn(
    task="爬取100个网站的内容并分析",
    runTimeoutSeconds=3600  # 允许1小时
)

# 开放式任务：无超时（慎用！）
sessions_spawn(
    task="持续监控服务器日志，发现异常立即告警",
    runTimeoutSeconds=0  # 不超时（但会在archiveAfterMinutes后清理）
)
```

**超时后会发生什么**？
- 子Agent自动停止
- announce返回status="timeout"
- 主Agent可以决定重试或放弃

---

## 📡 通信机制：Announce详解

### Announce格式

当子Agent完成任务时，会自动announce结果回主Agent：

```
✅ Sub-agent完成: research-subagent

Status: completed successfully
Runtime: 5m12s
Tokens: 15,234 input / 2,890 output (18,124 total)
Cost: $0.42

Result:
已完成AI论文研究，找到12篇相关论文。
关键发现：
1. 多模态模型成为主流趋势
2. Agent框架向标准化方向发展
3. 安全性和可控性是2026年重点

详细报告已保存到：research/ai-papers-2026.md

Session: agent:main:subagent:a3f2e1b...
Transcript: ~/.openclaw/transcripts/agent-main-subagent-a3f2e1b.jsonl
```

### 跳过Announce

如果子Agent不想announce（例如中间步骤），可以返回特殊字符串：

```python
# 子Agent内部
if 这是中间步骤:
    return "ANNOUNCE_SKIP"
# 主Agent不会收到这个结果
```

### 自定义Announce内容

子Agent可以控制announce的内容：

```python
# 子Agent的announce step
"""
简短总结: 完成数据收集，共1,234条记录

详细路径:
- 原始数据: data/raw/2026-02-24.csv
- 清洗后数据: data/clean/2026-02-24.csv
- 统计报告: reports/stats.md

下一步建议: 开始数据分析阶段
"""
```

---

## 🧰 管理子Agent

### 命令行工具

```bash
# 列出当前session的所有子Agent
/subagents list

# 输出：
# 1. research-subagent [running] 5m23s
# 2. writing-subagent [running] 2m10s
# 3. editing-subagent [completed] 8m45s

# 查看特定子Agent的详情
/subagents info research-subagent

# 查看日志
/subagents log research-subagent
/subagents log research-subagent 50 tools  # 显示最近50行，包括工具调用

# 向子Agent发送消息
/subagents send research-subagent "请加快速度，优先关注前5篇论文"

# 引导子Agent方向（steering）
/subagents steer writing-subagent "风格改为更技术化，减少比喻"

# 停止子Agent
/subagents kill research-subagent
/subagents kill all  # 停止所有子Agent
```

### 编程式管理

```python
# 使用sessions_list查询子Agent状态
sessions_list(agentId="main")
# 返回所有session，包括子Agent

# 使用sessions_history查看子Agent日志
sessions_history(sessionKey="agent:main:subagent:a3f2e1b...")

# 使用sessions_send与子Agent通信
sessions_send(
    sessionKey="agent:main:subagent:a3f2e1b...",
    message="请暂停，等待进一步指示"
)
```

---

## ✅ 最佳实践

### 1. 清晰的任务描述

**❌ 不好**：
```python
sessions_spawn(task="研究AI")
```

**✅ 好**：
```python
sessions_spawn(
    task="""
    研究2026年AI Agent领域的最新进展。
    
    具体要求：
    1. 搜索最近3个月的学术论文（arxiv, ACL, NeurIPS）
    2. 关注以下主题：多Agent协作、工具使用、长上下文
    3. 每个主题找3-5篇代表性论文
    4. 提取核心观点和技术亮点
    5. 输出格式：Markdown表格，包含论文标题、作者、关键发现
    6. 保存到：research/ai-agents-2026.md
    
    预计时间：15-20分钟
    """
)
```

### 2. 合理的超时设置

根据任务类型设置超时：

| 任务类型 | 推荐超时 | 示例 |
|---------|---------|------|
| 快速查询 | 1-3分钟 | 搜索、简单计算 |
| 数据处理 | 5-15分钟 | 爬虫、数据清洗 |
| 深度分析 | 15-30分钟 | 研究、写作、代码review |
| 长时间任务 | 30-60分钟 | 大规模数据分析、复杂工作流 |

### 3. 错误处理

```python
# 主Agent的逻辑
result = sessions_spawn(
    task="爬取100个网站内容",
    label="web-scraper",
    runTimeoutSeconds=600
)

# 检查返回值
if result["status"] != "accepted":
    print(f"Spawn失败: {result.get('error')}")
    # 降级方案：使用本地缓存数据
    
# 等待announce
# （通过monitor子Agent announce消息）
if announce_status == "timeout":
    print("爬虫超时，重试一次")
    sessions_spawn(task="...", runTimeoutSeconds=1200)  # 加倍超时
elif announce_status == "error":
    print(f"爬虫失败: {announce_error}")
    # 人工介入或放弃任务
```

### 4. 资源清理

```python
# 短期任务：自动清理
sessions_spawn(
    task="快速查询天气",
    cleanup="delete"  # 完成后立即清理
)

# 长期任务：保留日志
sessions_spawn(
    task="24小时监控服务器",
    cleanup="keep",  # 保留日志供审计
    archiveAfterMinutes=1440  # 24小时后清理
)
```

### 5. 成本监控

在config中配置模型定价，自动计算成本：

```json5
{
  models: {
    providers: {
      anthropic: {
        models: [{
          name: "claude-opus-4-6",
          cost: {
            input: 15.00,   // $/1M tokens
            output: 75.00
          }
        }]
      },
      openai: {
        models: [{
          name: "gpt-4o-mini",
          cost: {
            input: 0.15,
            output: 0.60
          }
        }]
      }
    }
  }
}
```

每次announce会显示成本：
```
Cost: $0.42
```

---

## 🎯 实战案例：内容工厂自动化

让我们用sub-agent模式构建一个完整的内容生产流水线。

### 需求

- 每天生产3篇技术博客文章
- 流程：选题 → 研究 → 撰写 → 校对 → 发布
- 质量要求：深度分析，1500-2000字
- 成本约束：每篇< $1

### 实现

**主Agent（内容总监）**：

```python
# 每天早上9点运行
for i in range(3):
    # Spawn一个orchestrator负责单篇文章
    sessions_spawn(
        task=f"""
        你是文章生产orchestrator，负责完成一篇技术博客。
        
        今日主题方向：AI Agent, LLM应用, 开发工具
        文章编号：{i+1}/3
        
        工作流程：
        1. 选题：从主题方向中选一个具体话题
        2. 研究：收集资料（论文、博客、GitHub）
        3. 撰写：写1500-2000字文章
        4. 校对：检查语法、逻辑、格式
        5. SEO优化：标题、meta、关键词
        6. 发布：推送到CMS
        
        你需要spawn子Agent完成各个步骤。
        完成后announce文章URL。
        
        质量标准：
        - 有技术深度，不是简单科普
        - 有代码示例或架构图
        - 结构清晰，逻辑连贯
        - SEO友好
        
        成本约束：< $1
        
        预计时间：30-45分钟
        """,
        label=f"article-orchestrator-{i+1}",
        model="anthropic/claude-sonnet-4-5",
        runTimeoutSeconds=3600
    )

# 主Agent等待3个orchestrator完成
# 预计2-3小时后，3篇文章全部发布
```

**Orchestrator Sub-agent**（单篇文章）：

```python
# 1. 选题
topic = sessions_spawn(
    task="""
    从以下主题中选一个具体话题，要求：
    1. 有时效性（最近3个月的新发展）
    2. 有技术深度
    3. 有实战价值
    
    主题方向：AI Agent, LLM应用, 开发工具
    
    返回格式：
    - 话题标题
    - 为什么选这个话题（1-2句）
    - 目标读者
    """,
    model="openai/gpt-4o-mini",
    thinking="low"
).wait()  # 快速决策，等待结果

# 2. 研究
research = sessions_spawn(
    task=f"""
    深度研究话题：{topic}
    
    要求：
    1. 搜索最新论文（arxiv）
    2. 找GitHub上的相关项目（stars > 100）
    3. 阅读顶级博客的相关文章
    4. 总结核心观点和技术细节
    
    输出：research/article-{i+1}.md
    """,
    model="anthropic/claude-opus-4-6",  # 研究用强模型
    thinking="high",
    runTimeoutSeconds=900
).wait()

# 3. 撰写
draft = sessions_spawn(
    task=f"""
    根据研究报告撰写博客文章。
    
    话题：{topic}
    研究资料：{research.path}
    
    要求：
    - 1500-2000字
    - 包含代码示例
    - 结构：引言、背景、核心内容、实战案例、总结
    - 风格：技术但易读，面向中高级开发者
    
    输出：drafts/article-{i+1}.md
    """,
    model="openai/gpt-4o-mini",  # 写作用便宜模型
    thinking="medium",
    runTimeoutSeconds=600
).wait()

# 4. 校对
proofread = sessions_spawn(
    task=f"""
    校对文章，修复问题。
    
    文章路径：{draft.path}
    
    检查项：
    - 语法和拼写错误
    - 逻辑连贯性
    - 技术准确性
    - Markdown格式
    
    直接修改文件，输出修改总结。
    """,
    model="anthropic/claude-haiku-4",  # 校对用最便宜模型
    thinking="low"
).wait()

# 5. SEO优化
seo = sessions_spawn(
    task=f"""
    SEO优化。
    
    文章路径：{proofread.path}
    
    任务：
    1. 生成吸引人的标题（40-60字符）
    2. 提取5-7个关键词
    3. 写meta description（150-160字符）
    4. 添加内部链接建议
    
    输出：在文章开头添加YAML front matter
    """,
    model="openai/gpt-4o-mini",
    thinking="low"
).wait()

# 6. 发布
publish_url = sessions_spawn(
    task=f"""
    发布文章到CMS。
    
    文章路径：{seo.path}
    
    步骤：
    1. 调用CMS API创建文章
    2. 上传文章内容
    3. 设置分类和标签
    4. 状态设为"published"
    
    返回文章URL
    """,
    model="openai/gpt-4o-mini",
    thinking="off"
).wait()

# 7. Announce最终结果
return f"""
✅ 文章发布成功！

标题：{topic}
URL：{publish_url}
字数：{word_count}
研究深度：⭐⭐⭐⭐
SEO评分：92/100

成本：${total_cost:.2f}
耗时：{duration}分钟
"""
```

### 成本分析

| 步骤 | 模型 | 预估Token | 成本 |
|------|------|----------|------|
| 选题 | GPT-4o-mini | 1K in / 0.5K out | $0.001 |
| 研究 | Claude Opus | 50K in / 5K out | $1.125 |
| 撰写 | GPT-4o-mini | 10K in / 3K out | $0.003 |
| 校对 | Claude Haiku | 5K in / 1K out | $0.002 |
| SEO | GPT-4o-mini | 5K in / 1K out | $0.001 |
| 发布 | GPT-4o-mini | 2K in / 0.5K out | $0.001 |
| **总计** | - | - | **$1.133** |

稍微超预算，优化方案：
- 研究阶段用Claude Sonnet替代Opus（$0.42）
- 或者限制研究的输入token（压缩资料）

优化后成本：**$0.43/篇**，符合预算！

---

## 🚨 常见问题

### Q1: Sub-agent会"失控"吗？

**A**: 有保护机制：
- 超时自动停止
- 并发上限保护
- 可以随时kill
- 工具权限限制（默认无session工具）

### Q2: Sub-agent能访问主Agent的记忆吗？

**A**: 部分：
- ✅ 读取`AGENTS.md`和`TOOLS.md`
- ❌ 不读取`SOUL.md`, `USER.md`, `MEMORY.md`
- 原因：避免隐私泄露，保持独立

### Q3: 如何调试Sub-agent？

**A**: 多种方式：
```bash
# 1. 实时查看日志
/subagents log research-subagent

# 2. 查看完整transcript
cat ~/.openclaw/transcripts/agent-main-subagent-xxx.jsonl

# 3. 发送调试消息
/subagents send research-subagent "输出当前进度和遇到的问题"
```

### Q4: Sub-agent能spawn sub-sub-agent吗？

**A**: 可以，但需要配置：
```json5
{
  agents: {
    defaults: {
      subagents: {
        maxSpawnDepth: 2  // 允许2层嵌套
      }
    }
  }
}
```

只有orchestrator模式需要，一般任务用1层就够。

### Q5: 如何处理Sub-agent失败？

**A**: 在announce中检查status：
```python
if announce.status == "error":
    # 重试
    sessions_spawn(task="...", runTimeoutSeconds=1200)
elif announce.status == "timeout":
    # 加长超时或拆分任务
    pass
```

---

## 🆕 ACP Thread-bound Agents（2/27 Release）

> 📅 更新于 2026-03-01

OpenClaw 2/27 版本将 **ACP Agent 提升为一等公民**的线程会话运行时，支持 `acp spawn/send` 分发集成、完整的生命周期控制（启动协调、运行时清理）以及线程消息合并回复。

### 什么是 ACP Thread-bound Agent？

ACP（Agent Control Protocol）是 OpenClaw 支持的一种外部 Coding Agent 运行时（如 Claude Code、Codex、Gemini CLI）。Thread-bound 模式意味着：**一个 ACP Agent 实例绑定到一个特定的 thread（对话线程），持久存活，处理该 thread 内的所有消息**。

```
用户消息 (Discord thread)
    ↓
OpenClaw Gateway
    ↓ (sessions_spawn runtime="acp", thread=true)
ACP Agent (Claude Code / Codex)  ← 持久绑定到这个 thread
    ↓ 回复合并
用户看到统一的 AI 回复
```

### 使用方法

**在 Discord thread 中启动持久 ACP Agent**：

```python
# 在 Discord 中，一个 thread 对应一个持久的编码助手
sessions_spawn(
    task="你是这个 Discord thread 的专属编码助手，帮助用户解决 Python 问题",
    runtime="acp",
    agentId="claude-code",   # 或 "codex"
    thread=True,             # 绑定到当前 thread
    mode="session"           # 持久会话模式
)
```

**发送消息到 Thread-bound Agent**：

```python
# 向已绑定的 ACP Agent 发送消息
sessions_send(
    label="my-thread-agent",
    message="帮我优化这段代码: [代码片段]"
)
```

### ACP Thread-bound vs 普通 Sub-agent

| 特性 | 普通 Sub-agent | ACP Thread-bound |
|------|---------------|-----------------|
| 运行时 | OpenClaw 内置 | 外部 Coding Agent |
| 生命周期 | 任务完成即退出 | 绑定 thread，持续存活 |
| 适用场景 | 后台批处理任务 | 交互式编码协作 |
| 消息合并 | 独立回复 | 同 thread 合并回复 |
| 模型选择 | claude/codex/gemini | 取决于 acp.agentId |

### 实战：Discord 频道专属编码助手

```python
# 用户在 Discord 创建新 thread 时，自动启动一个持久编码助手
# 在 AGENTS.md 或 heartbeat 中配置触发逻辑：

sessions_spawn(
    label="discord-coding-thread-{thread_id}",
    task="""
    你是这个 Discord 编码讨论频道的专属助手。
    - 回答代码问题
    - 提供代码审查
    - 解释技术概念
    在这个 thread 内持续服务，直到用户关闭。
    """,
    runtime="acp",
    agentId="claude-code",
    thread=True,
    mode="session"
)
```

> 💡 **使用场景**：团队在 Discord 创建"编码讨论 thread"，每个 thread 自动绑定一个 Claude Code 助手，持续协作而不丢失上下文。

---

## 📚 总结

**Sub-agent模式的适用场景**：

✅ **应该用Sub-agent**：
- 任务耗时长（>5分钟）
- 需要并行处理
- 需要成本优化（不同模型）
- 复杂工作流需要orchestrator
- 后台任务不阻塞主流程

❌ **不应该用Sub-agent**：
- 简单快速任务（<1分钟）
- 需要频繁交互的任务
- 对实时性要求极高
- 任务间有强依赖（用STATE文件更好）

**与其他模式对比**：

| 场景 | 推荐模式 | 原因 |
|------|---------|------|
| 并行研究3个主题 | Sub-agent | 独立任务，可并行 |
| 网站重构（多人协作） | STATE文件 | 长期项目，任务间有依赖 |
| 简单查询数据库 | 直接工具调用 | 太简单，不需要Agent |
| 需要人类监督的任务 | 消息传递 | 透明度和可控性 |
| 复杂工作流（4+步骤） | Orchestrator Sub-agent | 需要中央协调 |

**下一步**：
- 阅读[第6章](ch06.md)：持久化与定时任务
- 实战练习：用sub-agent构建你的第一个自动化工作流
- 参考[OpenClaw官方文档](https://docs.openclaw.ai/tools/subagents)

---

**参考资料**：
- [OpenClaw Sub-agents文档](https://docs.openclaw.ai/tools/subagents)
- [GitHub源码](https://github.com/openclaw/openclaw)
- [社区案例集](https://github.com/hesamsheikh/awesome-openclaw-usecases)
