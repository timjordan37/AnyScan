import sqlite3


class DBFunctions():

    # Saves a new device to the database
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

    # Saving a Vulnerability to the database
    @staticmethod
    def save_vulnerability(Model, cpeName, cpe23URI, versionsAffected,
                           description, CVSSScore, attackVector, attackComplexity, priviledgesRequired,
                           userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                           baseScore, baseSeverity, exploitabilityScore):
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute('SELECT MAX(VulnID) FROM Vulnerabilities')
        conn.commit()
        maxIDTuple = cursor.fetchone()
        maxID = maxIDTuple[0]
        vulnID = maxID + 1

        vulnerability_info = (vulnID, Model, cpeName, cpe23URI, versionsAffected,
                              description, CVSSScore, attackVector, attackComplexity, priviledgesRequired,
                              userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                              baseScore, baseSeverity, exploitabilityScore)
        try:
            cursor.execute('''INSERT INTO Vulnerabilities VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '
                           '?, ?, ?, ?, ?,)''', vulnerability_info)
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
        if maxIDTuple is not None:
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

        cursor.execute('''CREATE TABLE Devices (Model TEXT PRIMARY KEY, Manufacturer TEXT, cpeURI TEXT)''')
        conn.commit()
        cursor.execute('''CREATE TABLE Vulnerabilities (VulnID INTEGER PRIMARY KEY, Model, cpeName TEXT, cpe22uri TEXT , 
            cpe23uri TEXT, versionsAffected TEXT, description TEXT, CVSSScore INTEGER, attackVector TEXT, attackComplexity TEXT,
            priviligesRequired TEXT, userInteraction TEXT, confidentialityImpact TEXT, integrityImpact TEXT, availabilityImpact TEXT,
            baseScore TEXT, baseSeverity TEXT, exploitabilityScore INTEGER, FOREIGN KEY(Model) REFERENCES Devices(Model))''')
        cursor.execute(
            '''CREATE TABLE ScanHistory (ScanID INTEGER PRIMARY KEY, ScanDate TEXT, Duration INTEGER)''')
        cursor.execute(
            '''CREATE TABLE Hosts (HostID INTEGER PRIMARY KEY, ip TEXT, macAddress TEXT, osFamily TEXT, osGen TEXT, name TEXT, vendor TEXT, ScanID INTEGER, FOREIGN KEY(ScanID) REFERENCES ScanHistory(ScanID))''')
        conn.commit()
        cursor.execute(
            '''CREATE TABLE Parameters (ScanID INTEGER, ParameterValue TEXT, ParameterType TEXT, PRIMARY KEY(ScanID, ParameterType))''')
        cursor.execute('''CREATE TABLE PenTestHistory (PenTestID INTEGER PRIMARY KEY, VulnID INTEGER, Model TEXT,
            ScanID INTEGER, Result TEXT, FOREIGN KEY(VulnID) REFERENCES Vulnerabilities(VulnID), FOREIGN KEY(Model) REFERENCES Devices(Model), 
            FOREIGN KEY(VulnID) REFERENCES Vulnerabilities(VulnID), FOREIGN KEY(ScanID) REFERENCES ScanHistory(ScanID))''')
        conn.commit()
