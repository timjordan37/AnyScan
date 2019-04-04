import xml.etree.ElementTree as ET

tree = ET.parse('official-cpe-dictionary_v2.3.xml')
root = tree.getroot()

# refernce
# https://docs.python.org/2/library/xml.etree.elementtree.html#parsing-xml-with-namespaces
for cpe in root.findall('{http://cpe.mitre.org/dictionary/2.0}cpe-item'):
    print(cpe.attrib['name'])
    tmp = cpe.find('{http://scap.nist.gov/schema/cpe-extension/2.3}cpe23-item')
    print(tmp.attrib['name'])

