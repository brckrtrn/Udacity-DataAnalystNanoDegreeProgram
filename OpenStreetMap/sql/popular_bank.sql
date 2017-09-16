SELECT nodes_tags.value, COUNT(*) as num
        FROM nodes_tags
            JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value like '%Bank%') i
            ON nodes_tags.id=i.id
        WHERE nodes_tags.key='name'
        GROUP BY nodes_tags.value
        ORDER BY num DESC
        LIMIT 10;