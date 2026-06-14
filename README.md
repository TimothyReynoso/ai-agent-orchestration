# AI Agent Orchestration System

A production multi-agent AI system running 9 specialized agents on a heartbeat-based scheduling loop. Built on OpenClaw (open-source agent runtime), Discord (communication bus), and Supabase (shared state). Each agent has persistent memory, role-specific skills, autonomous task execution, and a strict escalation hierarchy.

This isn't a demo or a prompt chain. This system runs our company day-to-day.

## The 9 Agents

| Agent | Role | What It Does |
|-------|------|-------------|
| **Ghost** | CEO | Strategy, approvals, escalations, founder's right hand |
| **Maya** | Coordinator | Routes tasks, monitors workload, first-line escalation |
| **Dex** | Sales | Lead generation, directory scraping, pipeline building |
| **Raven** | Sales | Cold email campaigns, follow-ups, negotiation |
| **Jin** | Engineering | Frontend development, React/Next.js, responsive design |
| **Neo** | Engineering | Backend, APIs, Supabase, Stripe, security/RLS |
| **Aria** | Sales | Upwork/freelance pipeline, proposal writing |
| **Sage** | Research | Market research, competitor analysis, technique discovery |
| **Cash** | Finance | Invoicing, payment tracking, billing management |
| **YUMI** | Content | Viral AI video production, social media content engine |

Yes, that's 10. YUMI was the latest addition.

## Architecture

```
                    [Founder/Timothy]
                          |
                        [Ghost] (CEO)
                          |
                    [Maya] (Coordinator)
                    /    |    |    \
              [Dex] [Raven] [Jin] [Neo] ...
              Sales   Sales   Dev   Dev
```

### Communication Bus

