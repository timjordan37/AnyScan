import tkinter as tk
from util import DBFunctions as df

from tkinter import ttk

"""
The following class creates a popup window that allows the user to add a specific type of vulnerability 
to the current list of vulnerabilities present in the database
"""


class VulnPopup:

    @staticmethod
    def new_popup():
        cve_name = tk.StringVar()
        description = tk.StringVar()
        cvss_score = tk.StringVar()
        attack_vector = tk.StringVar()
        attack_complexity = tk.StringVar()
        custom_score = tk.StringVar()
        custom_score_reason = tk.StringVar()
        privileges_required = tk.StringVar()
        user_interaction = tk.StringVar()
        confidentiality_impact = tk.StringVar()
        integrity_impact = tk.StringVar()
        availability_impact = tk.StringVar()
        base_score = tk.StringVar()
        base_severity = tk.StringVar()
        exploitability_score = tk.StringVar()

        # Creating the Popup Window

        root = tk.Toplevel(padx=1, pady=1)
        root.wm_title("Add Vulnerability")
        top_level_frame = ttk.Frame(root)
        top_level_frame.grid(row=0, column=0, sticky="nsew")
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        # Adding the fields to the popup
        cve_name_entry = ttk.Entry(top_level_frame, textvariable=cve_name)
        cve_name_label = ttk.Label(top_level_frame, text="CPE Name")
        cve_name_label.grid(column=0, row=0, padx=5, pady=5)
        cve_name_entry.grid(column=1, row=0, padx=5, pady=5)

        description_entry = ttk.Entry(top_level_frame, textvariable=description)
        description_label = ttk.Label(top_level_frame, text="Description")
        description_label.grid(column=0, row=1, padx=5, pady=5)
        description_entry.grid(column=1, row=1, padx=5, pady=5)

        cvss_score_entry = ttk.Entry(top_level_frame, textvariable=cvss_score)
        cvss_score_label = ttk.Label(top_level_frame, text="CVSS Score")
        cvss_score_label.grid(column=0, row=2, padx=5, pady=5)
        cvss_score_entry.grid(column=1, row=2, padx=5, pady=5)

        attack_vector_entry = ttk.Entry(top_level_frame, textvariable=attack_vector)
        attack_vector_label = ttk.Label(top_level_frame, text="Attack Vector")
        attack_vector_label.grid(column=0, row=3, padx=5, pady=5)
        attack_vector_entry.grid(column=1, row=3, padx=5, pady=5)

        attack_complexity_entry = ttk.Entry(top_level_frame, textvariable=attack_complexity)
        attack_complexity_label = ttk.Label(top_level_frame, text="Attack Complexity")
        attack_complexity_label.grid(column=0, row=4, padx=5, pady=5)
        attack_complexity_entry.grid(column=1, row=4, padx=5, pady=5)

        custom_score_entry = ttk.Entry(top_level_frame, textvariable=custom_score)
        custom_score_label = ttk.Label(top_level_frame, text="Custom Score")
        custom_score_label.grid(column=0, row=5, padx=5, pady=5)
        custom_score_entry.grid(column=1, row=5, padx=5, pady=5)

        custom_score_reason_entry = ttk.Entry(top_level_frame, textvariable=custom_score_reason)
        custom_score_reason_label = ttk.Label(top_level_frame, text="Custom Score")
        custom_score_reason_label.grid(column=0, row=6, padx=5, pady=5)
        custom_score_reason_entry.grid(column=1, row=6, padx=5, pady=5)

        privileges_required_entry = ttk.Entry(top_level_frame, textvariable=privileges_required)
        privileges_required_label = ttk.Label(top_level_frame, text="Privileges Required")
        privileges_required_label.grid(column=0, row=7, padx=5, pady=5)
        privileges_required_entry.grid(column=1, row=7, padx=5, pady=5)

        user_interaction_entry = ttk.Entry(top_level_frame, textvariable=user_interaction)
        user_interaction_label = ttk.Label(top_level_frame, text="User Interaction")
        user_interaction_label.grid(column=0, row=8, padx=5, pady=5)
        user_interaction_entry.grid(column=1, row=8, padx=5, pady=5)

        confidentiality_impact_entry = ttk.Entry(top_level_frame, textvariable=confidentiality_impact)
        confidentiality_impact_label = ttk.Label(top_level_frame, text="Confidentiality Impact")
        confidentiality_impact_label.grid(column=0, row=8, padx=5, pady=5)
        confidentiality_impact_entry.grid(column=1, row=8, padx=5, pady=5)

        integrity_impact_entry = ttk.Entry(top_level_frame, textvariable=integrity_impact)
        integrity_impact_label = ttk.Label(top_level_frame, text="Integrity Impact")
        integrity_impact_label.grid(column=0, row=10, padx=5, pady=5)
        integrity_impact_entry.grid(column=1, row=10, padx=5, pady=5)

        availability_impact_entry = ttk.Entry(top_level_frame, textvariable=availability_impact)
        availability_impact_label = ttk.Label(top_level_frame, text="Availability Impact")
        availability_impact_label.grid(column=0, row=11, padx=5, pady=5)
        availability_impact_entry.grid(column=1, row=11, padx=5, pady=5)

        base_score_entry = ttk.Entry(top_level_frame, textvariable=base_score)
        base_score_label = ttk.Label(top_level_frame, text="Base Score")
        base_score_label.grid(column=0, row=12, padx=5, pady=5)
        base_score_entry.grid(column=1, row=12, padx=5, pady=5)

        base_severity_entry = ttk.Entry(top_level_frame, textvariable=base_severity)
        base_severity_label = ttk.Label(top_level_frame, text="Base Severity")
        base_severity_label.grid(column=0, row=13, padx=5, pady=5)
        base_severity_entry.grid(column=1, row=13, padx=5, pady=5)

        exploitability_score_entry = ttk.Entry(top_level_frame, textvariable=exploitability_score)
        exploitability_score_label = ttk.Label(top_level_frame, text="Exploitability Score")
        exploitability_score_label.grid(column=0, row=14, padx=5, pady=5)
        exploitability_score_entry.grid(column=1, row=14, padx=5, pady=5)

        # Function to call the save vulnerability function
        def save_vuln():
            if df.DBFunctions.save_vulnerability(cve_name.get(), description.get(), cvss_score.get(),
                                                 attack_vector.get(), attack_complexity.get(), custom_score.get(),
                                                 custom_score_reason.get(),
                                                 privileges_required.get(), user_interaction.get(),
                                                 confidentiality_impact.get(),
                                                 integrity_impact.get(), availability_impact.get(), base_score.get(),
                                                 base_severity.get(),
                                                 exploitability_score.get()):
                tk.messagebox.showinfo("Success", "Vulnerability Added Successfully")

            else:
                tk.messagebox.showinfo("Failure", "Vulnerability Did Not Save Correctly")

            top_level_frame.destroy()

        # Adding the save button to the popup window
        save_button = ttk.Button(top_level_frame, text="Save", command=save_vuln)
        save_button.grid(columnspan=2, row=16, padx=5, pady=5)
