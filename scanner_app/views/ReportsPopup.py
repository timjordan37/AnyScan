import tkinter as tk

class ReportsPopup():

    _report_generator = ''

    host_id = ''
    host_ip = ''
    host_macaddress = ''
    host_osfamily = ''
    host_osgen = ''
    host_name = ''
    host_vendor = ''
    scan_id = ''

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

    def __init__(self, report_generator):
        # todo throw error if report_generator is empty
        self._report_generator = report_generator
        print('From ReportsPopup: ')
        # Devices
        print(self._report_generator[0])
        print('\n\n')
        # Vulnerabilities
        print(self._report_generator[1])
        print('\n\n')
        # Vuln 1
        print(self._report_generator[1][0])
        # Vuln 2
        print(self._report_generator[1][1])
        # Vuln 3
        print(self._report_generator[1][2])
        # Vuln 4
        print(self._report_generator[1][3])


        self.host_id = report_generator[0]
        self.host_ip = report_generator[1]
        self.host_macaddress = report_generator[2]
        self.host_osfamily = report_generator[3]
        self.host_osgen = report_generator[4]
        self.host_name = report_generator[5]
        self.host_vendor = report_generator[6]
        self.scan_id = report_generator[7]

        self.vuln_id = report_generator[8]
        self.cve_name = report_generator[9]
        self.description = report_generator[10]
        self.attack_vector = report_generator[11]
        self.attack_complexity = report_generator[12]
        self.custom_score = report_generator[13]
        self.custom_score_reason = report_generator[14]
        self.privileges_required = report_generator[15]
        self.user_interaction = report_generator[16]
        self.confidentiality_impact = report_generator[17]
        self.integrity_impact = report_generator[18]
        self.availability_impact = report_generator[19]
        self.base_score = report_generator[20]
        self.base_severity = report_generator[21]
        self.exploitability_score = report_generator[22]

    def new_popup(self):

        popup = tk.Toplevel(padx=10, pady=10)
        popup.wm_title("Scan Report")

        host_id_label = tk.Label(popup, text="Host ID: ")
        host_id_entry = tk.Label(popup, text=self.host_id)
        host_id_label.grid(column=0, row=0, padx=5, pady=5)
        host_id_entry.grid(column=1, row=0, padx=5, pady=5)

        host_ip_label = tk.Label(popup, text="Host IP: ")
        host_ip_entry = tk.Label(popup, text=self.host_ip)
        host_ip_label.grid(column=0, row=1, padx=5, pady=5)
        host_ip_entry.grid(column=1, row=1, padx=5, pady=5)

        host_macaddress_label = tk.Label(popup, text="Host MacAddress: ")
        host_macaddress_entry = tk.Label(popup, text=self.host_macaddress)
        host_macaddress_label.grid(column=0, row=2, padx=5, pady=5)
        host_macaddress_entry.grid(column=1, row=2, padx=5, pady=5)

        host_osfamily_label = tk.Label(popup, text="Host OS Family: ")
        host_osfamily_entry = tk.Label(popup, text=self.host_osfamily)
        host_osfamily_label.grid(column=0, row=3, padx=5, pady=5)
        host_osfamily_entry.grid(column=1, row=3, padx=5, pady=5)

        host_osgen_label = tk.Label(popup, text="Host OS Gen: ")
        host_osgen_entry = tk.Label(popup, text=self.host_osgen)
        host_osgen_label.grid(column=0, row=4, padx=5, pady=5)
        host_osgen_entry.grid(column=1, row=4, padx=5, pady=5)

        host_name_label = tk.Label(popup, text="Host Name: ")
        host_name_entry = tk.Label(popup, text=self.host_name)
        host_name_label.grid(column=0, row=5, padx=5, pady=5)
        host_name_entry.grid(column=1, row=5, padx=5, pady=5)

        host_vendor_label = tk.Label(popup, text="Host Vendor: ")
        host_vendor_entry = tk.Label(popup, text=self.host_vendor)
        host_vendor_label.grid(column=0, row=6, padx=5, pady=5)
        host_vendor_entry.grid(column=1, row=6, padx=5, pady=5)

        scan_id_label = tk.Label(popup, text="Scan ID: ")
        scan_id_entry = tk.Label(popup, text=self.scan_id)
        scan_id_label.grid(column=0, row=7, padx=5, pady=5)
        scan_id_entry.grid(column=1, row=7, padx=5, pady=5)

        vuln_id_label = tk.Label(popup, text="Vulnerability ID: ")
        vuln_id_entry = tk.Label(popup, text=self.vuln_id)
        vuln_id_label.grid(column=0, row=8, padx=5, pady=5)
        vuln_id_entry.grid(column=1, row=8, padx=5, pady=5)

        cve_name_label = tk.Label(popup, text="CPE Name: ")
        cve_name_entry = tk.Label(popup, text=self.cve_name)
        cve_name_label.grid(column=0, row=9, padx=5, pady=5)
        cve_name_entry.grid(column=1, row=9, padx=5, pady=5)

        description_label = tk.Label(popup, text="Description: ")
        description_entry = tk.Text(popup, width=60, height=5, wrap="word")
        description_entry.insert("1.0", self.description)
        description_label.grid(column=0, row=10, padx=5, pady=5)
        description_entry.grid(column=1, row=10, padx=5, pady=5)

        attack_vector_label = tk.Label(popup, text="Attack Vector: ")
        attack_vector_entry = tk.Label(popup, text=self.attack_vector)
        attack_vector_label.grid(column=0, row=11, padx=5, pady=5)
        attack_vector_entry.grid(column=1, row=11, padx=5, pady=5)

        attack_complexity_label = tk.Label(popup, text="Attack Complexity: ")
        attack_complexity_entry = tk.Label(popup, text=self.attack_complexity)
        attack_complexity_label.grid(column=0, row=12, padx=5, pady=5)
        attack_complexity_entry.grid(column=1, row=12, padx=5, pady=5)

        custom_score_label = tk.Label(popup, text="Custom Score: ")
        custom_score_entry = tk.Label(popup, text=self.custom_score)
        custom_score_label.grid(column=0, row=13, padx=5, pady=5)
        custom_score_entry.grid(column=1, row=13, padx=5, pady=5)

        custom_score_reason_label = tk.Label(popup, text="Custom Score Reason: ")
        custom_score_reason_entry = tk.Label(popup, text=self.custom_score_reason)
        custom_score_reason_label.grid(column=0, row=14, padx=5, pady=5)
        custom_score_reason_entry.grid(column=1, row=14, padx=5, pady=5)

        privileges_required_label = tk.Label(popup, text="Privileges Required: ")
        privileges_required_entry = tk.Label(popup, text=self.privileges_required)
        privileges_required_label.grid(column=0, row=15, padx=5, pady=5)
        privileges_required_entry.grid(column=1, row=15, padx=5, pady=5)

        user_interaction_label = tk.Label(popup, text="User Interaction: ")
        user_interaction_entry = tk.Label(popup, text=self.user_interaction)
        user_interaction_label.grid(column=0, row=16, padx=5, pady=5)
        user_interaction_entry.grid(column=1, row=16, padx=5, pady=5)

        confidentiality_impact_label = tk.Label(popup, text="Confidentiality Impact: ")
        confidentiality_impact_entry = tk.Label(popup, text=self.confidentiality_impact)
        confidentiality_impact_label.grid(column=0, row=17, padx=5, pady=5)
        confidentiality_impact_entry.grid(column=1, row=17, padx=5, pady=5)

        integrity_impact_label = tk.Label(popup, text="Integrity Impact: ")
        integrity_impact_entry = tk.Label(popup, text=self.integrity_impact)
        integrity_impact_label.grid(column=0, row=18, padx=5, pady=5)
        integrity_impact_entry.grid(column=1, row=18, padx=5, pady=5)

        availability_impact_label = tk.Label(popup, text="Availability Impact: ")
        availability_impact_entry = tk.Label(popup, text=self.availability_impact)
        availability_impact_label.grid(column=0, row=19, padx=5, pady=5)
        availability_impact_entry.grid(column=1, row=19, padx=5, pady=5)

        base_score_label = tk.Label(popup, text="Base Score: ")
        base_score_entry = tk.Label(popup, text=self.base_score)
        base_score_label.grid(column=0, row=20, padx=5, pady=5)
        base_score_entry.grid(column=1, row=20, padx=5, pady=5)

        base_severity_label = tk.Label(popup, text="Base Severity: ")
        base_severity_entry = tk.Label(popup, text=self.base_severity)
        base_severity_label.grid(column=0, row=21, padx=5, pady=5)
        base_severity_entry.grid(column=1, row=21, padx=5, pady=5)

        exploitability_score_label = tk.Label(popup, text="Exploitability Score: ")
        exploitability_score_entry = tk.Label(popup, text=self.exploitability_score)
        exploitability_score_label.grid(column=0, row=22, padx=5, pady=5)
        exploitability_score_entry.grid(column=1, row=22, padx=5, pady=5)
