import nmap

class Scanner:
    """Scanner class wraps nmap scans for quick scan types"""
    _ips = ''
    _ports = ''
    _scanner = None

    def __init__(self, ips, ports):
        self._ips  = ips
        self._ports = ports
        self._scanner = nmap.PortScanner()

    def host_discover(self):
        """Scans for live host that respond to pings"""
        return self._scanner.scan(self._ips, self._ports, arguments='-sP')

    # Won't run from pycharm because stealth scans require sudo and pycharm doesn't have a
    # console to ask for password. Researching further.
    def full_scan(self):
        """Performs a full TCP scan with service discovery, good for initial scans"""
        return self._scanner.scan(self._ips, self._ports, arguments='-sV -sS -T4', sudo=True)

    def script_scan(self):
        """Runs default scripts without host discovery. All host assumed up."""
        return _scanner.scan(_ips, _ports, arguments='-Pn -sn -sC')

    def udp_scan(self):
        """Runs a UDP scan good for DNS, SNMP, and DHCP. Typically takes longer than a TCP scan"""
        return _scanner.scan(_ips, _ports, arguments='-sU')



testScan = Scanner('192.168.1.0/28', '7-1024')
# Won't run from pycharm because it requires sudo and needs password
results = testScan.full_scan()
print(results)
