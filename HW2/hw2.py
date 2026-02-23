import sys

# Use this file to write your queries. Submit this file in Gradescope after finishing your assignment.

# TODO: Write your username (The prefix of your Purdue email) and answer to each query as a string in the return statements in the functions below.
# Do not change the function names.

# Your resulting tables should have the attributes in the same order as appeared in the sample answers.
# Don't forget the semicolon at the end of your query!


def username():
    return "YourUsername"


def query1():
    return r"""
        SELECT circuitId, circuitRef, name, location, country, MIN(lat) as lat, lng, alt, url
        FROM circuits;
"""


def query2():
    return r"""
        SELECT c.name, c.location, c.country, COUNT(r.raceId) as count_races
        FROM races r JOIN circuits c ON r.circuitId = c.circuitId
        GROUP BY r.circuitId
        HAVING COUNT(r.raceId) = (
                SELECT MAX (count)
                FROM (
                        SELECT COUNT(r2.raceId) AS count
                        FROM races r2
                        GROUP BY r2.circuitId
                ) as temp
    );
"""


def query3():
    return r"""
        SELECT r.raceId, r.year, r.name, r.date
        FROM races r
        WHERE r.circuitId in (
            SELECT circuitId
            FROM races
            GROUP BY circuitId
            HAVING count(raceId) in (
                SELECT MAX(count)
                FROM (
                    SELECT COUNT(r2.raceId) AS count
                    FROM races r2
                    GROUP BY r2.circuitId
                ) as temp
            )
        )
        ORDER BY r.year;
"""


def query4():
    return r"""
        SELECT R.raceId, R.name, D.forename, D.surname, Ds.position, Ds.points, Ds.wins,
            (
            SELECT COUNT(driverId)
            FROM results Re
            JOIN races R2 ON Re.raceId = R2.raceId
            WHERE Re.driverId = Ds.driverId
                AND Re.position = 2
                AND R2.year = R.year
            ) AS second_place
        FROM driver_standings Ds JOIN drivers D ON D.driverId = Ds.driverId
            JOIN races R ON Ds.raceId = R.raceId
        WHERE R.raceId = 988
        ORDER BY Ds.position
"""


def query5():
    return r"""
        SELECT C.name AS constructor, SUM(Rs.points) AS sum_points,
            (
                SELECT AVG(total_points)
                FROM (
                    SELECT SUM(Rs2.points) AS total_points, Rs2.constructorId
                    FROM results Rs2
                    GROUP BY Rs2.constructorId
                ) AS totals
            ) AS average_total_points
        FROM results Rs JOIN constructors C ON Rs.constructorId = C.constructorId
        GROUP BY C.name
        HAVING SUM(Rs.points) >= 100
        ORDER BY sum_points DESC;
"""


def query6():
    return r"""
        SELECT C.name AS constructor, SUM(Rs.points) AS sum_points

        FROM results Rs JOIN constructors C ON Rs.constructorId = C.constructorId
        GROUP BY C.name
        HAVING SUM(Rs.points) >= (
                SELECT AVG(total_points)
                FROM (
                    SELECT SUM(Rs2.points) AS total_points, Rs2.constructorId
                    FROM results Rs2
                    GROUP BY Rs2.constructorId
                ) AS totals
            )
        ORDER BY sum_points DESC;
"""


def query7():
    return r"""
        SELECT AVG(ABS(Cs1_points - Cs2_points)) AS avg_gap
        FROM (
            SELECT Cs1.points AS Cs1_points, Cs2.points AS Cs2_points, Cs1.position, Cs2.position
            FROM constructor_standings Cs1 JOIN constructor_standings Cs2 ON Cs1.raceId = Cs2.raceId
            JOIN races R ON Cs1.raceId = R.raceId
            WHERE R.year = 2017 AND Cs1.position = 2 AND Cs2.position = 1
);
"""


def query8():
    return r"""
        SELECT Co.name as constructor_name
        FROM constructors Co
        WHERE Co.constructorId NOT IN (
                SELECT C2.constructorId
                FROM constructor_results C2
                JOIN races R2 ON C2.raceId = R2.raceId
                WHERE R2.year = 2004
                AND C2.points = 0
        ) AND Co.constructorId IN (
                SELECT C2.constructorId
                FROM constructor_results C2
                JOIN races R2 ON C2.raceId = R2.raceId
                WHERE R2.year = 2004
        )
"""


