import nmap

from scanner_app.models.Host import Host

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
        return self._scanner.scan(self._ips, self._ports)
        # return self._scanner.scan(self._ips, self._ports, arguments='-sP')

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
        return self._scanner.scan(self._ips, self._ports, arguments='-A')

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

    def get_host_details(self):
        if self._scanned:
            hosts = []
            # for each host scanned
            for host in self._scanner.all_hosts():
                # print the ip and associated hostname if available and state
                hosts.append(Host(host, self._scanner[host].state()))
                print('\nIP: %s\t State: %s' % (host, self._scanner[host].state()))

            return hosts


    def print_scan(self):
        """Print a scan result to the console with relevant information"""
        if self._scanned:
            # for each host scanned
            for host in self._scanner.all_hosts():
                # print the ip and associated hostname if available and state
                print('\nIP: %s\t State: %s' % (host, self._scanner[host].state()))
                print("CHECK:",self._scanner[host])
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
