import discord
from discord.ext import commands
from discord import app_commands
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import librosa
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

MY_GUILD = discord.Object(id=1176471349896683550)

SPOTIPY_CLIENT_ID = 'ID_HERE'
SPOTIPY_CLIENT_SECRET = 'TOKEN_HERE'

# Set up Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

class MyClient(discord.Client):
  def __init__(self, *, intents: discord.Intents):
    super().__init__(intents=intents)
    # A CommandTree is a special type that holds all the application command
    # state required to make it work. This is a separate class because it
    # allows all the extra state to be opt-in.
    # Whenever you want to work with application commands, your tree is used
    # to store and work with them.
    # Note: When using commands.Bot instead of discord.Client, the bot will
    # maintain its own tree instead.
    self.tree = app_commands.CommandTree(self)

  async def setup_hook(self):
    # This copies the global commands over to your guild.
    self.tree.copy_global_to(guild=MY_GUILD)
    await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)

all_songs_to_compare = ['2YmfV4lAjrAQvuggKCUX6m', '1OG1NoKpZZLrMqMYCk9m84', '5XWlyfo0kZ8LF7VSyfS4Ew', '74X2u8JMVooG2QbjRxXwR8', '68gQG2HpRMxIRom4pCugMq', '2KslE17cAJNHTsI2MI0jb2', '4jMwQaDiDICry8Ia1gFnAn', '6ehWdR7cGDXnT7aKEASJxE', '7AGq5qaaF9awHDaKuCvVjj', '618OKP1lBkNJL8uZdNSvQE', '7uyeEbG6hyApgXuEypGcsZ', '2qiWQf7ka0C4XoA7JAZ1q5', '4MTNimMDRyFZv37Thcktwa', '3F2BLyGt6zYLrHYpbdTw5L', '1qosh64U6CR5ki1g1Rf2dZ', '2cEwQnP4284g37N6D7ETND', '7mpdNiaQvygj2rHoxkzMfa', '6gcuJpHu0Ey30D5WR76y98', '4uOBL4DDWWVx4RhYKlPbPC', '3AOf6YEpxQ894FmrwI9k96', '3syxwxJqX5jpgjNYmvzdW6', '70t7Q6AYG6ZgTYmJWcnkUM', '0ZPjVmof45INEERgYfadtv', '4yorFTfi9Tay8tG0NNK7vB', '51vRumtqbkNW9wrKfESwfu', '4fsQ0K37TOXa3hEQfjEic1', '7jzOZuWgZ5gaMet9V5Ix1d', '65FftemJ1DbbZ45DUfHJXE', '1qRfAvzRIJQodWKBNFAb6C', '0pHylQR53epYtRcVIhUSCh', '1ULdASrNy5rurl1TZfFaMP', '5EtiQveQFQy0R05hLVDyKv', '5sdQOyqq2IDhvmx2lHOpwd', '3G7MgLuWLzUJQflWOCDZit', '0rKWJnmo6Q0ovoPOLoLm0t', '3gTQwwDNJ42CCLo3Sf4JDd', '6zZWoHlF2zNSLUNLvx4GUl', '4H65EdACzwqV8sTt3dDyA0', '2nWVowkuFVY6hCRBylnaZh', '4Cyf87ul1le0xTWRFBoYd7', '76qqDJijAjFph7sjUxNVG8', '6SePnvTZkIXZznc8Ftc6vM', '2pozUjd7AVIPwSNDqoU3ek', '210JJAa9nJOgNa0YNrsT5g', '5KyOUICJIvO0z71MBdPGiX', '6ezYHltHYhuJckdCsYsRJI', '02wk5BttM0QL38ERjLPQJB', '6uTPA1xlcsk6dbchB2dhzl', '253P6uwLnelVQ6MdwXMIJk', '3ISOK4T54v6O1g1AB8FiEK', '5IAESfJjmOYu7cHyX557kz', '42h7yc9Rda1IOMYLACVgld', '69CrOS7vEHIrhC2ILyEi0s', '6auT8cRBu3BgPRBrdVBY15', '2KwOuFfwQyT9mZqjvchd81', '43Pmqpiw4zFY77pT5QdxQ8', '3r8RuvgbX9s7ammBn07D3W', '0rhI6gvOeCKA502RdJAbfs', '0IkWksfw3Qxob96bjFKhyF', '4OtVQ2ZxS7yigIjGz5yKg1', '3F4lHPNHlvr3RpO4tpVOIs', '6adPuBjUw3Zh6wK27d8Rgv', '60KWPwY1iwKIOszBGXxlmh', '2pCcl9FB4KCqYXYzloAMRK', '7nkp1uuSbKkoxMvEs8cSw0', '5HiSc2ZCGn8L3cH3qSwzBT', '6hvczQ05jc1yGlp9zhb95V', '0sq2QUCf3ykmfYxjCDWcir', '0bMoNdAnxNR0OuQbGDovrr', '21aOLk12MksET8AsbU0SI6', '56v8WEnGzLByGsDAXDiv4d', '3CYH422oy1cZNoo0GTG1TK', '63J1RStsmoVKXNTCHRNxii', '2UP7KnRSvc4taXbjOoSX0f', '3ejAkJLWQSEJDqDXxK3efB', '7gRFDGEzF9UkBV233yv2dc', '1rp986nzkyAX1wFpxzbwlC', '5GKwq4sO5ZHKuWaDmdwMQc', '0jFHMDRXxKaREor3hBEEST', '0L8LOav65XwLjCLS11gNPD', '6I2tqFhk8tq69iursYxuxd', '5C2d3tz8WACjmw7T6TthQ2', '5SusX17QvBBkH7WfMbTU0j', '7fK0csBoqbcgUuWGV0cpoD', '4SFknyjLcyTLJFPKD2m96o', '3gFcGnU4kTdMYLXDjH1TK8', '5gA9Xn8oPts2aewPgxVkPD', '462OPOKW0VMbvW9H7HIb0U', '5FVbvttjEvQ8r2BgUcJgNg', '6LnEoRQKMcaFTR5UvaKuBy', '5zwwW9Oq7ubSxoCGyW1nbY', '0LrhTHjmH2ATnbCbsqKZyf', '6DIW7GJbuGZdHolRcPWprP', '4QhnNyKDsAkXPwHkSnuc89', '7BDHDiidJ8WV349p3HTxTV', '3Hd6zm1J4bVeu4VXwaDQL3', '405SQUJdQut02dxtuQ0CZ3', '3G1aAxWS2Nd17FQs4PWV6X', '6Upu6yjkdi0DVI8E3IBZEU', '0IxEQbRKjdc0fKPmovjEYw', '0Qzs7eyyx6Il1qkA4wqUHm', '1ADlTU9mFc3oDdD9Vla2Yw', '6SpPr7K4YQ2wp8jU6uOTmQ', '2U6RSyXFnDVNYoD9iUgi09', '2FXd6kKCtBIc6UfN1gH1pA', '3QwiidVHfeE9y5jl4n2MTC', '2pIUpMhHL6L9Z5lnKxJJr9', '2gYj9lubBorOPIVWsTXugG', '5oH4DQAuu1J1800RzUsBWa', '0skYUMpS0AcbpjcGsAbRGj', '3Ua0m0YmEjrMi9XErKcNiR', '5e6hUjvQG2inD4Svco0PvP', '0IGUXY4JbK18bu9oD4mPIm', '07fqC2Puj13frv9iYtlcri', '0RDqNCRBGrSegk16Avfzuq', '69xohKu8C1fsflYAiSNbwM', '5rJ7bdPmr8nfmm2JQ8xHOz', '7nthiiDfS9WHNHDMwmAz98', '4LJgBT9yo0beHlaBesCFEv', '0u8rZGtXJrLtiSe34FPjGG', '4hbU7BVioG3WnoRNEy5YUf', '3o3bRIOKDwGOdqL9HBUNrO', '4dKa5ZzlGqUy3Wo0yaXKNI', '3WUyu94psXrYV6HZbXgcFA', '59hBR0BCtJsfIbV9VzCVAp', '3IelG5zYpWWCZIH4cqWlPV', '2s2PGt2yeQly8auhPuHGIn', '7eBpUuPnDTfbeP1P4P93CS', '4kSDi21MeOoSvpZs6MveI9', '5NcLyVjUgG0yfwHgr5t81w', '70yszWsLJvNZuZwaHNMROf', '6QCPweR3aP6nj7P43WpiZs', '0mlxHb4jbPr1PUBUv0WHRS', '61AZsmFB3VoJdmraMk5ZSn', '1F6qqwgyBjcIMzen8RrOXQ', '5cTnKClHyczcUhFT8MKBZe', '27bIik73QCu8Xzt3xpG1bI', '63irPUP3xB74fHdw1Aw9zR', '5uFqjHOo3Sh0bVPCKf3DdH', '7xNCacksfUkYXsXuSW4vNF', '1RDvyOk4WtPCtoqciJwVn8', '7ixVW7RobslvMrvlzHYLha', '5p8ThxM2OhJ0igfxkz0Z1q', '6NnCWIWV740gP7DQ8kqdIE', '6vq6B6ENjap5Ea1T4GkrFA', '1RHTdr5QfviCYI70QPPDJN', '0h7QMc9ZRzA9QJrbEHytn2', '34y2pV3RGFiCHSP12bNHVk', '3O8G8eVrhfXTGttyQ1xVuq', '0oeVHAgY8Q7Mdce5Quj2G4', '1ex8euBuzVyqjThnYfwY2k', '1nmc8ngLcvccw7Lay5v5SP', '1QpwvWMQGdOgA8MXXfgs4H', '0ARKW62l9uWIDYMZTUmJHF', '1dfsPqH09vnzUWEOsN98Ex', '7IkuRNVAjwXpZ2DheQHL4L', '5mdWIwsJAzR97ShGkt8gcR', '7F0MuIk5glqtowCUjbn9es', '4OelNEcxPGoCOU29fchcsv', '1pdFdv8R6ezIAUUNkn785b', '1oen3GpTcA486fTHaT7neg', '0a4MMyCrzT0En247IhqZbD', '2WoluqyWzsgRmFCeHeGlnm', '52uklJhyhJbLvHrgkiqCaW', '6PRy17C5LiiN7VCLS6IA98', '56s2s5e8WuBsWVKnmz6J9L', '3XZAvh2NCDQYHgJei35VQ1', '2QWEMqQMJR1KDf6hDjJOs6', '2DwUdMJ5uxv20EhAildreg', '0Q5VnK2DYzRyfqQRJuUtvi', '4XKXphKH76W4zNpkgFS5o2', '10SRMwb9EuVS1K9rYsBfHQ', '296nXCOv97WJNRWzIBQnoj', '4IaxDf2FixiQXq0mW7key9', '0CatzXH85XWyBqqdB6qPMB', '1fdlTXD7obDyqOpx96BEL9', '1HsSIPLTQT354yJcQGfEY3', '6vo0dV9t7PCQZKsLFwVwZ5', '2oBMZYteeO8DyXV9gDx6Za', '2gzhQaCTeNgxpeB2TPllyY', '3TSLqZssCoCdDlMhCJ08XW', '5quFr5s5PXYfUX5jV2EBZ1', '37YoRLUu1qId0ewavgvnkG', '7rXcCpIAoOUCydkVDMcoPV', '3lrNsPdn98i6rxO142pLT6', '7CAdT0HdiQNlt1C7xk2hep', '0dcnrLo8s1rhjm8euGjI4n', '5elW2CKSoqjYoJ32AGDxf1', '6xy9JYFKcpb9L62PRNnYW5', '4VOySTQM7rAgem85lhM9rZ', '5g3QE1JG8o6zZgYTHoDOll', '1agmptGOYRBOLozOCcrZem', '75tM4GO1MOORpDgeXaypbH', '03M319GUVn9pCJ1SO2jJkC', '2x2kV1apQtg0Esd4m33NVX', '0mxBXzoj8bU9zHTkJo2jUl', '6TMw2Yr2hpzzcU54DpbHM8', '3z33a2AvtL5lBX5bcgQhay', '7kt7bs7L3EA4FZkmgy3yig', '0foxokbWTaklEtzCFBuktJ', '1hrZVbWwU6v4WAjOjv0xGo', '0JMok6kVfl3Cfy2kuz3Mg6', '4Hmv3GGx5DDeKU493kVYB5', '3Jfstvgm1SLE2IgoWoOHt8', '1ixJzrovXOvEzT0EbI1dOv', '4lZ7t0GhxkViSi6LKmiL2I', '2S26xIvywKXmWanaallklu', '4YoqBiaUbJj8MJHbTkEDk4', '7KP2vFrG0EZA34Z6CRJklp', '2yngiU9VWoxySD6TehxeDZ', '7bE0L65oh3vLNe9cI0QXCA', '7IUAkw9BmdzrOTx5J9KVUp', '1ovCFlbOwSsGp2CadHLnt0', '6HbeNWoU255aAIjHiWUJh2', '3HoikAu7DyjXbWufErOgZT', '4sk5jpMmS1AiahoYPpnw49', '0XLB5sYc79B39PYKk4QJkU', '5Mj9ynF2FQ2d2FIvR0bfWM', '4m2eqw1rvuhkdho1DY7GZI', '2h5DGrY3jSJfLf0Op1OHCD', '2SQrg7WIPRKMKrlILjGdQH', '7uVSccPZMVXdOQXq8H1gWS', '2klCjJcucgGQysgH170npL', '2ePS8oLQEpNCM5imRUO58L', '4QlEV1R8S0mFiUz48GY5s5', '19xdWAP56JYpHrbKpuNoZc', '56xwRXkTTpsB1ASKJclpZF', '0NeCqOJkCX9tNeIHLof3OH', '4e9K1aweNsSVjeuDHKaGOT', '6hzTTnBE5n1nsGEmDFYKvr', '74d0dFh27t64iMb7JKd59f', '7gf1Qjcp9nrpcLeR7lrOEo', '5iFdWzUzem2HYsmGdOH64H', '7rXhnFjG74YKMgq0R89Bpz', '5S5gGOsUarzRXKoaSstwba', '1H2qNVjNn13tlpKv6MtiYn', '7xePxAMPRq6WuRzuWxK8hJ', '0VxRqtpDdnk4L6kM5kbTBF', '5ANbXf5qR48a4jfFnSq80w', '4b1sQpvL7QVgamRZ74F1oA', '0oSNOJEcBIKNcQzRc5TfyR', '1hSIAnwHB4QPHo4PJgHn05', '0gb636CX4wHmcgqV0ydKdm', '22iz04Hw1tz0NBpiyoEMT1', '0pGHou9D7JTMKbMfOLKy50', '0BU2OFDU7NvV7zza77F2YN', '1ZgfAxHQCXLt8o1VXEHHAt', '1Rrj7KyS2R6SP9CQMDJW1w', '4LCOHlJqbILfOrYvAdgJbs', '2dTwsBJXXLGoW6ikFE8UnS', '7pNNnrmd3pBIsQTenWExLy', '3b7OgfU9SY8C7YBJgTKS74', '24PhZrRiALtUXgdwXkEwGt', '0pWxUlYb3EM2WkcTJfwBdP', '6MXdCx8C4KoeBf2o8duV0S', '15efgYAJ06VffSUNwwKmk0', '7czyJpFnAl18Bwye8wETky', '0YVsrgp4OOUhFuYMAVQazV', '5FLuHcyUiAlq2wCoqVuqUa', '0fp7yXkUbwmM8ML6sWu6HW', '2VDvDc0s1EvvdO2vu9vnTG', '6gorwqDJ7bsdCHcVs5uS9u', '68ABnHNR4y2COQa4eaM6PS', '5WitNasXEIRptoLIQUcXMx', '0j7nKZ1WNZyK2oTJfseFNQ', '2OUCEz0B8chI3FcqloinyN', '3GdvlmQ8GgfFokp1hpdRJ2', '5l4u7LfxvtBPIiV3ptriqs', '5kCz0W7rPge3IRWseLF5Fv', '1BSncOsSJPQkpl29QM0ipj', '4MSiPP89oZupNNq2CvjEeR', '0cCm1PbOd6nqAPDdA3PRfs', '3CEs5Jnov3YkmYn0Vezrcr', '3VC1IEz9M1txlMSx3h3tPM', '0WJVy5IYA9AeAI1htZDq0C', '7LJjWqhqK594nN7qJzLVXE', '2JTjDYA0vfx8sp5XMTbeqU', '5O3I7UPYpdJHLwA6Nw3Qhx', '0NeNAcCVtGqLAAmf4FhWWT', '1pLh3xuAaDMyux3laCEqaq', '6KmWiz0zpYSPA56Poz0Cjb', '43Y6XibvJzLJj3GyVQaEFJ', '42tFTth2jcF7iSo0RBjfJF', '1cgBWgoL6520lR2QZDzdGN', '1dJQaGuotdQeGeI6gToWLc', '5CrqXQtcgpKA6e53ldOTSm', '1zZ9IuDffZGH5OoVoUXlHz']

