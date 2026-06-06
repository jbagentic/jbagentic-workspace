# JB Agentic Meetup #1 — YouTube Publishing Pack

Metadata for all three talks: A/B test titles, description, tags, category.
Meetup date: 30 May 2026.

**How to use the A/B titles:** YouTube Studio → video → **Test & Compare** → add up to 3 titles. Each variant below tests a *different angle* (so the result actually teaches you something), with the keyword kept up front. Let it run ~2 weeks or until YouTube declares a winner.

**Category for all three:** `Science & Technology`

**Series tip:** keep `JB Agentic Meetup #1` as the suffix on every video so episodes group cleanly. Put the speaker's original talk title in the description (preserved below), not the title field.

---

## Talk 1 — Khew Jia Peng

**Original talk title:** *AI Meets Infrastructure*
**One-liner:** Driving Infrastructure-as-Code (Terraform) with markdown-defined AI agents to deploy cloud infra.

### A/B Test Titles (pick all 3 for Test & Compare)

| # | Angle | Title |
|---|-------|-------|
| A | Keyword / SEO | `AI Agents + Terraform: Automate Cloud Infra (IaC) \| JB Agentic Meetup #1` |
| B | Curiosity hook | `I Let an AI Agent Write My Terraform \| JB Agentic Meetup #1` |
| C | Benefit / outcome | `Deploy Cloud Infrastructure Faster with AI + IaC \| JB Agentic Meetup #1` |

### Description

```
An AI agent that reads your requirements and writes your Terraform. Cloud engineer Khew Jia Peng shows a working proof-of-concept where markdown-defined agents generate Infrastructure-as-Code and deploy to Azure / AWS — with human PR review before anything hits production.

🎤 Talk: "AI Meets Infrastructure" by Khew Jia Peng
📍 JB Agentic Meetup #1 — 30 May 2026

What's covered:
• What Infrastructure as Code (IaC) is and why manual portal-clicking doesn't scale
• Driving Terraform with AI agents via markdown (requirements.md, skills.md, agent.md)
• Guardrails so the agent never runs `terraform apply` on its own
• Plan → validate → PR review → deploy workflow on Azure & AWS
• Where this is headed next: CI/CD automation

Chapters:
0:00 Intro & speaker background
0:40 What is Infrastructure as Code (IaC)?
2:00 The problem with manual provisioning
2:45 Idea: driving IaC with markdown AI agents
3:40 Deploy workflow: plan, validate, PR review
5:10 Terraform code walkthrough
6:45 Agent setup: agent.md, skills.md, requirements.md
7:25 Guardrails to protect production
10:25 Live demo: adding a subnet end-to-end
15:00 Traditional vs AI-assisted + what's next (CI/CD)
17:10 Q&A: Terraform state & change safety
30:40 Q&A: estimating cloud costs

📅 JB Agentic is a friendly community in Johor Bahru for people building software with AI. We meet on the 4th Saturday of every month. Join the next one: https://luma.com/jbagentic

👉 Subscribe for more talks: https://www.youtube.com/@jbagentic

#AIAgents #Terraform #InfrastructureAsCode #DevOps #CloudComputing
```

### Tags
```
AI agents, Terraform, infrastructure as code, IaC, DevOps, cloud computing, Azure, AWS, AI DevOps, cloud automation, AI infrastructure, Codex agent, JB Agentic Meetup, agentic AI, software engineering Malaysia
```

---

## Talk 2 — Kowa Jia Liang

**Original talk title:** *From Manual Coding to ChatGPT, Cursor and Claude Code*
**One-liner:** A dev team's real evolution from copy-pasting into ChatGPT to running Claude Code with permanent context, custom skills, and MCP.

### A/B Test Titles (pick all 3 for Test & Compare)

