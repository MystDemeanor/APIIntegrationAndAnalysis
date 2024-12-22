import pytest
from Project_Code import IntegratedData, YouTubeDataSource, TMDbDataSource, IMDb

class MockYoutubeDataSourceQuotaExceeded:

    def search_videos_by_title(self,title):

        raise Exception("Youtube API quota exceeded")
    
    def fetch_video_stats(self, video_id):

        pass

class MockTMDbDataSource:

    def fetch_most_popular_movies(self):

        return [ {

            'id': '1',
            'title': 'Mock Movie 1'

        },]
    
    def fetch_movie_details_with_credits(self, movie_id):

        return {

            'title': 'Mock Movie 1',
            'average_rating': 8.5,
            'number_of_ratings': 100,
            'director': 'Mock Director',
            'lead_actor': 'Mock Lead Actor',
            'budget': 1000000
    
        }
    
class MockIMDb:

    def get_movie_info(self, title):

        return {

            'Director': 'Mock Director',
            'Lead Actor': 'Mock Lead Actor',
            'Number of Reviews': '100',
            'Average Review': '8.5'

        }
    
@pytest.fixture
def mock_data_sources():

    youtube_ds = MockYoutubeDataSourceQuotaExceeded()
    tmdb_ds = MockTMDbDataSource()
    imdb_ds = MockIMDb()
    return youtube_ds, tmdb_ds, imdb_ds

def test_quota_exceeded_integration(mock_data_sources):

    youtube_ds, tmdb_ds, imdb_ds = mock_data_sources
    integrated_data_handler = IntegratedData(youtube_ds, tmdb_ds, imdb_ds)

    response = integrated_data_handler.integrate_popular_movies_youtube_data()

    assert "No Youtube results available (Youtube API quota reached, try using a new key). No information Available." in str(response)
    