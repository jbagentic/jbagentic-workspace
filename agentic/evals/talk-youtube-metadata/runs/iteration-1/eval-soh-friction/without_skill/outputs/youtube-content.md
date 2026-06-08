# YouTube Content — AI for Everyday Friction

**Speaker:** Soh Jun Wei
**Event:** JB Agentic Meetup #1 (30 May 2026)
**Topic:** Building a personal expense-tracking AI agent with Hermes + MCP

---

## Category

**Science & Technology**

(YouTube category ID 28)

---

## Title Options

Pick one. All are under 100 characters and front-load the hook.

1. AI for Everyday Friction: Building a Personal Expense Agent with Hermes & MCP
2. I Built an AI Expense Tracker on Telegram (Hermes Agent + MCP) — Soh Jun Wei
3. Stop Logging Expenses Manually: A Telegram AI Agent with MCP Tools
4. From Coder to Orchestrator: Building a Real AI Agent with Hermes + MCP
5. MCP vs CLI: How I Built an AI Budget Tracker That Actually Works

**Recommended primary title:**
> AI for Everyday Friction: Building a Personal Expense Agent with Hermes & MCP

---

## Description

```
What if logging an expense was as easy as sending a text, a voice note, or a photo of a receipt?

In this JB Agentic Meetup #1 talk, Soh Jun Wei walks through how he built a personal expense-tracking AI agent to kill the everyday friction of recording spending. Instead of opening an app and keying in numbers manually, he sends a quick Telegram message — "lunch 5.5" — and an AI agent extracts the details, runs any calculations, and saves the record to a database automatically. Voice messages and receipt photos work too.

The real lesson isn't the finance app — it's the architecture. Jun Wei shares why he splits an AI application into two halves: fuzzy input (natural language, voice, receipt images) where AI shines, and deterministic actions (database writes, money validation, calculations) that belong to reliable tools. That's where the Model Context Protocol (MCP) comes in — giving the agent well-defined tool boundaries instead of letting it improvise SQL or invent its own workflows.

He also makes the case that AI won't replace developers — it transforms the job. We shift from writing 80% of the code to designing 80% of the system: deciding what to build, defining how the AI is allowed to act, and verifying the result. We move from coder to orchestrator to architect.

Chapters:
00:00 — Intro & the problem: friction is the enemy
02:00 — The vision: effortless text, voice, and receipt input
04:30 — System design: Telegram + Hermes agent + MCP
06:00 — Live demo: Telegram bot and the dashboard
08:00 — Architecture deep dive (Oracle Cloud, Docker, Groq, OpenRouter)
11:30 — Why MCP? Reducing the agent's guesswork
13:30 — Inside the MCP: tools, schemas, and a calculator
15:30 — Fuzzy input vs deterministic action
17:00 — From coder to orchestrator: how the developer's role changes
21:00 — MCP vs CLI: which should you use?
22:30 — Limitations & next steps (tax errors, personality "Auria")
25:00 — Key takeaways
26:30 — Q&A (Telegram polling, WhatsApp support, Whisper models, Groq limits)

Tech stack covered:
• Hermes agent (running 24/7 in a Docker container on Oracle Cloud's free VPS tier)
• Telegram as the messaging channel (via bot token + polling/gateway)
• MCP server (Node.js) for deterministic tools like add-expense and calculate
• SQLite database + Next.js admin dashboard
• Speech-to-text via Whisper (Groq free API, large model) and OpenRouter for reasoning (Qwen) and receipt vision (Gemini Flash)

Key takeaway: You don't need a huge AI project to get started. Spot the small frictions in your daily life, use AI for the fuzzy understanding, use tools for the deterministic actions, and design the boundaries the AI is allowed to operate within.

#AI #MCP #AIAgents #Telegram #SoftwareEngineering
```

---

## Tags

```
AI for everyday friction, AI agent, Hermes agent, MCP, Model Context Protocol, expense tracker, AI expense tracking, budget tracking app, Telegram bot, Telegram AI agent, MCP server, MCP vs CLI, Node.js MCP, personal finance AI, AI agent architecture, fuzzy input deterministic action, LLM tools, AI tool calling, Whisper speech to text, Groq API, OpenRouter, Qwen, Gemini Flash vision, SQLite, Next.js dashboard, Docker, Oracle Cloud free tier, AI for developers, coder to orchestrator, AI software architecture, JB Agentic, Soh Jun Wei, build an AI agent, receipt OCR, voice to text expense
```

---

## Notes

- The transcript is auto-generated from a non-native English speaker, so some phrasing was cleaned up for the description (e.g., "OpenClaw" appears to refer to an open-source agent framework discussed alongside Hermes; "Auria" is the assistant personality the speaker is adding).
- Chapter timestamps are derived from the SRT cue times and rounded to natural section boundaries; verify against the final published video, as exact cut points may shift slightly.
- Model names mentioned (e.g., "Qwen 3.5 27B") are as spoken in the talk and may be approximations by the speaker.
- Category "Science & Technology" is the best fit for a technical developer talk; "Education" is a reasonable alternative if the channel positions content as tutorials.
```
