import nmap

IP_LOOPBACK = '127.0.0.1'
COMMON_PORTS = '0-1023'

scanner = nmap.PortScanner()

# Quick scan of the most common ports stored in var
result = scanner.scan(IP_LOOPBACK, COMMON_PORTS)

# Function for fun
def get_command(scan):
    return scan.command_line()

#   TEST
# 
print(result)
print()
print(get_command(scanner))