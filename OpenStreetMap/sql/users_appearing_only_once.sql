SELECT COUNT(*)
FROM
    (SELECT a.user, COUNT(*) as num
     FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) a
     GROUP BY a.user
     HAVING num=1)  b