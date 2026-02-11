# Use this file to write your queries. Submit this file to Gradescope after finishing your homework.

# To verify your submission is in the correct format: `python3 hw1.py`

# Make sure the program prints out your SQL statements correctly. That means the autograder will read you SQL correctly. 

# Running the Python file will not execute your SQL statements, it simply prints them. You can test your SQL statements in your own SQL environment.

# Please only edit the parts that say `Your code here` and do not edit anything else. 

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
		SELECT raceId, year, round, circuitId, name, date, url
		FROM races
		WHERE date LIKE '1950%';
	"""

def query2():
	return """
		SELECT R.year, R.round, R.circuitId, R.name, R.date, C.location, C.country
		FROM races R, circuits C
		WHERE R.circuitId = C.circuitId AND date LIKE '1950-%';
	"""

def query3():
	return """
		SELECT R.raceId, Ra.name, R.position, D.driverId, D.forename, D.surname, C.constructorId, C.name
		FROM results R, races Ra, drivers D, constructors C
		WHERE R.raceId = '42' AND Ra.raceId = R.raceId AND R.driverId = D.driverId AND R.constructorId = C.constructorId
		ORDER BY position;
	"""
	
def query4():
	return """
		SELECT R.raceId, R.name, D.forename, D.surname, Ds.position, Ds.points, Ds.wins
		FROM races R, drivers D, driver_standings Ds
		WHERE R.raceId = 988 AND R.raceId = Ds.raceId AND Ds.driverId = D.driverId
		ORDER BY position;
	"""
#

def query5():
	return """
		SELECT DISTINCT R.raceId, R.name, Re.position, D.forename, D.surname, C.name as constructor, Re.laps, Re.milliseconds, Re.statusId, S.status
		FROM results Re JOIN races R ON Re.raceId = R.raceId
				JOIN drivers D ON Re.driverId = D.driverId
				JOIN constructors C ON Re.constructorId = C.constructorId
				JOIN driver_standings Ds ON D.driverId = Ds.driverId
				JOIN status S ON Re.statusId = S.statusId
		WHERE R.raceId = '988';
	"""

def query6():
	return """
		SELECT DISTINCT R.raceId, R.name, C.constructorId, C.name as constructor, Cs.position, Cs.points, Cs.wins
		FROM races R JOIN constructor_standings Cs ON R.raceId = Cs.raceId
		    JOIN constructors C ON C.constructorId = Cs.constructorId
		WHERE R.raceId = '988'
		ORDER BY Cs.position;
	"""

def query7():
	return """
		SELECT DISTINCT D.forename, D.surname, C.name as constructor, C.nationality
		FROM results Re JOIN drivers D ON Re.driverId = D.driverId
		    JOIN constructors C ON Re.constructorId = C.constructorId
		WHERE Re.points >= 9 AND D.nationality = C.nationality;
	"""

def query8():
	return """
		SELECT DISTINCT D.nationality
		FROM drivers D
			  LEFT JOIN constructors C ON D.nationality = C.nationality
		WHERE C.nationality IS NULL;
	"""

def query9():
	return """
		SELECT C.name AS constructor, SUM(Rs.points) AS sum_points
		FROM results Rs JOIN constructors C ON Rs.constructorId = C.constructorId
		GROUP BY C.name
		HAVING SUM(Rs.points) >= 100
		ORDER BY sum_points DESC;
	"""

def query10():
	return """
		SELECT C.name AS constructor, R.year, SUM(Rs.points) AS sum_points
		FROM results Rs JOIN constructors C ON Rs.constructorId = C.constructorId
				JOIN races R ON Rs.raceId = R.raceId
		GROUP BY C.name, R.year
		HAVING SUM(Rs.points) >= 100
		ORDER BY sum_points DESC;
	"""

def query11():
	return """
		SELECT C.name AS constructor, R.year, SUM(Rs.points) AS sum_points
		FROM results Rs JOIN constructors C ON Rs.constructorId = C.constructorId
					JOIN races R ON Rs.raceId = R.raceId
		GROUP BY C.name, R.year
		HAVING SUM(Rs.points) > 0 AND C.name = 'Ferrari'
		ORDER BY R.year DESC;
	"""

def query12():
	return """
		SELECT D1.forename, D1.surname, D2.forename, D2.surname, D1.nationality
		FROM drivers D1, drivers D2
		WHERE D1.nationality = D2.nationality AND D1.surname = D2.surname AND D1.driverId < D2.driverId;
	"""

def query13():
	return """
		SELECT DISTINCT D1.forename, D1.surname, D1.nationality
		FROM drivers D1 JOIN drivers D2 ON D1.surname = D2.surname 
						                				AND D1.nationality = D2.nationality 
										                AND D1.driverId <> D2.driverId
		ORDER BY D1.nationality, D1.surname, D1.forename;
	"""

def query14():
	return """
		SELECT Ra.raceId, Ra.year, Ra.name, Ra.date, COUNT(DISTINCT R.driverId) as cnt
		FROM races Ra LEFT JOIN results R ON Ra.raceId = R.raceId
		GROUP BY Ra.raceId
		HAVING COUNT(DISTINCT R.driverId) <= 15
		ORDER BY cnt;
	"""

def query15():
	return """
    SELECT D.driverId, D.forename, D.surname, D.dob, D.nationality
    FROM drivers D
    WHERE D.driverId IN (
        SELECT R.driverId
        FROM results R JOIN status S ON R.statusId = S.statusId
        WHERE S.status = 'Water pipe'
    ) AND D.driverId IN (
        SELECT R.driverId
        FROM results R JOIN status S ON R.statusId = S.statusId
        WHERE S.status = 'Fuel leak'
    );
	"""

# Do not edit below

if __name__ == "__main__":
	try:
		if all(type(eval(f'print(t:=query{f+1}()),t')[1])==str for f in range(15)):
			print(f'Your submission is valid.')
		else:
			raise TypeError('Invalid Return Types.')
	except Exception as e:
		print(f'Your submission is invalid.\n{instr}\n{e}')
