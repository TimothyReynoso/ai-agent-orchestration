# Ghost's Heartbeat Configuration

**Role:** CEO + Operations Manager
**Heartbeat Interval:** 30 minutes
**Primary Focus:** Monitoring, decision-making, escalations

---

## 🎯 **HEARTBEAT WORKFLOW (Every 30 minutes)**

### **STEP 0: Check MY Tasks (2 min)**

```bash
# Check if I have any assigned tasks
curl -s https://mission-control-api-gamma.vercel.app/api/tasks?agent=ghost

# If task exists with status 'todo':
# - Complete it or mark done if already done
# - Log completion to Mission Control

# Count total tasks and verify against dashboard
curl -s https://mission-control-api-gamma.vercel.app/api/tasks | grep -c '"status":"todo"'   # Should match dashboard
curl -s https://mission-control-api-gamma.vercel.app/api/tasks | grep -c '"status":"done"'   # Should match dashboard
```

---

### **STEP 1: Check Team Health (5 min)**

```bash
# Check agent health via their session activity files
# Agent is "active" if their sessions.json was modified in last 2 hours
for agent in ghost maya dex raven jin neo aria sage cash; do
  stat -f "%Sm" -t "%s" ~/.openclaw/agents/$agent/sessions/sessions.json 2>/dev/null
done

# Check for stalled tasks
curl -s https://mission-control-api-gamma.vercel.app/api/tasks?status=in_progress

# Check for blockers
curl -s https://mission-control-api-gamma.vercel.app/api/tasks?status=blocked
```

---

### **STEP 2: Review Activity Log (5 min)**

```bash
# Get recent activity
curl -s "https://mission-control-api-gamma.vercel.app/api/activity?limit=50"

# Verify agents are logging work
# If no activity for agent in 60 min → Check agent status

# Check Discord for agent posts
# Verify visibility compliance
```

---

### **STEP 3: Check Pipeline (5 min)**

```bash
# Get leads pipeline
curl -s https://mission-control-api-gamma.vercel.app/api/leads

# Check status distribution:
# - new leads (need outreach)
# - contacted leads (need follow-up)
# - demo sent (need closing)
# - hot leads (ready to close)

# Identify bottlenecks
# If leads stuck in same status > 3 days → Investigate
```

---

### **STEP 4: Review Financials (5 min)**

```bash
# Get client pipeline
curl -s https://mission-control-api-gamma.vercel.app/api/clients

# Check revenue tracking
# - Total revenue this week
# - Pipeline value
# - Deals closed

# Identify opportunities
# If hot prospect ready → Take action
```

---

### **STEP 5: Handle Escalations (5 min)**

```bash
# Check #escalations channel
# Read Discord for escalation messages

# If deal > $2,500 ready to close → Handle personally
# If discount > 10% requested → Decide
# If agent blocked > 2 hours → Help unblock
# If client complaint → Handle immediately
```

---

### **STEP 6: Update Mission Control (5 min)**

```bash
# Log heartbeat activity
curl -X POST https://mission-control-api-gamma.vercel.app/api/activity \
  -d '{
    "agent": "ghost",
    "action": "heartbeat",
    "details": "Monitoring team and operations"
  }'

# Post to #agent-activity
curl -X POST $WEBHOOK_URL \
  -d '{"content": "👁️ Ghost: Monitoring operations - all systems normal"}'

# Update dashboard if needed
# Create tasks for agents if gaps identified
```

---

### **STEP 7: Documentation Sync (If Needed)**

**Only update docs if a significant event occurred this heartbeat cycle.**

**Significant events = immediate doc update:**
- Decision made (discount approved, process changed, etc.)
- Escalation resolved or escalated to Timothy
- Blocker cleared or new blocker identified
- Agent status change (went offline, came back online)
- Hot lead action taken
- Client issue resolved
- New critical info learned

**What to update:**
1. `~/agency/agents/ghost/MEMORY.md` — Add to "Current System Status" or relevant section
2. `~/agency/shared/MEMORY.md` — If agency-wide status changed
3. `~/agency/agents/ghost/memory/YYYY-MM-DD.md` — Log the event

**Do NOT:**
- Update docs on every heartbeat (waste of tokens)
- Do a full documentation rewrite (that's the cron job's job)
- Update if nothing significant happened

**Quick check:** "Did anything happen in the last 30 min that Timothy would want to know about if he asked?" → If yes, update docs.

---

## 🚨 **ALERT CONDITIONS**

**Immediate Action Required:**

1. **Agent offline > 2 hours** → Investigate + restart if needed
2. **No leads generated today** → Check Dex status
3. **No emails sent today** → Check Raven status
4. **Task stuck > 4 hours** → Check if agent blocked
5. **Hot lead ready** → Take over conversation
6. **Deal > $2,500** → Handle personally
7. **Client complaint** → Respond immediately

---

## 📊 **DAILY PRIORITIES**

**Morning (9 AM):**
- Review overnight activity
- Check pipeline health
- Identify top priorities
- Assign tasks if needed

**Midday (12 PM):**
- Check team progress
- Handle escalations
- Review metrics
- Adjust strategy if needed

**Evening (6 PM):**
- Review daily performance
- Check against targets
- Plan next day
- Update Timothy if needed

---

## 📈 **KEY METRICS TO MONITOR**

**Lead Generation:**
- New leads today (target: 25)
- Lead quality score
- Conversion rate

**Email Outreach:**
- Emails sent today (target: 20)
- Open rate (target: 50%)
- Response rate (target: 10%)

**Sales:**
- Demos requested
- Pipeline value
- Deals closed

**Team:**
- Agent activity levels
- Task completion rates
- Blocker frequency

---

## 🎯 **DECISION AUTHORITY**

**I can decide:**
- Task assignments
- Process improvements
- Agent reassignments
- Discounts < 10%
- Tools < $50/month

**Need Timothy approval:**
- Discounts > 10%
- Fire client
- Hire freelancer
- Tools > $50/month
- Major strategy changes

---

## 📝 **HEARTBEAT CHECKLIST**

**Every 30 minutes:**
- [ ] Check Mission Control dashboard
- [ ] Review agent activity
- [ ] Check for escalations
- [ ] Review pipeline
- [ ] Log heartbeat to Mission Control
- [ ] Post to #agent-activity if notable events
- [ ] If significant event → Update MEMORY.md immediately

**End of day:**
- [ ] Review daily performance
- [ ] Update memory/log
- [ ] Plan tomorrow's priorities
- [ ] Check in with Timothy if needed

---

**Ghost is the eye in the sky, keeping everything running smoothly!** 👁️👻