| # | Angle | Title |
|---|-------|-------|
| A | Keyword / SEO (speaker's own framing) | `From Manual Coding to Claude Code: A Dev's AI Journey \| JB Agentic Meetup #1` |
| B | Tool-stack hook | `How We Use Claude Code, Cursor & MCP to Ship Faster \| JB Agentic Meetup #1` |
| C | Evolution arc | `ChatGPT → Cursor → Claude Code: Our Real AI Workflow \| JB Agentic Meetup #1` |

### Description

```
How does a real engineering team actually adopt AI? Senior software engineer Kowa Jia Liang (Payboy, Singapore) walks through his team's evolution — from manual coding and copy-pasting into ChatGPT, to Cursor, to running Claude Code with permanent context, custom skills, and MCP.

🎤 Talk: "From Manual Coding to ChatGPT, Cursor and Claude Code" by Kowa Jia Liang
📍 JB Agentic Meetup #1 — 30 May 2026

What's covered:
• The 4 eras: manual coding → ChatGPT → Cursor IDE → VS Code + Claude Code
• Why "context blindness" makes web-chat AI slow for real codebases
• Permanent context with a CLAUDE.md project-root file
• Building custom Claude Code skills for repo workflows
• Using MCP to connect tools without manual config
• Real impact on team speed, knowledge sharing, and onboarding

Tech stack: Ruby on Rails, Vue.js, HRMS SaaS

Chapters:
0:00 Intro: speaker & Payboy (HRMS SaaS)
0:45 The 4 eras: manual → ChatGPT → Cursor → Claude Code
2:15 Browser-era AI vs editor-native AI
3:40 Permanent context with CLAUDE.md
5:15 Custom Claude Code skills for your repo
7:25 Skill: auto-writing PR descriptions
8:55 Skill: automated pre-PR code review
13:25 Spec-driven planning ("Superpower")
17:55 Debugging with Sentry + subagents
20:10 Quality over speed: their philosophy
21:40 Q&A: what goes in CLAUDE.md
28:25 Q&A: staging, cost & trying Codex

📅 JB Agentic is a friendly community in Johor Bahru for people building software with AI. We meet on the 4th Saturday of every month. Join the next one: https://luma.com/jbagentic

👉 Subscribe for more talks: https://www.youtube.com/@jbagentic

#ClaudeCode #Cursor #MCP #AIcoding #SoftwareEngineering
```

### Tags
```
Claude Code, Cursor IDE, MCP, AI coding, AI pair programming, ChatGPT coding, software engineering, developer productivity, AI workflow, coding agents, CLAUDE.md, model context protocol, Ruby on Rails, JB Agentic Meetup, agentic AI
```

---

## Talk 3 — Soh Jun Wei

**Original talk title:** *AI For Everyday Friction*
**One-liner:** Building a personal expense-tracking AI agent on Telegram — log spending by text, voice, or receipt photo, powered by Hermes + MCP.

### A/B Test Titles (pick all 3 for Test & Compare)

| # | Angle | Title |
|---|-------|-------|
| A | Concrete build / outcome | `I Built an AI Expense Tracker on Telegram \| JB Agentic Meetup #1` |
| B | Keyword / technical | `AI Agent + MCP: Log Expenses by Text, Voice & Photo \| JB Agentic Meetup #1` |
| C | Tutorial intent | `Build a Personal AI Agent with Hermes & MCP \| JB Agentic Meetup #1` |

### Description

```
What if recording an expense was as easy as sending a text? Soh Jun Wei builds a personal AI agent on Telegram that logs spending from a quick message, a voice note, or a photo of a receipt — doing the categorization, the math, and the database entry for you. The real enemy isn't the expense app; it's friction.

🎤 Talk: "AI For Everyday Friction" by Soh Jun Wei
📍 JB Agentic Meetup #1 — 30 May 2026

What's covered:
• The problem: friction is what kills good habits like expense tracking
• Designing the agent on Telegram with the Hermes agent + MCP
• Three input modes: text, voice message, and receipt photo
• Category detection, arithmetic, and saving to a SQLite database
• Why MCP matters — the agent takes real actions, not just chats
• A custom dashboard for manual edits and review

Chapters:
0:00 Intro: building for everyday friction
0:45 The problem: expense tracking gets tiresome
3:00 The real enemy is friction
3:40 The vision: text, voice & receipt input
5:10 Stack: Hermes agent, OpenClaw & Telegram
6:40 Live demo: logging expenses on Telegram
8:15 Dashboard & cheap hosting (Oracle Cloud, Whisper)
11:15 Why MCP instead of prompting
13:25 MCP explained: an API built for agents
16:30 Fuzzy input vs deterministic action
17:15 Will AI replace developers?
21:45 MCP vs CLI: which to use
27:00 Q&A: tokens, WhatsApp, hosting & Whisper

📅 JB Agentic is a friendly community in Johor Bahru for people building software with AI. We meet on the 4th Saturday of every month. Join the next one: https://luma.com/jbagentic

👉 Subscribe for more talks: https://www.youtube.com/@jbagentic

#AIAgent #MCP #Telegram #BuildInPublic #AIapps
```

### Tags
```
AI agent, MCP, model context protocol, Telegram bot, expense tracker, personal finance app, Hermes agent, AI automation, build in public, side project, voice AI, receipt scanning, SQLite, JB Agentic Meetup, agentic AI
```

---

## Quick reference — Original vs SEO title (to share with speakers)

| Speaker | Original talk title | Recommended primary SEO title |
|---------|--------------------|-------------------------------|
| Khew Jia Peng | AI Meets Infrastructure | AI Agents + Terraform: Automate Cloud Infra (IaC) \| JB Agentic Meetup #1 |
| Kowa Jia Liang | From Manual Coding to ChatGPT, Cursor and Claude Code | From Manual Coding to Claude Code: A Dev's AI Journey \| JB Agentic Meetup #1 |
| Soh Jun Wei | AI For Everyday Friction | I Built an AI Expense Tracker on Telegram \| JB Agentic Meetup #1 |

**Notes**
- Tag lists are kept well under YouTube's 500-character limit.
- First 2 lines of each description carry the keywords — that's the part shown before "...more" and indexed most heavily.
- Run Test & Compare with all 3 titles per video; YouTube auto-promotes the winner by watch time.
