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

        name = equipment_name.strip().lower()

        result = self.inspections[
            self.inspections["Equipment"].str.lower() == name
        ]

        if result.empty:
            return {
                "found": False,
                "message": "Equipment record not found. "
                           "Check the equipment name."
            }

        record = result.iloc[0]

        equipment = record["Equipment"]
        inspection = record["Inspection"]
        status = record["Status"]

        if inspection == "Expired":

            risk_level = "HIGH"
            priority = "Urgent review"

            department = "Maintenance"

            recommendation = (
                "Recommend restricting equipment use pending "
                "an authorized inspection and clearance. "
                "Notify the maintenance department."
            )

            reason = "The recorded inspection has expired."

        elif inspection == "Missing Record":

            risk_level = "CRITICAL"
            priority = "Immediate documentation review"

            department = "Maintenance and Compliance"

            recommendation = (
                "Recommend withholding operational clearance "
                "until inspection history is verified and "
                "required documentation is obtained."
            )

            reason = (
                "The available dataset contains no inspection record. "
                "This does not establish the equipment's physical condition."
            )

        else:

            risk_level = "LOW"
            priority = "Routine monitoring"

            department = "Ground Operations"

            recommendation = (
                "No inspection issue is recorded in this demo dataset. "
                "Continue approved pre-use checks and routine monitoring."
            )

            reason = "The recorded inspection is complete."

        return {
            "found": True,
            "equipment": equipment,
            "inspection": inspection,
            "status": status,
            "risk_level": risk_level,
            "priority": priority,
            "responsible_department": department,
            "reason": reason,
            "recommendation": recommendation,
            "requires_human_approval": True,
            "decision_status": "Pending human review",
            "demo": True
        }

    def get_equipment_overview(self):

        total = len(self.inspections)

        review = len(
            self.inspections[
                self.inspections["Status"] == "Review Required"
            ]
        )

        ready = total - review

        return {
            "total_equipment": total,
            "ready_records": ready,
            "records_requiring_review": review,
            "demo": True
        }

    def generate_report(self, equipment_name):

        result = self.investigate_equipment(equipment_name)

        if not result["found"]:
            return result["message"]

        return f"""
AEROTRUST AI
AIRPORT EQUIPMENT INTELLIGENCE REPORT

Equipment: {result['equipment']}

Inspection: {result['inspection']}

Recorded status: {result['status']}

Risk level: {result['risk_level']}

Priority: {result['priority']}

Responsible department:
{result['responsible_department']}

Reason:
{result['reason']}

AI recommendation:
{result['recommendation']}

Decision status:
{result['decision_status']}

Human approval required: Yes

IMPORTANT:
This is a demonstration decision-support report.
It does not authorize equipment operation or restriction.
An authorized airport operator must verify findings
and make the final operational decision.
"""
