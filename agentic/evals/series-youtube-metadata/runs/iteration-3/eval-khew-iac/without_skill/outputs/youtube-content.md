# YouTube Publishing Pack — Khew Jia Peng

**Original talk title:** *AI Meets Infrastructure*
**Speaker:** Khew Jia Peng
**Meetup:** JB Agentic Meetup #1 — 30 May 2026
**Category:** `Science & Technology`

> Note: chapter timestamps assume the published video starts where the transcript starts (0:00 = first word). If you add an intro card or trim a lead-in, shift every marker by the same offset and sanity-check against the final cut.

---

## A/B Test Titles (pick all 3 for Test & Compare)

Each variant tests a *different angle* so the result actually teaches you something. Keyword is kept up front so it survives YouTube's ~60-char search truncation. The ` | JB Agentic Meetup #1` suffix keeps the series grouped.

| # | Angle | Title | Chars |
|---|-------|-------|-------|
| A | Keyword / SEO | `AI Agents + Terraform: Deploy Cloud Infra from Markdown \| JB Agentic Meetup #1` | 78 |
| B | Curiosity hook | `I Let an AI Agent Provision My Cloud Infrastructure \| JB Agentic Meetup #1` | 74 |
| C | Benefit / outcome | `Stop Clicking the Cloud Portal: AI + IaC Provisioning \| JB Agentic Meetup #1` | 76 |

---

## Description (copy-paste ready)

```
What if you provisioned cloud infrastructure by writing requirements in a markdown file and letting an AI agent generate the Terraform for you? Khew Jia Peng, a cloud engineer, shows a working proof of concept: write the requirement in Markdown, the AI agent reads it, updates the Infrastructure-as-Code (Terraform), and runs validation and a plan — so you stop clicking through the Azure or AWS portal one resource at a time.

🎤 Talk: "AI Meets Infrastructure" by Khew Jia Peng
📍 JB Agentic Meetup #1 — 30 May 2026

What's covered:
• What Infrastructure as Code (IaC) is, and why clicking the cloud portal by hand is slow and error-prone
• The setup: requirement.md + agent.md (behaviour/guardrails) + skills.md (workflow) driving a Terraform project
• Live demo: add a new subnet by editing requirement.md, then let the Codex agent generate the code
• Safety first: plan, never blind-apply — the agent is told not to run `terraform apply` against production
• How Terraform's state file (tfstate) tracks what already exists, so plans show only adds, changes, and destroys
• The role shift: the engineer becomes a cloud architect who designs, while the agent drafts and documents
• Q&A gems: git diff for change detection, plan-first with reasoning, Context7 for fresh docs, and cloud costing

Chapters:
0:00 Intro: a cloud engineer's take on AI + infrastructure
0:36 The topic: IaC, AI agents, and Markdown
0:47 What is Infrastructure as Code (IaC)?
1:24 Before IaC: manual clicking in the cloud portal
2:55 The idea: drive Terraform with Markdown + an AI agent
4:46 Inside the Terraform code: main.tf, plan, and apply
6:30 The Markdown setup: agent.md behaviour and skills.md workflow
8:55 requirement.md: capturing what you want to build
9:30 Live demo: add a new subnet via the Codex agent
12:45 Plan, don't auto-apply: keeping production safe
14:00 End-to-end POC recap and the CI/CD next step
15:30 Traditional vs AI-assisted: the cloud-architect role shift
16:19 Wrap-up and the architecture/handover docs
17:00 Q&A: detecting changes with the state file and git diff
22:30 Q&A: plan-first and reasoning before approving
24:00 Q&A: real-project use and the portfolio plan
30:00 Q&A: cloud costing, pricing calculator, and reservations
33:00 Q&A: using AI for architecture diagrams

📅 JB Agentic is a friendly community in Johor Bahru for people building software with AI. We meet on the 4th Saturday of every month. Join the next one: https://lu.ma/jbagentic

👉 Subscribe for more talks: https://www.youtube.com/@jbagentic

#AIAgents #Terraform #InfrastructureAsCode #DevOps #AgenticAI
```

---

## Tags

```
infrastructure as code, IaC, Terraform, AI agent, cloud engineering, DevOps, Azure, AWS, cloud provisioning, agentic AI, Codex agent, markdown driven development, Context7, cloud architect, JB Agentic Meetup
```

Total: 234 characters (under YouTube's 500 limit). 15 tags.

---

## Category

`Science & Technology`
