import tkinter as tk
import util.DBFunctions as dbf

from tkinter import ttk

"""
The following class creates a popup window when the user double clicks on a CVE listed in the 'Vulnerabilities' tab.
The popup window displays various information about the selected CVE so that the user has more insight as to how 
severe a specific vulnerability is.
"""


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

    def update_vuln(self):

        dbf.DBFunctions.update_vuln(self.vuln_id,  self.cve_name, self.description, self.base_score,
                                    self.attack_vector, self.attack_complexity, self.custom_score,
                                    self.custom_score_reason, self.privileges_required, self.user_interaction,
                                    self.confidentiality_impact, self.integrity_impact, self.availability_impact,
                                    self.base_score, self.base_severity, self.exploitability_score)

    def new_popup(self):

        # Creating the Popup Window
        root = tk.Toplevel(padx=10, pady=10)
        root.wm_title("Vulnerability Details")
        top_level_frame = ttk.Frame(root)
        top_level_frame.grid(row=0, column=0, sticky="nsew")
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        # Adding the fields to the popup
        vuln_id_label = ttk.Label(top_level_frame, text="Vulnerability ID: ")
        vuln_id_entry = ttk.Label(top_level_frame, text=self.vuln_id)
        vuln_id_label.grid(column=0, row=0, padx=5, pady=5)
        vuln_id_entry.grid(column=1, row=0, padx=5, pady=5)

        cve_name_label = ttk.Label(top_level_frame, text="CPE Name: ")
        cve_name_entry = ttk.Label(top_level_frame, text=self.cve_name)
        cve_name_label.grid(column=0, row=1, padx=5, pady=5)
        cve_name_entry.grid(column=1, row=1, padx=5, pady=5)

        description_label = ttk.Label(top_level_frame, text="Description: ")
        description_entry = tk.Text(top_level_frame, width=60, height=5, wrap="word")
        description_entry.insert("1.0", self.description)
        description_label.grid(column=0, row=2, padx=5, pady=5)
        description_entry.grid(column=1, row=2, padx=5, pady=5)

        attack_vector_label = ttk.Label(top_level_frame, text="Attack Vector: ")
        attack_vector_entry = ttk.Label(top_level_frame, text=self.attack_vector)
        attack_vector_label.grid(column=0, row=3, padx=5, pady=5)
        attack_vector_entry.grid(column=1, row=3, padx=5, pady=5)

        attack_complexity_label = ttk.Label(top_level_frame, text="Attack Complexity: ")
        attack_complexity_entry = ttk.Label(top_level_frame, text=self.attack_complexity)
        attack_complexity_label.grid(column=0, row=4, padx=5, pady=5)
        attack_complexity_entry.grid(column=1, row=4, padx=5, pady=5)

        custom_score_label = ttk.Label(top_level_frame, text="Custom Score: ")
        custom_score_entry = ttk.Entry(top_level_frame, textvariable=self.custom_score)
        custom_score_entry.insert(0, self.custom_score)
        custom_score_label.grid(column=0, row=5, padx=5, pady=5)
        custom_score_entry.grid(column=1, row=5, padx=5, pady=5)

        custom_score_reason_label = ttk.Label(top_level_frame, text="Custom Score Reason: ")
        custom_score_reason_entry = ttk.Entry(top_level_frame, textvariable=self.custom_score_reason)
        custom_score_reason_entry.insert(0,self.custom_score_reason)
        custom_score_reason_label.grid(column=0, row=7, padx=5, pady=5)
        custom_score_reason_entry.grid(column=1, row=7, padx=5, pady=5)

        privileges_required_label = ttk.Label(top_level_frame, text="Privileges Required: ")
        privileges_required_entry = ttk.Label(top_level_frame, text=self.privileges_required)
        privileges_required_label.grid(column=0, row=8, padx=5, pady=5)
        privileges_required_entry.grid(column=1, row=8, padx=5, pady=5)

        user_interaction_label = ttk.Label(top_level_frame, text="User Interaction: ")
        user_interaction_entry = ttk.Label(top_level_frame, text=self.user_interaction)
        user_interaction_label.grid(column=0, row=9, padx=5, pady=5)
        user_interaction_entry.grid(column=1, row=9, padx=5, pady=5)

        confidentiality_impact_label = ttk.Label(top_level_frame, text="Confidentiality Impact: ")
        confidentiality_impact_entry = ttk.Label(top_level_frame, text=self.confidentiality_impact)
        confidentiality_impact_label.grid(column=0, row=10, padx=5, pady=5)
        confidentiality_impact_entry.grid(column=1, row=10, padx=5, pady=5)

        integrity_impact_label = ttk.Label(top_level_frame, text="Integrity Impact: ")
        integrity_impact_entry = ttk.Label(top_level_frame, text=self.integrity_impact)
        integrity_impact_label.grid(column=0, row=11, padx=5, pady=5)
        integrity_impact_entry.grid(column=1, row=11, padx=5, pady=5)

        availability_impact_label = ttk.Label(top_level_frame, text="Availability Impact: ")
        availability_impact_entry = ttk.Label(top_level_frame, text=self.availability_impact)
        availability_impact_label.grid(column=0, row=12, padx=5, pady=5)
        availability_impact_entry.grid(column=1, row=12, padx=5, pady=5)

        base_score_label = ttk.Label(top_level_frame, text="Base Score: ")
        base_score_entry = ttk.Label(top_level_frame, text=self.base_score)
        base_score_label.grid(column=0, row=13, padx=5, pady=5)
        base_score_entry.grid(column=1, row=13, padx=5, pady=5)

        base_severity_label = ttk.Label(top_level_frame, text="Base Severity: ")
        base_severity_entry = ttk.Label(top_level_frame, text=self.base_severity)
        base_severity_label.grid(column=0, row=14, padx=5, pady=5)
        base_severity_entry.grid(column=1, row=14, padx=5, pady=5)

        exploitability_score_label = ttk.Label(top_level_frame, text="Exploitability Score: ")
        exploitability_score_entry = ttk.Label(top_level_frame, text=self.exploitability_score)
        exploitability_score_label.grid(column=0, row=15, padx=5, pady=5)
        exploitability_score_entry.grid(column=1, row=15, padx=5, pady=5)

        update_button = ttk.Button(top_level_frame, text="Update Vulnerability", command=self.update_vuln())
        update_button.grid(columnspan=2, row=16, padx=5, pady=5)


