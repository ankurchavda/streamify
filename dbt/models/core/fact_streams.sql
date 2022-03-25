

select users.userKey, artists.artistKey, d_songs.songKey, d_datetime.dateKey, stats.location, stats.session_id, stats.ts
 from stats
  join users on stats.user_id = users.user_id and users.current_row = 1
  join artists on stats.artist_name = artists.artist_name
  join d_songs on d_songs.artist_name = stats.artist_name and d_songs.title = stats.song
  join d_datetime on d_datetime.date = date_trunc('hour', stats.ts)