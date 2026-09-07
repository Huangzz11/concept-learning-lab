# Concept Learning Lab · 概念学习实验室

课程作业仓库：用「项目级 Skill」组织概念学习任务。仓库内包含一个可复用的**概念学习资料生成 Skill（concept-learner）**，以及由该 Skill 生成、经本人人工核查的三份 AI 概念学习资料。

**作者**：Huangzz11 ｜ **仓库性质**：Public（公开）

## 仓库用途

1. 实践并展示"项目级 Skill"的完整工作流：**写 Skill → 调用 Skill → 产出资料 → 提交归档**。
2. 沉淀一份可继续迭代的 AI 概念学习资料库（可随时新增概念）。
3. 作为后续课程项目的个人工具基础。

## 目录结构

```text
concept-learning-lab/
├── .workbuddy/
│   └── skills/
│       └── concept-learner/     # 项目级 Skill（核心交付物）
│           └── SKILL.md
├── learning-materials/          # 由 Skill 生成的学习资料
│   ├── agent.md                 # Agent（智能体）
│   ├── llm-context.md           # 大模型的上下文（Context）
│   ├── skill.md                 # Skill（Agent Skill）
│   └── concept-relationship.md  # 三概念关系说明
├── README.md
└── .gitignore
```

> 说明：作业示例中的文件名后缀为 `.html`，我按"允许自行调整"的规则改用 **Markdown**，便于在 GitHub 上直接阅读渲染、用 git 做差异对比。内容结构完全对应作业要求（解释/机制/场景/辨析/边界/来源/自测）。

## 项目级 Skill 说明

- **存放路径**：仓库根目录 `.workbuddy/skills/concept-learner/SKILL.md`（项目级 = 随仓库走、随 Git 分发、团队共享）。
- **它能做什么**：接收**任意**新概念作为学习主题，输出一份 8 小节结构化学习资料（学习目标/一句话理解/核心机制/应用场景/概念辨析/使用边界/自测问题/可核查来源）。它不是为三个概念写的一次性提示词，而是可复用的方法包。
- **SKILL.md 内容**：YAML 元数据（name/description）+ 适用场景、输入信息表、七步生成流程、输出结构模板、资料来源要求、落盘前自检清单。

## 如何在 WorkBuddy 中调用

1. 在 WorkBuddy 中**打开本仓库文件夹**（作为项目）。
2. WorkBuddy 会自动发现项目级 Skill（加载 `.workbuddy/skills/` 下的技能）。
3. 在对话中输入类似：
   > "使用 concept-learner Skill，帮我学习一下 **RAG** 这个概念"
4. Skill 会自动触发，按 SKILL.md 流程检索权威资料并生成一份学习资料到 `learning-materials/rag.md`。
5. 通读生成结果，人工核查后自行决定是否保留。

> 提示：只有"打开该仓库为当前项目"时，这个项目级 Skill 才可用；个人级 Skill（所有项目可用）存放在用户主目录 `~/.workbuddy/skills/`。

## 已生成的学习资料（2026-09-07）

| 文件 | 内容 | 一句话主题 |
|---|---|---|
| `learning-materials/agent.md` | Agent 智能体 | 把"方向盘"交给大模型的系统：组成、与 Workflow 的界线、ReAct 循环 |
| `learning-materials/llm-context.md` | 大模型的上下文 | 模型决策依据的"工作台"：token、上下文窗口、与记忆的区分 |
| `learning-materials/skill.md` | Skill | 把任务方法论固化成文件的机制：SKILL.md、渐进式披露、两级存放 |
| `learning-materials/concept-relationship.md` | 三概念关系 | 上下文决定 Agent 决策质量，Skill 给 Agent 跨会话的可复用知识 |

## AI 使用说明与人工核查记录

> 按作业要求如实记录：允许借助 AI，但资料须经本人阅读、理解与核查，来源不得伪造。

**AI 协助的部分**
- 用 AI 完成 Skill 结构设计、Git 命令编写、初始资料草稿与文件组织。
- AI 先检索并**核实了参考来源链接的真实性**（Anthropic / OpenAI / Claude / WorkBuddy 官方文档），再写入资料。

**我人工核查与修改的部分**
1. 通读三份概念资料，确认概念解释与我的课堂理解一致，修正了表述含糊处；
2. 逐条点击/检索了"参考来源"中的链接，确认可访问、内容与引用论断匹配；
3. 将资料中"整段式 AI 表述"改写为个人化语言，并加入自己的类比（白板/实习生/SOP 手册）与判断——关系说明文件 `concept-relationship.md` 主要是我按自己理解组织并请 AI 校对的；
4. 确认仓库不含任何 API Key、密码、个人隐私；`.gitignore` 已排除敏感与临时文件类型。

**核查状态**：每份资料文件头部均含元信息块（生成日期、调用 Skill、review_status），其中三份概念资料与关系说明均已标记"已人工核查"。

## 版本与提交

本仓库通过 Git 管理，本地提交后 push 至 GitHub（提交历史见仓库 Commits 页）。后续新增概念学习资料或新 Skill，按同样流程提交即可。
