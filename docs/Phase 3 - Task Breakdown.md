🧪 FAZ 3 — FAKE DATA FLOW (END-TO-END SIM)

✅ FAZ 3 — TASK BREAKDOWN

🧪 Simulation Modules
	•	FakeMarket (candle generator)
	•	FakePriceFeed
	•	FakeStrategy

🔁 Event Flow Wiring
	•	FakeMarket → MarketScanner
	•	MarketScanner → RegimeEvent
	•	FakeStrategy → OrderRequest
	•	ExecutionAgent → FakeExecutor
	•	ExecutionResult → PerformanceAgent
	•	PortfolioManager updates state

🧯 Risk Simulation
	•	Fake RiskEvent generator
	•	CRO blocks execution path

🧪 Tests
	•	Fake market emits data
	•	Full trade lifecycle works
	•	CRO kill-switch stops flow
	•	System runs 60+ minutes without crash