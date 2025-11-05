# Supply Chain Disruption Response System
Supply Chain Disruption Response System is a multi-agent platform that proactively monitors, assesses, and responds to global supply chain disruptions 
using AI agents powered by local LLMs (Ollama). The system combines real-time data monitoring, predictive analytics, 
and automated response coordination to minimize supply chain risks and costs.

## Project overview
```
External Data Sources
        ↓
    [Data Ingestion Layer]
    - Weather APIs
    - News feeds
    - Supplier APIs
    - Port/shipping data
        ↓
    [Data Lake (S3/MinIO)]
        ↓
    [Processing Layer]
    - ETL pipelines
    - Feature engineering
    - Data quality checks
        ↓
    [Database (PostgreSQL)]
        ↓
    [Agent Layer]
    - Risk Monitor ←→ Redis Pub/Sub
    - Impact Assessment ↕
    - Alternative Sourcing ↕
    - Communication ↕
    - Coordination (Orchestrator)
        ↓
    [API Layer (FastAPI)]
        ↓
    [Frontend (Streamlit)]
        ↓
    [End Users]
```

## Features
* Continuous monitoring of global supply chain events
* Multi-source data integration (weather, geopolitical, supplier, transportation)
* AI-powered analysis of disruption patterns
* Multi-agent collaboration for response planning
* Route optimization and rerouting
* Cost impact analytics and forecasting
* Agent activity monitoring
* Executive summary reports
* Experiment tracking and versioning
* Model deployment automation

## Agent Architecture
* Agent 1: Risk Monitoring Agent: Detect and classify supply chain disruptions
  - [x] Rule-based logic for risk score calculation (mathematical formula), severity classification (threshold-based), recommendations (if-then rules)
  - [ ] Add LLM to Risk Monitor agent
* Agent 2: Impact Assessment Agent: Analyze financial and operational impact of disruptions
* Agent 3: Alternative Sourcing Agent: Identify backup suppliers and alternative routes
* Agent 4: Communication Agent: Manage stakeholder communications and notifications
* Agent 5: Coordination Agent: Coordinate all agents and optimize overall response

## Technical Stack
* Backend: FastAPI, LangChain, Ollama, NumPy, Pandas, PostgreSQL, Redis 
* Frontend: Streamlit, Plotly, Folium, Geopy

## Deployment
* Docker, GitHub Actions (CI/CD)


