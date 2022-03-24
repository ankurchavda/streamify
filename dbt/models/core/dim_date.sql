{{ config(materialized = 'table') }}

WITH date_series AS
(
SELECT
  *
FROM
  UNNEST(GENERATE_TIMESTAMP_ARRAY('2018-10-01', '2023-01-01', INTERVAL 1 HOUR)) AS date
)
SELECT
    UNIX_SECONDS(date) AS dateKey,
    date,
    EXTRACT( DAYOFWEEK FROM date) AS dayOfWeek,
    EXTRACT( DAY FROM date) AS dayOfMonth,
    EXTRACT( WEEK FROM date) AS weekOfYear,
    EXTRACT( MONTH FROM date) AS month,
    EXTRACT( YEAR FROM date) AS year,
    CASE WHEN EXTRACT( DAYOFWEEK FROM date) IN (6,7) THEN True ELSE False END AS weekendFlag
FROM date_series