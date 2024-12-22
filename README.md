# APIIntegrationAndAnalysis



This project investigates the relationship between the performance statistics of the top trending movies and the audience interaction with their trailers on YouTube. The core question it addresses is: “How do the top movie performance statistics correlate to audience interaction with the trailers for those movies on YouTube?” This project aims to equip users with easily comparable data on the top 3 currently trending movies, including aspects like view counts and likes on YouTube, ratings, reviews, directing, and lead acting from TMDb and IMDb databases.  


#**System Components** 

The program pulls data from multiple YouTube trailers, interpreting view counts, and likes. That data is then compared against movie statistics pulled from the TMDb API as well as the IMDb API. By retrieving data from both APIs and comparing attributes such as ratings, reviews, directors, and lead actors, users can quickly gain insights about trending movies. Multiple data sources provide greater confidence to the user in the reliability of the information.   

\
**YouTube Class**

Responsible for interfacing with the YouTube API to retrieve data about movie trailers, including view counts and likes. It plays a critical role in understanding the level of audience engagement and interaction on YouTube 

*Key Methods*

 - ‘search_videos_by_title’: Searches for trailers based on movie titles.  
 - ‘fetch_video_stats’: Retrieves statistics for a given trailer, such as view count and likes.  

*TMDb Class*

Interacts with the TMDb API to fetch detailed information about movies. It supplies data on movie popularity, ratings, director name, lead actor name and basic data such as titles and budget.  

*Key Methods*

 - ‘fetch_most_popular_movies’: Gets the list of currently popular movies 
 - ‘fetch_movie_details_with_credits’: Retrieves detailed movie information including director and lead actor names.  

\
**IMDb Class**

*Key Method*

 - ‘def __init__(self, api_key)’: Constructor method that initializes the IMDb object using a given API key and sets a URL for API requests 
 - ‘def search(self, title)’: Searches for movie data based on its title and initialized API key  
 - ‘def get_movie_info(self, title)’: Retrieves movie info using the search function above and returns a dictionary containing information about the director, lead actor, number of reviews, and average rating 

*Integrated Class*

This class integrates data fetched by the YouTube, TMDB, and IMDB classes. It compares and analyzes movie performance statistics against YouTube audience interaction metrics to provide an overview of each movie’s reception.  

*Key Function*

 - ‘integrate_popular_movies_youtube_data’: Merges data from YouTube, TMDb, and IMDb into a cohesive dataset for each movie.  
 - ‘perform_analysis’: Computes and interprets correlations between movie statistics and YouTube engagement metrics.  

\
#**Data Flow and Processing**  

*Data Collection*

The system collects data from YouTube, TMDb, and IMDb APIs, focusing on the top 3 trending movies and their corresponding trailers on YouTube.  

*Data Integration*

Data from the three sources is integrated by the Integrateddata class, creating a unified dataset that includes both movie perfromance statistics and YouTube interaction metrics.  

*Analysis and Correlation*

The system analyzes the integrated data to identify correlations between movie performance and YouTube trailer interactions. Specifically, by analyzing the revenue produced by YouTube from the three most popular YouTube videos and displaying that along with the movie budget.  

*Reporting*

Generates a report presenting the analysis results, making it easy for users to compare data across the top trending movies.  

\
#**Additional Information** 

