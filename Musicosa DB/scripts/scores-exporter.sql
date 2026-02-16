SELECT awards.designation                   as "Premio",
       if(nominations.nominee <> '', concat(nominations.nominee, ' | ', nominations.game_title),
          nominations.game_title)           as "Nominado",
       sq1.score                            as "Casterlordio",
       sq2.score                            as "Anita La Ramita",
       sq3.score                            as "Pablo",
       avg(member_grades_nominations.score) as "Nota media",
       stats_nominations.ranking_place      as "Ranking"
FROM nominations
         INNER JOIN member_grades_nominations ON nominations.id = member_grades_nominations.nomination
         INNER JOIN members ON member_grades_nominations.member = members.id
         INNER JOIN stats_nominations ON nominations.id = stats_nominations.nomination
         INNER JOIN awards on nominations.award = awards.slug
         INNER JOIN (SELECT nomination, score
                     FROM member_grades_nominations
                              INNER JOIN members ON member_grades_nominations.member = members.id
                     WHERE name = 'Cáster') sq1 ON nominations.id = sq1.nomination
         INNER JOIN (SELECT nomination, score
                     FROM member_grades_nominations
                              INNER JOIN members ON member_grades_nominations.member = members.id
                     WHERE name = 'Ana') sq2 on nominations.id = sq2.nomination
         INNER JOIN (SELECT nomination, score
                     FROM member_grades_nominations
                              INNER JOIN members ON member_grades_nominations.member = members.id
                     WHERE name = 'Pablo') sq3 ON nominations.id = sq3.nomination
GROUP BY nominations.id;