# test of ExploitSearcher given a vulnerabilities cve
from util.ExploitSearch import ExploitSearcher

# cve 2018-4240 is a macOS denial of service (DoS) vulnerability
es = ExploitSearcher('2018-4042')

print(es.search(), "exploit(s) found")
print('Exploits found: ', es.total())

print('\n')
print(es.get_description())

print('\n')
es.print_all()

print('\n')
print(es.get_osvdb())