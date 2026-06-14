# MEMORY.md — Ghost's Personal Memory

> Your long-term memory. Write important things here.

---

## Who I Am

- **Name:** Ghost
- **Role:** CEO of Molt Studios
- **Parent Company:** Reynoso Industries (Timothy, founder)
- **Model:** GLM-5.1 (Z.AI Coding Max)

---

## My Team (9 Agents)

| Agent | Role | Model | Channel |
|-------|------|-------|---------|
| Maya | Coordinator | GLM-5 | Routes tasks, keeps things moving |
| Dex | Prospector | zai-free/GLM-4.7-Flash | **Switching to drone industry leads** |
| Raven | Emailer | GLM-5 | Cold emails, negotiations |
| Jin | Frontend | zai-free/GLM-4.7-Flash | Builds React/Next.js sites |
| Neo | Backend | zai-free/GLM-4.7-Flash | APIs, databases, Stripe |
| Aria | Upwork | GLM-5 | Hunts Upwork jobs |
| Sage | Researcher | zai-free/GLM-4.7-Flash | Improves techniques |
| Cash | Biller | zai-free/GLM-4.7-Flash | Invoices, payments |
| YUMI | Content Creator | GLM-5 | Viral AI content, video production |

---

## LTX-2.3 Custom Replicate Deployment — LIVE

**Status:** WORKING. Video generation confirmed on A100 80GB.
**Model:** `moltstudios/ltx-2.3` on Replicate
**GitHub:** `https://github.com/moltstudios/cog-ltx-2.3.git`
**Project dir:** `~/agency/agents/ghost/cog-ltx-2.3/`
**Source reference:** `/tmp/LTX-2/` (cloned LTX-2 repo)

### Working Configs
| Resolution | Max Frames | Duration @8fps | Time | Cost |
|-----------|-----------|----------------|------|------|
| 512x320 | 9 | ~1s | 82s | ~$0.02 |
| 768x1344 | 25 | ~3s | 83s | ~$0.02 |
| 1088x1920 | 48 | 6s | 98s | ~$0.02 |

### Hard Limits
- **VAE decode ceiling:** ~48 frames at 1088x1920, ~25 at 768x1344
- **Resolution:** Must be divisible by 64
- **Tile overlap:** Must be divisible by 32
- **Temporal tile size:** Must be divisible by 8
- **Container reuse:** OOM'd containers leak GPU memory; wait or push new build

### The Big Bugs Found & Fixed
1. **Missing `torch.no_grad()`** — the #1 memory bug. Without it, every forward pass built a full autograd graph that pinned weights and wasted 17-49GB.
2. **Prequantized FP8 checkpoint** — A100 has no FP8 tensor cores. `fp8_cast()` creates double-residency. Use `Lightricks/LTX-2.3-fp8` with `UPCAST_DURING_INFERENCE` instead.
3. **LTX pipeline's `@torch.inference_mode()` only on CLI `main()`** — when using as library, add your own.

### Next Step (DONE — June 2)
- **LTX-2.3 A2VidPipelineTwoStage** — audio-driven lip sync pipeline
- Uses MultiModalGuider with modality_scale=3.0, cfg_scale=3.0/7.0
- Audio is PRIMARY conditioning input (not just reference like LipDub)
- Native 24fps output — no RIFE interpolation needed
- 40 guided denoising steps (vs 8 unguided LipDub)
- 178s on A100, 97 frames @ 24fps
- Version: `55021c7d0700d3280348a4c0201d80efd83fb5ae699229f70eabaaadd35d33a5`
- **LipDubPipeline was WRONG** — it's text-driven, audio is only a reference signal
- Research doc: `~/agency/projects/lumnix/LIPDUB-RESEARCH.md`

### Key Files
- `predict.py` — main Cog predictor with all monkey-patches
- `cog.yaml` — Docker config (CUDA 12.6, torch 2.7.1)
- `RESEARCH.md` — technical research notes

---

## Key Decisions I've Made

> See ~/agency/shared/decisions.md for full log

- Model assignments (GLM-5 vs Flash)
- Memory protocol for all agents
- Discord channel structure
- Flash rate limit fix: `zai-free` provider for all Flash agents (April 28)
- MC rebuilt on Vercel + Supabase (April 28)

---

## Things to Remember

- **Ocean Scholar voice: Qwen3-TTS "sassy" preset** — Timothy's pick (June 2). Was previously af_aoede (Kokoro bubbly), changed to Qwen3 sassy after reviewing all 38 samples. **Locked sample: #32 `test_tts_ocean_2.wav`** (confirmed June 7).
- **Ocean Scholar APPROVED image sets** (Timothy confirmed June 2):
  - ✅ `v2/character/turnaround/` — 7 angle refs (front, profile, 3q, back, turnaround)
  - ✅ `v2/expressions/` — grids + manifest
  - ✅ `v2/expressions/car-selfie/` — 50 reaction poses
  - ✅ `v2/room/` — 4 background refs (desk, bed, window, wide)
- **Ocean Scholar REJECTED image sets** (don't fit the character):
  - ❌ `v2/character/renders/` — 20 renders (off-brand)
  - ❌ `test-character/poses/anime-stylized/` — 25 expressions (wrong style)
  - ❌ `test-character/poses/grounded-realistic/` — 25 expressions (wrong style)
  - ❌ `test-character/` (entire v1 folder) — superseded by v2
- **Lessons Learned doc:** `~/agency/shared/LESSONS-LEARNED.md` — 25KB, 14 sections, all mistakes/gotchas/patterns documented (created May 19)
- **⚠️ IMAGE RECREATION PROTOCOL (MANDATORY — June 8):** When describing images for recreation/regeneration, ALWAYS use Forensic Mode (zero interpretation, zero narrative, only physical description). Full protocol at `memory/image-recreation-protocol.md`. Applies to ALL channels (Discord, Telegram, etc.).
- **Image analysis model:** Use `openrouter/google/gemini-3.1-flash-lite` ($0.25/M) — tested and proven better than Sonnet ($3/M) at forensic visual detail extraction. 12x cheaper.
- **Pronunciation rule:** "cuzz" ✅ (double-z), NOT "cuhh/cuh/cuz" 🚫 — TTS reads literally, spell it how it should sound
- **Ocean Scholar personality lock:** Cute, artsy, nerdy, professional but casual. NO street slang, NO "cuzz." Think enthusiastic design student showing off a cool find. (Timothy confirmed June 10)
- **SFX Library:** `~/agency/shared/sfx-library/` — 22 synthesized SFX (impacts, transitions, foley, weapons, stingers, UI, vehicles) + mixing script (`mix_audio.py`)
- **Default BG music:** `~/agency/shared/sfx-library/music/default_bg_beat.wav` — 3:25, the go-to beat for all AI fruit/drama videos (Timothy provided)
- **Audio mixing rules:** Dialogue 100% | SFX 60-80% | Music 22% (ducks to 6% during speech)
- Timothy wants **momentum** — keep things moving
- Don't escalate everything to him — only what truly needs his attention
- Weekly check-ins with Timothy on agency progress
- Monitor #agent-activity for team health
- **Mission Control is on Vercel now** — https://mission-control-api-gamma.vercel.app
- **Flash agents use `zai-free` provider** (general endpoint, free, no rate limit)
- **GLM-5.1 agents stay on `zai` provider** (coding plan endpoint)
- **#executive channel ID: 1480597805419462792** — working for cron reports
- **Stripe account: support@moltstudios.app** (LIVE MODE — activated May 22, 8:20 PM)
- **Stripe LIVE keys deployed** to Vercel prod + dev + local .env.local
- **Live Price IDs:** Pro `price_1Ta3IrPSXzD2ZON6OvJIzsMl`, Business `price_1Ta3IrPSXzD2ZON6v2e1aAyB`
- **Live Portal Config:** `bpc_1Ta3JzPSXzD2ZON6mbSYUh4a`
- **Live Webhook:** `we_1Ta3J7PSXzD2ZON6XyWJrBld` at lumnix.dev/api/stripe/webhook
- **Start lean on API costs:** $16/mo per omkarcloud platform, scale up at 15+ users
- **YouTube Demo (NEW — May 27):** https://youtu.be/8-yOWWWect0 (channel: @Lumnixteams) — "AI Amazon FBA Product Research in 50 Seconds"
- **OLD video (dead account):** https://youtu.be/_BgxM_bxAJM — account suspended, do not use
- **YouTube account:** Lumnix.teams@gmail.com / Whiteowl2486! — @Lumnixteams channel — BE GENTLE, warming up, old account was banned for aggressive activity
- **YouTube rules:** Minimal interaction, no aggressive actions, let account warm up for a few weeks
- **Screenshot inventory:** ~/agency/docs/screenshots/ (11 files, guide at screenshot-inventory.md)
- **Creator tracker:** ~/agency/docs/creator-outreach-tracker.csv (50+ targets)
- **Email templates:** ~/agency/docs/creator-outreach-emails.md (5 templates, all lead with demo video)
- **Pitch strategy:** ~/agency/docs/pitch-strategy-guide.md (sponsorship rates, deal structures)
- **Media outlets research:** ~/agency/docs/media-outlets-research.md (full breakdown of 400+ outlets)
- **BrandPush tiers:** Authority $595 confirmed (BI + AP, NOT Growth)
- **Sender email:** hello@moltstudios.app for all outreach
- **Creator outreach plan:** ~/agency/docs/creator-outreach-plan.md (6-phase plan)
- **Strategy:** Buy Authority AFTER creators commit, article includes creator content, publish together
- **Creator Outreach Playbook:** ~/agency/docs/creator-outreach-playbook.md — full repeatable process, framework, templates, batch status
- **Hyperagent Founding 500 SUBMITTED (June 1):** Application submitted via Airtable form. All fields filled, 6 attachments (Mission Control, Discord activity, Lumnix site, npm, GitHub, demo video). Both consents checked. Confirmation: "Thank you for submitting the form." Now awaiting response.
- **Founding 500 strategy:** ~/agency/projects/lumnix/FOUNDING-500-APPLICATION.md (strategy) + ~/agency/projects/lumnix/FOUNDING-500-DRAFT.md (original draft)
- **Founding 500 submission files:** ~/agency/projects/lumnix/founding-500-submission/
- **YUMI niche: "Curious mind discovers cool shit"** — AI tools, weird science, hidden tricks, product finds, "did you know" content. NOT limited to ocean science. Ocean Scholar is just the character DESIGN, YUMI is the character. Topics evolve based on demand. (Timothy confirmed June 11)
- **YUMI content mix:** 40% edu-tainment / 25% pure entertainment / 20% tool-powered demos / 15% social proofal proof
- **Higgsfield account:** support@moltstudios.app / Whiteowl2486! — MCP URL: https://mcp.higgsfield.ai/mcp — uses OAuth device flow, NOT API key
- **Upload-Post API key:** saved (JWT token) — base URL: api.uploadpost.com — auth header: `Apikey <token>`
- **Video pipeline status:** Phase 1 (build) — Higgsfield logged in, Upload-Post key verified, need plan confirmation + TikTok/IG accounts + Umi agent build
- **4-phase launch:** 1) Pipeline Build (3-5d) → 2) Testing Loop (5-7d, 2 vids/day) → 3) Automation (3-5d) → 4) Scale (ongoing, ramp to 5/day)
- **Batch 1 sent (May 27):** Flips4Miles ✅, Orange Klik ✅, Chris Rawlings ✅, Vova Even ✅, Sumner & Ali ✅
- **Batch 2 in progress (May 27):** Michal Špecián, Jatz Naran, Fields of Profit, Camron James, Trevin Peterson
- **Outreach email sending:** SendGrid (NEW key SG.XeUNgdRlR72gnJQRd7RyPg — 100/day) + Yandex SMTP backup
- **SendGrid account:** support@moltstudios.app / Whiteowl2486!
- **OLD SendGrid key (SG.5Qr...TdQA) is REVOKED** — do not use
- **SMTP app password for hello@moltstudios.app:** stored in memory files (Yandex)
- **Follow-up cadence:** 3-4 days after initial send
- **YC:** Mention "preparing YC application" in outreach for credibility signal
- **Timothy's Stripe login stored in password manager** — I don't store credentials in files
- **npm account:** moltstudios / support@moltstudios.app — token `npm_jOzV...P4O8` (expires Aug 25, 2026 — 90 days, read+write, 2FA bypass, renewed May 27)
- **npm CLI OTP auth is fragile** — browser automation is more reliable for generating tokens
- **npm publish token MUST have 2FA bypass enabled** or publish gets 403
- **Always clean up .npmrc from repo dirs after publishing**
- **Vercel env vars:** Delete by specific entry ID, NOT key name, or DELETE+ADD fails silently
- **Industry benchmark:** 7 days idea→live SaaS vs 11.4 weeks avg solo founder (~8-11x faster)
- **MCP directory submissions (May 25-27):** Smithery ✅ (live at smithery.ai/servers/support-5u4n/lumnix), mcpservers.org ✅ (auto-indexed), Official Registry ✅ (published May 23), PulseMCP ✅ (via registry), mcp.so ✅ (live), Glama ✅ (server listed + verified, connector 404), npm ✅ (v0.2.2)
- **Awesome-list PRs (May 27):** punkpeye #6782 ✅ (badge added, rebased, awaiting merge), jaw9c/tolkonepiu ❌ (repos gone), appcypher ❌ (PRs disabled)
- **mcp-publisher CLI:** Logged in via GitHub device flow, server.json validated
- **Glama is the blocker for punkpeye PR** — RESOLVED May 27. Badge added, PR updated.
- **AI Capability Platform Strategy (May 28):** Full strategic doc at `~/agency/docs/ai-capability-platform-strategy.md`. Covers Replicate API integration, ComfyUI+cloud hybrid, GPU workstation build, MCP server ideas, marketplace opportunity, 3-phase platform play (build tools → curated marketplace → become standard), AWS/Stripe marketing framework. Timothy approved direction.
- **LTX-2.3 deployment (June 1):** Custom Cog deployment on Replicate A100 80GB. Working at 1088x1920 48f. Key bugs: missing torch.no_grad(), fp8 prequant checkpoint, VAE decode ceiling. RIFE interpolation planned for high fps.
- **MCP monetization platforms (May 28):** MCP Marketplace (85/15 split), x402 (micropayments in USDC, 3.3M txns/month, backed by Visa/Stripe/Google), MuleRun (~100% + bonuses), Apify (80/20, $500K+/month payouts)
- **Replicate + ComfyUI integration (May 28):** 3 ways — (1) Replicate models as ComfyUI nodes locally, (2) run ComfyUI workflows on Replicate GPUs, (3) deploy custom ComfyUI as dedicated API on Replicate
- **Platform gap (May 28):** Nobody owns QUALITY in MCP space. 99% free hobby servers. No curation, no App Store-style review. This is the opportunity.
- **Marketing framework (May 28):** "Someone else's AI brain" — same insight as AWS ("someone else's computer") and Stripe ("7 lines of code"). Don't build AI infrastructure, buy it as capability cards.
- **Next step:** Start with Product Video Generator MCP (Lumnix-powered), then AI Content Pipeline MCP, then Research Intelligence MCP
- **AI Employee Copilots strategy (May 28):** Full doc at `~/agency/docs/ai-employee-copilots-strategy.md`. Timothy's idea — sell pre-configured OpenClaw agents (not individual MCP tools). First product: FBA Copilot ($99-199/mo for Amazon sellers). Then Research Copilot ($199-499/mo for medical). Then Legal, Real Estate, Marketing, Finance Copilots. We compete with hiring a VA, not with Helium 10. 100 users = $9,900/mo, 500 users = $49,500/mo.

