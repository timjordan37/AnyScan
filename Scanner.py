import nmap

IP_LOOPBACK = '127.0.0.1'
COMMON_PORTS = '0-1023'

scanner = nmap.PortScanner()

# Quick scan of the most common ports stored in var
#result = scanner.scan(IP_LOOPBACK, COMMON_PORTS)

# Function for fun
def get_command(scan):
    return scan.command_line()

# Conducts ping scan -- host discovery without port scan
scanner.scan('192.168.1.0/24', arguments='-sn')

# Print found host and state
for host in scanner.all_hosts():
    print('Host: %s \tState: %s' % (host, scanner[host].state()))

#########################
# Trying out Async scans

scanner2 = nmap.PortScannerAsync()

def callback_when_done(host, result):
    print('-------------------------')
    print('%s is all done being scanned!' % host)

scanner2.scan('192.168.1.0/28', arguments='-sn', callback=callback_when_done)

while scanner2.still_scanning():
    print("Still scanning...")
    # Make scanner wait a second after each host
    scanner2.wait(1)