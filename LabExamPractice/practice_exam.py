# Use this file to write your queries. Submit this file to Gradescope after finishing your homework.

# Make sure to test that this script prints out the strings (your SQL queries) correctly.

# To verify your submission is in the correct format: `python3 hw1.py`

# Make sure the program prints out your SQL statements correctly. That means the autograder will read you SQL correctly. Running the Python file will not execute your SQL statements, it simply prints them.

'''
-- Patients Table
CREATE TABLE IF NOT EXISTS Patients (
    PatientID INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Age INTEGER,
    StreetAddress TEXT,
    City TEXT,
    ZipCode TEXT
);
-- Doctors Table
CREATE TABLE IF NOT EXISTS Doctors (
    DoctorID INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Age INTEGER,
    Specialty TEXT,
    StreetAddress TEXT,
    City TEXT,
    ZipCode TEXT
);

-- Appointments Table
CREATE TABLE IF NOT EXISTS Appointments (
    AppointmentID INTEGER PRIMARY KEY,
    PatientID INTEGER,
    DoctorID INTEGER,
    AppointmentDateTime TEXT NOT NULL,
    Reason TEXT,
    Diagnosis TEXT,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
);

-- Vitals Table
CREATE TABLE IF NOT EXISTS Vitals (
    RecordID INTEGER PRIMARY KEY,
    AppointmentID INTEGER,
    DateTime TEXT NOT NULL,
    BloodPressureHigh INTEGER,
    BloodPressureLow INTEGER,
    OxygenLevel INTEGER,
    Temperature REAL,
    FOREIGN KEY (AppointmentID) REFERENCES Appointments(AppointmentID)
);

-- Prescriptions Table
CREATE TABLE IF NOT EXISTS Prescriptions (
    AppointmentID INTEGER,
    DrugID INTEGER,
    Dosage TEXT,
    Duration TEXT,
    Price REAL,
    PRIMARY KEY (AppointmentID, DrugID),
    FOREIGN KEY (AppointmentID) REFERENCES Appointments(AppointmentID),
    FOREIGN KEY (DrugID) REFERENCES Drugs(ID)
);
-- Drugs Table
CREATE TABLE IF NOT EXISTS Drugs (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL
);
'''

instr = '''Instructions:
	Please put the queries under the corresponding functions below.
	Running this python file will check if the formatting is okay.
	Example:
		def query1():
			return """
				SELECT * FROM agent
			"""
'''

def query1():
	return """
SELECT
  D.FirstName || ' ' || D.LastName AS DoctorName,
  COUNT(*)                         AS total_appointments,
  COUNT(DISTINCT A.PatientID)      AS distinct_patients
FROM Doctors D
JOIN Appointments A ON A.DoctorID = D.DoctorID
GROUP BY D.DoctorID
ORDER BY total_appointments DESC, DoctorName;
	"""

def query2():
	return """
SELECT DISTINCT P.city, P.zipcode
FROM Patients P
WHERE NOT EXISTS (
    SELECT D.DoctorId
    FROM Doctors D
    WHERE D.city = P.city AND D.ZipCode = P.ZipCode
)
	"""

def query3():
	return """
SELECT
  P1.FirstName || ' ' || P1.LastName AS Patient1,
  P2.FirstName || ' ' || P2.LastName AS Patient2,
  P1.City
FROM Patients P1
JOIN Patients P2
  ON P1.City = P2.City
 AND P1.PatientID < P2.PatientID
	"""
	
def query4():
	return """
SELECT DISTINCT
    P.FirstName, P.LastName, V.Temperature
FROM Patients P JOIN Appointments A ON P.PatientID = A.PatientID
     JOIN Vitals V ON A.AppointmentID = V.AppointmentId
WHERE V.Temperature = (
    SELECT MAX(Temperature)
    FROM Vitals
);
	"""

def query5():
	return """
    SELECT
    P.FirstName || ' ' || P.LastName AS PatientName,
    D.FirstName || ' ' || D.LastName AS DoctorName,
    V.DateTime AS vital_time,
    V.Temperature,
    (
        SELECT MAX(V2.Temperature)
        FROM Appointments A2
        JOIN Vitals V2
            ON A2.AppointmentID = V2.AppointmentID
        WHERE A2.PatientID = P.PatientID
    ) AS patient_high
    FROM Patients P
    JOIN Appointments A
        ON P.PatientID = A.PatientID
    JOIN Doctors D
        ON A.DoctorID = D.DoctorID
    JOIN Vitals V
        ON A.AppointmentID = V.AppointmentID
	"""

def query6():
	return """
SELECT
  C1.Specialty AS Specialty1,
  C1.num_doctors,
  C2.Specialty AS Specialty2,
  C2.num_doctors
FROM (
  SELECT Specialty, COUNT(*) AS num_doctors
  FROM Doctors
  GROUP BY Specialty
) C1
JOIN (
  SELECT Specialty, COUNT(*) AS num_doctors
  FROM Doctors
  GROUP BY Specialty
) C2
  ON C1.num_doctors = C2.num_doctors
 AND C1.Specialty < C2.Specialty
	"""

# Do not edit below

if __name__ == "__main__":
	try:
		if all(type(eval(f'print(t:=query{f+1}()),t')[1])==str for f in range(6)):
			print(f'Your submission is valid.')
		else:
			raise TypeError('Invalid Return Types.')
	except Exception as e:
		print(f'Your submission is invalid.\n{instr}\n{e}')