def get_audio_features(track_id):
  track_info = sp.track(track_id)
  if track_id is not None:
    audio_features = sp.audio_features(track_id)[0]

    return {
        'track_id': track_id,
        'name': track_info['name'],
        'artist': track_info['artists'][0]['name'],
        'features': {
            'danceability': audio_features['danceability'],
            'energy': audio_features['energy'],
            'loudness': audio_features['loudness'],
            'speechiness': audio_features['speechiness'],
            'acousticness': audio_features['acousticness'],
            'instrumentalness': audio_features['instrumentalness'],
            'liveness': audio_features['liveness'],
            'valence': audio_features['valence'],
            'tempo': audio_features['tempo']
        }
  }

# Function to calculate similarity between two songs based on audio features
def calculate_similarity(song1, song2):
  features1 = np.array(list(song1['features'].values())).reshape(1, -1)
  features2 = np.array(list(song2['features'].values())).reshape(1, -1)

  # Normalize features
  features1_normalized = features1 / np.linalg.norm(features1)
  features2_normalized = features2 / np.linalg.norm(features2)

  return cosine_similarity(features1_normalized, features2_normalized)[0][0]

# Function to recommend similar songs
def recommend_songs(selected_song, all_songs, top_n=5):
  selected_song_features = get_audio_features(selected_song)
  similarities = []

  for song_id in all_songs:
      if song_id != selected_song:
          song_features = get_audio_features(song_id)
          similarity = calculate_similarity(selected_song_features, song_features)
          similarities.append((song_id, similarity))

  # Sort by similarity and get top N recommendations
  sorted_songs = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_n]

  return sorted_songs

@client.event
async def on_ready():
  print("Bot is ready")

@client.tree.command()
async def hello(interaction: discord.Interaction):
  """Says Hello!"""
  await interaction.response.send_message("Hello! Nice to see you here!")

@client.tree.command()
@app_commands.describe(
  song_id="The ID of the song you recommendations from."
)
async def recommend(interaction: discord.Interaction, song_id: str):
  """Recommend a song based on your spotify ID!"""
  await interaction.response.send_message(recommend_songs(song_id, all_songs_to_compare))






client.run(TOKEN)
