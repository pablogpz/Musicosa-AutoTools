SELECT nominations.award                        as "Premio",
       group_concat(if(nominations.nominee <> '', concat(nominations.nominee, ' | ', nominations.game_title),
                       nominations.game_title)) as "Ganador"
FROM nominations
         INNER JOIN stats_nominations ON nominations.id = stats_nominations.nomination
WHERE ranking_place = 1
GROUP BY nominations.award
ORDER BY nominations.award;