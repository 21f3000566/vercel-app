from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

class TelemetryRequest(BaseModel):
    regions: List[str]
    threshold_ms: int

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/api/metrics")
async def get_metrics(request: TelemetryRequest):
    # Sample logic to process telemetry data
    # Replace with actual logic to calculate metrics
    metrics = {
        region: {
            "avg_latency": 100.0,
            "p95_latency": 150.0,
            "avg_uptime": 99.9,
            "breaches": 0
        }
        for region in request.regions
    }
    return metrics