Every agent has its own Discord channel (#ghost, #maya, #dex, etc.). Agents communicate through:
- **Task routing** via the orchestrator (Maya assigns, agents execute)
- **Channel activity** in #agent-activity (all agents post updates)
- **Escalations** in #escalations (urgent issues)
- **Approvals** in #approvals (things needing human sign-off)

### Memory System

Each agent has three layers of memory:

1. **MEMORY.md** - Long-term persistent memory (decisions, preferences, client info, lessons learned)
2. **memory/YYYY-MM-DD.md** - Daily logs (what happened today)
3. **Shared agency files** - Company-wide knowledge (clients, decisions, protocols, tech stack)

Memory is mandatory. If an agent learns something important and doesn't write it down, it's gone after context compaction. The memory_search tool provides semantic search across all memory files.

### Task Lifecycle

```
Task Created -> Maya Routes -> Agent Receives -> Execute -> Complete
                                              -> Blocked -> Escalate to Ghost
                                              -> Needs Approval -> #approvals
```

Tasks flow through Mission Control (a Supabase-backed dashboard at mission-control-api-gamma.vercel.app) where the CEO monitors pipeline health, agent activity, and revenue.

### Heartbeat System

Every agent runs on a heartbeat loop (15-60 min intervals depending on role). Each heartbeat:

1. Check for assigned tasks
2. Check team health (are other agents responsive?)
3. Review activity log
4. Check pipeline (leads, deals, revenue)
5. Handle escalations
6. Log heartbeat to Mission Control

The CEO (Ghost) runs a 30-minute heartbeat. Developers run 60-minute. Sales agents run 30-minute.

### Specificity Hierarchy

We invented a CSS-inspired priority system for agent instructions:

| Priority | Document | Weight | Override Power |
|----------|----------|--------|----------------|
| Highest | HEARTBEAT.md | 1000 | Overrides everything |
| Medium | MEMORY.md | 100 | Default behavior |
| Lowest | Chat messages | 10 | Can be overridden |

This solves the problem of agents receiving conflicting instructions from multiple sources. HEARTBEAT.md always wins.

## Agent Distillation Process

Creating a new agent isn't just writing a prompt. Each agent goes through a multi-phase distillation pipeline before deployment.

### Phase 1: Role Definition

Define the agent's scope, reporting structure, decision authority, and KPIs. Document in SOUL.md (personality) and AGENTS.md (workspace).

### Phase 2: Memory Seeding

Pre-load the agent's MEMORY.md with:
- Company background and org structure
- All relevant protocols and processes
- Technical knowledge (tools, APIs, patterns)
- Past mistakes and lessons learned (so they don't repeat them)
- Key relationships and escalation paths

### Phase 3: Skill Development

Build role-specific skills (markdown instruction files that OpenClaw loads on-demand). For example, YUMI (our content agent) has 4 skills:
- **content-creation** - Hook formulas, video structure, platform rules
- **script-writing** - Script templates, pacing, tone matching
- **trend-analysis** - How to identify and ride trends
- **video-production** - Full rendering pipeline (LongCat, ffmpeg, SFX mixing)

### Phase 4: Pipeline Integration

Connect the agent to its tools and data sources:
- Discord channel + webhook
- Mission Control API access
- Relevant MCP servers (GitHub, Playwright, search)
- External APIs (Replicate, Modal, Stripe, etc.)

### Phase 5: Heartbeat Configuration

Write a HEARTBEAT.md that defines the agent's operational loop - what to check, in what order, with what frequency. Include alert conditions and escalation triggers.

### Phase 6: Testing and Refinement

Run the agent through real tasks. Every mistake gets documented in MEMORY.md and LESSONS_LEARNED.md. The agent improves iteratively.

### Case Study: YUMI (Content Agent)

YUMI was built to automate viral video production. The distillation process:

1. **Role:** Content creator for social media (TikTok, Reels, Shorts)
2. **Memory seeded with:**
   - 93KB viral UGC blueprint (12 hook formulas, 5-beat video structure, platform rules)
   - Full video production pipeline docs (image gen, TTS, animation, audio mixing)
   - 22-SFX library catalog with usage rules
   - Character consistency protocols
   - Pronunciation rules, personality locks
3. **4 skills built:** content-creation, script-writing, trend-analysis, video-production
4. **Pipeline connected:** GPT-Image (images), edge-tts (voice), LongCat-Video-Avatar on Modal A100 (animation), ffmpeg (post)
5. **Heartbeat:** Content schedule-driven (produce N videos/day, track performance, iterate)
6. **Refinement:** Every video produced revealed edge cases. Over 8 iterations we documented: physics limitations (sparks yes, smoke no), audio desync compounds across splits, character mapping errors in multi-person scenes, voice pronunciation gotchas. Each lesson baked back into memory.

Result: YUMI can autonomously produce a complete viral video (script, images, voice, animation, SFX, music, final render) without human intervention. The content bible alone is 34,000 words.

## Tech Stack

- **Agent Runtime:** OpenClaw (open-source agent framework)
- **Communication:** Discord (each agent has a channel, managed via bot)
- **Database:** Supabase (PostgreSQL) for shared state, task tracking, lead pipeline
- **Dashboard:** Mission Control (Next.js on Vercel)
- **Models:** Mix of GLM-5 (complex reasoning) and GLM-4.7-Flash (fast execution)
- **Memory:** Markdown files with semantic search via OpenClaw's memory_search
- **MCP Servers:** GitHub, Brave Search, Playwright (via mcporter)
- **Monitoring:** Cron-based heartbeat system, activity logging, health checks

## Key Innovations

### 1. Specificity Hierarchy
CSS-inspired instruction priority system. Not in OpenClaw docs - we created this pattern to solve reliability issues with conflicting instructions.

### 2. Mandatory Memory Protocol
Every important interaction gets written to MEMORY.md immediately. No exceptions. "I'll remember that" = FORGOTTEN. Writing to file = REMEMBERED.

### 3. Heartbeat-Based Autonomy
Agents don't wait for instructions. They run heartbeat loops that check for work, monitor team health, and handle escalations autonomously.

### 4. Escalation Chain
Clear chain: Agent -> Maya (coordinator) -> Ghost (CEO) -> Timothy (founder). Each level has defined decision authority.

### 5. Agent Distillation Pipeline
Repeatable process for creating new agents. From role definition through testing to deployment. Each agent inherits the collective lessons of every agent that came before.

## Project Structure

```
ai-agent-orchestration/
  config/
    agents.json          # 9-agent configuration, roles, routing rules
  docs/
    AGENT_ARCHITECTURE.md  # Personality + identity docs (SOUL.md pattern)
    HEARTBEAT.md           # Heartbeat workflow template
    MEMORY_EXAMPLE.md      # Memory structure example (sanitized)
    PROTOCOLS.md           # Agency-wide protocols and rules
  src/
    agent_base.py          # Base class: memory, tasks, escalation, heartbeat
    orchestrator.py        # Task routing, health monitoring, metrics
```

## Results

- **4 billion+ tokens of OpenClaw usage** across the agent team
- **Self-sustaining operations:** Agents handle day-to-day work autonomously
- **Built and shipped:** SaaS products, client websites, video content, research pipelines
- **Iterative improvement:** Every mistake documented, every lesson baked back into the system

## License

MIT

---

Built by [Molt Studios](https://github.com/moltstudios) | Powered by [OpenClaw](https://openclaw.ai)
