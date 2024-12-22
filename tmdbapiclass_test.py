import pytest
import requests
from Project_Code import TMDbDataSource

@pytest.fixture
def tmdb_data_source():

    return TMDbDataSource(api_key= 'test_api_key')

def test_fetch_most_popular_movies_error_handling(tmdb_data_source, requests_mock):

    #Simulates Network error

    requests_mock.get("https://api.themoviedb.org/3/movie/popular?api_key=test_api_key&language=en-US&page=1", exc = requests.exceptions.RequestException)

    assert tmdb_data_source.fetch_most_popular_movies() == 'Possible Network Error'

def test_fetch_movie_details_with_credits_error_handling(tmdb_data_source, requests_mock):

    #Simulates a server error

    requests_mock.get("https://api.themoviedb.org/3/movie/12345?api_key=test_api_key&append_to_response=credits", status_code = 500)

    assert tmdb_data_source.fetch_movie_details_with_credits(movie_id = '12345') == None


def test_fetch_details_response_missing_title(tmdb_data_source):

    tmdb_data_source.fetch_movie_details_with_credits = lambda movie_id: {
        
        'vote_average': 8.5, 
        'vote_count': 1000, 
        'credits': {'crew': [], 'cast': []},
        'budget': 16000000
        
        }
    
    movie_details = tmdb_data_source.fetch_movie_details_with_credits(movie_id = '12345')

    assert movie_details.get('title') is None

def test_fetch_movie_details_response_missing_lead_actor_and_director(tmdb_data_source):

    tmdb_data_source.fetch_movie_details_with_credits = lambda movie_id: {
            
        'title': 'Test Movie', 
        'vote_average': 8.5, 
        'vote_count': 1000, 
        'budget': 16000000
            
        }
    
    movie_details = tmdb_data_source.fetch_movie_details_with_credits(movie_id = '12345')

    assert movie_details.get('lead_actor') == None
    assert movie_details.get('director') == None

def test_fetch_movie_details_response_missing_average_rating(tmdb_data_source):

    tmdb_data_source.fetch_movie_details_with_credits = lambda movie_id: {

        'title': 'Test Movie', 
        'vote_count': 1000, 
        'credits': {'crew': [], 'cast':[]},
        'budget': 16000000

        }

    movie_details = tmdb_data_source.fetch_movie_details_with_credits(movie_id = '12345')

    assert movie_details.get('average_rating') == None

def test_fetch_movie_details_response_missing_number_of_ratings(tmdb_data_source):

    tmdb_data_source.fetch_movie_details_with_credits = lambda movie_id: {

        'title': 'Test Movie', 
        'vote_average': 8.5, 
        'credits': {'crew': [], 'cast':[]},
        'budget': 16000000

        }

    movie_details = tmdb_data_source.fetch_movie_details_with_credits(movie_id = '12345')

    assert movie_details.get('number_of_ratings') == None

def test_fetch_movie_details_response_missing_budget(tmdb_data_source):

    tmdb_data_source.fetch_movie_details_with_credits = lambda movie_id: {

        'title': 'Test Movie', 
        'vote_average': 8.5, 
        'vote_count': 1000,
        'credits': {'crew': [], 'cast':[]}

        }

    movie_details = tmdb_data_source.fetch_movie_details_with_credits(movie_id = '12345')

    assert movie_details.get('budget') == None 