Assumed the [average price of tickets](https://www.google.com/search?q=average+movie+ticket+price+2023&sca_esv=9f58efb118f0a45e&rlz=1C1RXQR_enCA981CA981&sxsrf=ACQVn0-pDQwdifKq66S_IBieTwamK3XFUw%3A1711139253570&ei=ten9ZfqzItOwptQP1Li5oAg&ved=0ahUKEwi64vq62oiFAxVTmIkEHVRcDoQQ4dUDCBA&uact=5&oq=average+movie+ticket+price+2023&gs_lp=Egxnd3Mtd2l6LXNlcnAaAhgCIh9hdmVyYWdlIG1vdmllIHRpY2tldCBwcmljZSAyMDIzMgUQABiABDIFEAAYgAQyBRAAGIAEMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB5I9zFQAFjEL3ACeAGQAQGYAdUCoAGDGqoBCDIyLjkuMC4xuAEDyAEA-AEBmAIhoALwF6gCEsICBxAjGOoCGCfCAhQQABiABBjjBBjpBBjqAhi0AtgBAcICBBAjGCfCAgsQABiABBiKBRiRAsICFhAuGEMYgwEYxwEYsQMY0QMYgAQYigXCAhEQLhiABBixAxiDARjHARjRA8ICCxAAGIAEGLEDGIMBwgIOEC4YgAQYigUYsQMYgwHCAgoQIxiABBiKBRgnwgIKEC4YQxiABBiKBcICHBAuGEMY1AIYsQMYgAQYigUYiwMY8AMYqAMYpAPCAgoQABiABBiKBRhDwgIQEC4YQxjUAhixAxiABBiKBcICDRAuGIAEGIoFGEMYsQPCAgoQLhiABBiKBRhDwgINEAAYgAQYigUYQxixA8ICChAAGIAEGBQYhwLCAggQABiABBixA8ICBxAAGIAEGAqYAwW6BgYIARABGAGSBwQyNC45oAf77gE&sclient=gws-wiz-serp&) is $11.23 


Assumed the conversion of likes to ticket sales is 10% for each video. Revenue is calculated by multiplying the average likes of all YouTube videos by the ticket price, the number of youtube video, and by 10%.

\
#**Expected Output** 

----------------------------------------------------------------------------------

Movie Title: Kung Fu Panda 4

TMDB Data:
   [Director: Mike Mitchell]
   [Lead Actor: Jack Black]
   [Budget: $85,000,000 USD]
   [Number of Ratings: 314, Average Rating: 6.986]

IMDb Data:
   [Director: Mike Mitchell, Stephanie Stine]
   [Lead Actor: Jack Black]
   [Number of Reviews: 11,124, Average Review: 6.5]

Youtube Data:
   CHANNEL 1
      [Channel: Universal Pictures]
      [Title: KUNG FU PANDA 4 | Official Trailer]
      [Views: 27428297, Likes: 636769]
   CHANNEL 2
      [Channel: Schaffrillas Productions]
      [Title: Kung Fu Panda 4 is a movie that exists]
      [Views: 1087564, Likes: 65681]
   CHANNEL 3
      [Channel: Tenacious D]
      [Title: Tenacious D - ...Baby One More Time (from Kung Fu Panda 4)]
      [Views: 10087374, Likes: 452907]

-------------------------------------------------
Movie Title: Madame Web

TMDB Data:
   [Director: S.J. Clarkson]
   [Lead Actor: Dakota Johnson]
   [Budget: $80,000,000 USD]
   [Number of Ratings: 756, Average Rating: 5.608]

IMDb Data:
   [Director: S.J. Clarkson]
   [Lead Actor: Dakota Johnson]
   [Number of Reviews: 38,266, Average Review: 3.8]

Youtube Data:
   CHANNEL 1
      [Channel: Sony Pictures Entertainment]
      [Title: MADAME WEB – Official Trailer (HD)]
      [Views: 28309018, Likes: 153384]
   CHANNEL 2
      [Channel: Pitch Meeting]
      [Title: Madame Web Pitch Meeting]
      [Views: 1634241, Likes: 117050]
   CHANNEL 3
      [Channel: penguinz0]
      [Title: Madame Web is Horrible]
      [Views: 2798753, Likes: 129012]



-------------------------------------------------
Movie Title: Damsel

TMDB Data:
   [Director: Juan Carlos Fresnadillo]
   [Lead Actor: Millie Bobby Brown]
   [Budget: $60,000,000 USD]
   [Number of Ratings: 1176, Average Rating: 7.202]

IMDb Data:
   [Director: David Zellner, Nathan Zellner]
   [Lead Actor: Robert Pattinson]
   [Number of Reviews: 5,848, Average Review: 5.6]

Youtube Data:
   CHANNEL 1
      [Channel: Netflix]
      [Title: Damsel | Official Trailer | Netflix]
      [Views: 11597936, Likes: 132378]
   CHANNEL 2
      [Channel: Netflix]
      [Title: DAMSEL | Official Teaser | Netflix]
      [Views: 8340844, Likes: 142341]
   CHANNEL 3
      [Channel: The Critical Drinker]
      [Title: Damsel Is Hilariously Bad]
      [Views: 1592982, Likes: 115548]

-------------------------------------------------

--- Movie Popularity and Engagement Analysis ---

Title: Kung Fu Panda 4

Budget: $60,000,000 USD

TMDb Rating: 6.986

IMDb Rating: 6.5

Average YouTube Views: 12,867,745

Average YouTube Likes: 385,119

Engagement Ratio (Likes/Views): 2.99%

Estimated Revenue from YouTube Engagement From 3 Videos: $432,488.64

-------------------------------------------------

Title: Madame Web

Budget: $60,000,000 USD

TMDb Rating: 5.608

IMDb Rating: 3.8

Average YouTube Views: 10,914,004

Average YouTube Likes: 133,149

Engagement Ratio (Likes/Views): 1.22%

Estimated Revenue from YouTube Engagement From 3 Videos: $149,525.95

-------------------------------------------------

Title: Damsel

Budget: $60,000,000 USD

TMDb Rating: 7.202

IMDb Rating: 5.6

Average YouTube Views: 7,177,254

Average YouTube Likes: 130,089

Engagement Ratio (Likes/Views): 1.81%

Estimated Revenue from YouTube Engagement From 3 Videos: $146,089.95

-------------------------------------------------

----------------------------------------------------------------------------------
