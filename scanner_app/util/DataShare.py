vulnerabilities = []
scanned_hosts = []
selected_host_index = None
cpes = {}
cve_selection = ''




class DataShare:
    """This class is a singleton class used to pass various data between the different tabs of the application.
    This data is used in multiple different ways according to what specific tab the user is viewing at the time.
    """
    __instance = None

    def __init__(self):
        """Virtually private constructor

        :raises Exception if object already exist
        """
        if DataShare.__instance is not None:
            raise Exception("DataShare is a singleton and has already been created")
        else:
            DataShare.__instance = self

    @staticmethod
    def get_vulns():
        """

        :return current vulnerabilities
        """
        global vulnerabilities
        if vulnerabilities:
            return vulnerabilities

    @staticmethod
    def set_vulns(vulns):
        """

        :param vulns: selected vulnerabilities to be set
        """
        global vulnerabilities
        if vulns:
            vulnerabilities = vulns

    @staticmethod
    def get_hosts():
        """

        :return: current hosts
        """
        global scanned_hosts
        if scanned_hosts:
            return scanned_hosts

    @staticmethod
    def set_hosts(hosts):
        """

        :param hosts: selected hosts to be set
        """
        global scanned_hosts
        if hosts:
            scanned_hosts = hosts

    @staticmethod
    def get_hosts_total():
        """

        :return: total hosts stored
        """
        global scanned_hosts
        return len(scanned_hosts)

    @staticmethod
    def get_cpes():
        """

        :return: current cpes
        """
        global cpes
        if cpes:
            return cpes

    @staticmethod
    def set_cpes(cpes_dict):
        """

        :param cpes_dict: selected cpes to be set
        """
        global cpes
        if cpes_dict:
            cpes = cpes_dict

    @staticmethod
    def get_selected_cve():
        """

        :return: current cve
        """
        global cve_selection
        if cve_selection:
            return cve_selection

    @staticmethod
    def set_selected_cve(cve):
        """

        :param cve: selected cve to be set
        """
        global cve_selection
        if cve:
            cve_selection = cve
