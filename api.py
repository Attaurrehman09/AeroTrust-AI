from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from flight_predictor import predict_flight_risk
from agent import AeroTrustAgent

app = FastAPI(title="AeroTrust AI API")

# Allow the Lovable website to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FlightRiskRequest(BaseModel):
    delay_minutes: int
    weather: str
    congestion: str

@app.get("/")
def home():
    return {
        "message": "AeroTrust AI API is running",
        "status": "online"
    }

@app.post("/predict-risk")
def flight_risk(request: FlightRiskRequest):
    return predict_flight_risk(
        request.delay_minutes,
        request.weather,
        request.congestion
    )

@app.get("/inspections")
def get_inspections():
    agent = AeroTrustAgent()
    return agent.inspections.to_dict(orient="records")