#!/usr/bin/env python3
"""
为各章节添加参考资料部分
"""

import os

# 定义每章引用的案例
chapter_citations = {
    "part-1/ch01.md": [
        ("Daily Reddit Digest", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/daily-reddit-digest.md"),
        ("Daily YouTube Digest", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/daily-youtube-digest.md"),
        ("Multi-Source Tech News Digest", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/multi-source-tech-news-digest.md"),
        ("Phone-Based Personal Assistant", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/phone-based-personal-assistant.md"),
    ],
    "part-1/ch02.md": [
        ("Autonomous Project Management", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/autonomous-project-management.md"),
        ("Self-Healing Home Server", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/self-healing-home-server.md"),
        ("Phone-Based Personal Assistant", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/phone-based-personal-assistant.md"),
    ],
    "part-2/ch04.md": [
        ("Daily Reddit Digest", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/daily-reddit-digest.md"),
        ("Health & Symptom Tracker", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/health-symptom-tracker.md"),
        ("Multi-Agent Team", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/multi-agent-team.md"),
    ],
    "part-2/ch05.md": [
        ("Multi-Agent Content Factory", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/content-factory.md"),
    ],
    "part-2/ch06.md": [
        ("Custom Morning Brief", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/custom-morning-brief.md"),
        ("Self-Healing Home Server", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/self-healing-home-server.md"),
        ("Health & Symptom Tracker", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/health-symptom-tracker.md"),
    ],
    "part-2/ch07.md": [
        ("n8n Workflow Orchestration", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/n8n-workflow-orchestration.md"),
        ("Self-Healing Home Server", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/self-healing-home-server.md"),
    ],
    "part-3/ch08.md": [
        ("Daily Reddit Digest", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/daily-reddit-digest.md"),
        ("Daily YouTube Digest", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/daily-youtube-digest.md"),
        ("X Account Analysis", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/x-account-analysis.md"),
        ("Multi-Source Tech News Digest", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/multi-source-tech-news-digest.md"),
        ("AI Earnings Tracker", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/earnings-tracker.md"),
    ],
    "part-3/ch09.md": [
        ("YouTube Content Pipeline", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/youtube-content-pipeline.md"),
        ("Multi-Agent Content Factory", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/content-factory.md"),
        ("Goal-Driven Autonomous Tasks", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/overnight-mini-app-builder.md"),
    ],
    "part-3/ch10.md": [
        ("Custom Morning Brief", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/custom-morning-brief.md"),
        ("Inbox De-clutter", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/inbox-declutter.md"),
        ("Multi-Channel Assistant", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/multi-channel-assistant.md"),
        ("Todoist Task Manager", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/todoist-task-manager.md"),
        ("Autonomous Project Management", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/autonomous-project-management.md"),
        ("Multi-Channel Customer Service", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/multi-channel-customer-service.md"),
    ],
    "part-3/ch11.md": [
        ("Self-Healing Home Server", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/self-healing-home-server.md"),
        ("n8n Workflow Orchestration", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/n8n-workflow-orchestration.md"),
    ],
    "part-3/ch12.md": [
        ("Knowledge Base RAG", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/knowledge-base-rag.md"),
        ("Second Brain", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/second-brain.md"),
        ("Semantic Memory Search", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/semantic-memory-search.md"),
        ("AI Earnings Tracker", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/earnings-tracker.md"),
    ],
    "part-4/ch13.md": [
        ("Multi-Agent Team", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/multi-agent-team.md"),
    ],
    "part-4/ch14.md": [
        ("n8n Workflow Orchestration", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/n8n-workflow-orchestration.md"),
    ],
    "part-4/ch15.md": [
        ("Multi-Agent Team", "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/multi-agent-team.md"),
    ],
}

def add_references_to_chapter(filepath, citations):
    """为章节文件添加参考资料部分"""
    
    # 读取文件
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经有参考资料部分
    if '## 参考资料' in content or '##参考资料' in content:
        print(f"⚠️  {filepath} 已有参考资料部分,跳过")
        return False
    
    # 构建参考资料部分
    references = "\n\n---\n\n## 参考资料\n\n"
    references += "本章引用的案例均来自 [awesome-openclaw-usecases](https://github.com/hesamsheikh/awesome-openclaw-usecases) 社区仓库：\n\n"
    
    for name, url in citations:
        references += f"- [{name}]({url})\n"
    
    # 添加到文件末尾
    new_content = content.rstrip() + references
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ {filepath} 添加了 {len(citations)} 个案例引用")
    return True

def main():
    """主函数"""
    src_dir = "src"
    updated_count = 0
    skipped_count = 0
    
    print("开始为各章节添加参考资料...\n")
    
    for chapter, citations in chapter_citations.items():
        filepath = os.path.join(src_dir, chapter)
        
        if not os.path.exists(filepath):
            print(f"⚠️  文件不存在: {filepath}")
            continue
        
        if add_references_to_chapter(filepath, citations):
            updated_count += 1
        else:
            skipped_count += 1
    
    print(f"\n完成！")
    print(f"✅ 更新: {updated_count} 个文件")
    print(f"⚠️  跳过: {skipped_count} 个文件")

if __name__ == "__main__":
    main()
