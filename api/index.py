from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from flight_predictor import predict_flight_risk
from agent import AeroTrustAgent

app = FastAPI(title="AeroTrust AI API")

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
    return {"message": "AeroTrust AI API is running", "status": "online"}

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


class ChatRequest(BaseModel):
    message: str
    delay_minutes: int | None = None
    weather: str | None = None
    congestion: str | None = None


@app.post("/chat")
def chat(request: ChatRequest):
    message = request.message.lower()

    if any(word in message for word in [
        "inspection", "equipment", "baggage",
        "tractor", "gpu", "air conditioning"
    ]):
        agent = AeroTrustAgent()
        records = agent.inspections.to_dict(orient="records")

        review = [
            item for item in records
            if item["Status"] == "Review Required"
        ]

        return {
            "reply": f"I checked {len(records)} equipment records. "
                     f"{len(review)} require review.",
            "inspections": records,
            "review_required": review
        }

    if any(word in message for word in [
        "flight", "delay", "risk", "weather", "congestion"
    ]):
        if (
            request.delay_minutes is None
            or request.weather is None
            or request.congestion is None
        ):
            return {
                "reply": "Please provide delay_minutes, weather, "
                         "and congestion to calculate flight risk."
            }

        result = predict_flight_risk(
            request.delay_minutes,
            request.weather,
            request.congestion
        )

        return {
            "reply": f"Flight risk is {result['risk_level']} "
                     f"with a score of {result['risk_score']}.",
            "risk_analysis": result
        }

    return {
        "reply": "I am AeroTrust AI. I can help with flight "
                 "risk predictions and equipment inspections."
    }
