import pandas as pd


class AeroTrustAgent:

    def __init__(self):
        self.inspections = pd.DataFrame({
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

    def investigate_equipment(self, equipment_name):

        # Find the requested equipment
        result = self.inspections[
            self.inspections["Equipment"].str.lower()
            == equipment_name.lower()
        ]

        if result.empty:
            return {
                "found": False,
                "message": "Equipment record not found."
            }

        record = result.iloc[0]

        inspection = record["Inspection"]
        status = record["Status"]

        # Analyze the inspection record
        if inspection == "Expired":

            recommendation = (
                "Hold the equipment from use until an "
                "authorized inspection and clearance are completed."
            )

            risk = "High priority review"

        elif inspection == "Missing Record":

            recommendation = (
                "Verify the inspection history and obtain "
                "the required documentation before clearance."
            )

            risk = "Documentation review required"

        else:

            recommendation = (
                "No inspection issue is recorded in this demo dataset. "
                "Continue normal checks under approved procedures."
            )

            risk = "No alert in available record"

        return {
            "found": True,
            "equipment": equipment_name,
            "inspection": inspection,
            "status": status,
            "risk": risk,
            "recommendation": recommendation
        }

    def generate_report(self, equipment_name):

        result = self.investigate_equipment(equipment_name)

        if not result["found"]:
            return result["message"]

        report = f"""
AEROTRUST AI
EQUIPMENT INVESTIGATION REPORT

Equipment: {result['equipment']}

Inspection: {result['inspection']}

Current status: {result['status']}

Review priority: {result['risk']}

AI recommendation:
{result['recommendation']}

Note:
This report is based on demonstration records.
An authorized aviation operator must verify findings
and approve operational decisions.
"""

        return report