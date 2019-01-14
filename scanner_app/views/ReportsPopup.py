import tkinter as tk

class ReportsPopup():

    _report_generator = ''

    device_name = ''
    device_manufacturer = ''
    cpe_uri = ''

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

    scan_id = ''
    date = ''
    duration = ''

    host_id = ''
    host_ip = ''
    host_macAddress = ''
    host_osFamily = ''
    host_osGen = ''
    host_name = ''
    host_vendor = ''

    parameter_value = ''
    parameter_type = ''

    pen_test_id = ''
    result = ''

    def __init__(self, report_generator):
        self._report_generator = report_generator
