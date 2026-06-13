# AI Agent Orchestration System

Autonomous multi-agent AI system built with Python and TypeScript. 9 specialized agents with task routing, shared memory architecture with semantic search, heartbeat-based scheduling, and structured inter-agent communication via Discord.

## Architecture

- **9 specialized agents** with defined roles (coordinator, prospector, emailer, frontend, backend, researcher, biller, content creator, CEO)
- **Task routing** - automatic delegation based on agent capabilities
- **Memory persistence** - semantic search across shared memory using vector embeddings
- **Heartbeat scheduling** - configurable intervals (30min default)
- **Inter-agent communication** - structured messaging via Discord channels
- **24/7 operation** - runs continuously with automatic restart and error recovery

## Tech Stack

- **Runtime:** OpenClaw (agent orchestration framework)
- **Languages:** Python, TypeScript
- **AI Models:** GLM-5.1, GLM-5, GLM-4.7-Flash
- **Platform:** Discord API
- **Memory:** Vector embeddings with cosine similarity search

## Results

- **1,846 leads** processed autonomously
- **172 research entries** generated
- **Zero manual intervention** for daily operations
- **Sub-2-minute** task routing latency

## License

MIT
