INSERT {{ BIGQUERY_DATASET }}.{{ AUTH_EVENTS_TABLE }}
SELECT
    ts,
    COALESCE(level, 'NA') AS level,
    COALESCE(city, 'NA') AS city,
    COALESCE(state, 'NA') AS state,
    COALESCE(userAgent, 'NA') AS userAgent,
    COALESCE(CAST(lon AS NUMERIC), 0.0) AS lon,
    COALESCE(CAST(lat AS NUMERIC), 0.0) AS lat,
    COALESCE(userId, 0) AS userId,
    COALESCE(lastName, 'NA') AS lastName,
    COALESCE(firstName, 'NA') AS firstName,
    COALESCE(gender, 'NA') AS gender,
    COALESCE(registration, 9999999999999) AS registration,
    COALESCE(success, FALSE)
FROM {{ BIGQUERY_DATASET }}.{{ AUTH_EVENTS_TABLE}}_{{ logical_date.strftime("%m%d%H") }} -- Creates a table name with month day and hour values appended to it
                                                                                            -- like listen_events_032313 for 23-03-2022 13:00:00