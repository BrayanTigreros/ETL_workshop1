-- Select de DW
USE workshop1;

-- Hired by year
SELECT 
    dd.year AS anio,
    COUNT(*) AS contratados
FROM fact_application fa
JOIN dim_date dd ON fa.date_key = dd.date_key
WHERE fa.hired_flag = TRUE
GROUP BY dd.year
ORDER BY dd.year;


-- Hired by technology
SELECT 
    dt.technology AS cargo,
    COUNT(*) AS contratados
FROM fact_application fa
JOIN dim_technology dt ON fa.technology_key = dt.technology_key
WHERE fa.hired_flag = TRUE
GROUP BY dt.technology
ORDER BY contratados DESC;


-- Hired by Country over Years
SELECT 
    dc.country AS pais,
    COUNT(*) AS contratados
FROM fact_application fa
JOIN dim_country dc ON fa.country_key = dc.country_key
WHERE fa.hired_flag = TRUE
    AND dc.country IN ('Colombia', 'Brazil', 'United States of America', 'Ecuador')
GROUP BY dc.country
ORDER BY contratados DESC;


-- Hired by Seniority
SELECT 
    ds.seniority AS senioridad,
    COUNT(*) AS contratados
FROM fact_application fa
JOIN dim_seniority ds ON fa.seniority_key = ds.seniority_key
WHERE fa.hired_flag = TRUE
GROUP BY ds.seniority
ORDER BY contratados DESC;


-- Average code challegue score and technical enterview score by Technology
SELECT 
    dt.technology AS tecnologia,
    ROUND(AVG(fa.code_challenge_score), 2) AS avg_code_score,
    ROUND(AVG(fa.technical_interview_score), 2) AS avg_interview_score
FROM fact_application fa
JOIN dim_technology dt ON fa.technology_key = dt.technology_key
GROUP BY dt.technology
ORDER BY avg_code_score DESC
LIMIT 10;

-- Average by Age range
SELECT 
    CASE 
        WHEN fa.yoe <= 5  THEN '0-5 años'
        WHEN fa.yoe <= 10 THEN '6-10 años'
        WHEN fa.yoe <= 15 THEN '11-15 años'
        WHEN fa.yoe <= 20 THEN '16-20 años'
        WHEN fa.yoe <= 25 THEN '21-25 años'
        ELSE '26-30 años'
    END AS rango_experiencia,
    COUNT(*) AS contratados
FROM fact_application fa
WHERE fa.hired_flag = TRUE
GROUP BY rango_experiencia
ORDER BY rango_experiencia;