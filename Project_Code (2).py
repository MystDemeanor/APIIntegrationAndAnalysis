import requests
import sys
import os

class YouTubeDataSource:

    #Fetches data related to videos from the YouTube Api

    def __init__(self, api_key):

        #Initializes the data source with a given YouTube API key and sets the base URL for the YouTube API

        self.api_key = api_key
        self.base_url = 'https://www.googleapis.com/youtube/v3/'

    def search_videos_by_title(self, title):

        #Search YouTube for videos matching the given movie title and returns their IDs.

        #Constructs the search URL with the API key and search title and asks to recieve 3 videos from YouTube
        search_url = f'{self.base_url}search?key={self.api_key}&q={title}&part=snippet&type=video&maxResults=3'
        #Performs the HTTP GET request to the YouTube API
        response = requests.get(search_url) 

        #Checks the response status code is accepted
        if response.status_code == 200:

            #Extracts the video IDs from the search results and returns them as a list
            return [item['id']['videoId'] for item in response.json()['items']]
        
        if response.status_code == 200:

            return [item['id']['videoId'] for item in response.json()['items']]
        
        elif response.status_code == 403:  # Assuming 403 is the status code for quota exceeded

            raise Exception("YouTube API quota exceeded")
        
        else:
            
            return []  # Return an empty list or consider raising a different exception for other error conditions

    def fetch_video_stats(self, video_id):

        #Fetches statistics for a given video ID

        #Constructs the URL to get the video statistics and snippet information using the video ID
        stats_url = f'{self.base_url}videos?key={self.api_key}&id={video_id}&part=statistics,snippet'
        #Performs the HTTP GET request to the YouTube API
        response = requests.get(stats_url)

        #Checks the response status code is accepted
        if response.status_code == 200:

            #Extracts the only item in the response
            item = response.json()['items'][0]
            #Extracts the statistics part of the item
            stats_data = item['statistics']
            #Extracts the snippet part of the item which contains the title and channel information. 
            snippet = item['snippet']

            return {

                #Returns a dictionary containing the channel name, video title, view count, and like count. 

                'channelName': snippet['channelTitle'],
                'videoTitle': snippet['title'],
                'views': int(stats_data.get('viewCount', 0)),
                'likes': int(stats_data.get('likeCount', 0))

            }
        
        else:

            #Returns a dictionary with empty values if the request was unsuccessful. 
            return {'channelName': '', 'videoTitle': '', 'views': 0, 'likes': 0}

class TMDbDataSource:

    #Fetches movie data from the TMDb API

    def __init__(self, api_key):

        #Initializes the data source with a given TMDb API key and sets the base URL for the TMDb API

        self.api_key = api_key
        self.base_url = 'https://api.themoviedb.org/3/'

    def fetch_most_popular_movies(self):

        #Fetches the most popular movies

        try: 
        
            #Constructs the URL to get the list of popular movies on the first page with the API key
            url = f"{self.base_url}movie/popular?api_key={self.api_key}&language=en-US&page=1"
            #Performs the HTTP GET request to the YouTube API
            response = requests.get(url)

            #Checks the response status code is accepted
            if response.status_code == 200:

                #Extracts the top 3 popular movies from the response and returns them. 
                return response.json()['results'][:3]  
        
            else:
            
                #Returns an empty list if the request was unsuccessful
                return []
            
        except Exception as e:

            print(f"Error fetching most popular movies: {e}")
            return 'Possible Network Error'

    def fetch_movie_details_with_credits(self, movie_id):

        #Fetches movie details, including credits

        #Constructs the URL to get movie details and credits information using the movie ID
        details_url = f"{self.base_url}movie/{movie_id}?api_key={self.api_key}&append_to_response=credits"
        #Performs the HTTP GET request to the YouTube API
        response = requests.get(details_url)

        #Checks the response status code is accepted
        if response.status_code == 200:

            data = response.json()
            
            #Extracts the director's name from the crewq list where the job title is 'Directore
            director = next((crew['name'] for crew in data['credits']['crew'] if crew['job'] == 'Director'), None)
            #Extracts the lead actor's name from the cast list based on the order. This is usually the first person on the cast list so index[0]. 
            lead_actor = next((cast['name'] for cast in data['credits']['cast'] if cast['order'] == 0), None)
            #Extracts the movie's budget, defaults to 0 if not available. 
            budget = data.get('budget', 0)

            return {

                #Returns a dictionary containing information about the movie. 

                'title': data['title'],
                'average_rating': data['vote_average'],
                'number_of_ratings': data['vote_count'],
                'director': director,
                'lead_actor': lead_actor,
                'budget': budget

            }
        
        else:

            #Returns None if the request to fetch movie details was unsuccessful. 
            return None

