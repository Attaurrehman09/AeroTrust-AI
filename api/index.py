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


# Request models

class FlightRiskRequest(BaseModel):
    delay_minutes: int
    weather: str
    congestion: str


class EquipmentInvestigationRequest(BaseModel):
    equipment_name: str


class ChatRequest(BaseModel):
    message: str
    delay_minutes: int | None = None
    weather: str | None = None
    congestion: str | None = None


# Home

@app.get("/")
def home():
    return {
        "message": "AeroTrust AI API is running",
        "status": "online"
    }


# Equipment inspection records

@app.get("/inspections")
def get_inspections():
    agent = AeroTrustAgent()
    return agent.inspections.to_dict(orient="records")


# Equipment overview

@app.get("/equipment-overview")
def equipment_overview():
    agent = AeroTrustAgent()
    return agent.get_equipment_overview()


# Investigate a specific equipment item

@app.post("/investigate-equipment")
def investigate_equipment(request: EquipmentInvestigationRequest):
    agent = AeroTrustAgent()
    return agent.investigate_equipment(request.equipment_name)


# Generate equipment report

@app.get("/equipment-report/{equipment_name}")
def equipment_report(equipment_name: str):
    agent = AeroTrustAgent()
    return {
        "report": agent.generate_report(equipment_name)
    }


# Flight risk prediction

@app.post("/predict-risk")
def flight_risk(request: FlightRiskRequest):
    return predict_flight_risk(
        request.delay_minutes,
        request.weather,
        request.congestion
    )


# AeroTrust AI Assistant

@app.post("/chat")
def chat(request: ChatRequest):

    message = request.message.lower().strip()

    agent = AeroTrustAgent()

    # Equipment investigation

    equipment_aliases = {
        "gpu": "Ground Power Unit",
        "ground power unit": "Ground Power Unit",
        "baggage tug": "Baggage Tug",
        "aircraft tow tractor": "Aircraft Tow Tractor",
        "tow tractor": "Aircraft Tow Tractor",
        "acu": "Air Conditioning Unit",
        "air conditioning unit": "Air Conditioning Unit"
    }

    for alias, equipment_name in equipment_aliases.items():

        if alias in message:

            result = agent.investigate_equipment(equipment_name)

            return {
                "reply": (
                    f"I investigated {equipment_name}. "
                    f"Risk level: {result.get('risk_level', 'Unknown')}. "
                    f"Decision status: "
                    f"{result.get('decision_status', 'Not available')}."
                ),
                "equipment_analysis": result
            }

    # General equipment overview

    if any(word in message for word in [
        "inspection",
        "equipment",
        "maintenance",
        "baggage",
        "ground operations"
    ]):

        overview = agent.get_equipment_overview()

        records = agent.inspections.to_dict(orient="records")

        return {
            "reply": (
                f"I checked {overview['total_equipment']} equipment records. "
                f"{overview['records_requiring_review']} records require review."
            ),
            "equipment_overview": overview,
            "inspections": records
        }

    # Flight risk analysis

    if any(word in message for word in [
        "flight",
        "delay",
        "risk",
        "weather",
        "congestion"
    ]):

        if (
            request.delay_minutes is None
            or request.weather is None
            or request.congestion is None
        ):
            return {
                "reply": (
                    "Please provide delay_minutes, weather, "
                    "and congestion to calculate flight risk."
                )
            }

        result = predict_flight_risk(
            request.delay_minutes,
            request.weather,
            request.congestion
        )

        return {
            "reply": (
                f"Flight risk is {result['risk_level']} "
                f"with a score of {result['risk_score']}."
            ),
            "risk_analysis": result
        }

    return {
        "reply": (
            "I am AeroTrust AI. I can investigate ground equipment, "
            "review inspection records, generate reports, "
            "and analyze flight disruption risk."
        )
    }