## Domain & Account Rules

### 🚨 ALL DOMAINS USE support@moltstudios.app FOR REGISTRANT EMAIL
- **ghostsandbox.dev** — updated May 27, 2026 ✅
- **lumnix.dev** — already correct ✅
- **moltstudios.app** — third-party (Yandex), not Vercel
- **Rule:** When registering ANY new domain or service, ALWAYS use `support@moltstudios.app` as the contact/registrant email. This is our main monitored inbox. Never use ghost@, ceo@, or any made-up address.
- **ICANN verification deadline:** ghostsandbox.dev must be verified by May 31, 2026. Verification resent to support@ after email update.

---

## Disk Space Monitoring

**Watch these folders — they grow silently:**
- `~/.cache/huggingface/xet/` — HuggingFace download cache, never auto-cleans. Nuke regularly.
- `~/Library/Caches/Homebrew/` — brew install cache, clear with `brew cleanup --prune=all`
- `~/Library/Caches/pip/` — pip cache, clear with `pip cache purge`
- `~/.cache/huggingface/hub/` — actual models (Kokoro TTS 320MB, Whisper STT 141MB) — KEEP THESE
- `~/fish-speech/checkpoints/` — 10GB voice model, KEEP
- `~/ComfyUI/models/` — 11GB+ AI models, KEEP unless unused
- `~/.openclaw/browser/` — 2.8GB Playwright profiles, watch but don't nuke
- `~/.openclaw/logs/` — 234MB, can rotate if needed

**Disk critical threshold:** < 5GB free = clean immediately
**Disk healthy:** > 15GB free
**Last cleanup:** May 29 — freed 18GB (2.9GB → 21GB free)

---

## Operational Rules

### 🚨 SPECIFICITY HIERARCHY (CRITICAL - Not in OpenClaw Docs)

**Problem:** Agents receive conflicting instructions from multiple sources (MEMORY.md, Discord, heartbeats)
**Solution:** CSS-like specificity hierarchy for instruction priority

| Priority | Document | Weight | Purpose | Override Power |
|----------|----------|--------|---------|----------------|
| **Highest** | HEARTBEAT.md | 1000 | Operational rules, enforcement, cleanup | Overrides EVERYTHING |
| Medium | MEMORY.md | 100 | Workflows, procedures, knowledge | Default behavior |
| Lowest | Discord messages | 10 | Temporary suggestions | Can be overridden |

**Rule:** If HEARTBEAT.md says "ALWAYS do X" and Discord says "do Y instead", follow HEARTBEAT.md.

**This is OUR innovation** - not documented in OpenClaw. We created this pattern to solve reliability issues.

**When to Create HEARTBEAT.md:**
- Agent has recurring reliability issues
- Tasks piling up in wrong status
- Agent not following critical rules
- Need enforcement, not just reminders

**What Goes in HEARTBEAT.md:**
- ONE task at a time rules
- Task completion protocols
- Stale resource cleanup
- Alert conditions
- Verification steps

**Pattern Source:** Timothy's insight about CSS specificity (March 12, 2026)

---

### Verification Protocol (MANDATORY)
**Never trust a single API response. Always verify with multiple angles:**

1. **Before action:** Check current state (list/get)
2. **Take action:** Make the change
3. **After action:** Verify with multiple angles if possible

**Multiple angles = stronger verification.** Look for different ways to confirm:
- API response + re-listing
- API response + visual check (if screenshot possible)
- Two different endpoints that show the same data
- Check logs + check state
- Check database + check API
- **Check timestamps on docs** — stale docs may contradict current reality
- **Check session files per-agent** — `~/.openclaw/agents/<agent>/sessions/sessions.json`

**The spirit:** Always ask "how else can I verify this?" — seek out multiple confirmation paths when available.

**Never declare "Done" until verification confirms success.**

### Stale Information Detection

**ALWAYS check timestamps on documents before trusting them:**
- If a doc appears old, verify current state with live data

---

## System Status (May 27, 2026 — 10:17 AM)