class IMDb:

    def __init__(self, api_key):    #initialization

        self.api_key = api_key
        self.base_url = "http://www.omdbapi.com/"

    def search(self, title):        #title refers to the movie title

        parameters= {               # returns movie info in json
            
            'apikey': self.api_key,
            't': title 
            
        }

        response = requests.get(self.base_url, params = parameters)

        if response.status_code == 200:

            try:

                return response.json()
            
            except ValueError:

                return None    
               
        else:

            return None
        
    def get_movie_info(self, title):

        data = self.search(title)

        if data and data.get('Response','False') == 'True':

            return {

                'Director' : data.get('Director', 'N/A'),
                'Lead Actor' : data.get('Actors', 'N/A').split(',')[0] if data.get('Actors') else 'N/A',
                'Number of Reviews' : data.get('imdbVotes', 'N/A'),
                'Average Review' : data.get('imdbRating', 'N/A')


            }
            
        else:

            return None

class IntegratedData:

    #Integrates YouTube video stats with TMDb movie details

    def __init__(self, youtube_data_source, tmdb_data_source, imdb_data_source):

        #Initializes the integrated data object with YouTube and TMDb data sources.
        self.youtube_data_source = youtube_data_source
        self.tmdb_data_source = tmdb_data_source
        self.imdb_data_source = imdb_data_source

    def integrate_popular_movies_youtube_data(self):

        #Integrates popular movie data from TMDb with corresponding Youtube video stats. 

        #Fetches the list of most popular movies from TMDb
        popular_movies = self.tmdb_data_source.fetch_most_popular_movies()
        
        #Initializes an empty list to store the integrated movie data. 
        integrated_data = []

        #Iterate over each popular movie fetched from TMDb
        for movie in popular_movies:

            #Fetched movie details including credits. 
            movie_details = self.tmdb_data_source.fetch_movie_details_with_credits(movie['id'])

            #Checks if movie details were successfully fetched
            if movie_details:

                #Extracts the movie title from the details.
                movie_title = movie_details['title']
                imdb_movie_details = self.imdb_data_source.get_movie_info(movie_title)
                youtube_video_stats = [{"error": "No Youtube results available (Youtube API quota reached, try using a new key). No information Available."}]

                try:

                    #Searches for YouTube videos related to the movie title
                    youtube_video_stats = [self.youtube_data_source.fetch_video_stats(video_id) for video_id in self.youtube_data_source.search_videos_by_title(movie_title)]
                    
                except Exception as e:

                    if str(e) == "YouTube API quota exceeded":
                        print(f"No Youtube results available (Youtube API quota reached, try using a new key). No information Available.")
                        sys.exit(0)
 
                movie_data = {

                    #Compiles the integrated movie data including TMDb details and YouTube video stats.

                    'title': movie_title,
                    'tmdb_details': movie_details,
                    'imdb_details': imdb_movie_details,
                    'youtube_videos_stats': youtube_video_stats

                }

                #Appends the compiled movie data to the integrated data list. 
                integrated_data.append(movie_data)

        #Returns the list of integrated movie data. 
        return integrated_data
    
    def perform_analysis(self, integrated_data):

        print("\n--- Movie Popularity and Engagement Analysis ---\n")
        print("------------------------------------------------\n")

        for movie_data in integrated_data:

            title = movie_data['title']
            tmdb_details = movie_data['tmdb_details'] 
            budget = tmdb_details['budget']
            tmdb_rating = movie_data['tmdb_details']['average_rating']
            imdb_rating = movie_data['imdb_details'].get('Average Review', 'N/A')
            youtube_views = sum(stat['views'] for stat in movie_data['youtube_videos_stats']) / len(movie_data['youtube_videos_stats']) if movie_data['youtube_videos_stats'] else 0
            youtube_likes = sum(stat['likes'] for stat in movie_data['youtube_videos_stats']) / len(movie_data['youtube_videos_stats']) if movie_data['youtube_videos_stats'] else 0
            engagement_ratio = (youtube_likes / youtube_views) * 100 if youtube_views else 0
            potential_revenue = youtube_likes * 11.23 * 0.1  # Assuming 10% of likes convert to movie ticket purchases

            print(f"  Title: {title}")
            print(f"  Budget: ${budget:,} USD" if budget else "N/A")
            print(f"  TMDb Rating: {tmdb_rating}")
            print(f"  IMDb Rating: {imdb_rating}")
            print(f"  Average YouTube Views: {youtube_views:,.0f}")
            print(f"  Average YouTube Likes: {youtube_likes:,.0f}")
            print(f"  Engagement Ratio (Likes/Views): {engagement_ratio:.2f}%")
            print(f"  Estimated Revenue from YouTube Engagement From 3 Videos: ${potential_revenue:,.2f}\n")
            print("------------------------------------------------\n")



