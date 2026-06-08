# YouTube content — Khew Jia Peng, "AI Meets Infrastructure"

## Original talk title

**AI Meets Infrastructure** — integrating IaC, AI agents, and markdown (Khew Jia Peng, JB Agentic Meetup #1, 2026-05-30)

## 3 A/B-test titles

Each is ≤70 characters including the ` | JB Agentic Meetup #1` suffix, with the searchable keyword ahead of the suffix. The three test different angles.

1. **Keyword / SEO** — `Terraform + AI Agents for Cloud Infrastructure | JB Agentic Meetup #1` (69 chars)
2. **Curiosity hook** — `Can AI Agents Safely Deploy Your Cloud Infra? | JB Agentic Meetup #1` (68 chars)
3. **Benefit / outcome** — `Deploy Cloud Infra from Markdown, Not Portals | JB Agentic Meetup #1` (68 chars)

## Description (copy-paste ready)

```
Terraform + AI agents for cloud infrastructure: a live proof-of-concept where you write requirements in markdown, an AI agent generates the IaC, and Terraform plans and deploys to AWS/Azure — no more clicking portals one by one.

Cloud engineer Khew Jia Peng walks through his end-to-end workflow for "AI Meets Infrastructure" — integrating Infrastructure as Code (Terraform), AI agents (Codex), and markdown — at JB Agentic Meetup #1.

What's covered
- What Infrastructure as Code (IaC) is, and why manual portal provisioning is painful
- The markdown setup: requirement.md, skills.md, and agent.md to steer the agent safely
- Live demo: add a new subnet requirement → agent updates Terraform → terraform plan → apply on AWS
- Guardrails so the agent never runs a destructive terraform apply on its own
- How Terraform state (tfstate) tracks what exists, and how plan shows creates vs destroys
- Traditional manual workflow vs the AI-assisted "cloud architect" workflow
- Costing with the cloud pricing calculator: pay-as-you-go vs reserved instances
- Q&A: git diffs for change review, plan-and-reason-first agents, and Context7 for fresh docs

Chapters
0:00 Intro — a cloud engineer's background and what IaC is
2:15 The idea: bring AI agents to the infrastructure layer
3:00 Markdown + IaC workflow: requirements → agent → Terraform → PR review
4:30 Terraform code walkthrough: main.tf, regions, subnets, VM instances
6:45 The agent setup: agent.md behaviour, skills.md, requirement.md
9:00 Live demo: adding a new subnet requirement with Codex
12:00 terraform plan and the apply guardrail
13:30 Applying the change and seeing the new subnet in AWS
14:15 Next step: CI/CD pipelines for review and deployment
15:00 Traditional manual workflow vs the AI-assisted approach
17:15 Q&A: handling updates to live infra and Terraform state (tfstate)
20:15 Q&A: git diff for change review and plan-first agents
22:30 Q&A: real-project status, importing existing resources, portfolio plans
26:30 Q&A: keeping agents from hallucinating params — Context7
30:45 Q&A: costing, pricing calculator, and reserved instances

📅 JB Agentic is a friendly community in Johor Bahru for people building software with AI. We meet on the 4th Saturday of every month. Join the next one: https://lu.ma/jbagentic

👉 Subscribe for more talks: https://www.youtube.com/@jbagentic

#JBAgentic #InfrastructureAsCode #Terraform #AIagents #CloudEngineering
```

## Tags

```
AI agents, Infrastructure as Code, Terraform, IaC, cloud engineering, DevOps, AWS, Azure, Codex, AI coding agents, markdown driven development, cloud automation, terraform plan, Context7, JB Agentic
```

(15 tags, 198 characters — under YouTube's 500-character limit.)

## Category

Science & Technology
