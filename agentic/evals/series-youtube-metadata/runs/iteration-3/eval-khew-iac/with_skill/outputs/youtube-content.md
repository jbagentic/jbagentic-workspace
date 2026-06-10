# YouTube content — AI Meets Infrastructure

**Full title:** AI Meets Infrastructure

## Titles (A/B test — 3 angles)

1. Infrastructure as Code with AI Agents + Terraform | JB Agentic Meetup #1
2. I Let an AI Agent Provision My Cloud Infra | JB Agentic Meetup #1
3. Ship Cloud Infra Faster: Markdown to Terraform | JB Agentic Meetup #1

## Description

Infrastructure as Code meets AI agents. Khew Jia Peng, a cloud engineer, shows a working proof of concept where you write your cloud requirements in plain markdown, an AI agent turns them into Terraform, and a `terraform plan` step keeps it from touching production. No more clicking through the Azure portal one resource at a time.

🎤 Talk: "AI Meets Infrastructure" by Khew Jia Peng
📍 JB Agentic Meetup #1 — 30 May 2026

What's covered:
• What Infrastructure as Code (IaC) is, and why manual portal provisioning is painful
• The workflow: requirement.md → AI agent → Terraform code → plan → PR review → apply
• Wiring agent behaviour and skills with agent.md, skills.md, and requirement.md
• A live demo: add a new subnet requirement and watch Codex update Terraform and deploy to AWS
• Guardrails so the agent never runs `terraform apply` and wrecks production
• How Terraform's tfstate tracks existing infrastructure, plus using git diff for change context
• Q&A on Context7 for live docs, costing with the pricing calculator, and CI/CD next steps

Tech stack: Terraform, AWS, Azure (Bicep), Codex, agent.md / skills.md / requirement.md, Context7, MCP

Chapters:
0:00 Intro — a cloud engineer's take on AI
0:49 What is Infrastructure as Code?
2:27 Before IaC: clicking the portal one by one
3:00 The idea: markdown + AI agents + IaC
5:42 Terraform demo: main.tf and terraform plan
6:47 Wiring the agent: agent.md, skills.md, requirement.md
10:17 Live demo: a new requirement, deployed to AWS
14:29 Next step: CI/CD with PR approval
15:08 Traditional vs AI-assisted workflow
16:59 Q&A begins
18:09 How Terraform tracks state with tfstate
29:06 Context7 for always-fresh docs
30:40 Costing: pricing calculator and reservations

📅 JB Agentic is a friendly community in Johor Bahru for people building software with AI. We meet on the 4th Saturday of every month. Join the next one: https://lu.ma/jbagentic

👉 Subscribe for more talks: https://www.youtube.com/@jbagentic

#InfrastructureAsCode #Terraform #AIAgents #CloudEngineering #JBAgentic

## Tags

Infrastructure as Code, IaC, Terraform, AI agents, cloud infrastructure, DevOps, AWS, Azure, Bicep, agentic AI, Codex, Context7, MCP, terraform plan, cloud engineering, AI for DevOps, markdown driven development, JB Agentic, infrastructure automation, prompt engineering

## Category

Science & Technology
