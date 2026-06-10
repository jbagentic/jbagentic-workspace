# YouTube content — Khew Jia Peng, "AI Meets Infrastructure"

## Original talk title

**AI Meets Infrastructure** — integrating IaC, AI agents, and markdown (Khew Jia Peng, JB Agentic Meetup #1, 2026-05-30)

## 3 A/B-test titles

1. **Terraform + AI Agents: Deploy Cloud Infra from Markdown | JB Agentic Meetup #1** (70 chars)
2. **Can AI Agents Replace Manual Cloud Provisioning? | JB Agentic Meetup #1** (68 chars)
3. **AI Meets Infrastructure: IaC with AI Agents Demo | JB Agentic Meetup #1** (68 chars)

## Description (copy-paste ready)

```
Cloud engineer Khew Jia Peng demos his proof-of-concept for using AI agents to generate and deploy Infrastructure as Code (Terraform) from markdown requirements — no more clicking through cloud portals one by one.

At JB Agentic Meetup #1, Jia Peng walks through his end-to-end workflow: write infrastructure requirements in markdown, let an AI agent (Codex) read them and generate Terraform code, validate with terraform plan, and deploy to AWS — with guardrails to prevent accidental destruction.

What's covered
- What Infrastructure as Code (IaC) is and why manual portal provisioning is painful
- The markdown-driven approach: requirement.md, skills.md, and agent.md
- Defining agent behaviour and security rules to protect production infrastructure
- Live demo: adding a new subnet requirement and watching the agent generate Terraform code
- terraform plan validation and the "no terraform apply" guardrail
- Seeing the new subnet created live in the AWS console
- Traditional manual workflow vs AI-assisted cloud architect workflow
- Future plans: CI/CD pipeline integration with PR review before deployment
- Q&A highlights: Terraform state (tfstate), git diffs for change tracking, Context7 for up-to-date docs, and cloud costing with pricing calculators

Chapters
0:00 Intro — Jia Peng's background as a cloud engineer
0:40 What is Infrastructure as Code (IaC)?
1:25 Before IaC: manual portal provisioning pain points
2:15 The idea: integrating AI agents with IaC and markdown
3:00 The workflow: requirements in markdown, agent generates Terraform, PR review
4:30 Terraform code walkthrough: main.tf, variables, regions, subnets
6:45 Agent markdown setup: behaviour rules and security guardrails
8:00 Skills and requirement markdown files
9:00 Live demo: adding a new subnet requirement with Codex
12:00 Terraform plan validation and apply guardrail
13:30 Applying the change — new subnet appears in AWS
14:15 End-to-end workflow summary and CI/CD next steps
15:00 Traditional vs AI-assisted workflow comparison
17:00 Q&A: Handling updates to existing infrastructure and Terraform state
20:00 Q&A: Git diffs for change review and plan-first agent approach
22:30 Q&A: Real-project adoption and portfolio plans
26:30 Q&A: Keeping agents accurate — Context7 for latest documentation
30:45 Q&A: Cloud costing, pricing calculators, and reserved instances

JB Agentic is a friendly community in Johor Bahru for people building software with AI. We meet on the 4th Saturday of every month. Join the next one: https://lu.ma/jbagentic

Subscribe for more talks: https://www.youtube.com/@jbagentic

#JBAgentic #InfrastructureAsCode #Terraform #AIagents #CloudEngineering
```

## Tags

```
AI agents, Infrastructure as Code, Terraform, IaC, cloud engineering, AWS, Azure, Codex, cloud automation, terraform plan, markdown driven development, DevOps, Context7, cloud architect, JB Agentic
```

(15 tags, 201 characters — under YouTube's 500-character limit.)

## Category

Science & Technology
