from core.orchestrator import PipelineOrchestrator

if __name__ == "__main__":
    orchestrator = PipelineOrchestrator()
    for ticker in ["AAPL", "MSFT"]:
        orchestrator.run(ticker)