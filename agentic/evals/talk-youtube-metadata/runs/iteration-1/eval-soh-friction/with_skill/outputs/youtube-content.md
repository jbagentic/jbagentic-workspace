# YouTube content — Soh Jun Wei, "AI for Everyday Friction"

## Original talk title

**AI for Everyday Friction** — building a personal expense agent with Hermes and MCP (Soh Jun Wei, JB Agentic Meetup #1, 2026-05-30)

## 3 A/B-test titles

Each is ≤70 characters including the ` | JB Agentic Meetup #1` suffix, with the searchable keyword ahead of the suffix. The three test different angles.

1. **Keyword / SEO** — `Build an AI Expense Tracker with MCP + Telegram | JB Agentic Meetup #1` (70 chars)
2. **Curiosity hook** — `Why I Stopped Letting AI Write My SQL | JB Agentic Meetup #1` (60 chars)
3. **Benefit / outcome** — `Log Expenses by Voice, Text or Receipt Photo | JB Agentic Meetup #1` (67 chars)

## Description (copy-paste ready)

```
Build an AI expense tracker that logs spending from a plain Telegram message, a voice note, or a photo of a receipt — and learn why the reliable part isn't the AI, it's the MCP tools behind it.

Soh Jun Wei shares the full journey of building "AI for Everyday Friction" — a personal expense-tracking agent on the Hermes agent framework, using MCP to give the AI safe, predictable tools — at JB Agentic Meetup #1.

What's covered
- The real enemy isn't a bad app, it's friction: the small steps that stop you logging expenses
- The idea: log "lunch 5.5" by text, voice, or a receipt photo and have it just save
- Live demo: Telegram bot capturing snacks, voice notes, and receipts into a dashboard
- The architecture: Telegram → Hermes agent → MCP tools → SQLite, hosted free on Oracle Cloud
- Speech-to-text with Whisper (local vs Groq free API) and OpenRouter (Qwen, Gemini Flash vision)
- Why prompting the agent to write SQL is unpredictable, and how an MCP tool fixes it
- The core lesson: AI for fuzzy input, deterministic tools for hard rules like money and validation
- From coder to orchestrator: developers design the boundaries the AI is allowed to act within
- MCP vs CLI: when each makes sense for handing work to an agent
- Q&A: how Hermes polls Telegram via a gateway, WhatsApp support, open-sourcing, Whisper limits

Chapters
0:00 Intro: AI for everyday friction, and the expense-logging problem
2:15 The enemy is friction, not the app
3:00 The idea: effortless input by text, voice, or receipt photo
4:30 Implementation: Telegram + Hermes agent + MCP
6:00 Live demo: logging snacks, voice notes, and receipts
7:30 Building a dashboard for manual control
8:15 Architecture and hosting free on Oracle Cloud
9:45 Speech-to-text and models: Whisper, Groq, OpenRouter, Gemini
10:30 The MCP execution layer and why raw SQL is risky
13:30 What MCP actually is, and why it beats prompting
15:45 Fuzzy input for AI, deterministic tools for hard rules
17:15 AI won't replace developers — coder to orchestrator
19:30 Splitting fuzzy input from deterministic action
21:00 MCP vs CLI: how much work to hand the AI
24:00 Limitations, next steps, and adding a personality
25:30 Conclusion: start from small friction
26:15 Q&A: how Hermes integrates with Telegram (polling, gateway)
28:30 Q&A: WhatsApp support and open-sourcing the project
30:45 Q&A: Whisper small vs large, accuracy, and usage limits

Timestamps assume the published video starts where the transcript starts; if an intro card or trimmed lead-in shifts the timeline, sanity-check the chapters against the final cut.

About JB Agentic
JB Agentic is a friendly community in Johor Bahru for people building software with AI. We meet on the 4th Saturday of every month to share what's working, honest lessons, and the problems we're still figuring out. Join us: https://lu.ma/jbagentic

Subscribe for past and future talks: https://www.youtube.com/@jbagentic?sub_confirmation=1

#JBAgentic #MCP #AIagents #ExpenseTracker #TelegramBot
```

## Tags

```
AI agents, MCP, Model Context Protocol, Telegram bot, expense tracker, personal finance app, Hermes agent, OpenClaw, SQLite, vibe coding, AI app development, voice to text, Whisper, OpenRouter, JB Agentic
```

(15 tags, 204 characters — under YouTube's 500-character limit.)

## Category

Science & Technology
