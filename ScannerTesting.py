from Scanner import *

# Test scanning on local gateway (router)
testScan = Scanner('192.168.1.1', '7-1024')
try:
    all_hosts = testScan.get_hosts()
except ScannerError as err:
    print(err)

testScan.fast_scan()
print(testScan.get_hosts())
testScan.print_scan()
print()
result = testScan.get_csv();
print('This is a CSV representation of a scan: ')
print(result, '\n');

testScan.detect_os_service_scan()
testScan.print_scan()
