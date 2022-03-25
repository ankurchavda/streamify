{{ config(materialized = 'table') }}

SELECT {{ dbt_utils.surrogate_key(['latitude', 'longitude', 'city', 'state']) }} as locationKey,
*
FROM
    (
        SELECT 
            distinct city,
            state,
            lat as latitude,
            lon as longitude
        FROM source('staging', 'listen_events')

        UNION ALL

        SELECT 
            'NA',
            'NA',
            0.0,
            0.0
    )