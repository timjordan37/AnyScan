import tkinter as tk


class DetailsPopup:
    """Details pop up displays information about the selected CVE"""

    _cve_details = ''
    vuln_id = ''
    cve_name = ''
    description = ''
    attack_vector = ''

    attack_complexity = ''
    custom_score = ''
    custom_score_reason = ''
    privileges_required = ''
    user_interaction = ''
    confidentiality_impact = ''
    integrity_impact = ''
    availability_impact = ''
    base_score = ''
    base_severity = ''
    exploitability_score = ''

    def __init__(self, cve_details):
        self._cve_details = cve_details

        self.vuln_id = cve_details[0]
        self.cve_name = cve_details[1]
        self.description = cve_details[2]
        self.attack_vector = cve_details[3]
        self.attack_complexity = cve_details[4]
        self.custom_score = cve_details[5]
        self.custom_score_reason = cve_details[6]
        self.privileges_required = cve_details[7]
        self.user_interaction = cve_details[8]
        self.confidentiality_impact = cve_details[9]
        self.integrity_impact = cve_details[10]
        self.availability_impact = cve_details[11]
        self.base_score = cve_details[12]
        self.base_severity = cve_details[13]
        self.exploitability_score = cve_details[14]

    def new_popup(self):

        # Creating the Popup Window
        popup = tk.Toplevel(padx=10, pady=10)
        popup.wm_title("Vulnerability Details")

        # Adding the fields to the popup
        vuln_id_label = tk.Label(popup, text="Vulnerability ID: ")
        vuln_id_entry = tk.Label(popup, text=self.vuln_id)
        vuln_id_label.grid(column=0, row=0, padx=5, pady=5)
        vuln_id_entry.grid(column=1, row=0, padx=5, pady=5)

        cve_name_label = tk.Label(popup, text="CPE Name: ")
        cve_name_entry = tk.Label(popup, text=self.cve_name)
        cve_name_label.grid(column=0, row=1, padx=5, pady=5)
        cve_name_entry.grid(column=1, row=1, padx=5, pady=5)

        description_label = tk.Label(popup, text="Description: ")
        description_entry = tk.Text(popup, width=60, height=5, wrap="word")
        description_entry.insert("1.0", self.description)
        description_label.grid(column=0, row=2, padx=5, pady=5)
        description_entry.grid(column=1, row=2, padx=5, pady=5)

        attack_vector_label = tk.Label(popup, text="Attack Vector: ")
        attack_vector_entry = tk.Label(popup, text=self.attack_vector)
        attack_vector_label.grid(column=0, row=3, padx=5, pady=5)
        attack_vector_entry.grid(column=1, row=3, padx=5, pady=5)

        attack_complexity_label = tk.Label(popup, text="Attack Complexity: ")
        attack_complexity_entry = tk.Label(popup, text=self.attack_complexity)
        attack_complexity_label.grid(column=0, row=4, padx=5, pady=5)
        attack_complexity_entry.grid(column=1, row=4, padx=5, pady=5)

        custom_score_label = tk.Label(popup, text="Custom Score: ")
        custom_score_entry = tk.Label(popup, text=self.custom_score)
        custom_score_label.grid(column=0, row=5, padx=5, pady=5)
        custom_score_entry.grid(column=1, row=5, padx=5, pady=5)

        custom_score_reason_label = tk.Label(popup, text="Custom Score Reason: ")
        custom_score_reason_entry = tk.Label(popup, text=self.custom_score_reason)
        custom_score_reason_label.grid(column=0, row=7, padx=5, pady=5)
        custom_score_reason_entry.grid(column=1, row=7, padx=5, pady=5)

        privileges_required_label = tk.Label(popup, text="Privileges Required: ")
        privileges_required_entry = tk.Label(popup, text=self.privileges_required)
        privileges_required_label.grid(column=0, row=8, padx=5, pady=5)
        privileges_required_entry.grid(column=1, row=8, padx=5, pady=5)

        user_interaction_label = tk.Label(popup, text="User Interaction: ")
        user_interaction_entry = tk.Label(popup, text=self.user_interaction)
        user_interaction_label.grid(column=0, row=9, padx=5, pady=5)
        user_interaction_entry.grid(column=1, row=9, padx=5, pady=5)

        confidentiality_impact_label = tk.Label(popup, text="Confidentiality Impact: ")
        confidentiality_impact_entry = tk.Label(popup, text=self.confidentiality_impact)
        confidentiality_impact_label.grid(column=0, row=10, padx=5, pady=5)
        confidentiality_impact_entry.grid(column=1, row=10, padx=5, pady=5)

        integrity_impact_label = tk.Label(popup, text="Integrity Impact: ")
        integrity_impact_entry = tk.Label(popup, text=self.integrity_impact)
        integrity_impact_label.grid(column=0, row=11, padx=5, pady=5)
        integrity_impact_entry.grid(column=1, row=11, padx=5, pady=5)

        availability_impact_label = tk.Label(popup, text="Availability Impact: ")
        availability_impact_entry = tk.Label(popup, text=self.availability_impact)
        availability_impact_label.grid(column=0, row=12, padx=5, pady=5)
        availability_impact_entry.grid(column=1, row=12, padx=5, pady=5)

        base_score_label = tk.Label(popup, text="Base Score: ")
        base_score_entry = tk.Label(popup, text=self.base_score)
        base_score_label.grid(column=0, row=13, padx=5, pady=5)
        base_score_entry.grid(column=1, row=13, padx=5, pady=5)

        base_severity_label = tk.Label(popup, text="Base Severity: ")
        base_severity_entry = tk.Label(popup, text=self.base_severity)
        base_severity_label.grid(column=0, row=14, padx=5, pady=5)
        base_severity_entry.grid(column=1, row=14, padx=5, pady=5)

        exploitability_score_label = tk.Label(popup, text="Exploitability Score: ")
        exploitability_score_entry = tk.Label(popup, text=self.exploitability_score)
        exploitability_score_label.grid(column=0, row=15, padx=5, pady=5)
        exploitability_score_entry.grid(column=1, row=15, padx=5, pady=5)


