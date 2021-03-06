import sqlite3
import json
from pathlib import Path
import xml.etree.ElementTree as ET

"""
This class sets up our database and the various other search functions that we use in order to filter through our 
data and display it properly to the user via the application.
"""


class DBFunctions:

    # Saves a new device to the database
    @staticmethod
    def save_device(deviceName, deviceManufacturer, cpeURI):
        """Save a found device to the database with device name, manufacturer, and cpe

        :param deviceName:
        :param deviceManufacturer:
        :param cpeURI: device cpe found via nmap scan
        :return true if device saved successfully
        """

        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        device_info = (deviceName, deviceManufacturer, cpeURI)

        try:
            cursor.execute('''INSERT INTO Devices VALUES(?, ?, ?)''', device_info)
            conn.commit()
        except sqlite3.IntegrityError as e:
            return False

        return True

    # Saving a Vulnerability to the database
    @staticmethod
    def save_vulnerability(cveName, description, CVSSScore, attackVector, attackComplexity, customScore,
                           customScoreReason, privilegesRequired,
                           userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                           baseScore, baseSeverity, exploitabilityScore):
        """Save a Vulnerability to the database given various details

        :param cveName:
        :param description:
        :param CVSSScore:
        :param attackVector:
        :param attackComplexity:
        :param customScore:
        :param customScoreReason: logic associated with deviating from standard score
        :param privilegesRequired:
        :param userInteraction:
        :param confidentialityImpact:
        :param integrityImpact:
        :param availibilityImpact:
        :param baseScore:
        :param baseSeverity:
        :param exploitabilityScore:
        :return true if vulnerability was saved successfully
        """

        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute('SELECT MAX(VulnID) FROM Vulnerabilities')
        conn.commit()
        maxIDTuple = cursor.fetchone()

        # print("LOOK TUPLE: ", maxIDTuple)

        maxID = maxIDTuple[0]

        if maxID is None:
            maxID = 0

        vulnID = maxID + 1

        vulnerability_info = (vulnID, cveName, description, CVSSScore, attackVector, attackComplexity, customScore,
                              customScoreReason, privilegesRequired,
                              userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                              baseScore, baseSeverity, exploitabilityScore)
        try:
            cursor.execute('''INSERT INTO Vulnerabilities VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           vulnerability_info)
            conn.commit()
        except sqlite3.IntegrityError:
            return False

        return True

    # todo CVSSScore isn't used. is this an issue or can we get rid of it?
    @staticmethod
    def update_vuln(vulnID, cveName, description, CVSSScore, attackVector, attackComplexity, customScore,
                    customScoreReason, privilegesRequired,
                    userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                    baseScore, baseSeverity, exploitabilityScore):
        """Update a vulnerability in the database given arious details

        :param vulnID:
        :param cveName:
        :param description:
        :param CVSSScore:
        :param attackVector:
        :param attackComplexity:
        :param customScore:
        :param customScoreReason:
        :param privilegesRequired:
        :param userInteraction:
        :param confidentialityImpact:
        :param integrityImpact:
        :param availibilityImpact:
        :param baseScore:
        :param baseSeverity:
        :param exploitabilityScore:
        :return
        """
        conn = sqlite3.connect("vulnDB.db")
        cursor = conn.cursor()

        vulnerability_info = (cveName, description, attackVector, attackComplexity, customScore,
                              customScoreReason, privilegesRequired,
                              userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                              baseScore, baseSeverity, exploitabilityScore, vulnID)

        cursor.execute('''UPDATE Vulnerabilities 
                        SET 
                        cveName = ?,
                        description = ?,
                        attackVector = ?,
                        attackComplexity = ?,
                        customScore = ?,
                        customScoreReason = ?,
                        priviligesRequired = ?,
                        userInteraction = ?,
                        confidentialityImpact = ?,
                        integrityImpact = ?,
                        availabilityImpact = ?,
                        baseScore = ?,
                        baseSeverity = ?,
                        exploitabilityScore = ? 
                        WHERE VulnID = ?''', vulnerability_info)
        conn.commit()

    # Saves a scan to the database
    @staticmethod
    def save_scan(Date, Duration):
        """Save a scan to the Db

        :param Date: date of scan to be imported
        :param Duration: time scan took to complete
        :return id of last row inserted into scan history table
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute('SELECT MAX(ScanID) FROM ScanHistory')
        conn.commit()

        maxIDTuple = cursor.fetchone()
        maxID = 0
        if maxIDTuple is not None and maxIDTuple[0] is not None:
            maxID = maxIDTuple[0]
            maxID += 1

        scanID = maxID

        scan_info = (scanID, Date, Duration)
        cursor.execute('''INSERT INTO ScanHistory VALUES(?, ?, ?)''', scan_info)
        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def build_db():
        """Build database"""
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE Devices (Model TEXT PRIMARY KEY,
             Manufacturer TEXT, 
             cpeURI TEXT)''')
        cursor.execute('''CREATE TABLE CPEVulns (
            cpeURI TEXT, 
            cveName TEXT, 
            PRIMARY KEY(cpeURI, cveName))''')
        cursor.execute('''CREATE TABLE CPEVersions (
                    cpe22 TEXT NOT NULL, 
                    cpe23 TEXT NOT NULL, 
            PRIMARY KEY(cpe22,cpe23),
            UNIQUE (cpe22, cpe23))''')
        # todo is there a reason this commit is here and below? Do we need 2?
        conn.commit()
        cursor.execute('''CREATE TABLE Vulnerabilities (VulnID INTEGER PRIMARY KEY, 
            cveName TEXT,
            description TEXT, 
            CVSSScore INTEGER, 
            attackVector TEXT, 
            attackComplexity TEXT, 
            customScore TEXT, 
            customScoreReason TEXT,
            priviligesRequired TEXT, 
            userInteraction TEXT, 
            confidentialityImpact TEXT, 
            integrityImpact TEXT, 
            availabilityImpact TEXT,
            baseScore TEXT, 
            baseSeverity TEXT, 
            exploitabilityScore INTEGER)''')
        cursor.execute('''CREATE TABLE ScanHistory (ScanID INTEGER PRIMARY KEY, 
            ScanDate TEXT, 
            Duration INTEGER)''')
        cursor.execute('''CREATE TABLE Hosts (HostID INTEGER PRIMARY KEY, 
            ip TEXT, 
            macAddress TEXT, 
            osFamily TEXT, 
            osGen TEXT, 
            name TEXT, 
            vendor TEXT, 
            ScanID INTEGER, 
            FOREIGN KEY(ScanID) REFERENCES ScanHistory(ScanID))''')
        conn.commit()
        cursor.execute('''CREATE TABLE Parameters (ScanID INTEGER, 
            ParameterValue TEXT, 
            ParameterType TEXT, 
            PRIMARY KEY(ScanID, ParameterType))''')
        cursor.execute('''CREATE TABLE PenTestHistory (PenTestID INTEGER PRIMARY KEY, 
            VulnID INTEGER, 
            Model TEXT,
            ScanID INTEGER, 
            Result TEXT, 
            FOREIGN KEY(VulnID) REFERENCES Vulnerabilities(VulnID), 
            FOREIGN KEY(Model) REFERENCES Devices(Model), 
            FOREIGN KEY(ScanID) REFERENCES ScanHistory(ScanID))''')
        conn.commit()
        cursor.execute('''CREATE TABLE CVE_By_Host (HostID INTEGER,
            VulnID INTEGER,
            PRIMARY KEY(HostID, VulnID),
            FOREIGN KEY(HostID) REFERENCES Hosts(HostID),
            FOREIGN KEY(VulnID) REFERENCES Vulnerabilities(VulnID))''')
        conn.commit()

    @staticmethod
    def save_host(host, scanID):
        """Saves a scan to the database

        :param host: host name
        :param scanID: scan ID
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute('SELECT MAX(HostID) FROM Hosts')
        conn.commit()
        maxIDTuple = cursor.fetchone()
        maxID = 0
        if maxIDTuple is not None and maxIDTuple[0] is not None:
            maxID = maxIDTuple[0]
            maxID += 1

        hostID = maxID
        scan_info = (hostID, host._ip, host._macAddress, host._osFamily, host._osGen, host._name, host._vendor, scanID)
        cursor.execute('''INSERT INTO Hosts VALUES(?, ?, ?, ?, ?, ?, ?, ?)''', scan_info)
        conn.commit()

    @staticmethod
    def save_cve_by_host(hostID, cve):
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        host_cve = (hostID, cve)
        cursor.execute('''INSERT INTO CVE_By_Host VALUES(?,?)''', host_cve)
        conn.commit()

    @staticmethod
    def save_cpeVuln(cpe, cve):
        """Saves a new cpe\cve combo into the cpeVulns table
        :param cpe: cpe to import to db
        :param cve: cve to import to db
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cpeVuln = (cpe, cve)

        cpe_test = cpe[0:7]
        if cpe_test != 'cpe:2.3':
            error = f'\nCPE version 2.2: {cpe}\n'
            print(error)
            # update version to 2.3 if not already
            cpe = DBFunctions.cpe_version_reference(cpe)
            print(DBFunctions.cpe_version_reference(cpe))

        try:
            cursor.execute('''INSERT INTO CPEVulns VALUES (?, ?)''', cpeVuln)
        except sqlite3.IntegrityError:
            # only works for python3.6 or greater
            error = f'Combo already exist in DB:\nCVE {cve} \nCPE: {cpe}'
            print(error)
        conn.commit()

    @staticmethod
    def query_cves(cpe_dict):
        """query DB for CVEs according to CPEs found by scanner

        :param cpe_dict: cpe dictionary in the form {host0 : [cpe, list0], host1: [cpe, list1]
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        cves = []
        vulns = {}
        print("\nDBFunctions 309 query_cves\n")

        for hList in cpe_dict:
            for cpe in cpe_dict[hList]:
                print('CPE: ', cpe)

                cpe_test = cpe[0:7]
                if cpe_test != 'cpe:2.3':
                    error = f'DBFunctions 317 CPE version 2.2: {cpe}'
                    print(error)
                    # update version to 2.3 if not already
                    cpe = DBFunctions.cpe_version_reference(cpe)
                    print('DBFunciton 321 CPE23: ', cpe)


                cursor.execute("""SELECT * FROM CPEVulns WHERE cpeURI IS (?)""", (cpe,))
                value = cursor.fetchone()
                if value:
                    vulns[hList] = value[1]
                    print('Host: ', hList)
                    print('Vuln: ', value)

        conn.commit()
        conn.close()

        return vulns

    @staticmethod
    def query_vulns(cve):
        """Query the database for a specific vulnerability

        :param cve: vulnerability to be searched for
        :return vulnerabilities for the given CVE
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Vulnerabilities WHERE cveName IS (?)""", (cve,))
        return cursor.fetchone()

    @staticmethod
    def query_report_info():
        """Gather information from database that is needed for report generation

        :return tuple of IP, MAC addresses, and name of hosts from Hosts table
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        cursor2 = conn.cursor()
        cursor3 = conn.cursor()
        # cursor4 = conn.cursor()


        cursor.execute("""SELECT ip FROM Hosts""")
        cursor2.execute("""SELECT macAddress FROM Hosts""")
        cursor3.execute("""SELECT name FROM Hosts""")
        # I fixed this, but we'll want to add a range of baseScore vulns to the DB to test
        # Also, if baseScore isn't a number I'm pretty sure sqlite will consider it bigger no matter what
        # We will want to test what happens there too  
        # cursor4.execute("""SELECT * FROM Vulnerabilities WHERE baseScore >= 7.0""")
        results = (cursor.fetchall(), cursor2.fetchall(), cursor3.fetchall())
        return results

    # Imports Data from NVD JSON file
    @staticmethod
    def import_NVD_JSON(json_fp=None):
        """Imports json file from NVD into database

        :param json_fp: file path of json file to be import. Default assumes working directory contains nvdcve-1.0-2019.json
        """
        if not json_fp:
            # default file I've been using for testing. We could get rid of this for release
            json_fp = Path("nvdcve-1.0-2019.json")
            print(json_fp)
        else:
            json_fp = Path(json_fp)
            print(json_fp)

        nvd_json = json.loads(json_fp.read_text())
        cve_items_list = nvd_json['CVE_Items']

        for cve in cve_items_list:
            cve_meta_data = cve.get("cve").get("CVE_data_meta")

            description_data = cve.get("cve").get("description").get("description_data")
            description = description_data[0].get("value")

            configurations = cve['configurations']
            cpe_list = configurations['nodes']

            try:
                cvssV3 = cve.get("impact").get("baseMetricV3").get("cvssV3")
                baseMetric = cve.get("impact").get("baseMetricV3")
                DBFunctions.save_vulnerability(cve_meta_data['ID'], description, cvssV3['attackVector'],
                                               cvssV3['attackComplexity'], "", "", cvssV3['privilegesRequired'],
                                               cvssV3['userInteraction'],
                                               cvssV3['confidentialityImpact'], cvssV3['integrityImpact'],
                                               cvssV3['availabilityImpact'],
                                               cvssV3['baseScore'], cvssV3['baseSeverity'],
                                               baseMetric['exploitabilityScore'])
            except:
                # todo determine why this always errors
                DBFunctions.save_vulnerability(cve_meta_data['ID'], description, "N/A", "N/A", "", "", "N/A",
                                               "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A")
            for item in cpe_list:
                try:
                    cpe_match = item['cpe_match']
                    for match in cpe_match:
                        try:
                            cpe_URI = match['cpe23Uri']
                        except:
                            cpe_URI = match['cpe22Uri']
                        DBFunctions.save_cpeVuln(cpe_URI, cve_meta_data['ID'])
                except KeyError:
                    print('No CVE Match for CPE: ', cpe_URI)

    @staticmethod
    def import_cve_verison_matches(nvd_file='official-cpe-dictionary_v2.3.xml'):
        """Imports xml file from NVD into database for cpe version matching

        :param nvd_file: file path of xml file to import. Default assumes working directory contains official-cpe-dictionary_v2.3.xml
        """
        # assumes the default file is available
        tree = ET.parse(nvd_file)
        root = tree.getroot()
        # cursor for DB addition
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        # get matches accoridng to xml namespace and adds to DB
        for cpe in root.findall('{http://cpe.mitre.org/dictionary/2.0}cpe-item'):
            tmp = cpe.find('{http://scap.nist.gov/schema/cpe-extension/2.3}cpe23-item')
            pair = (cpe.attrib['name'], tmp.attrib['name'])
            cursor.execute('''INSERT INTO CPEVersions VALUES(?, ?)''', pair)
            conn.commit()

    # Retrieves all data for specified ScanID
    @staticmethod
    def retrieve_scanID_data(scanID):
        """Get the data from ScanHistory table given the scan id

        :param scanID:
        :return data associated with given scan id
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        retrievalID = int(scanID)
        cursor.execute('''SELECT * FROM ScanHistory WHERE ScanID = ?''', (retrievalID,))
        results = cursor.fetchall()
        return results

    # Retrieves scanIDs and Dates for all Scans
    @staticmethod
    def retrieve_scan_history():
        """Get the all data from the Scanhistory table

        :return all data saved into the ScanHistory table
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT ScanID, ScanDate FROM ScanHistory''')
        results = cursor.fetchall()
        return results

    # Deletes specified ScanID
    @staticmethod
    def delete_scan_ID(scanID):
        """Remove data from ScanHistory table given the scan id

        :param scanID:
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        deleteID = (scanID)
        cursor.execute('''DELETE FROM ScanHistory WHERE ScanID = ?''', deleteID)

    @staticmethod
    def get_full_cve():
        """Returns all unique CVEs in database

        :return all cves in database
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        results = set()
        cursor.execute('''SELECT cveName FROM CPEvulns''')

        for row in cursor:
            results.add(row[0])

        return results

    @staticmethod
    def get_all_devices():
        """Query the database for all saved devices

        :return model and manufacturer for all devices in Device table
        """

        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute("""SELECT Model, Manufacturer from Devices""", ())
        return cursor.fetchall()

    @staticmethod
    def get_all_scans():
        """Query the database for all saved scans

        :return data for all scans saved
        """

        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute("""SELECT sh.ScanID as ScanID, 
                                sh.Duration as Duration, 
                                sh.ScanDate as Date, 
                                (SELECT COUNT(*) from Hosts where ScanID = sh.ScanID) as HostCount 
                                from ScanHistory sh JOIN Hosts h on sh.ScanID = h.ScanID 
                                GROUP BY sh.ScanID""", ())
        return cursor.fetchall()

    @staticmethod
    def get_all_where(query_str, query_params):
        """Query the database for all saved entiries with the given string and params

        :param query_str: query to be executed
        :param query_params: parameters needed to properly execute given query
        :return data returned depends on the database query given
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        try:
            cursor.execute(query_str, query_params)
            conn.commit()

        except sqlite3.Error as er:
            print
            'er:', er.message

        return cursor.fetchall()

    """Vulnerabilities Methods"""

    @staticmethod
    def get_all_vulns():
        """Query the database for all saved vulnerabilities

        :return all vulnerabilities saved into the database
        """

        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute("""SELECT VulnID, cveName, CVSSScore, baseScore, baseSeverity from Vulnerabilities ORDER BY 
        CVSSScore DESC""", ())
        return cursor.fetchall()

    @staticmethod
    def cpe_version_reference(cpe22):
        """Given the 2.2 version of a cpe return the 2.3 version

        :param cpe22: assumed to be a valid cpe2.2
        :return: CPE v2.3 given v2.2
        """

        if not cpe22:
            return

        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        # Wild card to find closest match
        cpe22 += '%'
        print('DBFunctions 584 cpe22 updated: ', cpe22)

        # needs the comma at the end so you are passing
        # a tuple with 1 string not a sequence of chars
        cursor.execute("""SELECT cpe23 FROM CPEVersions where cpe22 LIKE ?""", (cpe22,))

        cpe23 = cursor.fetchone()
        if cpe23:
            return cpe23[0]


# TESTING
if __name__=="__main__":
    # quick unit testing, I'm sure python has something built in I could use
    cpes_version_test = {
        'cpe:/a:zzcms:zzcms:6.0', # yes
        'cpe:/a:zzcms:zzcms:6.1', # yes
        'cpe:/a:zzcms:zzcms:7.0', # yes
        'cpe:/a:zzcms:zzcms:7.1', # yes
        'cpe:/a:zzcms:zzcms:7.2', # yes
        'cpe:/a:zzcms:zzcms:8.0', # yes
        'cpe:/a:zzcms:zzcms:8.1', # yes
        'cpe:/a:zzcms:zzcms:8.2', # yes
        'cpe:/a:zzcms:zzcms:8.3', # yes
        'cpe:/a:zzcms:zzcms:2018', # yes
        'cpe:/a:zzcms:zzcms:2019', # yes
        'thisshouldntwork', # no
        'cpe:/a:zzzcms:zz.1', # no
        'cpe:/a:zzzcms:zzzphp:1.6', # no
        'cpe:/a:zzzs:zzzphp:1.6.1', # no
        'cpeazzzcms:zphp:1.6.1', # no
        'cpe:/a:%240.99_kindle_books_project:%240.99_kindle_books:6::~~~android~~' # yes
    }

    for item in cpes_version_test:
        print('Test item: ', item)
        item = DBFunctions.cpe_version_reference(item)
        if item:
            print('Found: ', item)
        else:
            print('Not valid')

