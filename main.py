from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import numpy as np

# Request model
class TelemetryRequest(BaseModel):
    regions: List[str]
    threshold_ms: int

app = FastAPI()

# Enable CORS for all POST requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Load telemetry data at startup
with open("q-vercel-latency.json") as f:
    telemetry_data = json.load(f)

@app.post("/api/metrics")
async def get_metrics(request: TelemetryRequest):
    response = {}

    for region in request.regions:
        region_data = [r for r in telemetry_data if r["region"] == region]

        if not region_data:
            response[region] = {
                "avg_latency": 0,
                "p95_latency": 0,
                "avg_uptime": 0,
                "breaches": 0
            }
            continue

        latencies = [r["latency_ms"] for r in region_data]
        uptimes = [r["uptime_pct"] for r in region_data]
        breaches = sum(1 for l in latencies if l > request.threshold_ms)

        response[region] = {
            "avg_latency": round(float(np.mean(latencies)), 3),
            "p95_latency": round(float(np.percentile(latencies, 95)), 3),
            "avg_uptime": round(float(np.mean(uptimes)), 3),
            "breaches": breaches
        }

    return response
