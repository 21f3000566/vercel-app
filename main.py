# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import numpy as np

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

# Load telemetry data once at startup
with open("q-vercel-latency.json") as f:
    telemetry_data = json.load(f)

@app.post("/api/metrics")
async def get_metrics(request: TelemetryRequest):
    response = {}
    for region in request.regions:
        # Filter data for this region
        records = [r for r in telemetry_data if r["region"] == region]
        if not records:
            # If no data for region, return zeros
            response[region] = {
                "avg_latency": 0,
                "p95_latency": 0,
                "avg_uptime": 0,
                "breaches": 0
            }
            continue

        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime"] for r in records]
        breaches = sum(1 for l in latencies if l > request.threshold_ms)

        response[region] = {
            "avg_latency": float(np.mean(latencies)),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": float(np.mean(uptimes)),
            "breaches": int(breaches)
        }

    return response
