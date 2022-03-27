{{ config(materialized = 'table') }}

SELECT {{ dbt_utils.surrogate_key(['artistId']) }} AS artistKey,
    *
FROM (
        SELECT 
            MAX(artist_id) AS artistId,
            MAX(artist_latitude) AS latitude,
            MAX(artist_longitude) AS longitude,
            MAX(artist_location) AS location,
            REPLACE(REPLACE(artist_name, '"', ''), '\\', '') AS name
        FROM {{ source('staging', 'songs') }}
        GROUP BY artist_name

        UNION ALL

        SELECT 'NNNNNNNNNNNNNNN',
            0,
            0,
            'NA',
            'NA'

    )