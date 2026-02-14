SELECT nominations.game_title as "Juego", count(*) as "# Premios"
FROM nominations
         INNER JOIN stats_nominations ON nominations.id = stats_nominations.nomination
WHERE ranking_place = 1
GROUP BY nominations.game_title
ORDER BY "Juego", "# Premios" DESC;
