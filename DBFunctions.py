import sqlite3
import json
from pathlib import Path

class DBFunctions():

    #Saves a new device to the database
    @staticmethod
    def save_device(deviceName, deviceManufacturer, cpeURI):
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        device_info = (deviceName, deviceManufacturer, cpeURI)

        try:
            cursor.execute('''INSERT INTO Devices VALUES(?, ?, ?)''', device_info)
        except sqlite3.IntegrityError as e:
            return False

        return True

    #Saving a Vulnerability to the database
    @staticmethod
    def save_vulnerability(cveName, description, attackVector, attackComplexity, customScore,
                           customScoreReason, priviledgesRequired,
                           userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                           baseScore, baseSeverity, exploitabilityScore):
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute('SELECT MAX(VulnID) FROM Vulnerabilities')
        conn.commit()

        maxIDTuple = cursor.fetchone()
        maxID = 0

        if maxIDTuple[0] is not None:
            maxID = maxIDTuple[0]
            maxID += 1

        vulnID = maxID

        vulnerability_info = (vulnID, cveName, description, attackVector, attackComplexity, customScore,
                           customScoreReason, priviledgesRequired,
                           userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                           baseScore, baseSeverity, exploitabilityScore)
        try:
            cursor.execute('''INSERT INTO Vulnerabilities VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                           ?, ?)''', vulnerability_info)
            conn.commit()
        except sqlite3.IntegrityError:
            return "That device already exists in the database."

    # Saves a scan to the database
    @staticmethod
    def save_scan(Date, Duration):
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute('SELECT MAX(ScanID) FROM ScanHistory')
        conn.commit()

        maxIDTuple = cursor.fetchone()
        maxID = 0
        if maxIDTuple[0] is not None:
            maxID = maxIDTuple[0]
            maxID += 1

        scanID = maxID

        scan_info = (scanID, Date, Duration)
        cursor.execute('''INSERT INTO ScanHistory VALUES(?, ?, ?)''', scan_info)
        conn.commit()
        return cursor.lastrowid

    # Saves a scan to the database
    @staticmethod
    def save_host(host, scanID):
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

    # Builds the database
    @staticmethod
    def build_db():
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE Devices (Model TEXT PRIMARY KEY,
             Manufacturer TEXT, 
             cpeURI TEXT)''')
        cursor.execute('''CREATE TABLE CPEVulns (
            cpeURI TEXT, 
            cveName TEXT, 
            PRIMARY KEY(cpeURI, cveName))''')
        conn.commit()
        cursor.execute('''CREATE TABLE Vulnerabilities (VulnID INTEGER PRIMARY KEY, 
            cveName TEXT,
            description TEXT,
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
            exploitabilityScore TEXT)''')
        cursor.execute('''CREATE TABLE ScanHistory (ScanID INTEGER PRIMARY KEY, 
            ScanDate TEXT, 
            Duration INTEGER)''')
        cursor.execute('''CREATE TABLE Hosts (HostID INTEGER PRIMARY KEY, 
            ip TEXT, 
            macAddress TEXT, 
            osFamily TEXT, 
            osGen TEXT, name TEXT, 
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

    # Saves a new cpe\cve combo into the cpeVulns table
    @staticmethod
    def save_cpeVuln(cpe, cve):
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cpeVuln = (cpe, cve)

        cursor.execute('''INSERT INTO CPEVulns VALUES (?, ?)''', cpeVuln)
        conn.commit()

    # Imports Data from NVD JSON file
    @staticmethod
    def import_NVD_JSON():

        json_fp = Path("test1.json")
        nvd_json = json.loads(json_fp.read_text())
        cve_items_list = nvd_json['CVE_Items']

        i = 0
        for cve in cve_items_list:
            cve_detail = cve_items_list[i]
            cve_meta_data = cve_detail.get("cve").get("CVE_data_meta")

            description_data = cve_detail.get("cve").get("description").get("description_data")
            description = description_data[0].get("value")

            configurations = cve_detail['configurations']
            cpe_list = configurations['nodes']

            cvssV3 = cve_detail.get("impact").get("baseMetricV3").get("cvssV3")
            baseMetric = cve_detail.get("impact").get("baseMetricV3")

            DBFunctions.save_vulnerability(cve_meta_data['ID'], description, cvssV3['attackVector'],
                                           cvssV3['attackComplexity'],"","",cvssV3['privilegesRequired'], cvssV3['userInteraction'],
                                           cvssV3['confidentialityImpact'], cvssV3['integrityImpact'], cvssV3['availabilityImpact'],
                                           cvssV3['baseScore'], cvssV3['baseSeverity'],baseMetric['exploitabilityScore'])


            for item in cpe_list:

                cpe_match = item['cpe_match']

                for item in cpe_match:
                    try:
                        cpe_URI = item['cpe23Uri']
                    except:
                        cpe_URI = item['cpe22Uri']
                    DBFunctions.save_cpeVuln(cpe_URI, cve_meta_data['ID'])

            i += 1
            print(i)









