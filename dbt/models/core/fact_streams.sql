{{ config(materialized = 'table') }}

SELECT 
    dim_users.userKey AS userKey,
    dim_artists.artistKey AS artistKey,
    dim_songs.songKey AS songKey ,
    dim_datetime.dateKey AS dateKey,
    dim_location.locationKey AS locationKey,
    listen_events.ts AS ts
 FROM {{ source('staging', 'listen_events') }}
  JOIN {{ ref('dim_users') }} 
    ON listen_events.userID = dim_users.userID AND dim_users.currentRow = 1
  JOIN {{ ref('dim_artists') }} 
    ON listen_events.artist = dim_artists.name
  JOIN {{ ref('dim_songs') }} 
    ON listen_events.artist = dim_songs.artistName AND listen_events.song = dim_songs.title
  JOIN {{ ref('dim_location') }} 
    ON listen_events.city = dim_location.city AND listen_events.state = dim_location.state AND listen_events.lat = dim_location.latitude AND listen_events.lon = dim_location.longitude 
  JOIN {{ ref('dim_datetime') }} 
    ON dim_datetime.date = date_trunc(listen_events.ts, HOUR)