def main():
    
    #API Keys

    #youtube_api_key = 'AIzaSyDPUAhv0MyBZvWHGixTFObO1ov41OMLh8k' #YouTube API Key that has reached its quota

    youtube_api_key = os.getenv('YOUTUBE_API_KEY', 'default_youtube_api_key')
    tmdb_api_key = os.getenv('TMDB_API_KEY', 'default_tmdb_api_key')
    imdb_api_key = os.getenv('IMDB_API_KEY', 'default_imdb_api_key')

    #youtube_api_key = 'AIzaSyDWS1A4PwZjaprW_y4dVpxyHZ2LdG_7b_c'
    #tmdb_api_key = 'ab161afc77261f0c9325f2b209cdb165'
    #imdb_api_key = 'badd6f81'

    #Create an instance of YouTubeDataSource and TMDbDataSource with the provided API keys. 
    youtube_ds = YouTubeDataSource(youtube_api_key)
    tmdb_ds = TMDbDataSource(tmdb_api_key)
    imdb_ds = IMDb(imdb_api_key)

    #Initializes the IntegratedData class with the YouTube and TMDb data sources. 
    integrated_data_handler = IntegratedData(youtube_ds, tmdb_ds, imdb_ds)
    #Calls the method to integrate popular movies from TMDb with their YouTube video stats.
    integrated_data = integrated_data_handler.integrate_popular_movies_youtube_data()

    #Checks if there is any integrated data. 
    if integrated_data:

        #Iterates through each movie's integrated data. 
        for movie_data in integrated_data:

            print(f"Movie Title: {movie_data.get('title', 'N/A')}")

            #TMDb Section

            print("\nTMDB Data:")

            #Retrieves the TMDb details for the movie. 
            tmdb_details = movie_data.get('tmdb_details', {})
            #Formats the movie's budget for printing. Displays 'N/A' if the budget is not available. 
            budget_formatted = f"${tmdb_details['budget']:,} USD" if tmdb_details['budget'] else "N/A"
  
            print(f"   [Director: {tmdb_details['director']}]")
            print(f"   [Lead Actor: {tmdb_details['lead_actor']}]")
            print(f"   [Budget: {budget_formatted}]")
            print(f"   [Number of Ratings: {tmdb_details['number_of_ratings']}, Average Rating: {tmdb_details['average_rating']}]")

            #IMDb Section
            
            imdb_details = movie_data.get('imdb_details', {})

            if imdb_details:
                imdb_reviews = imdb_details.get('Number of Reviews', 'N/A')
                imdb_average_review = imdb_details.get('Average Review', 'N/A')
            else:
                imdb_reviews = 'N/A'
                imdb_average_review = 'N/A'
            
            print("\nIMDb Data:")
            print(f"   [Director: {imdb_details.get('Director', 'N/A')}]")
            print(f"   [Lead Actor: {imdb_details.get('Lead Actor', 'N/A')}]")
            print(f"   [Number of Reviews: {imdb_details.get('Number of Reviews', 'N/A')}, Average Review: {imdb_details.get('Average Review', 'N/A')}]")
            
            #YouTube Section 

            print("\nYoutube Data:")

            #Initializes counters for total views and likes
            total_views = total_likes = 0
            #Retrieves YouTube video stats
            youtube_video_stats = movie_data.get('youtube_videos_stats', [])
            #Iterates through each YouTube video stat, with an index starting from 1. 
            for index, video_stat in enumerate(youtube_video_stats, start=1):

                print(f"   CHANNEL {index}")                
                print(f"      [Channel: {video_stat.get('channelName', 'N/A')}]")
                print(f"      [Title: {video_stat.get('videoTitle', 'N/A')}]")
                print(f"      [Views: {video_stat.get('views', 0)}, Likes: {video_stat.get('likes', 0)}]")

                #Updates the total views and likes with values from teh current video. 
                total_views += video_stat.get('views', 0)
                total_likes += video_stat.get('likes', 0)

            print("\n------------------------------------------------")

    else:
        print("No integrated data found.")

    integrated_data_handler.perform_analysis(integrated_data)

if __name__ == "__main__":
    main()


    


        