def query9():
    return r"""
        SELECT D.forename,D.surname
        FROM drivers D
        WHERE (
            SELECT COUNT(*)
            FROM driver_standings DS
            JOIN races R ON DS.raceId = R.raceId
            WHERE R.year = 2009
            AND DS.driverId = D.driverId
            AND (DS.position = 1 OR DS.position = 2 OR DS.position = 3)
        ) * 1.0 /
        (
            SELECT COUNT(*)
            FROM driver_standings DS2
            JOIN races R2 ON DS2.raceId = R2.raceId
            WHERE R2.year = 2009
            AND DS2.driverId = D.driverId
        )
        >= 0.9;
"""


def query10():
    return r"""
        SELECT DISTINCT R.raceId, R.name, Re.position, D.forename, D.surname, C.name as constructor, Re.laps, Re.milliseconds, Re.statusId, S.status
        FROM results Re JOIN races R ON Re.raceId = R.raceId
        JOIN drivers D ON Re.driverId = D.driverId
        JOIN constructors C ON Re.constructorId = C.constructorId
        JOIN driver_standings Ds ON D.driverId = Ds.driverId
        JOIN status S ON Re.statusId = S.statusId
        WHERE R.raceId = '988' AND Re.position IN (
            SELECT MIN(Res.position)
            FROM results Res
            WHERE Res.raceId = Re.raceId AND Res.constructorId = Re.constructorId
        );
"""


def query11():
    return r"""
        SELECT DISTINCT R.raceId, R.name, R.year, Re.position, Re.grid, D.forename, D.surname, C.name
        FROM results Re JOIN races R ON Re.raceId = R.raceId
        JOIN drivers D ON Re.driverId = D.driverId
        JOIN constructors C ON Re.constructorId = C.constructorId
        WHERE Re.position BETWEEN 1 AND 10 AND Re.raceId IN (
            SELECT raceId
            FROM (
                SELECT Re2.raceId, SUM(ABS(Re2.grid - Re2.position)) AS total_grid_diff
                FROM results Re2
                WHERE Re2.position BETWEEN 1 AND 10
                GROUP BY Re2.raceId
                HAVING COUNT(Re2.position) = 10
            ) AS race_totals

            WHERE total_grid_diff = (
                SELECT MAX(total_grid_diff)
                FROM (
                    SELECT SUM(ABS(Re3.grid - Re3.position)) AS total_grid_diff
                    FROM results Re3
                    WHERE Re3.position BETWEEN 1 AND 10
                    GROUP BY Re3.raceId
                    HAVING COUNT(Re3.position) = 10
                ) AS totals2
            )
        )
        ORDER BY R.raceId, Re.position;
"""


def query12():
    return r""" 
        SELECT R.year, Ds.position, D.forename, D.surname, DS.points, DS.wins
        FROM driver_standings Ds
        JOIN drivers D ON Ds.driverId = D.driverId
        JOIN races R ON Ds.raceId = R.raceId
        WHERE R.year BETWEEN 2010 AND 2017 AND Ds.position BETWEEN 1 AND 3 AND Ds.raceId = (
        SELECT R2.raceId
        FROM races R2
        WHERE R2.year = R.year AND R2.round = (
                SELECT MAX(round)
                FROM races R3
                WHERE R3.year = R.year
            )
        )
        ORDER BY R.year, DS.position;
"""


