"""
AI Agent Orchestrator — Core Coordination Layer
================================================
The orchestrator manages the 9-agent system: routing tasks,
monitoring health, handling escalations, and maintaining shared state.

Architecture:
  - Each agent runs as an independent session with its own memory
  - The orchestrator dispatches tasks via a simple message bus
  - Agents report status back through heartbeats
  - Escalations flow: Agent → Orchestrator → CEO → Founder

This file shows the core architecture. Production uses OpenClaw
for session management, Discord for communication, and Mission Control
for task tracking.
"""

import json
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class AgentRole(Enum):
    GHOST = "ghost"       # CEO — operations & strategy
    MAYA = "maya"         # Ops Coordinator — task routing
    DEX = "dex"           # Sales — lead generation
    RAVEN = "raven"       # Sales — email outreach
    JIN = "jin"           # Dev — frontend
    NEO = "neo"           # Dev — backend
    ARIA = "aria"         # Sales — Upwork/freelance
    SAGE = "sage"         # Research — lead gen & competitor analysis
    CASH = "cash"         # Finance — billing & invoicing


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"
    ESCALATED = "escalated"


class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Task:
    id: str
    title: str
    assigned_to: AgentRole
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    blocked_reason: Optional[str] = None
    parent_task_id: Optional[str] = None


@dataclass
class AgentState:
    role: AgentRole
    name: str
    active: bool = False
    current_task: Optional[str] = None
    last_heartbeat: float = field(default_factory=time.time)
    tasks_completed: int = 0
    tasks_failed: int = 0


# ============================================
# Task Routing Rules
# Maps task types to the appropriate agent
# ============================================
ROUTING_RULES = {
    "lead_generation": AgentRole.DEX,
    "email_outreach": AgentRole.RAVEN,
    "upwork_application": AgentRole.ARIA,
    "frontend_development": AgentRole.JIN,
    "backend_development": AgentRole.NEO,
    "research": AgentRole.SAGE,
    "billing": AgentRole.CASH,
    "task_routing": AgentRole.MAYA,
    "strategy": AgentRole.GHOST,
    "escalation": AgentRole.GHOST,
}


class Orchestrator:
    """
    Central orchestrator for the multi-agent system.

    Responsibilities:
    - Route tasks to the right agent
    - Monitor agent health via heartbeats
    - Manage escalations (Agent → Ghost → Timothy)
    - Track shared state and metrics
    """

    def __init__(self):
        self.agents: dict[AgentRole, AgentState] = {}
        self.tasks: dict[str, Task] = {}
        self.escalations: list[dict] = []

        # Initialize all agents
        for role in AgentRole:
            self.agents[role] = AgentState(
                role=role,
                name=role.value.capitalize(),
            )

    def route_task(self, task_type: str, title: str, priority: TaskPriority = TaskPriority.MEDIUM) -> Task:
        """Route a new task to the appropriate agent based on type."""
        agent = ROUTING_RULES.get(task_type, AgentRole.MAYA)
        task_id = f"task_{int(time.time() * 1000)}"

        task = Task(
            id=task_id,
            title=title,
            assigned_to=agent,
            priority=priority,
        )
        self.tasks[task_id] = task

        # Assign to agent
        self.agents[agent].current_task = task_id
        return task

    def check_agent_health(self, timeout_seconds: int = 7200) -> list[AgentRole]:
        """Check which agents have gone stale (no heartbeat in timeout period)."""
        stale = []
        now = time.time()
        for role, state in self.agents.items():
            if state.active and (now - state.last_heartbeat) > timeout_seconds:
                stale.append(role)
        return stale

    def escalate(self, task_id: str, reason: str, to_ceo: bool = True) -> dict:
        """Escalate a task. Default escalation path: Agent → Ghost → Timothy."""
        task = self.tasks.get(task_id)
        if not task:
            return {"error": "Task not found"}

        task.status = TaskStatus.ESCALATED

        escalation = {
            "task_id": task_id,
            "from_agent": task.assigned_to.value,
            "to_agent": "ghost" if to_ceo else "timothy",
            "reason": reason,
            "timestamp": time.time(),
        }
        self.escalations.append(escalation)
        return escalation

    def complete_task(self, task_id: str) -> bool:
        """Mark a task as complete and update agent stats."""
        task = self.tasks.get(task_id)
        if not task:
            return False

        task.status = TaskStatus.DONE
        task.updated_at = time.time()

        agent = self.agents[task.assigned_to]
        agent.current_task = None
        agent.tasks_completed += 1
        return True

    def get_metrics(self) -> dict:
        """Return system-wide metrics for dashboard/monitoring."""
        active_agents = sum(1 for s in self.agents.values() if s.active)
        tasks_by_status = {}
        for task in self.tasks.values():
            tasks_by_status[task.status.value] = tasks_by_status.get(task.status.value, 0) + 1

        return {
            "active_agents": active_agents,
            "total_agents": len(self.agents),
            "total_tasks": len(self.tasks),
            "tasks_by_status": tasks_by_status,
            "open_escalations": len([e for e in self.escalations]),
            "agents": {
                role.value: {
                    "active": state.active,
                    "tasks_completed": state.tasks_completed,
                    "current_task": state.current_task,
                }
                for role, state in self.agents.items()
            },
        }


if __name__ == "__main__":
    # Demo: create orchestrator and route some tasks
    orch = Orchestrator()

    # Route tasks
    t1 = orch.route_task("lead_generation", "Find dentists in LA without websites")
    t2 = orch.route_task("frontend_development", "Build landing page for client X")
    t3 = orch.route_task("billing", "Send invoice to client Y")

    print(f"Task 1 → {t1.assigned_to.value}")
    print(f"Task 2 → {t2.assigned_to.value}")
    print(f"Task 3 → {t3.assigned_to.value}")

    # Check metrics
    print(f"\nMetrics: {json.dumps(orch.get_metrics(), indent=2)}")
