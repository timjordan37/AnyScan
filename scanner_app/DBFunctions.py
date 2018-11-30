import sqlite3
import json

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
    def save_vulnerability(cveName, description, CVSSScore, attackVector, attackComplexity, customScore,
                           customScoreReason, priviledgesRequired,
                           userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                           baseScore, baseSeverity, exploitabilityScore):
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute('SELECT MAX(VulnID) FROM Vulnerabilities')
        conn.commit()
        maxIDTuple = cursor.fetchone()
        maxID = maxIDTuple[0]
        vulnID = maxID + 1

        vulnerability_info = (vulnID, cveName, description, CVSSScore, attackVector, attackComplexity, customScore,
                           customScoreReason, priviledgesRequired,
                           userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                           baseScore, baseSeverity, exploitabilityScore)
        try:
            cursor.execute('''INSERT INTO Vulnerabilities VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                           ?, ?, ?)''', vulnerability_info)
            conn.commit()
        except sqlite3.IntegrityError:
            return "That device already exists in the database."

    # Saves a scan to the database
    @staticmethod
    def save_scan(Date, Duration):
        """Save a scan to the Db

        :param Duration: time scan took to complete
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
        conn.commit()
        cursor.execute('''CREATE TABLE Vulnerabilities (VulnID INTEGER PRIMARY KEY, 
            cveName TEXT,
            description TEXT, 
            CVSSScore INTEGER, 
            attackVector TEXT, 
            attackComplexity TEXT, 
            customScore TEXT, 
            customScoreReason TEXT
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

    @staticmethod
    def save_host(host, scanID):
        """Saves a scan to the database

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

    def query_cves(cpeDict):
        """query DB for CVEs according to CPEs found by scanner
        :param cpeDict: cpe dictionary in the form {host0 : [cpe, list0], host1: [cpe, list1]
        """
        conn = sqlite3.connect('vulnDB.db')
        cves = []
        cursor = conn.cursor()
        print("Query HERE")

        # static example for below loop
        cursor.execute("""SELECT * FROM CPEVulns WHERE cpeURI IS (?)""", ("cpe:2.3:o:juniper:junos:12.1x46:d10:*:*:*:*:*:*",))
        str = cursor.fetchone()
        print(str[1])

        for hList in cpeDict:
            for cpe in cpeDict[hList]:
                print("CPE: ")
                print(cpe)
                cursor.execute("""SELECT * FROM CPEVulns WHERE cpeURI IS (?)""", (cpe,))
                testStr = cursor.fetchone()
                if testStr:
                    print("FOUND")
                    # todo import database to test loops and results from call in Main
                    print("CVE: ")
                    print(testStr[1])
                    cves.append(testStr[1])
                else:
                    print("NOT FOUND")

        # return all the fun stuff
        return cves

    # Imports Data from NVD JSON file
    @staticmethod
    def import_NVD_JSON():
        print("Still to implement")