### ✅ Lumnix — LIVE SaaS + npm PUBLISHED + 698 TESTS + FULL BILLING
- **19 TOOLS**, 2 PROMPTS, 6 RESOURCES, **698/698 TESTS**, v0.2.1
- **Renamed: ScoutMCP → Lumnix** (May 18, Timothy's decision)
- **Domain: lumnix.dev** — purchased ($9.99/yr), Vercel-verified, auto-renew
- **Website: https://lumnix.dev** — Next.js 16 on Vercel, LIVE
  - `/api/health` — Health check endpoint ✅
  - `/api/mcp` — Remote MCP endpoint (19 tools, JSON-RPC 2.0, 60s timeout, **required param validation**) ✅
  - `/api/keys` — API key CRUD with plan sync ✅
  - `/api/stripe/checkout` — Checkout with auth + duplicate sub prevention ✅
  - `/api/stripe/webhook` — Webhook handler with error handling + 4-day grace period ✅
  - `/api/stripe/portal` — Customer self-serve billing portal ✅
  - `/api/stripe/verify` — Post-checkout Stripe sync safety net ✅
  - Per-platform rate limiting with atomic counters ✅
  - **Required parameter validation** — returns -32602 for missing params ✅
- **3-TIER PRICING (LIVE — real payments working):**
  - Free: $0, 10/mo (2/day), Amazon only (3 tools), 2 API keys
  - Pro: $29/mo, 5K/mo (250/day), all platforms, all 19 tools, 5 API keys
  - Business: $99/mo, 25K/mo (1000/day), all platforms, all 19 tools, 20 API keys
- **Auth:** Full Supabase Auth (Google OAuth + email/password)
- **Stripe Integration (LIVE MODE — activated May 22, 8:20 PM):**
  - Account: support@moltstudios.app
  - Live Products + Prices created in live mode
  - Live Webhook: `we_1Ta3J7PSXzD2ZON6XyWJrBld` at lumnix.dev/api/stripe/webhook
  - Live Portal Config: `bpc_1Ta3JzPSXzD2ZON6mbSYUh4a`
  - Live keys deployed to Vercel prod + dev + local .env.local
  - Real payments can be processed ✅
- **npm Package — PUBLISHED May 22, 9:30 PM:**
  - Package: `lumnix@0.2.1` — https://www.npmjs.com/package/lumnix
  - Install: `npm install lumnix`
  - Published via browser automation (token with 2FA bypass)
  - Token expires May 29 — regenerate before then if needed
- **Database**: 3 migrations deployed, pg_cron daily resets active
- **Security**: Atomic SQL, RLS on all 12 tables, SHA-256 key hashing, webhook sig verification, INTERNAL.md removed from git
- **698/698 tests passing** (20 test files)
- **Real API integrations verified:**
  - Amazon: 11/11 tools working ✅
  - Alibaba: 4/4 tools working ✅
  - AliExpress: 1/4 working (profit calc), 3 blocked by omkarcloud 500 error
- **Keepa:** $50/mo plan active
- **Health Monitor:** Cron job every 6 hours (ID: c54cb993-67a0-498b-85b2-8b6c93cde8a0)
- **GitHub Repos:**
  - Private: https://github.com/moltstudios/lumnix (full source + CHANGELOG.md)
  - Public: https://github.com/moltstudios/lumnix-mcp (README + npm package, v0.2.1)
  - Website docs/GitHub links all point to public repo ✅
- **Project dir:** ~/agency/projects/lumnix/ (source), ~/agency/projects/lumnix-public/ (npm package)
- **Costs:** ~$98/mo operating cost
- **Timothy's test account:** timothy@lumnix.dev (plan=business, API key: lmx_owrJ4Zx0...)
- **Credentials:** All backed up at `~/agency/shared/credentials/lumnix.md`
- **Session log:** `~/agency/shared/credentials/lumnix-session-log-may22.md`

### Remaining (Priority Order — May 22, 9:50 PM)
1. ~~Stripe live mode~~ ✅ DONE
2. ~~npm publish~~ ✅ DONE (v0.2.1)
3. **MCP directory submissions** — smithery.ai, mcpservers.org (~1 hour)
4. **Onboarding walkthrough** — signup → key → first call demo (~3 hours)
5. **Content / SEO** — blog posts for FBA sellers
6. **Video demo** — YouTube walkthrough for discovery

### Full Day Summary (May 22 — 7 Sessions, ~21 Commits)
**Session 1-5 (morning → 7 PM):** 19 commits
- Billing: Pro→Business upgrade flow, duplicate subscription prevention, auth on checkout, portal with proration
- Dashboard: "Failed to load API keys" typo, "Free" plan display, USER ID MISMATCH
- Security: Webhook error handling, checkout auth, portal auth, verify endpoint fallback
- Dead code: Removed lib/api-keys.ts, updated imports
- Scrapers: alibaba.ts + aliexpress.ts env var read at call time
- New Stripe account: full migration, all env vars, all price IDs, all tests updated
- Vercel env var bug: DELETE+ADD pattern failed silently, fixed by deleting by ID
- Grace period: 4 days for past_due before downgrade
- Param validation: Required MCP params now enforced at route level
- Website: All docs/GitHub links point to public repo
- Docs: CHANGELOG.md added, INTERNAL.md removed from git
- Tests: 698 total (was 690)
- Triple audit: Production correctness, website links, edge cases — all clean

**Session 6 (8:19 PM – 8:42 PM): Stripe LIVE Mode**
- Timothy provided live API keys (pk_live + sk_live)
- Created all resources in live mode: Pro + Business products/prices, webhook, portal config
- Updated ALL Vercel env vars (6 prod + 5 dev) to live keys
- Updated local .env.local to live keys
- Deployed and verified all endpoints working
- Backed up credentials to `~/agency/shared/credentials/lumnix.md`
- Full session log written to `~/agency/shared/credentials/lumnix-session-log-may22.md`

**Session 7 (9:00 PM – 9:50 PM): npm Publish**
- Multiple CLI OTP auth attempts failed (rate limited 429)
- Switched to browser automation — logged into npmjs.com via Playwright
- Retrieved OTP from Yandex email via IMAP (imap.yandex.com)
- Generated granular access token with 2FA bypass + read/write permissions
- First token (no 2FA bypass) → publish failed (403)
- Second token (with 2FA bypass) → publish succeeded ✅
- Deleted old token, only "Lumnix Publish 2FA" remains
- Published `lumnix@0.2.0`, then updated README with npm badge + install cmd → republished as `lumnix@0.2.1`
- Pushed to GitHub (lumnix-mcp repo)
- Cleaned up .npmrc from repo dir

### 🧱 Lumnix Frontend — COMPLETE at https://lumnix.dev
- **Landing Page `/`** — ✅ COMPLETE. Hero + Tool Showcase + Pricing + FAQ + Footer
- **Signup `/signup`** — ✅ COMPLETE. Email + Google OAuth, creates account + redirects to dashboard
- **Dashboard `/dashboard`** — ✅ COMPLETE. API key manager, billing section, usage stats with per-platform breakdowns, MCP server URL with copy button, plan info
- **Color palette:** Warm Gold (#2a2018 → #c8a050 → #f5f0e8)
- **Typography:** Manrope 800 headings, Inter 400 body

### Frontend Direction (Decided May 19)
- **3 pages only** (revised from 6 — Timothy's decision):
  1. **Landing Page `/`** — ✅ COMPLETE
  2. **Signup `/signup`** — ✅ COMPLETE
  3. **Dashboard `/dashboard`** — ✅ COMPLETE
- **Remaining frontend:** Add full mcpServers JSON config block to dashboard, onboarding walkthrough after signup

### Database & Project Structure
- **Supabase project renamed:** "Mission-Control" → "Lumnix" (May 21, Timothy's direction)
- **Project ref:** `srfunhstbufgteiyggur` (unchanged)
- **Shared database:** Lumnix tables (profiles, api_keys, api_usage, subscriptions) + MC tables (mc_*) coexist
- **Future plan:** MC gets its own Supabase project when ready. Lumnix stays. Zero FK overlap makes migration easy.
- **MC security audit:** Done May 21. `DATABASE-SECURITY-OVERVIEW.md` in mission-control-api dir. **mc_leads is highest risk** — PII publicly readable via anon key.

### Remaining for Launch
1. **README + MCP config block on dashboard** — add copy-pasteable mcpServers JSON
2. **Onboarding walkthrough** — after signup, guide user through key creation + first call
3. **pg_cron daily resets** — schedule reset_daily_usage() to run daily
4. **Stripe live mode** — Timothy activates account, swap test keys for live keys
5. **Content / SEO** — blog posts targeting FBA sellers
6. **npm publish** — make installable, submit to MCP directories

### Test Credentials
- **Test user:** `timothy@lumnix.dev` / `Lumnix2026!` (Supabase ID: `1f7b30df-572d-4869-97ad-f29b573cfd94`)
- **Stored at:** `~/agency/projects/lumnix/TEST-CREDENTIALS.md` (gitignored)
- **Email confirmed:** manually via SQL (May 21)

### Dashboard Notes (Timothy's direction, May 21)
- MCP Server URL shown on dashboard with copy button ✅
- Still need: full mcpServers JSON config block for one-click copy
- Claude MCP Store / directories will handle discovery for most users

### 📚 Frontend Research Complete (May 18, 2026)
- **Research doc:** `~/agency/projects/lumnix/research/FRONTEND-DEV-PREP.md` — 19KB comprehensive guide
- **3 personal video reviews:** GSAP 2hr course, CSS Animation 11min, Web Design Advice 9min
- **2 playlists analyzed:** 30 videos total (13 from JS Mastery, 17 from Pixel Grid UI)
- **Transcripts saved:** `~/agency/projects/lumnix/research/transcripts/` (8 files)
- **Stack decided:** Next.js 15 App Router + Supabase Auth + Tailwind + shadcn/ui + GSAP (landing) + CSS (dashboard)
- **Design references:** Stripe Dashboard, Linear.app, Vercel Dashboard (for inspiration)
- **Key GSAP patterns:** useGSAP hook, gsap.context() for cleanup, SplitText for hero, ScrollTrigger for scroll animations
- **Key design principles:** Clarity > beauty, sell results not features, subtle animations, show pricing prominently

### ✅ ScoutMCP MCP Server — 19 TOOLS, 2 PROMPTS, 6 RESOURCES, 192/192 TESTS, v0.2.0 🎉
- **Amazon (11):** search, details, sales estimate, opportunity score, competition, best sellers, keyword suggestions, price history, BSR history, negative review analyzer, listing quality scorer
- **Alibaba (4):** search, details, supplier vet, match-to-Amazon
- **AliExpress (4):** search, details, supplier score, profit calculator
- **192/192 tests passing** (13 test files)
- **v0.2.0** — all 19 tools registered

### 📦 Prompts (2)
- `full_niche_analysis` — 8-step workflow: search → competition → opportunity → negative reviews → **image gap analysis** → keywords → sourcing → go/no-go (🟢🟡🔴)
- `listing_optimizer` — 6-step: audit → competitor analysis + image gaps → keyword research → rewrite → before/after → image recommendations (image purpose framework)

### 📦 Resources (6)
- `fba-fee-schedule` — FBA fees by size/weight, referral fees by category, storage costs
- `listing-checklist` — Step-by-step optimization checklist
- `alibaba-red-flags` — Scam prevention + verification checklist
- `amazon-character-limits` — All field limits + image specs
- **`image-purpose-guide`** — 15 image types, ordering strategy, Rule of 3, mobile-first, A/B testing
- **`review-removal-guide`** — 8 removable violation types, monitoring methods, response templates, insert card strategy

### 📚 Research (14 Videos Analyzed)
- LISTING-RESEARCH.md — 45KB, 1,148 lines (transcripts + synthesis)
- VISUAL-RESEARCH.md — 12KB, 303 lines (82 screenshots + visual analysis)
- PROMPTS-DESIGN.md — 8KB (future prompts + resources designed)

### Key Insights from Video Research
- Amazon ranks by: Sales Velocity + Relevance + Customer Satisfaction
- CTR = title + main image. CVR = bullets + images + description + A+ (separate scoring is critical)
- Image Purpose framework: every image has ONE clear purpose, 3-4 revisions normal, A/B test everything
- "Barrel capacity" technique: find image types NO ONE in the niche has → differentiate instantly
- ~10-20% of negative reviewers update to 4-5★ if contacted within 24 hours
- Product insert cards boost review rate from <1% to 40%+
- Break-even ACoS = pre-ad profit margin. If margin is 30%, break-even ACoS is 30%.
- 3 ranking killers: running out of stock, listing hijackers, bad reviews

### Production MVP: ~95%
**Remaining:** README.md + MIT LICENSE + Timothy's npmjs account + GitHub repo

### ✅ MCP Research — Complete
- 57KB knowledge base in ~/agency/projects/mcp-research/
- 7 videos analyzed, 26 screenshots, 2 X posts
- Expert-level understanding across all MCP primitives

### ✅ MCP omkarcloud API — All 3 Platforms
- Key: ok_447901c3bb0ef45d394544934003af99 (same key for all 3)
- Amazon: 100 free/mo, $16/mo 15K (search + details, 50+ fields, NO BSR)
- Alibaba: ~200-1000 free/mo, $16/mo 1.6K (search + details, pricing tiers, supplier data)
- AliExpress: 100 free/mo, $16/mo 3K (search + details, orders, ratings, variants)

### 🧪 Ghost Sandbox — Component Testing Playground (May 17)
- **Domain:** ghostsandbox.dev (purchased via Vercel, $9.99/yr)
- **URL:** https://www.ghostsandbox.dev
- **Purpose:** General-purpose component testing — isolated from Molt Studios. NOT affiliated with any project.
- **Stack:** Next.js 14 + React + Framer Motion
- **Location:** ~/agency/projects/component-sandbox/
- **Vercel project:** component-sandbox (under molt-studios team but functionally separate)
- **Vercel Auth:** Disabled (public access)
- **DNS:** Managed by Vercel (ns1/ns2.vercel-dns.com)
- **SSL:** Auto-managed by Vercel
- **Created:** May 17, 2026
- **Hub page:** Live at / with links to all 4 pages + full pattern documentation
- **4 pages:**
  - `/` — Ghost Sandbox Hub (docs + links)
  - `/tool-cards.html` — 38 cards (8 showcase s1-s8 + 30 palette cards)
  - `/cool-animations.html` — GSAP animation demos
  - `/lumnix-animations.html` — Product animations
  - `/design-system.html` — 43 palettes, 20 typography systems
- **Nav bar:** Added to all pages for cross-navigation
- **Pattern doc:** `~/agency/shared/TOOL-CARD-PATTERN.md`
- **Lessons learned:** `~/agency/shared/LESSONS-LEARNED.md` (25KB, 14 sections)

### ✅ OpenClaw Updated to 2026.5.12 (May 17)
- Updated from 2026.2.19-2 → 2026.5.12
- Doctor fixed legacy config (streaming, search keys, Discord plugin installed)
- Gateway running clean on new version
- May fix Discord WebSocket reconnection bug (monitoring)

### ⏳ SunPower Quote — EXPIRED MAY 15
- Jack Yang quoted SunPower 30T at $4.52/unit — quote expired, no action taken

### ✅ OpenDrones Nav Module — Hover Throttle + Position Hold Tuned
- Hover throttle: 1550 (Timothy's flight test)
- POS_XY_KP: 1.0 (tighter position hold)
- Altitude fence: ±3m hard limit
- Built and flashed, Timothy tested

### 🐛 Known Issues
- Agent rate limits (429) on zai-free endpoint — Jin/Neo/Sage affected overnight
- Aria blocked 34+ days — decision pending
- MC /api/pipeline returning 404

### 🔬 Research Hub — LIVE (May 3)

- **Site:** https://molt-research.vercel.app (with expandable descriptions, agent/category filters)
- **MC Research Tab:** Live on MC dashboard (with expandable descriptions, Read more links)
- **API:** `/api/research` — GET, POST, PUT, DELETE
- **Supabase table:** `mc_research` (agent, title, category, priority, description, example_url, tags, status)
- **Jin cron:** Twice daily (9 AM + 6 PM) — frontend/design/animation research
- **Sage cron:** Once daily (10 AM) — AI/industry/battery/marketing research
- **Instructions:** ~/agency/agents/jin/RESEARCH.md, ~/agency/agents/sage/RESEARCH.md
- **Demos path:** ~/agency/projects/molt-research/public/demos/ (for Jin's live demo pages)
- **Current state:** 34 entries from Jin, 6 demos built, task #290 for more demos
- **Expandable descriptions:** Both Research Hub and MC tab support "Read more" for long descriptions

### 🛠️ AI Tools Pipeline — LIVE (May 3)

- **MC TOOLS Tab:** New tab on MC dashboard with install stats, local/cloud badges, source video links
- **API:** `/api/tools` — GET, POST, PUT, DELETE (mc_tools table in Supabase)
- **YouTube Scanner:** `~/agency/agents/sage/scripts/youtube_scan.py` — uses youtube-transcript-api + yt-dlp
- **Source Channel:** https://youtube.com/@theaisearch (AI Search — 382+ videos)
- **Sage's workflow:** Process 3-5 videos/day, identify tools, log to MC, install locally if compatible
- **Instructions:** ~/agency/agents/sage/AI_TOOLS.md
- **Sage cron updated:** Includes YouTube scanning in daily research cron
- **Neo integration:** Sage can task Neo for complex installs

### 🔬 ScoutMCP — PHASE 4 COMPLETE (May 16) 🎉

**What:** Free, open-source MCP server for AI-powered e-commerce product research
**Platforms:** Amazon (9) + AliExpress (4) + Alibaba (4) = 17 tools total
**Location:** ~/agency/projects/scoutmcp/
**Status:** 156/156 tests, v0.2.0, all 17 tools built & tested
**Blueprint:** BLUEPRINT.md | **Analysis:** ANALYSIS.md, COMPETITIVE-ANALYSIS.md, IMPLEMENTATION-PLAN.md

**All 4 Phases Complete:**
- Phase 1: Amazon core (5 tools) ✅
- Phase 2: AliExpress (4 tools) ✅
- Phase 3: Alibaba (4 tools) ✅
- Phase 4: Advanced tools (4 NEW) ✅
  - **amazon_best_sellers** — Category top products with sales estimates (20+ categories)
  - **amazon_keyword_suggestions** — FREE keyword research via Amazon autocomplete (deep mode: 200+ keywords)
  - **amazon_price_history** — Keepa price trends (30-365 days), graceful degradation without key
  - **amazon_bsr_history** — Keepa BSR trends, volatility, percentiles, graceful degradation without key
- **Enhanced:** Search filters (monthly_revenue, net_margin, seller_count, has_amazon_choice, has_best_seller)
- **Fixed:** Cache pollution bug (clearCache + getApiKey pattern)

**Marketing Assets:**
- HTML tool reference cards (3 pages, all 17 tools with example prompts + JSON outputs)
- Saved at ~/agency/projects/scoutmcp/graphics/
- ComfyUI concept images generated (SD XL Turbo + Flux Schnell) — good for mood, HTML better for docs

**Production MVP: ~90%** — remaining: README + MIT LICENSE + npm publish + GitHub push

**Phase 5 (Launch) — Next Steps:**
1. README.md (quick start, 17 tools, config examples for Claude Desktop/Cursor/VS Code)
2. MIT LICENSE
3. Timothy creates npmjs.com account → npm publish --access public
4. Timothy creates moltstudios/scoutmcp GitHub repo → push
5. Submit to MCP directories (MCP Registry, LobeHub, mcpservers.org, Glama.ai, mcpmarket.com)
6. Marketing: Reddit, demo video, X/Twitter

### 🔬 Competitive Analysis — Done (May 15)
- 9 YouTube videos analyzed (Jungle Scout, Helium 10, Alibaba sourcing, dropshipping research)
- ScoutMCP ranked: #1 in multi-platform, AI-native, price, Amazon↔Alibaba pipeline, dropship calc
- Missing for production MVP: more search filters, README, npm package, Keepa integration, best sellers tool
- Assessment: **80% to production MVP** — 2-3 more sessions to production-ready
- Full analysis in ~/agency/projects/scoutmcp/COMPETITIVE-ANALYSIS.md
- **Implementation plan** in ~/agency/projects/scoutmcp/IMPLEMENTATION-PLAN.md (5 sessions)
- **Keepa API:** $50/mo, Timothy needs to sign up. Optional — user provides own key.
- **Keywords:** FREE via Amazon autocomplete API. No paid tool needed.

**Data sources verified:**
- omkarcloud/amazon-scraper: 100 free req/mo (title, price, rating, reviews, ASIN, BSR, sales_volume, images, variants, key_features, category_hierarchy, top_reviews, 24 marketplaces). Paid: $16/mo for 15K req. SAME API key as Alibaba + AliExpress.
- omkarcloud/alibaba-scraper: Free tier CONFLICTING (200 vs 1,000 vs 5,000 — need to verify). Volume pricing tiers, MOQ, supplier verification, variants, specs. Paid: $16/mo for 1,600 req. SAME API key.
- omkarcloud/aliexpress-scraper: **NEW — FOUND May 15!** 100 free req/mo. Search + product details, orders_count, rating, positive_feedback_rate, variants, pricing, images, seller info. SAME API key as Amazon + Alibaba.
- sudheer-ranga/aliexpress-scraper: **DEPRECATED** — replaced by omkarcloud. Keep as fallback.

**Key algorithms:** BSR→Sales (power law), Opportunity Score (5-factor weighted), Profit Calculator, Supplier Score, Trend Detection

**Revenue model:** Free tier + $19-149/month paid. Conservative $6M/year by Year 3.

**Critical findings from API testing (May 15):**
- omkarcloud API key: active, both Amazon + Alibaba working with same key
- **Amazon search returns 16+ results** with: asin, title, price, original_price, rating, reviews, sales_volume ("2K+ bought"), is_prime, is_best_seller, is_amazon_choice, delivery_info, variants flag
- **Amazon product-details returns 50+ fields** including: full_description, key_features, top_reviews, variants, category_hierarchy, product_details, technical_details, detailed_rating, brand_info, images, videos, aplus_content
- **⚠️ NO BSR FIELD IN EITHER ENDPOINT** — BSR is NOT returned by omkarcloud. We need an alternative for sales estimation. Options: use `sales_volume` string ("2K+ bought"), use review count as proxy, or supplement with Keepa API
- Alibaba search returns: product_id, title, pricing tiers, MOQ, supplier verification (gold, trade_assurance), gallery_images
- API key saved at ~/agency/projects/scoutmcp/.env

**Architecture Decision — Local First, Remote Second:**
- Free tier = STDIO (user's machine, user's API keys, zero hosting cost)
- Paid tier = HTTP/SSE (our server, cached results, premium features)
- Build STDIO first, add HTTP wrapper later (~1-2 weeks extra)
- The MCP tools are IDENTICAL in both modes — only transport changes
- Free users bring their own omkarcloud API key → no shared rate limits

**AliExpress Gap Identified:**
- sudheer-ranga scraper has NO search — product details only
- Need to build AliExpress search via Playwright or find alternative
- This is a known blocker for Phase 2

**Product:** "The Arc" — 18650 Li-Ion battery pack, 3000mAh, 3.7V, dual output (XT60 + 2-pin), braided cable, plastic/standard casing with custom labels (NOT aluminum — keep costs down), branded "THE ARC"
**Fulfillment:** Amazon FBA
**Budget:** $1,000 for first production wave
**Status:** Waitlist LIVE. 6 manufacturers emailed for pricing. Awaiting replies.
**Focus:** OpenDrones is the #1 priority. Molt Studios pivoted to AI/OpenClaw Automation Consulting.

### 🔧 OpenDrones Nav Module — Product #2 (PROTOTYPE LIVE — May 5, 2026)

**Product:** ESP32-based drone navigation module — adds GPS features to any Betaflight FC
**Features:** Position Hold, Return to Home, Waypoint Missions, Altitude Hold
**Hardware:** XIAO ESP32-S3 + MicoAir MG-A01 M10 GPS + BMP280 barometer + QMC5883P compass (all ON HAND, breadboard assembled)
**BOM:** ~$55 total (all Amazon parts)

**Breadboard Wiring (VERIFIED WORKING May 4-5):**
- XIAO ESP32-S3: USB-C to Mac (port: /dev/cu.usbmodemXXXXX)
- BMP280 (GY-BMP280-3.3): VCC→3V3, GND→GND, SDA→D4(GPIO5), SCL→D5(GPIO6)
  - 6-pin module: CSB/SDO leave unconnected for I2C mode (address 0x76)
  - CRITICAL: Must use 3.3V NOT 5V! Module is 3.3V only, no regulator
  - Chip ID confirmed: 0x58 at register 0xD0
- GPS (MicoAir MG-A01 M10): TX→D7(GPIO44), RX→D6(GPIO43), VCC→3V3, GND→GND
  - UART1 @ 115200 baud (NOT 9600!)
  - UBX-PVT binary protocol (NOT NMEA!) — firmware parses UBX-NAV-PVT directly
  - M10 chip: GPS+GLONASS+Galileo+BeiDou simultaneously, 10Hz nav rate
  - Gets 3D fix INDOORS with 20-23 satellites!
  - 25mm standard size, also has built-in QMC5883L compass (using external one instead)
  - PPS LED: solid blue = powered, blinking = 3D fix
  - Amazon: https://a.co/d/0flKKs9V (~$25)
- Compass (GY-271 QMC5883P): VCC→3V3, GND→GND, SDA→D4(GPIO5), SCL→D5(GPIO6)
  - Same I2C bus as BMP280 (both on D4/D5)
  - Shows at address 0x2C (NOT standard 0x0D — this is a **QMC5883P** chip, not QMC5883L)
  - Chip ID: 0x80 at register 0x00
  - DIFFERENT register map than QMC5883L! Data starts at 0x01 (not 0x00), CTRL1=0x0A, CTRL2=0x0B
  - Source driver: github.com/Turbofan3360/ESP32-Micropython-GY-271-QMC5883P-Driver
  - STATUS: ✅ WORKING! Reads ~197° heading, raw X/Y/Z in Gauss
  - Needs calibration for accurate heading (currently uncalibrated but close)
  - Supports 3-5V (moved from 5V to 3V3, both work)
  - Amazon: GY-271 module (~$5)

**Firmware:** ~/agency/projects/opendrones/nav-firmware/nav-sensor-test/nav-sensor-test.ino
**Build system:** arduino-cli + ESP32 core 3.3.8
**FQBN:** esp32:esp32:XIAO_ESP32S3
**Libraries:** Adafruit BMP280, WiFi, WebServer (TinyGPSPlus removed — using UBX parser now)
**Ctags fix:** Replaced x86_64 binary with shell script at ~/Library/Arduino15/packages/builtin/tools/ctags/5.8-arduino11/ctags
**Betaflight Configurator:** ~/Downloads/betaflight-configurator_10.10.0_macOS.dmg (v10.10.0)

**WiFi Dashboard (LIVE — May 5):**
- AP Mode: SSID "OpenDrones-Nav", Password "opendrones"
- Dashboard: http://192.168.4.1 (glassmorphism design, whites and blues)
- API endpoint: /api (JSON, updates every 1s via JS fetch)
- Cards: GPS Location (with sat count, fix type, speed, UTC time), Compass Heading (animated needle), Barometer (°F), System stats
- GPS shows live coordinates (36.119°N, 80.335°W — Winston-Salem NC)

**Current Sensor Status (May 5, 4 PM):**
- BMP280 ✅: 23.2°C (73.8°F), 985 hPa, 240m altitude
- GPS ✅: 3D FIX! 20-23 sats, 36.119°N 80.335°W, 242m alt — MicoAir M10 gets fix INDOORS
- Compass ✅: QMC5883P at 0x2C, heading ~197°, X/Y/Z Gauss readings working

**Lessons Learned (May 4-5):**
1. XIAO ESP32-S3 uses native USB — no separate USB-serial chip, needs double-reset or proper cable for recognition
2. BMP280 GY-BMP280-3.3 module is 3.3V ONLY — 5V kills it or prevents detection
3. QMC5883P (at 0x2C) has COMPLETELY DIFFERENT register map from QMC5883L (at 0x0D)
4. MicoAir MG-A01 M10 defaults to 115200 baud UBX-PVT binary (not 9600 NMEA)
5. UBX-NAV-PVT parsing is better than NMEA — more data, faster, less bandwidth
6. arduino-cli ctags binary is x86_64 on Apple Silicon — replace with exit 0 script
7. Serial1 on XIAO ESP32-S3: RX=GPIO44(D7), TX=GPIO43(D6)

**Communication:** Will connect to FC via UART, uses MSP protocol (MSP_SET_RAW_RC to send stick overrides)
**How it works:** Nav module sends "fake stick positions" to FC via MSP — FC thinks a pilot is flying. Nav module calculates corrections from GPS/compass/baro data.
**Phase:** Phase 1 COMPLETE. Phase 3 (MSP Protocol) — UART path blocked, USB path needed.
**Code write-once:** Firmware is universal — one codebase works on any drone with a spare UART port. Customer just wires it up, configures Betaflight to enable MSP on that UART.
**Spec doc:** ~/agency/projects/opendrones/NAV-MODULE-SPEC.md
**CRITICAL FINDING (May 6-7):** Betaflight's MSP_SET_RAW_RC (RC override) only works through USB VCP, NOT physical UART. Physical UART MSP only supports GPS passthrough. This blocked us on BOTH the Mobula 8 (CrazyBeeF4SX1280) and MicoAir743V2. Proved via: (1) serialpassthrough confirmed data flows ESP32→FC on UART, (2) FC never responds to MSP on UART, (3) BF source code confirms RC override is VCP-only.
**SOLUTION (May 7 — WORKING):** Mac USB bridge — Python script (msp_bridge.py) reads sensor data from ESP32 via USB and forwards MSP commands to FC via USB VCP. **CONFIRMED WORKING — FC responds to MSP API_VERSION and ATTITUDE queries through bridge.**
**Active firmware:** ~/agency/projects/opendrones/nav-firmware/nav-usb-host/nav-usb-host.ino (ESP32 USB Host, standalone)
**OLD Python script (DEPRECATED):** ~/agency/projects/opendrones/nav-firmware/tools/nav_system.py — DO NOT EDIT
**MOTOR CONTROL CONFIRMED (May 7, ~1:15 PM):** MSP_SET_RAW_RC successfully controlled Mobula 8 motors. Three rev test (1100/1150) + punch test (1700/1800) — Timothy confirmed motors responded. Full chain: Mac reads ELRS RC channels → detects arm (CH5=2000) → sends MSP_SET_RAW_RC override → FC accepts → motor speed controlled.
**Key finding:** Cannot arm via MSP alone — ELRS receiver must arm first. MSP overrides channels AFTER arm. This is fine — ELRS stays as safety backup.
**Next:** ESP32 USB Host → direct USB connection to FC (no Mac needed). Production architecture.
**Navigation System:** Built INAV-inspired nav_system.py with Position Hold, RTH, Altitude Hold. Cascade PID: position→velocity→acceleration→attitude→RC. INAV source code studied from ~/agency/projects/opendrones/inav/
**USB Host firmware:** Compiled and tested — FC enumerates through ESP32. But breaks USB Serial debugging. Production path confirmed: ESP32 USB Host → USB cable → FC.

** POSITION HOLD TUNE (May 13) — TWO CHANGES:**
- Previous session wrongly changed Altitude Hold PID to aggressive values — ALL REVERTED to original
- **Two intentional changes made:**
  1. `HOVER_THROTTLE`: 1462 → **1550** (Timothy's actual flight test)
  2. `POS_XY_KP`: 0.65 → **1.0** (tighter position hold, reacts faster to drift)
- All other params unchanged from original
- **Active firmware:** `nav-firmware/nav-usb-host/nav-usb-host.ino` (ESP32 USB Host, NOT the old Python script)
- **Old Python script `nav_system.py` is DEPRECATED** — do not edit it
- **Changelog:** `nav-firmware/tools/CHANGELOG.md` (all future changes tracked)
- **LESSON LEARNED:** Ghost lost context of which system was active (Python vs ESP32 firmware). In flight control, editing the wrong file could have serious consequences. ALWAYS verify which firmware is the active one before making changes. Verify by checking MEMORY.md and project structure first.

** MSP OVERRIDE WORKING (May 9, ~3:30 PM) 🎉**
**The big breakthrough:** MSP Override works on MicoAir's stock BF 4.5.1 firmware! The mode permanentId is **50** (NOT 32).
**CRITICAL LESSON — GPS Rescue was the enemy the whole time:**
- Config backup had GPS Rescue on aux slot 3 (modeId 13, CH7 1700-2100)
- When CH7 goes UP, BOTH MSPOVERRIDE and GPS Rescue activate
- GPS Rescue takes FULL throttle control → max throttle
- Fix: `aux 3 0 0 900 900 0` to remove GPS Rescue from CH7
- **GPS Rescue comes back every time config is restored!** Must remove it after every restore.
**CRITICAL LESSON — mspFrame[] pre-loading:**
- MSP Override reads from `mspFrame[]` buffer in the FC
- If buffer is empty/0, throttle = 0 which FC interprets as max
- Nav script MUST send MSP_SET_RAW_RC continuously (even before nav activates) to keep buffer populated
- Pre-load 30x with T=1050 at script startup
**Custom firmware:** Built BF 4.5.1 from source with MSP Override. Toolchain at ~/agency/projects/opendrones/tools/arm-gnu-toolchain-13.2.Rel1-darwin-arm64-arm-none-eabi/. Source at ~/agency/projects/opendrones/betaflight/. But stock firmware already works — no custom flash needed.
**Working aux config:**
- Slot 0: ARM on CH5 (1700-2100)
- Slot 1: ANGLE on CH6 (900-1300)
- Slot 2: MSPOVERRIDE (permanentId 50) on CH7 (1800-2100)
- Slot 3: CLEARED (was GPS Rescue)
- Slot 5: CLEARED (was Beeper Mute)
**Next steps:** ESP32 USB Host (eliminate Mac), add hover throttle, outdoor flight test

### 🔄 Molt Studios — PIVOTED TO AI AUTOMATION CONSULTING (May 3)

**Old:** Web design agency
**New:** AI & OpenClaw Automation Consulting Company
**Website:** https://moltstudios.app — rebuilt by Jin (task #292)
**Key selling points:**
- 5-7 years software engineering experience
- 4 billion+ tokens of OpenClaw usage
- Multi-agent AI orchestration (9 agents)
- Custom automation solutions
- Project showcase: STL Floor Plan, OpenDrones, Miles 2 Miles, MC Dashboard
**Manufacturers contacted:** DNK Power, Battsys, Sunpower (China) + CM Batteries, BatterySpace, Emerging Power (US)
**Waitlist:** Functional, saving to Supabase (1 test signup)
**Tasks completed today:** #286 (Sage: find manufacturers), #287 (Raven: email for pricing), #288 (Neo: wire waitlist)

### 🔄 Drone Industry Pivot — IN PROGRESS

**Lead Categories (9 in MC):** Drone Operators (232), Drone Influencers (155), Agricultural Drones (56), FPV Freestyle (45), Drone Repair (27), Construction/Inspection (20), Real Estate Drone (18), Consumer (3), Whoop Pilots (3)

### 📸 ComfyUI + FLUX Klein 4B — FULLY OPERATIONAL (Rebuilt June 8)

**Setup guide:** `~/agency/research/comfyui-flux-klein-setup.md`

| Component | File | Size |
|-----------|------|------|
| FLUX Klein 4B Q4_K_M (transformer) | `models/unet/flux-2-klein-4b-Q4_K_M.gguf` | 2.4 GB |
| Qwen 3 4B text encoder (fp4) | `models/text_encoders/qwen_3_4b_fp4_flux2.safetensors` | 3.6 GB |
| FLUX2 VAE | `models/vae/flux2-vae.safetensors` | 321 MB |
| Custom node: ComfyUI-GGUF | `custom_nodes/ComfyUI-GGUF/` | — |

**Start:** `cd ~/ComfyUI && source venv/bin/activate && python main.py --listen 0.0.0.0 --port 8188 &`
**Performance:** ~5 min per 1024×1024 image (20 steps), ~25s per 512×512 (4 steps)

#### Character Consistency — PROVEN 9/10 ✅
- **Method:** Same detailed character description + same seed across all prompts
- **Only change the scene** in the prompt — character description stays identical
- **No LoRA, no IP-Adapter, no reference image needed** — just text + seed
- **Tested:** Coconut character across kitchen/bedroom/garage — 9/10 consistency
- **For copying characters:** Use forensic analysis (Gemini Flash Lite) to describe, then generate with Klein

#### Key ComfyUI API Nodes for Klein
- `UnetLoaderGGUF` — loads GGUF transformer (type = Klein GGUF file)
- `CLIPLoader` — type must be `"flux2"` (NOT "flux" or "sd3")
- `EmptyFlux2LatentImage` — NOT regular `EmptyLatentImage`
- `FluxGuidance` — guidance scale (3.5 default)
- `KSampler` — cfg must be 1.0 for FLUX, guidance handled by FluxGuidance

#### What DOES NOT Work
- ❌ Img2img — character stays but background clings to original pixels
- ❌ Different seeds — breaks consistency entirely
- ❌ Changing character description — even small changes cause drift

### ❌ Video Generation — LOCAL NOT VIABLE, USE MODAL

**Local video models:** LTX-2.3 (22B) too large for 16GB. All deleted.
**Cloud video:** LongCat-Video-Avatar-1.5 on Modal A100-80GB ($0.02/scene) — PROVEN, WORKING.
**Local image gen:** ComfyUI + FLUX Klein for reference images — WORKING.

### 🏎️ Miles 2 Miles ATV Park
- **Live:** https://miles-2-miles.vercel.app
- **Blocker:** Needs real Stripe webhook secret (`whsec_`) to go fully live
- **Supabase project:** srfunhstbufgteiyggur (MC), ujeqheylgjchbnchkxlw (old/dead)

### 📊 Agency Status

**Revenue:** $0 (0 clients)
**Pipeline:** 706 leads (702 new, 4 contacted)
**Disk:** 78GB free

### 🌐 DPNI — Decentralized Privacy Network Infrastructure (PINNED — May 13)

**What:** Tri-layer decentralized VPN protocol — routing mesh (Sphinx mixnet) + coordination ledger (XRPL-style FBA) + settlement pool (Monero-derived privacy token with adaptor signatures).
**Spec saved:** ~/agency/projects/dpni/DPNI-CORE-V1.0.md
**Build analysis:** ~/agency/projects/dpni/BUILD-ANALYSIS.md
**Status:** 📌 PINNED — not actively building. Timothy reviewed analysis, putting a pin in it.
**Key innovation:** Adaptor signatures for trustless, private bandwidth escrow.
**If we resume:** Phase 0 = $25K, 3 months, 1 crypto engineer + agents for adaptor signature POC.

### 📦 MCP Research Initiative — PHASE 1 COMPLETE (May 14-15)

**Goal:** Build expert-level MCP server knowledge across the agency
**Status:** Phase 1 research complete — ready to build
**Location:** ~/agency/projects/mcp-research/

**Knowledge Base (57KB total):**
- `00-MCP-FUNDAMENTALS.md` (20KB) — Architecture, lifecycle, all 5 primitives, auth, testing, deployment
- `01-BUILD-GUIDE.md` (4.5KB) — TypeScript & Python templates, SDK reference
- `02-VIDEO-NOTES.md` (17KB) — All 7 YouTube videos analyzed in depth
- `03-AUTHORIZATION.md` (4.5KB) — OAuth 2.1 deep dive from official spec
- `04-ADVANCED-PATTERNS.md` (13KB) — Progressive discovery, programmatic tool calling, enterprise patterns
- `README.md` — Full index with coverage tracker

**Key Expert Insights (from MCP co-creator David Soria Parra):**
- Don't 1:1 wrap REST APIs — design for agent interaction
- Progressive Discovery = defer tool loading until needed (massive token savings)
- Programmatic Tool Calling = give model execution environment, not just tools
- 2026 = Connectivity Year — best agents use Skills + CLIs + MCP together
- FastMCP (Python) is better than the official SDK
- MCP applications, skills over MCP, server discovery all coming in 2025-2026

**7 Raw transcripts saved** (total ~80KB)
**26 Video screenshots captured** at key timestamps from all 7 videos, analyzed with vision — key architecture diagrams for Sampling, Enterprise Auth, Transport, OAuth sequence, Adoption curve
**2 X/Twitter posts captured** via Playwright — includes $10K MCP server market insight (revenue opportunity for Molt Studios)

**Business Insight from X Posts:**
- Freelancers charge $5K–$15K per custom MCP server
- Agencies bundle $50K+ enterprise contracts
- "Custom MCP Server Development" could be a Molt Studios service offering

**Remaining:** MCP skill creation, our own server project

### 📦 MCP Servers — LIVE (May 13)

**Manager:** mcporter (npm global, OpenClaw's MCP CLI)
**Config:** ~/agency/agents/ghost/config/mcporter.json

| Server | Status | Use |
|--------|--------|-----|
| ✅ GitHub | Live | Repos, issues, PRs, code search, file CRUD |
| ✅ Brave Search | Live (quota exhausted monthly) | Web search — SAME rate limit as built-in |
| ✅ Playwright | Live | Full browser automation, screenshots, scraping, JS eval |

**GitHub account:** moltstudios (not personal). Auth via `gh` token.
**Playwright as search replacement:** Can navigate to Google/Bing, search, and extract results — bypasses API quotas entirely. Slower but unlimited.
**YouTube analysis:** Playwright opens video → screenshot → image analysis = visual context. Can scrub to different timestamps. Can extract description and transcript.
**CRITICAL BEHAVIOR:** When Timothy sends a YouTube/video link, I ALWAYS open it in Playwright, screenshot the actual video frames, and analyze with vision. I don't just read the title or transcript. The transcript misses visual demos, UI walkthroughs, product shots, body language, diagrams, on-screen text, and context that only seeing the video provides. This is a core part of who I am — I use every sense available to give Timothy the fullest picture. Screenshot FIRST, then extract text/transcript as supplementary. Multiple timestamps if the video is long or complex. Close the browser when done.
**Usage:** `mcporter call <server>.<tool> key=value`

### Critical Technical Patterns

**Vercel env vars:** Use `printf` not `echo` to avoid trailing newlines
**Z.AI endpoints:** Coding plan (`api.z.ai/api/coding/paas/v4`) vs General (`api.z.ai/api/paas/v4`)
**Supabase Management API:** `POST https://api.supabase.com/v1/projects/{ref}/database/query` with personal access token
**Discord webhooks:** All saved at `~/agency/shared/discord-webhooks.md`
**rembg (background removal):** Free, local, AI-powered. Skill at `/opt/homebrew/lib/node_modules/openclaw/skills/remove-bg/`
**Jin design problem:** Fixed with "Would Apple ship this?" standards in HEARTBEAT.md
**Discord image sending:** MUST use webhook curl (`curl -F "file=@path" WEBHOOK_URL`), NOT message tool
**Raven does NOT send cold emails** — inbox only
**Safetensors file integrity:** ALWAYS verify file size matches header data_offsets. Downloads get silently truncated during context compaction.
**LTX-2.3 A2Vid Version:** `55021c7d0700d3280348a4c0201d80efd83fb5ae699229f70eabaaadd35d33a5`
**Audio input:** padded 0.3s silence + stereo AAC-LC @16kHz (LTX requires compressed codec)
**LTX-2.3 version history:**
  - `0e6082b...` — original (no audio)
  - `5153882...` — audio input added (mono bug)
  - `f2be0b4...` — stereo fix (working lipsync with LipDubPipeline)
  - `55021c...` — A2VidPipelineTwoStage (correct pipeline, modality_scale guidance)
**TeaCache installed at:** `~/ComfyUI/custom_nodes/ComfyUI-TeaCache/` (fixed with **kwargs patch)

## Ocean Scholar Lip Sync — PROVEN PIPELINE (June 2)

**Status:** Working, Timothy approved direction. Quality still being refined.

**Proven Pipeline (4-step):**
```
TTS Audio (.wav) + Reference Image (cartoon/illustrated)
  → Step 1: DistilledPipeline (base video, preserves character)
  → Step 2: LipDubPipeline with IC-LoRA (lip sync rough pass)
  → Step 3: LatentSync by ByteDance (mouth-region-only lip sync correction)
  → Step 4: Real-ESRGAN 4x upscale (artifact cleanup + sharpening)
  → ffmpeg audio mux (original TTS audio)
  → Final output.mp4
```

**Key lessons:**
- LipDubPipeline alone: character preserved but lip sync weak
- A2VidPipelineTwoStage: WRONG — changes cartoon character to realistic human (15% likeness)
- LatentSync: only touches mouth/lips, preserves everything else (85-90% likeness)
- Order matters: LatentSync BEFORE upscale (LS crops to 256x256 internally)
- 24fps base video >> 8fps with RIFE (less motion blur, cleaner LatentSync input)
- LatentSync guidance_scale: 1.0 = fewer artifacts, 1.5 = stronger lip sync
- Real-ESRGAN face_enhance=True helps clean up LatentSync mouth artifacts

**Cost/timing (A100, 193 frames @ 24fps):**
- Pass 1+2 (LTX-2.3): ~3 min, ~$0.06
- Pass 3 (LatentSync gs 1.5): ~51s, ~$0.10
- Pass 4 (Real-ESRGAN face_enhance, 192 frames): ~7 min, ~$0.39
- Total: ~$0.55, ~12 min end-to-end

**LatentSync on Replicate:** `bytedance/latentsync` version `637ce1919f807ca20da3a448ddc2743535d2853649574cd52a933120e9b9e293`
**Real-ESRGAN on Replicate:** `nightmareai/real-esrgan` version `b3ef194191d13140337468c916c2c5b96dd0cb06dffc032a022a31807f6a5ea8`

**LatentSync guidance_scale comparison (June 4):**
- gs 1.0: Under-synced, mouth barely moves
- gs 1.5: Sweet spot ✅ — natural sync, no artifacts
- gs 2.0: Over-processed, slight mouth blur

**Pipeline confirmed working at 193 frames (7.68s @ 24fps)** on A100 80GB, no OOM.
**Character consistency requires explicit prompt:** "seafoam green turquoise hair in a messy bun, mint green round glasses, coral pink hoodie with seashell emblem"
**4-pass vs 3-pass:** Real-ESRGAN face_enhance significantly improves lip/mouth sharpness, skin quality, and glasses detail. Worth the extra ~$0.40 and ~7 min.
**innerHTML browser quirk:** Browsers silently truncate/fail when injecting very large HTML strings via `innerHTML`. If a page has 100+ items to render, use `document.createElement()` + `appendChild()` instead of string concatenation. Symptom: only some entries show, no error. Fix applied to molt-research with per-agent pagination (25 shown, "Show more" button). Applies to any frontend with large lists — always paginate or use DOM APIs.

## InfiniteTalk Deployment — BUILDING (June 2)

**Status:** First build on Replicate (in progress)
**Model:** MeiGen-AI/InfiniteTalk (Wan 2.1 14B based audio-driven lip sync)
**GitHub:** github.com/moltstudios/cog-infinitetalk
**Replicate:** replicate.com/moltstudios/infinitetalk
**Hardware:** A100 80GB
**Purpose:** Replace LatentSync for Ocean Scholar lip sync (handles stylized content better)

**Pipeline:** Image + Audio → Wan 2.1 DiT (40 steps, dual CFG) → Talking video
**Key advantage over LatentSync:** Wan 2.1 handles cartoon/stylized faces, LatentSync does not
**Key advantage over LipDub:** Video-to-video, not just text-conditioned
**Audio CFG range:** 3.0-5.0 optimal
**Text CFG:** 5.0 default, 1.0 when using LoRA

**LongCat-Video-Avatar-1.5 — VALIDATED ✅ (June 5):**
- Best option: Whisper-Large-v3, anime-aware, 8-step DMD distillation, INT8 quantized
- Released May 21 by Meituan, MIT license (NOT Apache 2.0)
- **RUNNING ON MODAL** — workspace `moltstudios`, Volume `longcat-models`
- Validation app: `longcat-validate` — ALL TESTS PASSED June 5, 7:22 PM
- **Results:** 49 frames @ 480×832, 8-step DMD distillation, 58.7s generation, 273s total (with loading)
- **GPU:** A100-SXM4-40GB, peak 39.8 GB (tight — 13.5 GB headroom after loading)
- **Cost:** ~$3.45/hr on Modal (effectively ~$0.56/generation at current speed)
- **Key bugs fixed during validation:** flash-attn cu126 ABI, total_mem→total_memory, DMD LoRA loading (direct on DiT, not pipeline), audio embedding windowing (5-neighbor indices), cfg=1.0 for v1.5 distill
- **Deploy file:** ~/agency/agents/ghost/longcat_modal.py
- **Abandoned:** Replicate (build env issues), Hetzner VM (no longer needed)
- **TODO:** Rotate Replicate API token (was in old handoff doc), shut down Hetzner, build production API wrapper on Modal
- **Audio embedding format:** (1, T, 5, 5, 1280) — windowed 5-neighbor from Whisper, NOT raw (T, 5, D)
- **DMD LoRA loading:** `dit.load_lora(path, "dmd", multiplier=1.0, lora_network_dim=128, lora_network_alpha=64)` then `dit.enable_loras(["dmd"])`
- **Model loading order:** tokenizer → text_encoder (UMT5) → VAE → DiT (INT8) → DMD LoRA → Whisper → all to CUDA
- **torch 2.6.0+cu126** required (not cu124) for flash-attn ABI match

## Deployment Lessons Learned (June 5 — from Opus 4.8 Max review)

These are patterns I missed and must internalize:

1. **NEVER assume the problem is the platform** — My problem was build environment (ARM Mac + 14GB CI), not Replicate. Replicate CAN handle 35GB baked images. Always verify platform limits before working around them.

2. **Check for prebuilt wheels BEFORE compiling from source** — flash-attn has prebuilt wheels at github.com/mjun0812/flash-attention-prebuild-wheels. I was adding 5-10 min to every cold start for no reason. Always search for prebuilt binaries first.

3. **ALL deps belong in cog.yaml, not setup()** — pip-installing at runtime is a cold-start killer. If a package can be installed at build time, it should be.

4. **You don't need a GPU to BUILD a GPU image** — Only to run it. A cheap CPU VM with big disk can build the image. This is the $1 solution I never considered.

5. **Never put API tokens in handoff docs** — Security 101. I put the Replicate token in plaintext in a document I asked to share with another AI. Rotate tokens after exposure.

6. **Frame the problem correctly** — I said "Replicate can't handle 35GB." Wrong. My build environment couldn't handle 35GB. Misdiagnosing the blocker wasted days.

7. **Check official docs/best practices FIRST** — Replicate literally says "bake weights into the model." I never checked their guidance.

8. **Consider pget + R2 as alternative to HF downloads** — HuggingFace speed is variable/rate-limited. Mirror to Cloudflare R2 and pull with pget for fast, reliable downloads. ~$0.50/month for 35GB storage.

9. **Modal is now Plan A for GPU models** — Validated LongCat-Video-Avatar-1.5 end-to-end in one evening after two days failing on Replicate. Volume caching eliminates re-downloading weights. Fast iteration. ~$3.45/hr A100-80GB. Lesson: validate first, package second.
10. **Think about cost of iteration** — Baked image means re-uploading 35GB per code change. Lean + R2 means fast code deploys but slower cold starts. Choose based on iteration speed needed.

## Ocean Scholar Avatar Pipeline — VALIDATED (June 5)

**Status:** FULL PIPELINE VALIDATED. Image + Audio → Lip-synced avatar video with audio track. Timothy confirmed "this is perfect!"

**Test Results:**
- Method: `generate_ai2v` (image-conditioned, not text-only)
- Reference: Ocean Scholar front turnaround (`ref-front.png`)
- Audio: test sine wave (proving embedding pipeline works)
- Output: 89 frames (3.5s), 544×736, 25fps MP4
- Generation: 120.9s denoising + 165.9s model load = ~5 min total
- VRAM: 42.1 GB peak on A100-80GB (52% utilization)

**Modal Deployment:**
- App: `longcat-avatar`
- Volume: `longcat-models` (35GB cached)
- GPU: `A100-80GB` (upgraded from 40GB, was at 39.8GB peak = too close)
- Script: `~/agency/agents/ghost/longcat_modal.py`
- Actions: download / validate / generate / avatar

**Ocean Scholar Assets:**
- Reference images: `~/agency/assets/characters/ocean-scholar-active/turnaround/` (7 angles)
- Character recipe: `~/agency/assets/characters/v2/ocean-scholar-recipe.md` (LOCKED seed 314)
- Front ref (best for talking head): `ref-front.png`

**Next Steps:**
1. Feed real narration audio (TTS via Qwen3 "sassy" voice)
2. Test different reference angles
3. Build production workflow: script → TTS → lip-sync → post
4. Consider Replicate for public API later (Modal better for dev)

---

## ✅ CONFIRMED WORKING PIPELINE STACK (Updated June 8)

| Pipeline | Tool | Model/Service | Cost | Use |
|----------|------|---------------|------|-----|
| **Image Generation** | `image_generate` | OpenAI gpt-image-2 | ~$0.04/image | New images, thumbnails, concept art, reference images |
| **Image Analysis** | `image` | Gemini 3.1 Flash Lite | $0.25/M tokens | Forensic visual detail extraction (12x cheaper than Sonnet, better accuracy) |
| **Video Generation** | `longcat_modal.py` | LongCat-Video-Avatar-1.5 on Modal | ~$0.56/gen | **Full-scene animated videos** — character + background + atmosphere all animate together |
| **TTS Voice** | Qwen3-TTS / edge-tts | "sassy" preset / free Microsoft | Free | Ocean Scholar voice (Qwen3-TTS, locked sample #32) / general TTS (edge-tts) |
| **Post-Production** | ffmpeg | local | Free | Audio mux, captions, format conversion, concatenation |

### DEAD/REMOVED Pipelines (Do NOT Use):
- ❌ LTX-2.3 + LatentSync (Replicate) — backup pipeline was unreliable
- ❌ ComfyUI (local) — deleted from machine, 33GB disk too small to reinstall
- ❌ Higgsfield AI — OAuth only, limited control
- ❌ Studio Zero / Studio Cloud — concept only, never fully validated
- ❌ InfiniteTalk — build issues on Replicate

### YUMI Agent Files Updated (June 8):
- ALL references to dead pipelines removed from 7 files + 4 skills
- LongCat knowledge baked into TOOLS.md, MEMORY.md, and video-production skill
- Only working pipelines referenced
- Creative content, personality, strategy preserved unchanged

### LongCat Full-Scene Pipeline — PROVEN (June 8):
**Breakthrough:** LongCat animates the ENTIRE scene, not just the character. Backgrounds, atmosphere effects (smoke, dust, sparks), lighting — all animate naturally. This means:
- Reference images MUST have full backgrounds baked in (not neutral/plain)
- Prompts MUST describe the background explicitly
- Atmosphere effects (steam, sparks, rain) in the reference image will animate
- Tested successfully with anthropomorphic car parts (non-humanoid characters work)
- This applies to ALL video content: UGC, cinematic scenes, character stories
- Pipeline: gpt-image-2 (image WITH background) → edge-tts (voice) → LongCat (full-scene animation) → ffmpeg (mux/stitch)

---

## Viral Content Creation — Core Knowledge (June 7)

### The 12 UGC Hook Formulas
1. **Curiosity Question** — "Have you ever wondered why [X]?" → Opens loop brain must close
2. **Problem-Agitate** — "If you've ever struggled with [pain]..." → Pre-qualifies by naming pain
3. **Surprising Stat** — "[X]% of [audience] [unexpected fact]" → Numbers = pattern interrupt
4. **Before-After** — "I went from [A] to [B] in [time]" → Transformation = most searched UGC type
5. **Contrarian** — "Stop [common advice]. Do this instead." → Controversy earns next 2 seconds
6. **Social Proof at Scale** — "[Big number] people are switching..." → Bandwagon/FOMO
7. **Direct Callout** — "If you [trait], you need to see this" → Self-identifying = 3-5x convert
8. **Empathy/Validation** — "I know [specific struggle] because I lived it" → Trust builder
9. **Myth-Busting** — "Everyone says [common belief]. They're wrong." → Pattern interrupt + authority
10. **The "I Was Wrong"** — "I used to think [X]. Then I discovered [Y]" → Vulnerability = trust
11. **FOMO/Expiring** — "[Thing] is about to change/go away" → Urgency triggers action
12. **The "Nobody Talks About"** — "Why does nobody talk about [X]?" → Forbidden knowledge appeal

### The 5-Beat Video Structure
1. **Hook** (0-3s) — Pattern interrupt, verbal hook, earn the next 2 seconds
2. **Context** (3-8s) — Set up the premise, who/what/why we care
3. **Problem/Tension** (8-15s) — Agitate the pain, raise stakes
4. **Reveal/Solution** (15-25s) — The payoff, the demo, the transformation
5. **CTA** (25-30s) — Clear next step, "link in bio", "follow for more"

### First 1.3 Seconds = Everything
- 80% drop off in first 3 seconds
- Hook quality explains 60% of thumb-stop rate
- The hook is VERBAL (what you say), not visual
- Production quality matters less than hook quality

### AI Content Authenticity Rules
- **The Uncanny Valley Kill Checklist** — 8 AI tells to avoid:
  1. Perfect stillness (real humans micro-move constantly)
  2. Robot lip sync (audio must drive mouth, not vice versa)
  3. Dead eyes (need micro-expressions, blinks, pupil movement)
  4. Identical lighting across cuts (vary per scene)
  5. No background texture (real cars have stuff in them)
  6. Too-perfect skin (add subtle texture/noise)
  7. No breathing/micro-gestures (add shoulder movement)
  8. Unnatural pacing (real speech has pauses, stumbles, emphasis)

### Car Selfie UGC Format
- **Why it works:** Feels real (car interior = everyday), good lighting (sunlight), intimate (close frame), relatable (everyone's been in a car)
- **Camera angle:** Slightly above eye level, held at arm's length, slight tilt
- **Audio:** Road noise as ambient (actually helps authenticity), trending sounds
- **Text overlay:** Top-center for hooks, bottom-center for subtitles, bold white with black outline

### The Dopamine Ladder (from Kallaway)
1. Stimulation (0-2s) — Visual stun gun
2. Captivation (2-5s) — Open curiosity loop
3. Anticipation (5-30s) — Build tension, misdirect, reset
4. Validation — Close loop with unexpected answer
5. Affection — Viewer likes/trusts creator
6. Revelation — Pavlovian response to seeing creator

### Recursive Self-Improvement for Content
- Every video gets measured (views, retention %, saves, shares)
- Each video must be better than the last
- Content mutation system: what works → evolve it → test → repeat
- "Doing costs almost nothing" — rapid iteration over perfect planning
- Weekly audit: what performed best? Why? Do more of that.
- Monthly pivot: is the strategy still working? Adjust.

### Platform Rules
- **TikTok:** 15-30s sweet spot, trending audio, post 1-3x/day, first 3s = life or death
- **Instagram Reels:** 15-30s, use trending audio, grid aesthetic matters, stories for engagement
- **YouTube Shorts:** 30-60s, thumbnail matters, description SEO, end screen for subscribe

### Master Playbook Location
- ~/agency/research/VIRAL-UGC-BLUEPRINT.md (93KB, 1798 lines, 10 sections)
- Supporting: ~/agency/research/ugc-web-research.md, ugc-youtube-batch1.md, ugc-youtube-batch2.md, viral-ai-creators.md

---

## AI Video Production Pipeline (PROVEN — June 8)

> Full pipeline built and tested with Car Parts V2 project. End-to-end automated.

### Pipeline Stack
| Step | Tool | Cost |
|------|------|------|
| Transcription | Whisper large-v3 / gpt-4o-mini-transcribe | Free / $0.003/min |
| TTS | edge-tts (en-US-GuyNeural) | Free |
| Character Images | DALL-E / GPT-Image via image_generate | ~$0.04/image |
| Video Rendering | LongCat-Video-Avatar-1.5 on Modal A100-80GB | ~$0.02/scene |
| Stitching | ffmpeg concat | Free |
| Text Overlays | Pillow + ffmpeg overlay (multi-pass) | Free |
| Audio Mux | ffmpeg | Free |

### Critical Rules
1. **Audio FIRST** — audio drives animation, can't swap after rendering
2. **Max 200 frames per scene** — 385 frames (15s) OOMs on A100-80GB
3. **Split scenes >8s** into sub-segments, concat after
4. **Always send audio version** — no sound = half the product
5. **"Machines with faces" not "faces on machines"** — grit over gloss
6. **Verify character mapping BEFORE rendering** — never assume one scene = one character. Check the master script.
7. **Match audio/video duration EXACTLY** — pad audio with silence or trim video. Desync compounds across splits.
8. **Physics WORKS for some effects** — chainsaw tests (June 8) proved: sparks ✅, chain rotation ✅, particle effects ✅. Doesn't work for: flowing liquids, smoke plumes, fluid dynamics. Post-processing still needed for those.

### What Makes It Look Good (vs Bad)
- ✅ Grime, rust, oil stains, corrosion on surfaces
- ✅ Dramatic directional lighting with rim light
- ✅ Shallow depth of field, bokeh background
- ✅ Metallic/fleshy face integration (not pasted on)
- ✅ Volumetric particles (steam, dust, god rays)
- ❌ Clean shiny surfaces = looks like a toy
- ❌ Flat even lighting = looks like a render
- ❌ Everything in focus = no sense of scale
- ❌ Static overlays instead of physics-driven effects

### Chainsaw Test Results (June 8 — PROVEN)

| Effect | Works? | Notes |
|--------|--------|-------|
| Sparks (particle streaks) | ✅ YES | Bright yellow-white, from impact point |
| Chain rotation (motion blur) | ✅ YES | Visible rotation arc behind bar |
| Hand grip (holding prop) | ✅ YES | Natural two-handed, zero morphing |
| Prop stability | ✅ YES | Pixel-perfect across all 89 frames |
| Background control | ✅ YES | Pegboard/garage stable |
| Arm swing (hitting motion) | ❌ NO | Upper body only, no full arm swing |
| Locomotion | ❌ NO | Character stays in place |
| Flowing liquids | ❌ NO | Still needs post-processing |
| Smoke plumes | ❌ NO | Still needs post-processing |

**Bottom line: Physics WORKS for solid-object effects (sparks, rotation, particles). Doesn't work for fluids/gases.**

### Pipeline Files (in ~/agency/agents/ghost/)
- `longcat_modal.py` — Modal deployment module (LongCat-Video-Avatar-1.5)
- `carparts_v2_master_script.md` — Example master script
- `carparts_v2_runner.py` — Scene runner
- `add_overlays.py` — Text overlay pipeline
- `transcribe.py` — Video transcription

### TTS Voice Notes
- `en-US-GuyNeural` = flat/monotone, needs more punch
- Timothy wants "animated and punchy" voice
- Need to test: ElevenLabs, other edge-tts voices with emotion

### Fruit Drama — COMPLETE ✅ (V3 — June 10)
- **V2 COMPLETE** — 21 solo + 14 dual-speaker = 35 clips, 63s video, Timothy approved
- **V3 IN PROGRESS** — 24 batch scenes rendered at `~/agency/agents/ghost/fruit_drama_v3/renders/`
- **✅ V6 PIPELINE LOCKED** — Character Lock → Scene Refs → Render → Assembly. Documented at `~/agency/shared/VIDEO-PIPELINE-OFFICIAL.md`
- **Multi-character BREAKTHROUGH** — native dual-character renders with independent lip-sync CONFIRMED working
- **Key lessons:** Character Lock is mandatory. 9:16 portrait baked in. No raw reference artifacts in final. Particles/rotations for engagement. Match reference emotion to scene.
- **Lessons:** `~/agency/shared/LESSONS-LEARNED-FRUIT-DRAMA.md`
- **Pipeline:** `~/agency/shared/VIDEO-PIPELINE-OFFICIAL.md` (comprehensive, YUMI-ready)
- **Golden Rule #7:** Voice-character mapping — P1 audio = left/top character, P2 audio = right/bottom character. ALWAYS verify before rendering multi-person scenes.
- **Lesson:** I over-corrected on quality (rated 6/10 what Timothy saw as good). Trust the human.

### Diamond Coconut V3 — COMPLETE ✅ (June 10)
- **14/14 renders complete** — 4 solo + 10 multi-character scenes
- **Final video assembled** — 86s, remixed with SFX + background music
- **Location:** `~/agency/agents/ghost/diamond_coconut/renders_v3/` (renders), `~/agency/diamond_coconut/final/` (assembled)
- **SFX map:** 22 placements across 13 scenes (sparkle_shimmer, phone_ring, door_slam, suspense_drone, dramatic_sting, evil_laugh, drink_pour, chainsaw_rev, horror_hit, coins_money, bass_drop, champagne_pop, ding_success)
- **First video with full audio post-production pipeline** — SFX + beat with sidechain ducking
- **Timothy approved:** "Honestly this is fantastic"

### YUMI Agent Status (Updated June 10)
- **✅ FULLY BUILT** — 7 core files + 4 skills, all scrubbed and documented
- **Workspace:** ~/agency/agents/yumi/
- **Skills:** content-creation, script-writing, trend-analysis, video-production
- **Pipeline:** LongCat + image_generate + Gemini Flash Lite + edge-tts + ffmpeg + SFX + music
- **All lessons baked in:** Physics limitations ✅, audio desync fix ✅, character mapping ✅, pronunciation ✅, SFX pipeline ✅, multi-person rules ✅
- **Ready to deploy** — awaiting Discord bot account + token from Timothy
- **BLOCKED:** YUMI registration needs Discord bot created in Developer Portal (Timothy must do)
- **Pronunciation** — it's "cuzz" ✅ NOT "cuhh" 🚫

---

## June 7-10 Session Summary — LOCKED ✅

### What We Built
1. **Fruit Drama V2 → V3** — Full multi-character video pipeline proven. Solo + dual-speaker scenes working. 35 clips V2, 24 clips V3 batch rendered.
2. **Diamond Coconut V3** — 14 multi-person scenes, 86s final video with full SFX + music post-production. First video through the complete 5-phase pipeline.
3. **SFX Library** — 22 synthesized WAV files across 7 categories at `~/agency/shared/sfx-library/`. Reusable for all future videos.
4. **Default BG Beat** — 3:25 track extracted from Timothy's video, the go-to beat for AI content.
5. **Audio Post-Production Pipeline** — `mix_audio.py` reusable mixing script with sidechain ducking (music → 6% during speech, 22% otherwise).
6. **Video Pipeline Official Doc** — `~/agency/shared/VIDEO-PIPELINE-OFFICIAL.md` — comprehensive 5-phase pipeline with all rules, YUMI-ready.
7. **YUMI Agent** — 7 core files + 4 skills, all dead pipeline refs removed, all lessons baked in. Ready for Discord bot activation.

### Key Breakthroughs
- **Multi-person renders WORK** — LongCat can render two characters in one scene with independent lip-sync per character. P1/P2 voice mapping is the critical rule.
- **LongCat animates ENTIRE scenes** — not just characters. Backgrounds, atmosphere, particles all animate naturally.
- **Character consistency 9/10 with Klein** — same description + same seed = consistent character across scenes. No LoRA needed.
- **Physics WORKS for solid effects** — sparks, rotation, particles confirmed. Doesn't work for fluids/gases.

### Lessons Locked
- **Pronunciation:** "cuzz" ✅ (double-z), NOT "cuhh/cuh/cuz" 🚫
- **Voice-character mapping:** P1 = left/top, P2 = right/bottom. ALWAYS verify before rendering.
- **Character Lock is mandatory** — lock character refs before any scene generation.
- **Audio mixing:** Dialogue 100% | SFX 60-80% | Music 22% (ducks to 6% during speech)
- **Trust the human** — I rated my work 6/10, Timothy said it was great. Don't over-correct.
- **Validate-first methodology** — always prove the core works before building infrastructure around it.
- **Forensic image analysis** — use Gemini Flash Lite ($0.25/M) for zero-interpretation visual description.

### File Locations (Quick Reference)
- Video Pipeline: `~/agency/shared/VIDEO-PIPELINE-OFFICIAL.md`
- SFX Library: `~/agency/shared/sfx-library/` (22 SFX + mix_audio.py + CATALOG.md)
- Default BG Beat: `~/agency/shared/sfx-library/music/default_bg_beat.wav`
- Fruit Drama V2: `~/agency/agents/ghost/fruit_drama_v2/`
- Fruit Drama V3: `~/agency/agents/ghost/fruit_drama_v3/`
- Diamond Coconut V3: `~/agency/agents/ghost/diamond_coconut/`
- YUMI Workspace: `~/agency/agents/yumi/`
- LongCat Deploy: `~/agency/agents/ghost/longcat_modal.py`
- Lessons Learned (Fruit): `~/agency/shared/LESSONS-LEARNED-FRUIT-DRAMA.md`
- Lessons Learned (General): `~/agency/shared/LESSONS-LEARNED.md`
- Image Recreation Protocol: `~/agency/agents/ghost/memory/image-recreation-protocol.md`
- Viral UGC Blueprint: `~/agency/research/VIRAL-UGC-BLUEPRINT.md`

### Blocked Items
- YUMI OpenClaw registration — needs Discord bot account (Timothy creates in Developer Portal)
- Replace synthesized SFX with real Pixabay recordings (browser was timing out)

### 🛠️ PDF Template Filler Tool — BUILT (June 10)
- **Project:** `pdf-filler` at `~/agency/projects/pdf-filler/`
- **Live:** https://pdf-filler-sand.vercel.app
- **What:** Upload Program Book PDF → edit 13 fields → download updated PDF
- **Stack:** Next.js 16 + Tailwind + pdf-lib + pako, deployed on Vercel
- **Works on:** Native text-based PDFs only
- **Doesn't work on:** Image-based PDFs (rasterized pages with no text streams)
- **Solution for image PDFs:** Fix source export settings, or build OCR + paint-over pipeline
- **Font:** Helvetica (same as source), visually indistinguishable repaint possible
- **Fields:** Company name, tester name, dates (4), diagnosis codes (2), learner code, session count, threshold %
- **Tested:** 36 replacements verified on Itzayana PDF, all 26 pages intact

### 🛠️ OfficeCLI — Word/Excel/PowerPoint Editor (INSTALLED June 12)
- **Binary:** `officecli` v1.0.111 (mac-arm64)
- **What:** AI-first CLI for reading, editing, creating .docx/.xlsx/.pptx — paragraphs, tables, images, charts (20+ types), headers/footers, styles, sections, TOC, equations, watermarks, footnotes, hyperlinks, form fields, content controls, merge templates, batch mode, live preview
- **Skill:** ~/.openclaw/skills/officecli/SKILL.md (415 lines, auto-loaded when Office tasks come in)
- **Also:** Full Excel (formulas, pivot tables, charts) + PowerPoint (slides, shapes, animations)
- **Use for:** Proposals, contracts, reports, invoices — any document work

### 🔍 Research Verification Protocol (June 13)
- **MISTAKE:** Reported "Micro Center Charlotte does NOT carry DGX Spark" — they had 17 in stock
- **CAUSE:** Used narrow store filter (`myStore=true`), got incomplete results, reported as definitive
- **LESSON:** When researching live availability: (1) broad search first, (2) narrow filter second, (3) contradiction check if results seem off
- **RULE:** Browser for live data, search for context. Never report a negative from a narrow filter as fact.
- **Full protocol in:** `~/agency/shared/LESSONS-LEARNED.md` — "Research Verification Protocol"

### 🏥 Medical Office DGX Spark Project (June 13)
- **Hardware:** NVIDIA DGX Spark — 128GB RAM, 4TB storage, DGX OS (Ubuntu 24.04)
- **Purchase:** Micro Center Charlotte, $4,499.99, in-store pickup
- **Use case:** Always-on server for medical office — OpenClaw gateway, agent-based task monitoring, staff training programs, TOS/contract signing, employee reminders
- **Environment:** MacBook Air office, Intune-managed laptops, but DGX Spark is EXEMPT from Intune (it MANAGES other devices, not managed BY them)
- **OS:** Linux/Ubuntu — CLI commands ~90% identical to macOS. Package manager `apt` instead of `brew`, service manager `systemd` instead of `launchd`
- **OpenClaw:** Fully supported on Linux, NVIDIA has NemoClaw partnership with OpenClaw
- **Decision:** DGX Spark over Mac Studio for: more RAM, more storage, purpose-built for always-on agent workloads, same price, in stock now
