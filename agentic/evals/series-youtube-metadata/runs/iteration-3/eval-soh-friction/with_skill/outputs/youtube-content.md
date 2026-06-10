# YouTube content — AI For Everyday Friction

**Full title:** AI For Everyday Friction: Building a personal expense agent with Hermes and MCP

## Titles (A/B test — 3 angles)

1. Build an AI Expense Agent with Hermes & MCP | JB Agentic Meetup #1
2. I Killed Expense-Logging Friction with AI | JB Agentic Meetup #1
3. Log Expenses by Voice & Photo with an AI Agent | JB Agentic Meetup #1

(Angles: 1 = keyword/SEO, 2 = curiosity hook, 3 = concrete benefit. Each ≤ 70 chars including the suffix, keyword ahead of the ~60-char search cut.)

## Description (copy-paste ready)

Logging every expense is a good habit — until the friction of opening an app and typing it in kills it. This talk builds a personal AI expense agent you message on Telegram: type "lunch 5.5", send a voice note, or snap a receipt, and it categorizes, calculates, and saves the record for you. The real lesson is the architecture — let AI handle the fuzzy input, but hand every hard rule to a tool through an MCP.

🎤 Talk: "AI For Everyday Friction: Building a personal expense agent with Hermes and MCP" by Soh Jun Wei
📍 JB Agentic Meetup #1 — 30 May 2026

What's covered:
• Why friction — not a bad app — is what makes you stop tracking expenses
• An agent that takes text, voice, and receipt photos over Telegram
• The stack: Hermes agent in Docker on Oracle Cloud free tier, SQLite, a Next.js dashboard
• Speech-to-text and model choices: Whisper, Groq's free API, OpenRouter (Qwen), Gemini Flash for receipts
• Why prompts alone are unreliable, and how an MCP gives the agent well-defined tools
• The core split: AI for fuzzy input, deterministic tools for validation, math, and database writes
• MCP vs CLI, and why a custom tool set leans toward MCP
• How the developer's role shifts from coder to orchestrator and architect

Tech stack: Hermes agent, MCP (Node.js), Telegram, Docker, Oracle Cloud, SQLite, Next.js, OpenRouter (Qwen), Groq Whisper, Gemini Flash

Chapters:
0:00 Intro — AI for everyday friction
1:30 The problem: friction kills expense tracking
3:15 The vision: effortless text, voice & receipt input
6:19 Live demo: Telegram bot + dashboard
8:27 Architecture: Oracle Cloud, Docker & Hermes
9:37 Speech-to-text & model choices (Whisper, Groq, Qwen)
10:51 Why a prompt isn't enough — LLMs are unpredictable
13:40 What an MCP actually is
15:45 Fuzzy input (AI) vs deterministic action (tools)
17:17 From coder to AI orchestrator and architect
21:40 MCP vs CLI: how much do you lift to the AI?
24:23 Limitations & next steps (meet Auria)
25:47 Takeaway: start small, design the boundary
26:36 Q&A

📅 JB Agentic is a friendly community in Johor Bahru for people building software with AI. We meet on the 4th Saturday of every month. Join the next one: https://lu.ma/jbagentic

👉 Subscribe for more talks: https://www.youtube.com/@jbagentic

#JBAgentic #AIAgents #MCP #BuildInPublic #ExpenseTracker

## Tags

AI agent, MCP, Model Context Protocol, Hermes agent, personal expense tracker, expense tracking app, Telegram bot, LLM tools, AI app development, Oracle Cloud free tier, SQLite, Next.js dashboard, OpenRouter, Groq Whisper, build in public

## Category

Science & Technology
