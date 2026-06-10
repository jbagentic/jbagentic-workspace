# YouTube Publishing Pack

**Talk:** AI For Everyday Friction: Building a personal expense agent with Hermes and MCP
**Speaker:** Soh Jun Wei
**Series:** JB Agentic Meetup #1 — 30 May 2026
**Content type:** Talk (recorded meetup talk)
**Recommended category:** Science & Technology

> Chapter timestamps assume the published video starts at the first spoken word (0:00). If you add an intro card or trim a lead-in, shift every marker by the same offset and re-check against the final cut.

---

## A/B Test Titles

Pick all three for YouTube's Test & Compare — each tries a different angle. The searchable keyword sits up front so it survives YouTube's ~60-char search truncation, and every title carries the ` | JB Agentic Meetup #1` series suffix.

| # | Angle | Title | Chars |
|---|-------|-------|-------|
| A | Keyword / SEO | `Build an AI Expense Tracker with MCP + Telegram \| JB Agentic Meetup #1` | 70 |
| B | Curiosity hook | `I Log Expenses by Texting a Telegram Bot — Here's How \| JB Agentic Meetup #1` | 76 |
| C | Lesson / outcome | `AI for Fuzzy Input, Tools for the Rest: An MCP Agent \| JB Agentic Meetup #1` | 75 |

---

## Description (copy-paste ready)

```
🎤 Talk: "AI For Everyday Friction: Building a personal expense agent with Hermes and MCP" by Soh Jun Wei
📍 JB Agentic Meetup #1 — 30 May 2026

Recording an expense should take one tap, not ten. Soh Jun Wei got tired of the friction in expense-tracking apps — open the app, wait for it to load, key everything in by hand — so he built a personal expense agent he can drive from Telegram. Send a quick text like "lunch 5.5", a voice message, or just a photo of the receipt, and the agent extracts the details, does the math, and saves the record to a database you can review in a dashboard.

This is a build story, not a product pitch. Soh walks through the whole journey: the architecture, why he wrapped the database work in an MCP server instead of letting the agent free-style SQL, and the bigger lesson he took away — use AI for the fuzzy parts (language, voice, receipts) and deterministic tools for everything that has to be exact (validation, calculation, database writes). The developer's job shifts from writing every line to designing the boundaries the AI is allowed to act within.

What's covered:
• The real problem: friction, not the app — and what "effortless input" could look like
• Text, voice, and receipt-photo input, all flowing through a Telegram bot
• Full architecture: Telegram → Hermes agent → MCP → SQLite → Next.js dashboard, hosted free on Oracle Cloud
• Speech-to-text trade-offs: local Whisper small vs Groq's free Whisper-large API
• Models behind it: OpenRouter for reasoning, Gemini Flash vision for receipts
• Why prompting alone breaks down, and how an MCP gives the agent predictable, reusable tool boundaries
• MCP vs CLI — how to decide how much work to lift to the AI
• The core idea: fuzzy input → AI, deterministic actions → tools
• From coder to orchestrator/architect: how an AI-era developer's role changes
• Q&A: Hermes + Telegram polling, WhatsApp support, open-sourcing the project, Whisper small vs large

Chapters:
0:00 Intro — AI for everyday friction
0:53 The problem: friction in recording expenses
2:51 The enemy is friction — imagining effortless input
3:27 Text, voice, and receipt-photo input
5:03 System design: Telegram + Hermes agent + MCP
6:19 Live demo: the Telegram bot and the dashboard
8:27 Architecture & hosting on Oracle Cloud
9:33 Models & speech-to-text: Whisper, Groq, OpenRouter, Gemini
10:54 The execution layer: why build an MCP
11:58 Why prompting alone breaks
14:49 What an MCP actually is — the expense tool walkthrough
16:04 The key split: fuzzy input (AI) vs deterministic actions (tools)
17:00 From coder to orchestrator and architect
21:05 MCP vs CLI: how much work to lift to the AI
22:33 Known limitations & next steps (the "Auria" personality)
25:09 Conclusion: start from small friction
26:34 Q&A

📅 JB Agentic is a friendly community in Johor Bahru for people building software with AI. We meet on the 4th Saturday of every month. Join the next one: https://lu.ma/jbagentic

👉 Subscribe for more talks: https://www.youtube.com/@jbagentic

#JBAgentic #AIAgents #MCP #TelegramBot #AgenticAI
```

---

## Tags

```
AI agent, MCP, Model Context Protocol, expense tracker, Telegram bot, Hermes agent, AI app development, personal finance app, SQLite, agentic AI, fuzzy input vs deterministic, OpenRouter, Whisper speech to text, Groq API, JB Agentic Meetup
```

Total: 15 tags, well under YouTube's 500-character limit.

---

## Category

`Science & Technology`
