import pytest 
from requests_mock import Mocker
from Project_Code import IMDb

@pytest.fixture
def imdb_api():
    return IMDb(api_key='test_api_key')

def test_search_movie_found(imdb_api, requests_mock):
    requests_mock.get("http://www.omdbapi.com/", json={'Title': 'The Matrix', 'Director': 'Lana Wachowski', 'Actors': 'Keanu Reeves, Laurence Fishburne', 'imdbVotes': '1234', 'imdbRating': '8.5', 'Response': 'True'})
    result = imdb_api.search('The Matrix')
    assert result == {'Title': 'The Matrix', 'Director': 'Lana Wachowski', 'Actors': 'Keanu Reeves, Laurence Fishburne', 'imdbVotes': '1234', 'imdbRating': '8.5', 'Response': 'True'}

def test_search_movie_not_found(imdb_api, requests_mock):
    requests_mock.get("http://www.omdbapi.com/", json={'Response': 'False'})
    result = imdb_api.search('Non-existent Movie')
    assert result == {'Response': 'False'}

def test_get_movie_info_found(imdb_api, requests_mock):
    requests_mock.get("http://www.omdbapi.com/", json={'Title': 'The Matrix', 'Director': 'Lana Wachowski', 'Actors': 'Keanu Reeves, Laurence Fishburne', 'imdbVotes': '1234', 'imdbRating': '8.5', 'Response': 'True'})
    result = imdb_api.get_movie_info('The Matrix')
    assert result == {'Director': 'Lana Wachowski', 'Lead Actor': 'Keanu Reeves', 'Number of Reviews': '1234', 'Average Review': '8.5'}

def test_get_movie_info_not_found(imdb_api, requests_mock):
    requests_mock.get("http://www.omdbapi.com/", json={'Response': 'False'})
    result = imdb_api.get_movie_info('Non-existent Movie')
    assert result == {'Response': 'False'}
