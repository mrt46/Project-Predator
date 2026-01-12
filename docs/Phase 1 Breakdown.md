🧱 FAZ 1 — CORE PLATFORM SKELETON

✅ FAZ 1 — TASK BREAKDOWN

🏗️ Core Infrastructure
	•	Repo folder structure oluştur
	•	Dockerfile yaz
	•	docker-compose.yml yaz
	•	FastAPI bootstrap kur
	•	/health endpoint ekle
	•	Structured logging kur

🧠 Core Engine
	•	CoreEngine state machine (INIT/BOOTING/IDLE/RUNNING/HALTED)
	•	EventBus (publish/subscribe)
	•	Scheduler (tick generator)
	•	Registry (engines/strategies/agents)
	•	PolicyGuard (CRO gate stub)

⚙️ Platform Stubs
	•	Selector stub
	•	Scoring stub
	•	Capital pools stub

🧪 Execution
	•	ExecutionBase interface
	•	FakeExecutor (fake FILLED)

📊 Monitoring
	•	Health module
	•	Metrics stub

🧪 Tests
	•	Boot test
	•	Tick flow test
	•	PolicyGuard block test
	•	Fake execution test
	•	Health endpoint test