vulnerabilities = []
scanned_hosts = []
selected_host_index = None
cpes = {}
cve_selection = ''

"""
This class is a singleton class used to pass various data between the different tabs of the application.  This data
is used in multiple different ways according to what specific tab the user is viewing at the time.
"""


class DataShare:
    """Singleton class to pass data between tabs for use throughout application"""
    __instance = None

    def __init__(self):
        """Virtually private constructor"""
        if DataShare.__instance is not None:
            raise Exception("DataShare is a singleton and has already been created")
        else:
            DataShare.__instance = self

    @staticmethod
    def get_vulns():
        global vulnerabilities
        if vulnerabilities:
            return vulnerabilities

    @staticmethod
    def set_vulns(vulns):
        global vulnerabilities
        if vulns:
            vulnerabilities = vulns

    @staticmethod
    def get_hosts():
        global scanned_hosts
        if scanned_hosts:
            return scanned_hosts

    @staticmethod
    def set_hosts(hosts):
        global scanned_hosts
        if hosts:
            scanned_hosts = hosts

    @staticmethod
    def get_hosts_total():
        global scanned_hosts
        return len(scanned_hosts)

    @staticmethod
    def get_cpes():
        global cpes
        if cpes:
            return cpes

    @staticmethod
    def set_cpes(cpes_dict):
        global cpes
        if cpes_dict:
            cpes = cpes_dict

    @staticmethod
    def get_selected_cve():
        global cve_selection
        if cve_selection:
            return cve_selection

    @staticmethod
    def set_selected_cve(cve):
        global cve_selection
        if cve:
            cve_selection = cve
