"""
Agent Base Class — Foundation for All Agents
=============================================
Each agent in the system extends this base class.

Core capabilities:
- Memory persistence (MEMORY.md + daily logs)
- Task execution lifecycle
- Heartbeat reporting
- Escalation handling
- Discord channel communication

In production, agents run as OpenClaw sessions with Discord channels
for communication. This base class shows the shared interface.
"""

import time
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Callable


class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    BLOCKED = "blocked"
    OFFLINE = "offline"


@dataclass
class MemoryEntry:
    """A single memory entry — persisted to MEMORY.md"""
    timestamp: float
    category: str  # "decision", "preference", "client_info", "mistake", "context"
    content: str
    tags: list[str] = field(default_factory=list)


class AgentBase:
    """
    Base class for all agents in the orchestration system.

    Subclasses implement:
    - execute_task(): The agent's core work logic
    - handle_escalation(): What to do when escalated to
    - heartbeat(): Periodic health check + monitoring
    """

    def __init__(
        self,
        name: str,
        role: str,
        discord_channel: str,
        memory_path: str,
    ):
        self.name = name
        self.role = role
        self.discord_channel = discord_channel
        self.memory_path = memory_path
        self.status = AgentStatus.IDLE
        self.memory: list[MemoryEntry] = []
        self.current_task: Optional[dict] = None
        self.last_heartbeat: float = time.time()

    # ============================================
    # Memory System
    # ============================================

    def remember(self, category: str, content: str, tags: list[str] = None):
        """Write to persistent memory. This is MANDATORY for important info."""
        entry = MemoryEntry(
            timestamp=time.time(),
            category=category,
            content=content,
            tags=tags or [],
        )
        self.memory.append(entry)
        # In production: append to MEMORY.md file
        return entry

    def search_memory(self, query: str) -> list[MemoryEntry]:
        """Search past memory for relevant entries."""
        # In production: use semantic search via memory_search tool
        query_lower = query.lower()
        return [
            entry for entry in self.memory
            if query_lower in entry.content.lower()
            or any(query_lower in tag.lower() for tag in entry.tags)
        ]

    # ============================================
    # Task Lifecycle
    # ============================================

    def receive_task(self, task: dict):
        """Receive a task from the orchestrator."""
        self.current_task = task
        self.status = AgentStatus.WORKING
        self.remember("context", f"Received task: {task.get('title', 'unknown')}")

    def execute_task(self, task: dict) -> dict:
        """
        Execute the core work for this agent's role.
        Override in subclasses.
        """
        raise NotImplementedError("Subclasses must implement execute_task()")

    def complete_task(self, result: dict):
        """Mark current task as complete."""
        if self.current_task:
            self.remember("context", f"Completed task: {self.current_task.get('title')}")
            self.current_task = None
            self.status = AgentStatus.IDLE
        return result

    def report_blocker(self, reason: str):
        """Report that the agent is blocked on its current task."""
        self.status = AgentStatus.BLOCKED
        self.remember("context", f"BLOCKED: {reason}")
        # In production: post to #agent-activity with BLOCKED: prefix

    # ============================================
    # Escalation
    # ============================================

    def escalate(self, reason: str, to: str = "ghost"):
        """Escalate an issue to a higher authority."""
        self.remember("context", f"Escalated to {to}: {reason}")
        # In production: post to #escalations channel
        return {
            "from": self.name,
            "to": to,
            "reason": reason,
            "task": self.current_task,
        }

    # ============================================
    # Heartbeat
    # ============================================

    def heartbeat(self) -> dict:
        """
        Periodic health check. Called every N minutes.
        Override for agent-specific monitoring logic.
        """
        self.last_heartbeat = time.time()
        return {
            "agent": self.name,
            "status": self.status.value,
            "current_task": self.current_task,
            "uptime": time.time() - self.last_heartbeat if self.status == AgentStatus.IDLE else 0,
        }

    # ============================================
    # Communication
    # ============================================

    def post_to_channel(self, channel: str, message: str):
        """Post a message to a Discord channel."""
        # In production: use Discord webhook or bot API
        pass

    def post_activity(self, message: str):
        """Post an update to #agent-activity."""
        self.post_to_channel("#agent-activity", f"[{self.name}] {message}")

    # ============================================
    # Daily Logging
    # ============================================

    def write_daily_log(self, date: str, content: str):
        """Write to daily log file (memory/YYYY-MM-DD.md)."""
        # In production: write to agent's memory directory
        pass


# ============================================
# Example: Creating a specialized agent
# ============================================

class SalesAgent(AgentBase):
    """Example: A sales-focused agent (like Dex or Raven)."""

    def execute_task(self, task: dict) -> dict:
        task_type = task.get("type")

        if task_type == "lead_generation":
            return self._find_leads(task)
        elif task_type == "email_outreach":
            return self._send_emails(task)
        else:
            return self.escalate(f"Unknown task type: {task_type}")

    def _find_leads(self, task: dict) -> dict:
        # In production: scrape directories, search Google, etc.
        self.post_activity(f"Searching for leads: {task.get('query', '')}")
        return {"status": "complete", "leads_found": 0}

    def _send_emails(self, task: dict) -> dict:
        # In production: send via Gmail/Outlook API
        self.post_activity(f"Sending {len(task.get('recipients', []))} emails")
        return {"status": "complete", "emails_sent": 0}
