from agent import AeroTrustAgent
from flight_predictor import predict_flight_risk
import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(
    page_title="AeroTrust AI",
    page_icon="✈️",
    layout="wide"
)

# Sidebar
st.sidebar.title("✈️ AeroTrust AI")
st.sidebar.write("Aviation Intelligence Platform")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Flight Intelligence", "Inspection Intelligence"]
)

# Dashboard
if page == "Dashboard":

    st.title("✈️ AeroTrust AI")
    st.subheader("Aviation Operations & Flight Disruption Intelligence")

    st.write(
        "An intelligent aviation operations assistant "
        "for monitoring flight disruptions and equipment readiness."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Flights Monitored", 24)
    col2.metric("Delayed Flights", 5)
    col3.metric("Inspection Alerts", 3)

    st.divider()

    st.subheader("Platform Capabilities")

    st.markdown("""
    - 🛫 Flight delay monitoring
    - 🔧 Ground equipment inspection checks
    - 🤖 AI-powered operational recommendations
    - 📊 Aviation operations reporting
    """)

# Flight intelligence
elif page == "Flight Intelligence":

    st.title("🛫 Flight Delay Intelligence")

    flights = pd.DataFrame({
        "Flight": ["EK201", "EK202", "FZ101", "EK501", "FZ205"],
        "Route": [
            "Dubai - New York",
            "Dubai - London",
            "Dubai - Karachi",
            "Dubai - Mumbai",
            "Dubai - Islamabad"
        ],
        "Scheduled": ["09:00", "10:30", "11:00", "12:15", "14:00"],
        "Delay (minutes)": [0, 45, 20, 70, 0],
        "Status": ["On Time", "Delayed", "Delayed", "Delayed", "On Time"]
    })

    st.dataframe(flights, use_container_width=True)

    selected_flight = st.selectbox(
        "Select a flight to investigate",
        flights["Flight"]
    )

    flight = flights[flights["Flight"] == selected_flight].iloc[0]

    st.subheader("Flight Investigation")

    st.write("Flight:", flight["Flight"])
    st.write("Route:", flight["Route"])
    st.write("Delay:", flight["Delay (minutes)"], "minutes")
    st.write("Status:", flight["Status"])

    if flight["Delay (minutes)"] > 0:
        st.warning("This flight requires operational review.")
    else:
        st.success("No delay recorded in this demo dataset.")

        st.divider()

    st.subheader("🤖 AeroTrust AI Flight Risk Prediction")

    st.write("Enter operational conditions to calculate demonstration risk.")

    weather = st.selectbox(
        "Weather Conditions",
        ["Clear", "Moderate", "Severe"]
    )

    congestion = st.selectbox(
        "Airport Congestion",
        ["Low", "Medium", "High"]
    )

    if st.button("Predict Flight Risk"):

        result = predict_flight_risk(
            int(flight["Delay (minutes)"]),
            weather,
            congestion
        )

        st.metric(
            "Flight Risk Score",
            str(result["risk_score"]) + "%"
        )

        st.write("Risk Level:", result["risk_level"])

        if result["risk_level"] == "High":
            st.error(result["recommendation"])

        elif result["risk_level"] == "Medium":
            st.warning(result["recommendation"])

        else:
            st.success(result["recommendation"])

        st.caption(
            "Demonstration rule-based calculator only. "
            "Not a validated aviation prediction model."
        )

# Inspection intelligence
elif page == "Inspection Intelligence":

    st.divider()

    st.subheader("🤖 AeroTrust AI Investigation Agent")

    agent = AeroTrustAgent()

    equipment = st.selectbox(
        "Select equipment to investigate",
        agent.inspections["Equipment"].tolist()
    )

    if st.button("Investigate with AeroTrust AI"):

        result = agent.investigate_equipment(equipment)

        if result["found"]:

            st.write("### Investigation Results")

            st.write("Equipment:", result["equipment"])
            st.write("Inspection:", result["inspection"])
            st.write("Status:", result["status"])
            st.write("Review priority:", result["risk"])

            st.info(result["recommendation"])

            report = agent.generate_report(equipment)

            st.download_button(
                "Download Investigation Report",
                report,
                file_name="AeroTrust_Investigation_Report.txt"
            )

        else:
            st.error(result["message"])

    st.title("🔧 Equipment Inspection Intelligence")

    inspections = pd.DataFrame({
        "Equipment": [
            "Ground Power Unit",
            "Baggage Tug",
            "Aircraft Tow Tractor",
            "Air Conditioning Unit"
        ],
        "Inspection": [
            "Complete",
            "Expired",
            "Missing Record",
            "Complete"
        ],
        "Status": [
            "Ready",
            "Review Required",
            "Review Required",
            "Ready"
        ]
    })

    st.dataframe(inspections, use_container_width=True)

    alerts = inspections[
        inspections["Status"] == "Review Required"
    ]

    st.subheader("Inspection Alerts")
    st.write("Records requiring review:", len(alerts))
    st.dataframe(alerts, use_container_width=True)

    st.info(
        "These are fictional demonstration records. "
        "An authorized human operator must review safety decisions."
    )

st.divider()
st.caption("AeroTrust AI | Prototype v0.1 | Demo data only")