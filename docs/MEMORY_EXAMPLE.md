# MEMORY.md — Agent Memory Structure (Example)

> This file shows the structure and format of an agent's persistent memory.
> In production, each agent maintains its own MEMORY.md with real operational data.

---

## Who I Am

- **Name:** [Agent Name]
- **Role:** [Agent Role]
- **Reports to:** [Manager Agent or Founder]

---

## My Team

| Agent | Role | Model | Channel |
|-------|------|-------|---------|
| Agent A | Coordinator | GLM-5 | Routes tasks |
| Agent B | Developer | GLM-4.7-Flash | Builds frontend |
| Agent C | Researcher | GLM-4.7-Flash | Finds leads |

---

## Key Decisions

- Model assignments based on task complexity vs cost
- Memory protocol enforced across all agents
- Flash agents use free-tier provider endpoints to avoid rate limits

---

## Things to Remember

- Founder wants momentum and progress
- Escalate only what truly needs human attention
- Write everything down immediately
- Search memory before answering questions about the past
- Daily logs go to memory/YYYY-MM-DD.md

---

## Operational Rules

### Specificity Hierarchy

| Priority | Document | Purpose |
|----------|----------|---------|
| Highest | HEARTBEAT.md | Operational enforcement |
| Medium | MEMORY.md | Workflows and procedures |
| Lowest | Chat messages | Temporary suggestions |

### Verification Protocol

1. Check current state before action
2. Take action
3. Verify after action with multiple angles

Never declare done until verification confirms success.

---

## System Status

### Active Projects
- Project A: Description and status
- Project B: Description and status

### Known Issues
- Issue 1: Description and impact

### Lessons Learned
- Always validate the core mechanic before building infrastructure
- Check timestamps on documents before trusting them
- When researching live data: broad search first, narrow filter second
