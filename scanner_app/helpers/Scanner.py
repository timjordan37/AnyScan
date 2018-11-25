import nmap

from models.Host import Host

class Scanner:
    """Scanner class wraps nmap scans for quick scan types"""
    _ips = ''
    _ports = ''
    _scanner = None
    _scanned = False

    def __init__(self, ips, ports):
        self._ips  = ips
        self._ports = ports
        self._scanner = nmap.PortScanner()

    def host_discover(self):
        """Scans for live host that respond to pings"""
        self._scanned = True
        # return self._scanner.scan(self._ips, self._ports)
        return self._scanner.scan(self._ips, arguments='-sP', sudo=True)

    # Won't run from pycharm because stealth scans require sudo and pycharm doesn't have a
    # console to ask for password. Researching further.
    def full_scan(self):
        """Performs a full TCP scan with service discovery, good for initial scans"""
        self._scanned = True
        return self._scanner.scan(self._ips, self._ports, arguments='-sV -sS -T4', sudo=True)

    def script_scan(self):
        """Runs default scripts without host discovery. All host assumed up."""
        self._scanned = True
        return self._scanner.scan(self._ips, self._ports, arguments='-Pn -sn -sC')

    def udp_scan(self):
        """Runs a UDP scan good for DNS, SNMP, and DHCP. Typically takes longer than a TCP scan"""
        self._scanned = True
        return self._scanner.scan(self._ips, self._ports, arguments='-sU')

    def fast_scan(self):
        """Quick scan of small port range with default arguments"""
        return self._scanner.scan(self._ips, self._ports)
        self._scanned = True

    def detect_os_service_scan(self):
        """Runs scan to detemine OS and running service of given host"""
        self._scanned = True
        return self._scanner.scan(self._ips, self._ports, arguments='-A', sudo=True)

    def get_os_details(self, result, host):
        print("--")
        print(result['scan'][host])
        print("--")
        print(result['scan'][host]["osmatch"])
        print("--")
        if result['scan'][host]["osmatch"] is not None and len(result['scan'][host]["osmatch"]) > 0:
            name = result['scan'][host]["osmatch"][0]["name"]
            os_family = result['scan'][host]["osmatch"][0]["osclass"][0]["osfamily"]
            os_gen = result['scan'][host]["osmatch"][0]["osclass"][0]["osgen"]
            return [name, os_family, os_gen];
        else:
            return ["", "", ""]

    def get_vendor(self, result, host):
        if "vendor" in result and host in result["vendor"]:
            return result["vendor"][host]
        else:
            return ""

    def get_mac_address(self, result, host):
        if "mac" in result['scan'][host]["addresses"]:
            return result['scan'][host]["addresses"]["mac"]
        else:
            return ""

    def get_os_service_scan_details(self):
        """Runs scan to detemine OS and running service of given host"""
        self._scanned = True
        result = self._scanner.scan(self._ips, self._ports, arguments='-A', sudo=True)
        hosts = []
        if self._scanned:
            # for each host scanned
            print("MUCHO DETAILS")
            for host in self._scanner.all_hosts():
                print("HOST: ")
                print("==================")
                print(result['scan'][host])
                print("==================")
                state = result['scan'][host]["status"]["state"]
                mac = self.get_mac_address(result, host)
                vendor = self.get_vendor(result, host)
                val_arr = self.get_os_details(result, host)
                name = val_arr[0]
                os_gen = val_arr[1]
                os_family = val_arr[2]
                hosts.append(Host(host, state, name, os_family, os_gen, " ", mac))

        return hosts

    def get_hosts(self):
        """Return all hosts found during scan"""
        if self._scanned:
            return self._scanner.all_hosts()
        else:
            raise ScannerError("ERROR: A scan has not yet been conducted!")

    def get_csv(self):
        """Return lastest scan information in csv format"""
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
                        print('Port: %s\tState: %s' %(port, self._scanner[host][pro][port]['state']))

class ScannerError(Exception):
    """Raised when Scanner encounters a possible error to be handled accordingly"""
    pass
