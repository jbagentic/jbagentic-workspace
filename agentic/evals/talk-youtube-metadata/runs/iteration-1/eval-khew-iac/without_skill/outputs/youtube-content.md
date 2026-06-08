# YouTube Content — AI Meets Infrastructure (Khew Jia Peng)

## Category

Science & Technology

---

## Title Options

1. AI Meets Infrastructure: Deploying Cloud with IaC, AI Agents & Markdown | Khew Jia Peng
2. How I Use AI Agents + Terraform to Deploy Cloud Infrastructure from Markdown
3. From Clicking Portals to Prompting Agents: AI-Driven Infrastructure as Code
4. Let AI Write Your Terraform: An IaC + Agent Markdown Workflow (Live Demo)
5. AI + Infrastructure as Code: Turning Requirements into Deployed Cloud Resources

Recommended primary title: **AI Meets Infrastructure: Deploying Cloud with IaC, AI Agents & Markdown | Khew Jia Peng**

---

## Description

What if you could deploy cloud infrastructure just by writing down your requirements and letting an AI agent do the rest?

In this JBAgentic meetup talk, cloud engineer Khew Jia Peng shares a proof-of-concept that brings AI into the infrastructure layer, not just the software layer. Instead of clicking through the Azure or AWS portal one resource at a time, Jia Peng captures requirements in a markdown file and lets an AI agent (Codex) read it, generate Terraform Infrastructure as Code (IaC), validate it, and run `terraform plan` before anything touches a live environment.

He walks through the full end-to-end workflow live: writing requirements in markdown, defining agent behaviour and skills markdown (including guardrails so the agent never blindly runs `terraform apply` on production), generating Terraform, planning a new subnet, and watching the resource appear in AWS. He also covers how Terraform state (`tfstate`) tracks existing infrastructure, how plan/apply handles updates and destroys, and where this is all heading next: a CI/CD pipeline with human PR review before deployment.

The talk closes with a rich Q&A on git diffing requirements, planning before implementing, avoiding agent hallucination with tools like Context7, cost planning with cloud pricing calculators and reservations, and splitting agents and skills (VM, network) for larger workflows.

Topics covered:
- What Infrastructure as Code (IaC) is and why it beats manual portal provisioning
- Integrating AI agents, skills markdown, and agent markdown with Terraform
- A live demo: requirement.md to generated Terraform to deployed AWS subnet
- Terraform plan vs apply, and how tfstate tracks existing resources
- Guardrails to stop agents from messing up production infrastructure
- Next steps: CI/CD with human-in-the-loop PR review and approval
- Q&A: Context7, git diff on requirements, cost planning, reservations, and scaling agents/skills

Speaker: Khew Jia Peng — Cloud Engineer

Recorded at a JBAgentic meetup, 30 May 2026.

Chapters:
00:00 Intro — who is Jia Peng and what is a cloud engineer
00:36 What is Infrastructure as Code (IaC)?
01:24 The problem: manual provisioning by clicking portals
02:55 The idea: integrating IaC with AI agents and markdown
04:46 Live: Terraform code, plan, and apply explained
06:45 Agent markdown, skills markdown, and requirement.md
09:13 Demo — adding a new subnet from a requirement
13:00 Deploying to AWS and the end-to-end workflow
15:08 Traditional vs AI-assisted method
16:19 Wrap-up: the proof of concept and next steps
17:00 Q&A — state files, git diff, plan-first, and reviews
22:34 Q&A — real-world use, MCP servers, and portfolio plans
26:48 Q&A — avoiding hallucination with Context7
30:40 Q&A — Terraform and cost planning (pricing calculator, reservations)
33:18 Q&A — AI for architecture diagrams
35:01 Closing

#InfrastructureAsCode #Terraform #AIAgents #CloudEngineering #DevOps

---

## Tags

infrastructure as code, IaC, terraform, AI agents, cloud engineering, devops, AWS, Azure, markdown, agentic AI, codex, AI infrastructure, cloud automation, terraform plan, terraform apply, tfstate, CI/CD, infrastructure automation, AI coding agents, skills markdown, agent markdown, cloud architecture, context7, JBAgentic, AI meets infrastructure, provisioning, subnet, VPC, pricing calculator, Khew Jia Peng
