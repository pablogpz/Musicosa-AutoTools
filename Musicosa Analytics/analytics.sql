-- MUSICOSA RANKING
SELECT stats_entries.ranking_place as '#',
       entries.title               as 'Entry',
       contestants.name            as 'Author',
       stats_entries.avg_score        'Avg. score'
FROM entries
         JOIN stats_entries ON entries.id = stats_entries.entry
         JOIN contestants ON entries.author = contestants.id
ORDER BY stats_entries.ranking_sequence DESC;
-- MUSICOSA RANKING (w/o author's grade)
SELECT row_number() OVER (ORDER BY avg(cge.score) DESC) AS "#", e.title, avg(cge.score) AS data
FROM entries e
         JOIN contestants a ON e.author = a.id
         JOIN contestant_grades_entries cge ON e.id = cge.entry
WHERE e.author <> cge.contestant
GROUP BY e.author, e.id
ORDER BY data;

-- 'ESTRELLIS' RANKING
SELECT entries.title, sum(cge.estrelli) AS estrelli_count
FROM entries
         JOIN contestant_grades_entries as cge on entries.id = cge.entry
GROUP BY entries.id
HAVING estrelli_count > 0
ORDER BY estrelli_count DESC;

-- Check for ties
SELECT stats_entries.ranking_place as '#', count(ranking_place) AS '# of Entries'
FROM stats_entries
GROUP BY ranking_place
HAVING count(ranking_place) > 1
ORDER BY ranking_place DESC;

-- **STATISTICS**

-- A) Contestant's average given scores
SELECT c.name, avg(cge.score) AS data
FROM contestants c
         JOIN contestant_grades_entries cge ON c.id = cge.contestant
GROUP BY c.id
ORDER BY data DESC;

-- B) Contestant's average received scores
SELECT c.name, sc.avg_received_score
FROM contestants c
         JOIN stats_contestants sc ON c.id = sc.contestant
ORDER BY sc.avg_received_score DESC;

-- C) Contestant's average scores given to themselves
SELECT a.name, avg(cge.score) AS data
FROM entries e
         JOIN contestants a ON e.author = a.id
         JOIN contestant_grades_entries cge ON e.id = cge.entry
WHERE e.author = cge.contestant
GROUP BY e.author
ORDER BY data DESC;
-- C.1) C) - A) (Autofelación [Cáster's ver.])
SELECT a.name, avg(cge.score) - sc.avg_given_score AS data
FROM entries e
         JOIN contestants a ON e.author = a.id
         JOIN contestant_grades_entries cge ON e.id = cge.entry
         JOIN stats_contestants sc on a.id = sc.contestant
WHERE e.author = cge.contestant
GROUP BY e.author
ORDER BY data DESC;

-- D) Enemies and Lovers
SELECT c.name AS contestant, a.name AS "gives scores to", avg(cge.score) AS data
FROM entries e
         JOIN contestants a ON e.author = a.id
         JOIN contestant_grades_entries cge ON e.id = cge.entry
         JOIN contestants c ON cge.contestant = c.id
WHERE e.author <> cge.contestant
GROUP BY e.author, cge.contestant
ORDER BY cge.contestant, data DESC;

-- E) Contestant's number of LEADING / TRAILING places in templates
-- TRAILING places
SELECT c.name, count(c.name) AS data
FROM (SELECT e.id as entryID, max(cge.score) AS maxScore, min(cge.score) AS minScore
      FROM entries e
               JOIN contestant_grades_entries cge ON e.id = cge.entry
      WHERE e.author <> cge.contestant
      GROUP BY e.id) sq
         JOIN entries e ON sq.entryID = e.id
         JOIN contestant_grades_entries cge ON e.id = cge.entry
         JOIN contestants c ON cge.contestant = c.id
WHERE cge.score = sq.minScore
  AND cge.contestant <> e.author
GROUP BY cge.contestant
ORDER BY data DESC;
-- LEADING places
SELECT c.name, count(c.name) AS data
FROM (SELECT e.id as entryID, max(cge.score) AS maxScore, min(cge.score) AS minScore
      FROM entries e
               JOIN contestant_grades_entries cge ON e.id = cge.entry
      WHERE e.author <> cge.contestant
      GROUP BY e.id) sq
         JOIN entries e ON sq.entryID = e.id
         JOIN contestant_grades_entries cge ON e.id = cge.entry
         JOIN contestants c ON cge.contestant = c.id
WHERE cge.score = sq.maxScore
  AND cge.contestant <> e.author
GROUP BY cge.contestant
ORDER BY data DESC;

-- F) Who does represent the group's taste the best
SELECT sq.contestant,
       (sq.data / (SELECT min(sq.data)
                   FROM (SELECT sum(abs(cge.score - se.avg_score)) AS data
                         FROM entries e
                                  JOIN stats_entries se ON e.id = se.entry
                                  JOIN contestant_grades_entries cge ON e.id = cge.entry
                                  JOIN contestants c ON cge.contestant = c.id
                         GROUP BY cge.contestant
                         ORDER BY data) sq) - 1) * 100 AS data
FROM (SELECT c.name AS contestant, sum(abs(cge.score - se.avg_score)) AS data
      FROM entries e
               JOIN stats_entries se ON e.id = se.entry
               JOIN contestant_grades_entries cge ON e.id = cge.entry
               JOIN contestants c ON cge.contestant = c.id
      GROUP BY cge.contestant
      ORDER BY data) sq;