# YouTube content — Khew Jia Peng, "AI Meets Infrastructure"

JB Agentic Meetup #1 · 2026-05-30 · Speaker: Khew Jia Peng

---

## Original talk title

**AI Meets Infrastructure** — integrating Infrastructure as Code (IaC), AI agents, and markdown.

---

## 3 A/B-test titles

Each is ≤ 70 characters including the ` | JB Agentic Meetup #1` suffix, with the searchable keyword ahead of the ~60-char search-truncation point. The three test different angles.

1. **(keyword / SEO)** `AI Agents + Terraform: IaC from Markdown | JB Agentic Meetup #1` — 63 chars
2. **(curiosity hook)** `I Let AI Write My Terraform Infrastructure | JB Agentic Meetup #1` — 65 chars
3. **(concrete benefit)** `Deploy Cloud Infra Faster with AI + IaC | JB Agentic Meetup #1` — 62 chars

---

## Description (copy-paste ready)

```
AI agents + Terraform: drive Infrastructure as Code (IaC) from plain markdown.
A cloud engineer's POC for provisioning Azure/AWS infra with an AI agent — write requirements in markdown, let the agent generate and validate the Terraform, then plan/apply behind a PR review.

"AI Meets Infrastructure" by Khew Jia Peng — JB Agentic Meetup #1.

What's covered:
• What Infrastructure as Code (IaC) is, and why click-by-click portal provisioning doesn't scale
• A markdown-driven setup: agents.md (behaviour + guardrails), skills.md (workflow), requirement.md
• Live demo: adding a new subnet via a Codex agent → terraform plan → apply on AWS
• Guardrails so the agent never blindly runs `terraform apply` in production
• How Terraform state (tfstate) tracks existing infra so changes are diffed, not recreated
• Q&A: git-diff + plan-first workflows, the Context7 docs skill, cost planning, AI for architecture

Chapters:
0:00 Background: cloud engineer meets AI, and what IaC is
2:15 The pain: manual, click-by-click portal provisioning
3:00 The idea: markdown + AI agent + IaC
4:30 Terraform demo: main.tf, terraform plan, apply
6:45 Markdown setup: agents.md, skills.md, requirement.md
9:00 Live demo: new requirement → Codex agent → new subnet
14:15 Next step: CI/CD with PR-gated deploys
15:00 Traditional vs AI-assisted infrastructure
16:30 Q&A: verifying the requirement → Terraform flow
18:00 Q&A: updating live infra and Terraform state (tfstate)
20:50 Q&A: git-diff and plan-first guardrails
22:41 Q&A: using it on a real project yet?
27:20 Q&A: avoiding hallucinated config + the Context7 skill
30:40 Q&A: cost planning with the pricing calculator
34:24 Q&A: using AI for architecture diagrams

(Chapter timestamps assume the published video starts where the transcript starts — sanity-check them against the final cut, since an intro card or trimmed lead-in shifts everything.)

JB Agentic is a friendly community in Johor Bahru for people building software with AI. We meet on the 4th Saturday of every month to share what's working, honest lessons, and the problems we're still figuring out. Join us: https://lu.ma/jbagentic

Subscribe for more talks: https://www.youtube.com/@jbagentic?sub_confirmation=1

#JBAgentic #InfrastructureAsCode #Terraform #AIagents #DevOps
```

---

## Tags

```
JB Agentic, AI infrastructure, Infrastructure as Code, IaC, Terraform, AI agents, Codex, Azure, AWS, cloud engineering, DevOps, markdown driven development, Terraform AI, Context7, provisioning automation
```

(15 tags, 204 characters — under YouTube's 500-character limit.)

---

## Category

Science & Technology
