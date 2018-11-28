import tkinter as tk
import DBFunctions as df


class VulnPopup():

    @staticmethod
    def new_popup():
        model = ""
        cpe_name = ""
        cpe_uri = ""
        description = ""
        versions_affected = ""
        cvss_score = ""
        attack_vector = ""
        attack_complexity = ""
        privileges_required = ""
        user_interaction = ""
        confidentiality_impact = ""
        integrity_impact = ""
        availability_impact = ""
        base_score = ""
        base_severity = ""
        exploitability_score = ""

        # Creating the Popup Window
        vuln_popup = tk.Toplevel(padx=10, pady=10)
        vuln_popup.wm_title("Add Vulnerability")

        # Adding the fields to the popup
        related_mod = tk.Entry(vuln_popup, textvariable=model)
        related_mod_label = tk.Label(vuln_popup, text="Model")
        related_mod_label.grid(column=0, row=0, padx=5, pady=5)
        related_mod.grid(column=1, row=0, padx=5, pady=5)

        cpe_name_entry = tk.Entry(vuln_popup, textvariable=cpe_name)
        cpe_name_label = tk.Label(vuln_popup, text="CPE Name")
        cpe_name_label.grid(column=0, row=1, padx=5, pady=5)
        cpe_name_entry.grid(column=1, row=1, padx=5, pady=5)

        cpe_uri_entry = tk.Entry(vuln_popup, textvariable=cpe_uri)
        cpe_uri_label = tk.Label(vuln_popup, text="CPE URI")
        cpe_uri_label.grid(column=0, row=2, padx=5, pady=5)
        cpe_uri_entry.grid(column=1, row=2, padx=5, pady=5)

        description_entry = tk.Entry(vuln_popup, textvariable=description)
        description_label = tk.Label(vuln_popup, text="Description")
        description_label.grid(column=0, row=3, padx=5, pady=5)
        description_entry.grid(column=1, row=3, padx=5, pady=5)

        versions_affected_entry = tk.Entry(vuln_popup, textvariable=versions_affected)
        versions_affected_label = tk.Label(vuln_popup, text="Versions Affected")
        versions_affected_label.grid(column=0, row=4, padx=5, pady=5)
        versions_affected_entry.grid(column=1, row=4, padx=5, pady=5)

        cvss_score_entry = tk.Entry(vuln_popup, textvariable=cvss_score)
        cvss_score_label = tk.Label(vuln_popup, text="CVSS Score")
        cvss_score_label.grid(column=0, row=5, padx=5, pady=5)
        cvss_score_entry.grid(column=1, row=5, padx=5, pady=5)

        attack_vector_entry = tk.Entry(vuln_popup, textvariable=attack_vector)
        attack_vector_label = tk.Label(vuln_popup, text="Attack Vector")
        attack_vector_label.grid(column=0, row=6, padx=5, pady=5)
        attack_vector_entry.grid(column=1, row=6, padx=5, pady=5)

        attack_complexity_entry = tk.Entry(vuln_popup, textvariable=attack_complexity)
        attack_complexity_label = tk.Label(vuln_popup, text="Attack Complexity")
        attack_complexity_label.grid(column=0, row=7, padx=5, pady=5)
        attack_complexity_entry.grid(column=1, row=7, padx=5, pady=5)


        privileges_required_entry = tk.Entry(vuln_popup, textvariable=privileges_required)
        privileges_required_label = tk.Label(vuln_popup, text="Privileges Required")
        privileges_required_label.grid(column=0, row=8, padx=5, pady=5)
        privileges_required_entry.grid(column=1, row=8, padx=5, pady=5)


        user_interaction_entry = tk.Entry(vuln_popup, textvariable=user_interaction)
        user_interaction_label = tk.Label(vuln_popup, text="User Interaction")
        user_interaction_label.grid(column=0, row=9, padx=5, pady=5)
        user_interaction_entry.grid(column=1, row=9, padx=5, pady=5)


        confidentiality_impact_entry = tk.Entry(vuln_popup, textvariable=confidentiality_impact)
        confidentiality_impact_label = tk.Label(vuln_popup, text="Confidentiality Impact")
        confidentiality_impact_label.grid(column=0, row=10, padx=5, pady=5)
        confidentiality_impact_entry.grid(column=1, row=10, padx=5, pady=5)

        integrity_impact_entry = tk.Entry(vuln_popup, textvariable=integrity_impact)
        integrity_impact_label = tk.Label(vuln_popup, text="Integrity Impact")
        integrity_impact_label.grid(column=0, row=11, padx=5, pady=5)
        integrity_impact_entry.grid(column=1, row=11, padx=5, pady=5)

        availability_impact_entry = tk.Entry(vuln_popup, textvariable=availability_impact)
        availability_impact_label = tk.Label(vuln_popup, text="Availability Impact")
        availability_impact_label.grid(column=0, row=12, padx=5, pady=5)
        availability_impact_entry.grid(column=1, row=12, padx=5, pady=5)

        base_score_entry = tk.Entry(vuln_popup, textvariable=base_score)
        base_score_label = tk.Label(vuln_popup, text="Base Score")
        base_score_label.grid(column=0, row=13, padx=5, pady=5)
        base_score_entry.grid(column=1, row=13, padx=5, pady=5)

        base_severity_entry = tk.Entry(vuln_popup, textvariable=base_severity)
        base_severity_label = tk.Label(vuln_popup, text="Base Severity")
        base_severity_label.grid(column=0, row=14, padx=5, pady=5)
        base_severity_entry.grid(column=1, row=14, padx=5, pady=5)

        exploitability_score_entry = tk.Entry(vuln_popup, textvariable=exploitability_score)
        exploitability_score_label = tk.Label(vuln_popup, text="Exploitability Score")
        exploitability_score_label.grid(column=0, row=15, padx=5, pady=5)
        exploitability_score_entry.grid(column=1, row=15, padx=5, pady=5)

        # Function to call the save vulnerability function
        def save_vuln():
            df.DBFunctions.save_vulnerability(model, cpe_name, cpe_uri, description, versions_affected, cvss_score,
                                              attack_vector, attack_complexity,
                                              privileges_required, user_interaction, confidentiality_impact,
                                              integrity_impact, availability_impact, base_score, base_severity,
                                              exploitability_score)

        # Adding the save button to the popup window
        save_button = tk.Button(vuln_popup, text="Save", command=save_vuln)
        save_button.grid(columnspan=2, row=16, padx=5, pady=5)