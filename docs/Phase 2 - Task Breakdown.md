🤖 FAZ 2 — AGENT SKELETONS

✅ FAZ 2 — TASK BREAKDOWN

🧩 Agent Infrastructure
	•	Agent base interface
	•	Agent registry integration
	•	Agent lifecycle hooks

🧠 Implement Agent Shells
	•	MarketScannerAgent
	•	DataEngineeringAgent
	•	ExecutionAgent
	•	PortfolioManagerAgent
	•	CRORiskAgent
	•	PerformanceKPIAgent
	•	ASPAAgent
	•	RRSAgent

🔌 Event Wiring
	•	Agents subscribe to EventBus
	•	Agents log on Tick / Event
	•	Agents emit heartbeat logs

🧪 Tests
	•	All agents register to registry
	•	All agents receive Tick
	•	Fake OrderRequest flows through ExecutionAgent
	•	PerformanceAgent receives ExecutionResult
	•	RRS heartbeat test
