

-- Stored Prcoedure Code
DELIMITER //
CREATE PROCEDURE prepWindowPrices (
	IN startDate DATE, IN endDate Date, IN duration integer)
    BEGIN
        DELETE FROM cheapestPrices;
        INSERT INTO cheapestPrices (place_id, startDate, endDate, total)
        SELECT s.place_id, s.win_start AS startDate, DATE_ADD(s.win_start, INTERVAL (duration - 1) DAY) AS endDate, SUM(pa.price) AS total
        FROM (
            SELECT DISTINCT place_id, ava_date AS win_start
            FROM placeAvailability
            WHERE ava_date BETWEEN startDate AND DATE_SUB(endDate, INTERVAL (duration - 1) DAY)
        ) AS s
        JOIN placeAvailability AS pa
        ON pa.place_id = s.place_id
        AND pa.ava_date BETWEEN s.win_start AND DATE_ADD(s.win_start, INTERVAL (duration - 1) DAY)
        GROUP BY s.place_id, s.win_start
        HAVING COUNT(*) = duration AND MIN(pa.available) = 1;

        DELETE FROM cheapestPrices
        WHERE total <> (
            SELECT MIN(t.total)
            FROM (SELECT total FROM cheapestPrices) AS t
        );
    END //
DELIMITER ; 

-- Calling code, remove the double dashes in the beginning when calling the stored procedure
-- set @startDate = '2022-02-20';
-- set @endDate  = '2022-02-24';
-- set @duration = 2;
 
-- call prepWindowPrices(@startDate, @endDate, @duration);
