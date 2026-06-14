# Molt Studios Protocols

> How we do things. All agents must follow these protocols.

---

## 🧠 Memory Protocol (MANDATORY — ALL AGENTS)

### Rule 1: Write Immediately
If ANY of these happen, write to MEMORY.md **immediately**:
- Timothy gives a preference or instruction
- A decision is made
- A client detail is learned
- A new process is established
- A mistake is made (document it to avoid repeating)

### Rule 2: Search Before Answering
Before answering questions about:
- Past decisions
- Client details
- Preferences
- Processes
- Anything discussed before

**ALWAYS run:** `memory_search("relevant query")`

### Rule 3: No Mental Notes
- "I'll remember that" = FORGOTTEN
- Writing to file = REMEMBERED
- If you want to remember something, WRITE IT DOWN

### Rule 4: Update Shared Memory
If something affects the whole agency:
1. Write to `~/agency/shared/MEMORY.md`
2. Or appropriate shared file (`decisions.md`, `clients.md`, etc.)

### Rule 5: Daily Logs
Every agent writes to their own `memory/YYYY-MM-DD.md`:
- What they did today
- What's pending
- Any blockers

---

## 💬 Discord Communication Protocol

### Channel Usage

| Channel | Who Posts | What Goes Here |
|---------|-----------|----------------|
| #server-updates | Ghost | Major agency announcements |
| #agent-activity | All agents | Daily updates, task completions |
| #pipeline | Maya | Lead status, deal stages |
| #revenue | Cash | Payment updates, invoices sent |
| #agent-status | Maya | Which agents are active/busy |
| #prospector-leads | Dex | New leads found |
| #email-campaigns | Raven | Email outreach status |
| #negotiations | Raven | Active deal negotiations |
| #upwork-jobs | Aria | Jobs found on Upwork |
| #active-projects | Jin, Neo | Project progress updates |
| #deployments | Jin, Neo | Site launch notifications |
| #lead-gen-research | Sage | New scraping techniques |
| #competitor-analysis | Sage | Competitor findings |
| #billing | Cash | Invoice questions, payment issues |
| #client-support | All | Client issues needing attention |
| #approvals | Ghost | Things needing Timothy's sign-off |
| #escalations | Ghost | Urgent issues |

### When to Escalate to Ghost
- Client issue beyond your authority
- Technical decision with no clear answer
- Budget/cost decision
- Anything Timothy should know about

### When to Escalate to Timothy
- Ghost can't decide
- Legal/contract issues
- Major budget decisions (>$500)
- Strategic direction questions

---

## 🎯 Task Routing Protocol

### Maya's Routing Rules

**Incoming Task → Route To:**

| Task Type | Route To | Example |
|-----------|----------|---------|
| Find leads | Dex | "Find dentists in LA without websites" |
| Send cold email | Raven | "Email these 20 leads" |
| Upwork job | Aria | "Apply to this job on Upwork" |
| Build frontend | Jin | "Create landing page for client X" |
| Build backend | Neo | "Set up Stripe payments for client X" |
| Research technique | Sage | "Find better scraping methods" |
| Send invoice | Cash | "Invoice client X $500" |
| Approval needed | Ghost → Timothy | "Client wants discount" |

---

## 💰 Pricing Protocol (TBD)

> To be established after first few clients

---

## 🚨 Emergency Protocol

### If Something Breaks
1. Post in #escalations
2. Tag Ghost
3. Ghost decides if Timothy needs to be woken up

### If Client is Angry
1. Post in #client-support
2. Ghost takes point
3. De-escalate, then solve

### If Agent Gets Stuck
1. Post in #agent-activity with "BLOCKED:" prefix
2. Maya reassigns or Ghost helps

---

## 🔬 Technical Validation Protocol (June 5 — MANDATORY)

> **Applies to:** Any project involving custom models, API integrations, complex pipelines, or unfamiliar frameworks.

### The Rule
**Never package before validating.** Prove the core mechanic works on the simplest possible setup before building any deployment infrastructure.

### The Sequence
1. **Validate (1-2 hrs):** Rent GPU/cloud resource → load models/data → run the simplest possible inference/call → confirm output exists and looks right
2. **Understand (1-2 hrs):** Read source code (not just README/docs) → document the actual API → test edge cases → understand failure modes
3. **Package (2-4 hrs):** Now build the Docker image / serverless function / API wrapper → bake all deps → test packaged version against validated baseline
4. **Deploy (1-2 hrs):** Push to production → set up monitoring → load test → document for team

### Red Flags — Stop and Re-evaluate
- **2 failed attempts at the same approach** → Step back, ask "Is there a faster way to test this?"
- **Spending time on build infrastructure without testing the core logic** → You're optimizing prematurely
- **Blaming the platform** → Verify it's actually a platform limit, not a local setup issue
- **Documentation says X but source code says Y** → Trust the source code

### Platform Preferences for GPU Work
- **Modal** (Plan A): Volume caching, fast image builds, $3.45/hr A100, proven
- **RunPod** (Plan B): Cheaper per-hour but less polished developer experience
- **Replicate** (Specific use): Good for serving models to others, bad for custom pipelines with unusual deps

### Key Reminders
- Prebuilt wheels exist for most compiled packages (flash-attn, xformers, etc.) — search before compiling
- `torch.no_grad()` not `torch.inference_mode()` for model inference (based on LTX-2.3 and LongCat experience)
- Always check GPU memory budget before starting: model weights + activations + intermediate tensors
- Never put API tokens or credentials in documentation files