def query13():
    return r"""
        SELECT D.forename, D.surname, L1.lap as lap, L1.position as position, L2.lap as lap, L2.position as position
        FROM laptimes L1 JOIN laptimes L2 ON L1.raceId = L2.raceId AND L1.driverId = L2.driverId AND L2.lap = L1.lap + 1
        JOIN drivers D ON L1.driverId = D.driverId
        WHERE L1.raceId = 987 AND L1.lap = (
            SELECT L_inner.lap
            FROM laptimes L_inner JOIN laptimes L_next ON L_inner.raceId = L_next.raceId AND L_inner.driverId = L_next.driverId AND L_next.lap = L_inner.lap + 1
            WHERE L_inner.raceId = 987
            GROUP BY L_inner.lap
            HAVING SUM(ABS(L_next.position - L_inner.position)) = (
                    SELECT MAX(total_change)
                    FROM (
                            SELECT SUM(ABS(L_b.position - L_a.position)) AS total_change
                            FROM laptimes L_a JOIN laptimes L_b ON L_a.raceId = L_b.raceId AND L_a.driverId = L_b.driverId AND L_b.lap = L_a.lap + 1
                            WHERE L_a.raceId = 987
                            GROUP BY L_a.lap
                        )
            )
        )
        ORDER BY L1.position;
"""


def query14():
    return r"""
SELECT F.constructor as constructor, F.race as race, F.finished as Finished, N.constructor as constructor, N.race as race, N.not_finished as Not_Finished
FROM
    (SELECT C.name as constructor, R.name as race, COUNT(*) as finished
     FROM results Re JOIN drivers D ON Re.driverId = D.driverId
          JOIN constructors C ON Re.constructorId = C.constructorId
          JOIN races R ON Re.raceId = R.raceId
     WHERE D.forename = 'Ayrton'
           AND D.surname = 'Senna'
           AND Re.statusId = 1
     GROUP BY C.name, R.name) as F
FULL OUTER JOIN
    (SELECT C.name as constructor, R.name as race, COUNT(*) as not_finished
     FROM results Re JOIN drivers D ON Re.driverId = D.driverId
          JOIN constructors C ON Re.constructorId = C.constructorId
          JOIN races R ON Re.raceId = R.raceId
     WHERE D.forename = 'Ayrton'
           AND D.surname = 'Senna'
           AND Re.statusId <> 1
     GROUP BY C.name, R.name) as N
ON F.constructor = N.constructor AND F.race = N.race;
"""


def query15():
    return r"""  
WITH ranked AS (
    SELECT r.circuitId, s.status, COUNT(*) AS cnt, ROW_NUMBER() OVER (PARTITION BY r.circuitId ORDER BY COUNT(*) DESC) AS rn
    FROM results res JOIN races r ON r.raceId = res.raceId JOIN status s ON s.statusId = res.statusId
    WHERE r.circuitId IN (13, 6, 9, 14) AND res.statusId <> 1 AND s.status NOT LIKE '%Lap%'
    GROUP BY r.circuitId, s.status
),
top_statuses AS (
    SELECT status
    FROM ranked
    WHERE rn <= 10
    GROUP BY status
),
pivoted AS (
    SELECT ts.status, MAX(CASE WHEN r.circuitId = 13 AND r.rn <= 10 THEN r.cnt END) AS Spa, MAX(CASE WHEN r.circuitId = 6  AND r.rn <= 10 THEN r.cnt END) AS Monaco,
           MAX(CASE WHEN r.circuitId = 9  AND r.rn <= 10 THEN r.cnt END) AS Silverstone, MAX(CASE WHEN r.circuitId = 14 AND r.rn <= 10 THEN r.cnt END) AS Monza
    FROM top_statuses ts LEFT JOIN ranked r ON r.status = ts.status
    GROUP BY ts.status
)
SELECT CASE WHEN Spa IS NOT NULL THEN status END AS status, Spa,
       CASE WHEN Monaco IS NOT NULL THEN status END AS status, Monaco,
       CASE WHEN Silverstone IS NOT NULL THEN status END AS status, Silverstone,
       CASE WHEN Monza IS NOT NULL THEN status END AS status, Monza
FROM pivoted
ORDER BY Spa, Monaco, Silverstone, Monza DESC;
"""

# Do not edit below


queries = [
    query1(),
    query2(),
    query3(),
    query4(),
    query5(),
    query6(),
    query7(),
    query8(),
    query9(),
    query10(),
    query11(),
    query12(),
    query13(),
    query14(),
    query15()
]
queries = [q.strip() for q in queries]

if __name__ == "__main__":
    breaker = "=" * 24
    print(f"Your username is {username()}!")
    print(breaker)
    for i, query in enumerate(queries):
        print(f"Your answer for query\
{i + 1} is:\n{breaker}\n{query}\n{breaker}")
