import nmap
from util import DBFunctions as df, System
from models.Host import Host

"""
This class handles the scanner portion of our application.  It handles the type of scan as well as information 
retrieval regarding the scan details that are displayed on the default page as well as the scanned hosts that
appear on the left hand side of the application.  This information will only be displayed post scan, provided
that the scan has successfully detected devices connected to the current network.
"""


class Scanner:
    """Scanner class wraps nmap scans for quick scan types"""
    _ips = ''
    _ports = ''
    _scanner = None
    _scanned = False

    def __init__(self, ips, ports):
        """Create Scanner object given IP and port ranges to scan"""
        self._ips = ips
        self._ports = ports
        self._scanner = nmap.PortScanner()

    def host_discover(self):
        """Scans for live host that respond to pings

        :return nmap host discovery scan data
        """
        self._scanned = True
        return self._scanner.scan(self._ips, arguments='-sP')

    def full_scan(self):
        """Performs a full TCP scan with service discovery, good for initial scans

        :return nmap full scan data
        """
        self._scanned = True
        return self._scanner.scan(self._ips, self._ports, arguments='-sV -sS -T4')

    def script_scan(self):
        """Runs default scripts without host discovery. All host assumed up.

        :return nmap script scan data
        """
        self._scanned = True
        return self._scanner.scan(self._ips, self._ports, arguments='-Pn -sn -sC')

    def udp_scan(self):
        """Runs a UDP scan good for DNS, SNMP, and DHCP. Typically takes longer than a TCP scan

        :return nmap UDP scan data
        """
        self._scanned = True
        return self._scanner.scan(self._ips, self._ports, arguments='-sU')

    def fast_scan(self):
        """Quick scan of small port range with default arguments

        :return nmap fast scan data
        """
        self._scanned = True
        return self._scanner.scan(self._ips, self._ports)

    def detect_os_service_scan(self):
        """Runs scan to detemine OS and running service of given host

        :return nmap detect OS scan data
        """
        self._scanned = True
        return self._scanner.scan(self._ips, self._ports, arguments='-A')

    def get_os_details(self, result, host):
        """Return host information from a scan given results and specific host

        :param result: scan results dictionary
        :param host: host ip to get os details from
        :return [name, OS family, OS generation] of scan data or ["","",""]
        """
        if "osmatch" in result['scan'][host] and len(result['scan'][host]["osmatch"]) > 0:
            name = result['scan'][host]["osmatch"][0]["name"]
            os_family = result['scan'][host]["osmatch"][0]["osclass"][0]["osfamily"]
            os_gen = result['scan'][host]["osmatch"][0]["osclass"][0]["osgen"]
            return [name, os_family, os_gen]
        elif "osclass" in result['scan'][host]:
            name = result['scan'][host]['osclass']['vendor']
            os_family = result['scan'][host]['osclass']['osfamily']
            os_gen = result['scan'][host]['osclass']['osgen']
            return [name, os_family, os_gen]
        else:
            return ["", "", ""]

    def get_vendor(self, result, host, mac):
        """Given results, host, and mac return vendor if found, check for empty string

        :param result: scan results dictionary
        :param host: host ip to get vendor from
        :param mac: mac address to get vendor from
        :return vendor data of given host
        """
        if "vendor" in result['scan'][host] and mac in result['scan'][host]['vendor']:
            return result['scan'][host]['vendor'][mac]
        else:
            return ""

    def get_mac_address(self, result, host):
        """Given results and host return mac if found, check for empty string

        :param result: scan results dictionary
        :param host: host ip to get mac from
        :return mac address of given host
        """
        if "mac" in result['scan'][host]["addresses"]:
            return result['scan'][host]["addresses"]["mac"]
        else:
            return ""

    """Runs a scan of the given type"""

    def get_scan_details(self, scan_type):
        """Runs scan to determine OS and running service of given host

        :return array of host data found in scan
        """
        result = None
        # Check scan type
        if scan_type == System.ScanType.full_scan:
            result = self.full_scan()
        elif scan_type == System.ScanType.script_scan:
            result = self.script_scan()
        elif scan_type == System.ScanType.udp_scan:
            result = self.udp_scan()
        elif scan_type == System.ScanType.fast_scan:
            result = self.fast_scan()
        elif scan_type == System.ScanType.detect_os_service_scan:
            result = self.detect_os_service_scan()

        hosts = []
        if self._scanned:
            # for each host scanned
            for host in self._scanner.all_hosts():
                print("-----------------")
                print(result['scan'][host])
                print("-----------------")
                state = result['scan'][host]["status"]["state"]
                mac = self.get_mac_address(result, host)
                vendor = self.get_vendor(result, host, mac)
                val_arr = self.get_os_details(result, host)
                name = val_arr[0]
                os_gen = val_arr[1]
                os_family = val_arr[2]
                hosts.append(Host(0, host, state, name, os_family, os_gen, vendor, mac))

        return hosts

    def get_os_service_scan_details(self):
        """Runs scan to determine OS and running service of given host

        :return array of host data found in scan
        """
        self._scanned = True
        result = self._scanner.scan(self._ips, self._ports, arguments='-A')
        hosts = []
        if self._scanned:
            # for each host scanned
            for host in self._scanner.all_hosts():
                print("-----------------")
                print(result['scan'][host])
                print("-----------------")
                state = result['scan'][host]["status"]["state"]
                mac = self.get_mac_address(result, host)
                vendor = self.get_vendor(result, host, mac)
                val_arr = self.get_os_details(result, host)
                name = val_arr[0]
                os_gen = val_arr[1]
                os_family = val_arr[2]
                hosts.append(Host(host, state, name, os_family, os_gen, vendor, mac))

        return hosts

    def get_cpes(self):
        """Returns CPEs found from scan

        :return dictionary of CPEs found via nmap scan
        :raises ScannerError is no scan has been conducted yet
        """
        full_cpes = {}
        host_cpes = []
        if self._scanned:
            for host in self._scanner.all_hosts():
                if 'tcp' in self._scanner[host]:
                    for port in self._scanner[host]['tcp']:
                        if 'cpe' in self._scanner[host]['tcp'][port] and self._scanner[host]['tcp'][port]['cpe'] != '':
                            host_cpes.append(self._scanner[host]['tcp'][port]['cpe'])
                full_cpes[host] = host_cpes
            return full_cpes
        else:
            raise ScannerError("ERROR: A scan has not yet been conducted!")

    def query_db_cves(self):
        if self._scanned:
            df.DBFunctions.query_cves(self.get_cpes())

    def get_hosts(self):
        """Return all hosts found during scan

        :return all hosts found via nmap scan
        :raises ScannerError is no scan has been conducted yet
        """
        if self._scanned:
            return self._scanner.all_hosts()
        else:
            raise ScannerError("ERROR: A scan has not yet been conducted!")

    def get_csv(self):
        """Return latest scan information in csv format

        :return csv scan data
        """
        if self._scanned:
            return self._scanner.csv()

    def print_scan(self):
        """Print a scan result to the console with relevant information"""
        if self._scanned:
            # for each host scanned
            for host in self._scanner.all_hosts():
                # print the ip and associated hostname if available and state
                # for each protocol of the given host
                for pro in self._scanner[host].all_protocols():
                    # print the protocol and all the port responses
                    print('\nProtocol: %s' % pro)
                    ports = self._scanner[host][pro].keys()
                    # for each port print its state
                    for port in ports:
                        print('Port: %s\tState: %s' % (port, self._scanner[host][pro][port]['state']))


class ScannerError(Exception):
    """Raised when Scanner encounters a possible error to be handled accordingly"""
    pass
