import sqlite3

conn = sqlite3.connect('vulnDB.db')

cursor = conn.cursor()
try:
    cursor.execute('''CREATE TABLE Devices (Model TEXT PRIMARY KEY, Manufacturer TEXT, cpeURI TEXT)''')
    conn.commit()
    cursor.execute('''CREATE TABLE Vulnerabilities (VulnID INTEGER PRIMARY KEY, cpeName TEXT, cpe22uri TEXT , 
    cpe23uri TEXT, versionsAffected TEXT, description TEXT, CVSSScore INTEGER, attackVector TEXT, attackComplexity TEXT, FOREIGN KEY(Model) REFERENCES Devices(Model)),
    priviligesRequired TEXT, userInteraction TEXT, confidentialityImpact TEXT, integrityImpact TEXT, availabilityImpact TEXT,
    baseScore TEXT, baseSeverity TEXT, exploitabilityScore INTEGER''')
    cursor.execute('''CREATE TABLE ScanHistory (ScanID INTEGER PRIMARY KEY, Model TEXT, ScanDate TEXT, Duration INTEGER)''')
    conn.commit()
    cursor.execute('''CREATE TABLE Parameters (ScanID INTEGER, ParameterValue TEXT, ParameterType TEXT, PRIMARY KEY(ScanID, Parameter))''')
    cursor.execute('''CREATE TABLE PenTestHistory (PenTestID INTEGER PRIMARY KEY, VulnID INTEGER, Model TEXT,
    ScanID INTEGER, Result TEXT, FOREIGN KEY(VulnID) REFERENCES Vulnerabilities(VulnID), FOREIGN KEY(Model) REFERENCES Devices(Model), 
    FOREIGN KEY(VulnID) REFERENCES Vulnerabilities(VulnID), FOREIGN KEY(ScanID) REFERENCES ScanHistory(ScanID))''')
    conn.commit()
except sqlite3.OperationalError:
    pass

