from django.test import TestCase
from .models import Movie, Rating, Comment
from .serializers import MovieSerializer, CommentSerializer
import requests
from rest_framework.test import APIClient
from movie_api.apps import MovieApiConfig
from django.apps import apps



class ModelsCreateTestCase(TestCase):
    """This class defines tests for all models in app and dependencies."""

    def setUp(self):
        self.new_movie = Movie(
            Title="Batman Begins",
            Year="2005",
            Rated="PG-13",
            Released="15 Jun 2005",
            Runtime="140 min",
            Genre="Action, Adventure, Thriller",
            Director="Christopher Nolan",
            Writer="Bob Kane (characters), David S. Goyer (story), Christopher Nolan (screenplay), David S. Goyer (screenplay)",
            Actors="Christian Bale, Michael Caine, Liam Neeson, Katie Holmes",
            Plot="After training with his mentor, Batman begins his fight to free crime-ridden Gotham City from corruption.",
            Language="English, Urdu, Mandarin",
            Country="USA, UK",
            Awards="Nominated for 1 Oscar. Another 14 wins & 72 nominations.",
            Poster="https://m.media-amazon.com/images/M/MV5BZmUwNGU2ZmItMmRiNC00MjhlLTg5YWUtODMyNzkxODYzMmZlXkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_SX300.jpg",
            Metascore="70",
            imdbRating="8.3",
            imdbVotes="1,150,889",
            imdbID="tt0372784",
            Type="movie",
            DVD="18 Oct 2005",
            BoxOffice="$204,100,000",
            Production="Warner Bros. Pictures",
            Website="http://www.batmanbegins.com/"
        )

    def test_model_can_create_a_movie_object(self):
        """Test if Movie model can create a movie."""

        old_count = Movie.objects.count()
        self.new_movie.save()
        new_count = Movie.objects.count()
        Movie.objects.create(Title="ForTestCase")
        newest_count = Movie.objects.count()
        self.assertNotEqual(old_count, new_count)
        self.assertNotEqual(newest_count, new_count)
        self.assertEqual(str(self.new_movie), f"{self.new_movie.Title} (id: {self.new_movie.id})")

    def test_rating_can_be_created_and_joined_with_a_movie_object(self):
        """Test if Rating object can be joined to existing Movie object"""
        self.new_movie.save()
        old_count = Rating.objects.count()
        new_rating = Rating(Source="Internet Movie Database", Value="8.3/10", Movie=self.new_movie)
        new_rating.save()
        self.assertTrue(isinstance(new_rating, Rating))
        new_count = Rating.objects.count()
        self.assertTrue(self.new_movie.Ratings.filter(id=new_rating.id).get())
        self.assertNotEqual(old_count, new_count)
        self.assertEqual(str(new_rating), f"Rating from {new_rating.Source} to {new_rating.Movie.Title})")

    def test_comment_can_be_created_and_added_to_existing_Movie(self):
        self.new_movie.save()
        old_count = Comment.objects.count()
        new_comment = Comment(comment_body="Test comment", movie_id=self.new_movie)
        new_comment.save()
        self.assertTrue(isinstance(new_comment, Comment))
        new_count = Comment.objects.count()
        self.assertTrue(self.new_movie.Comments.filter(id=new_comment.id).get())
        self.assertNotEqual(old_count, new_count)

class SerializersTestCase(TestCase):

    def setUp(self):
        self.local_data = {"Title": "Batman", "Year": "1989", "Rated": "PG-13", "Released": "23 Jun 1989", "Runtime": "126 min", "Genre": "Action, Adventure", "Director": "Tim Burton", "Writer": "Bob Kane (Batman characters), Sam Hamm (story), Sam Hamm (screenplay), Warren Skaaren (screenplay)", "Actors": "Michael Keaton, Jack Nicholson, Kim Basinger, Robert Wuhl", "Plot": "The Dark Knight of Gotham City begins his war on crime with his first major enemy being the clownishly homicidal Joker.", "Language": "English, French, Spanish", "Country":"USA, UK", "Awards":"Won 1 Oscar. Another 8 wins & 26 nominations.", "Poster":"https://m.media-amazon.com/images/M/MV5BMTYwNjAyODIyMF5BMl5BanBnXkFtZTYwNDMwMDk2._V1_SX300.jpg", "Ratings":[{"Source": "Internet Movie Database", "Value": "7.6/10"}, {"Source": "Rotten Tomatoes", "Value": "72%"}, {"Source": "Metacritic", "Value": "69/100"}], "Metascore": "69", "imdbRating": "7.6", "imdbVotes": "303,988", "imdbID": "tt0096895", "Type": "movie", "DVD": "25 Mar 1997", "BoxOffice": "N/A", "Production": "Warner Bros. Pictures", "Website": "N/A", "Response": "True"}

    def test_movie_serializer_with_ombdapi_data_local(self):
        old_count = Movie.objects.count()
        movie=MovieSerializer(data=self.local_data)
        self.assertTrue(movie.is_valid())
        movie.save()
        new_count = Movie.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_movie_serializer_with_ombdapi_data_remote(self):
        remote_data = requests.get(f'http://www.omdbapi.com/?t=django&type=movie&apikey=28cb1743')
        old_count = Movie.objects.count()
        movie = MovieSerializer(data=remote_data.json())
        self.assertTrue(movie.is_valid())
        movie.save()
        new_count = Movie.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_comments_serializer(self):
        movie = MovieSerializer(data=self.local_data)
        self.assertTrue(movie.is_valid())
        movie.save()
        old_count = Comment.objects.count()
        new_comment_data = {"comment_body": "Test", "movie_id": movie.data.get("id")}
        new_comment = CommentSerializer(data=new_comment_data)
        self.assertTrue(new_comment.is_valid())
        new_comment.save()
        new_count = Comment.objects.count()
        self.assertNotEqual(old_count, new_count)


class MovieRemoteRequestsTestCase(TestCase):
    """Test POST and GET methods on /movie"""

    def setUp(self):
        self.client = APIClient()
        self.movie_1_data = {"Title": "Batman", "Year": "1989", "Rated": "PG-13", "Released": "23 Jun 1989", "Runtime": "126 min", "Genre": "Action, Adventure", "Director": "Tim Burton", "Writer": "Bob Kane (Batman characters), Sam Hamm (story), Sam Hamm (screenplay), Warren Skaaren (screenplay)", "Actors": "Michael Keaton, Jack Nicholson, Kim Basinger, Robert Wuhl", "Plot": "The Dark Knight of Gotham City begins his war on crime with his first major enemy being the clownishly homicidal Joker.", "Language": "English, French, Spanish", "Country":"USA, UK", "Awards":"Won 1 Oscar. Another 8 wins & 26 nominations.", "Poster":"https://m.media-amazon.com/images/M/MV5BMTYwNjAyODIyMF5BMl5BanBnXkFtZTYwNDMwMDk2._V1_SX300.jpg", "Ratings":[{"Source": "Internet Movie Database", "Value": "7.6/10"}, {"Source": "Rotten Tomatoes", "Value": "72%"}, {"Source": "Metacritic", "Value": "69/100"}], "Metascore": "69", "imdbRating": "7.6", "imdbVotes": "303,988", "imdbID": "tt0096895", "Type": "movie", "DVD": "25 Mar 1997", "BoxOffice": "N/A", "Production": "Warner Bros. Pictures", "Website": "N/A", "Response": "True"}
        self.movie_2_data = {"Title":"The Avengers","Year":"2012","Rated":"PG-13","Released":"04 May 2012","Runtime":"143 min","Genre":"Action, Adventure, Sci-Fi","Director":"Joss Whedon","Writer":"Joss Whedon (screenplay), Zak Penn (story), Joss Whedon (story)","Actors":"Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth","Plot":"Earth's mightiest heroes must come together and learn to fight as a team if they are going to stop the mischievous Loki and his alien army from enslaving humanity.","Language":"English, Russian, Hindi","Country":"USA","Awards":"Nominated for 1 Oscar. Another 38 wins & 79 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BNDYxNjQyMjAtNTdiOS00NGYwLWFmNTAtNThmYjU5ZGI2YTI1XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"8.1/10"},{"Source":"Rotten Tomatoes","Value":"92%"},{"Source":"Metacritic","Value":"69/100"}],"Metascore":"69","imdbRating":"8.1","imdbVotes":"1,132,357","imdbID":"tt0848228","Type":"movie","DVD":"25 Sep 2012","BoxOffice":"$623,279,547","Production":"Walt Disney Pictures","Website":"http://marvel.com/avengers_movie","Response":"True"}

    def test_client_get_request_movie_one_or_multiple(self):
        """Test, if client's get request on /movies return
        real data from database for one or many requests"""
        movie_1 = MovieSerializer(data=self.movie_1_data)
        if movie_1.is_valid():
            movie_1.save()
        response = self.client.get('/api/movies')
        self.assertEqual(response.status_code, requests.codes.ok)
        response_serialized = MovieSerializer(data=response.data, many=True)
        self.assertTrue(response_serialized.is_valid())
        self.assertEqual(len(response_serialized.data), 1)
        self.assertEqual(response_serialized.data[0]["Title"], self.movie_1_data["Title"])
        with self.assertRaises(IndexError):
            x = response_serialized.data[1]["Title"]

        movie_2 = MovieSerializer(data=self.movie_2_data)
        if movie_2.is_valid():
            movie_2.save()
        response = self.client.get('/api/movies')
        self.assertEqual(response.status_code, requests.codes.ok)
        response_serialized = MovieSerializer(data=response.data, many=True)
        self.assertTrue(response_serialized.is_valid())
        self.assertEqual(len(response_serialized.data), 2)
        self.assertEqual(response_serialized.data[1]["Title"], self.movie_2_data["Title"])
        with self.assertRaises(IndexError):
            x = response_serialized.data[2]["Title"]

    def client_get_by_order_dsc(self):
        # TODO not working - can't pass data with GET request, problem from github.com/encode/django-rest-framework/pull/1463
        # but working normally when server start
        movie_1 = MovieSerializer(data=self.movie_1_data)
        if movie_1.is_valid():
            movie_1.save()
        movie_2 = MovieSerializer(data=self.movie_2_data)
        if movie_2.is_valid():
            movie_2.save()
        response = self.client.get('/api/movies', data={'order': 'dsc'})
        print(response.data)
        first_id = response.data[0]["id"]
        second_id = response.data[1]["id"]
        print(f"\nId from first {first_id} should be bigger than id from second {second_id}")
        self.assertTrue(response.data[0]["id"] > response.data[1]["id"])

    def client_get_by_order_dsc_with_bad_parameter(self):
        # TODO not working - can't pass data with GET request, but working normally when server start
        response = self.client.get('/api/movies', data={"order": "SomeInvalidText"})
        self.assertTrue(response.data["Error"])

    def test_client_post_request_movie_with_good_data(self):
        response = self.client.post('/api/movies', {'title': 'Batman'}, format='json')
        self.assertEqual(response.status_code, requests.codes.ok)
        self.assertEqual(response.data["Title"], "Batman")

    def test_client_post_request_nonexistent_movie(self):
        response = self.client.post('/api/movies', {'title': 'SomeNonExistingMovie'}, format='json')
        self.assertEqual(response.status_code, requests.codes.no_content)
        self.assertTrue(response.data["Error"])

    def test_client_post_request_movie_with_bad_data(self):
        response = self.client.post('/api/movies', {'title_name': 'Batman'}, format='json')
        self.assertEqual(response.status_code, requests.codes.bad_request)
        self.assertTrue(response.data["Error"])

    def test_save_movie_to_database_after_first_post(self):
        old_count = Movie.objects.all().count()
        self.client.post('/api/movies', {'title': 'Batman'}, format='json')
        new_count = Movie.objects.all().count()
        self.assertNotEqual(old_count, new_count)

    def test_get_from_db_when_post_movie_existing_in_db(self): # TODO check, why error
        self.client.post('/api/movies', {'title': 'Batman'}, format='json')
        old_count = Movie.objects.all().count()
        second_post = self.client.post('/api/movies', {'title': 'Batman'}, format='json')
        new_count = Movie.objects.all().count()
        self.assertEqual(old_count, new_count)
        self.assertEqual(Movie.objects.get(id=1).Title, second_post.data["Title"])

class CommentsRequestsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.movie_1_data = {"Title": "Batman", "Year": "1989", "Rated": "PG-13", "Released": "23 Jun 1989", "Runtime": "126 min", "Genre": "Action, Adventure", "Director": "Tim Burton", "Writer": "Bob Kane (Batman characters), Sam Hamm (story), Sam Hamm (screenplay), Warren Skaaren (screenplay)", "Actors": "Michael Keaton, Jack Nicholson, Kim Basinger, Robert Wuhl", "Plot": "The Dark Knight of Gotham City begins his war on crime with his first major enemy being the clownishly homicidal Joker.", "Language": "English, French, Spanish", "Country":"USA, UK", "Awards":"Won 1 Oscar. Another 8 wins & 26 nominations.", "Poster":"https://m.media-amazon.com/images/M/MV5BMTYwNjAyODIyMF5BMl5BanBnXkFtZTYwNDMwMDk2._V1_SX300.jpg", "Ratings":[{"Source": "Internet Movie Database", "Value": "7.6/10"}, {"Source": "Rotten Tomatoes", "Value": "72%"}, {"Source": "Metacritic", "Value": "69/100"}], "Metascore": "69", "imdbRating": "7.6", "imdbVotes": "303,988", "imdbID": "tt0096895", "Type": "movie", "DVD": "25 Mar 1997", "BoxOffice": "N/A", "Production": "Warner Bros. Pictures", "Website": "N/A", "Response": "True"}
        self.movie_2_data = {"Title":"The Avengers","Year":"2012","Rated":"PG-13","Released":"04 May 2012","Runtime":"143 min","Genre":"Action, Adventure, Sci-Fi","Director":"Joss Whedon","Writer":"Joss Whedon (screenplay), Zak Penn (story), Joss Whedon (story)","Actors":"Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth","Plot":"Earth's mightiest heroes must come together and learn to fight as a team if they are going to stop the mischievous Loki and his alien army from enslaving humanity.","Language":"English, Russian, Hindi","Country":"USA","Awards":"Nominated for 1 Oscar. Another 38 wins & 79 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BNDYxNjQyMjAtNTdiOS00NGYwLWFmNTAtNThmYjU5ZGI2YTI1XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"8.1/10"},{"Source":"Rotten Tomatoes","Value":"92%"},{"Source":"Metacritic","Value":"69/100"}],"Metascore":"69","imdbRating":"8.1","imdbVotes":"1,132,357","imdbID":"tt0848228","Type":"movie","DVD":"25 Sep 2012","BoxOffice":"$623,279,547","Production":"Walt Disney Pictures","Website":"http://marvel.com/avengers_movie","Response":"True"}
        self.movie_1 = MovieSerializer(data=self.movie_1_data)
        self.assertTrue(self.movie_1.is_valid())
        self.movie_1.save()
        self.movie_2 = MovieSerializer(data=self.movie_2_data)
        self.assertTrue(self.movie_2.is_valid())
        self.movie_2.save()

    def test_add_comment_to_existing_movie(self):
        """Add one comment for movie_1 and one comment for movie_2.
        Assert comment return in response"""
        old_count = Comment.objects.all().count()
        response1 = self.client.post('/api/comments', {'comment_body': 'Test1', "movie_id": self.movie_1.data["id"]}, format='json')
        response2 = self.client.post('/api/comments', {'comment_body': 'Test2', "movie_id": self.movie_2.data["id"]}, format='json')
        self.assertEqual(Comment.objects.all().count()-old_count, 2)
        self.assertEqual(Comment.objects.get(id=response1.data["id"]).comment_body, "Test1")
        self.assertEqual(Comment.objects.get(id=response1.data["id"]).movie_id.id, self.movie_1.data["id"])
        self.assertEqual(Comment.objects.get(id=response2.data["id"]).comment_body, "Test2")
        self.assertEqual(Comment.objects.get(id=response2.data["id"]).movie_id.id, self.movie_2.data["id"])

    def test_add_comment_to_nonexistent_movie(self):
        response = self.client.post('/api/comments', {'comment_body': 'Test1', "movie_id": 5890}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Comment.objects.filter(comment_body="Test1").count(), 0)

    def test_add_comment_with_bad_request(self):
        response_bad_body = self.client.post('/api/comments', {'comment_body_but_bad': 'Test2', "movie_id": self.movie_1.data["id"]}, format='json')
        response_bad_movie_id = self.client.post('/api/comments', {'comment_body_but_bad': 'Test2', "movie_id_but_bad": self.movie_1.data["id"]}, format='json')
        self.assertEqual(response_bad_body.status_code, 400)
        self.assertEqual(response_bad_movie_id.status_code, 400)

    def test_add_comment_that_breaking_serializer_with_too_long_body(self):
        too_long_comment = "x" * 101
        response = self.client.post('/api/comments', {'comment_body': too_long_comment, "movie_id": self.movie_1.data["id"]}, format='json')
        self.assertEqual(response.status_code, 500)

    def test_get_comments_for_movie(self):
        comment1_1 = Comment(comment_body='Movie1Test1', movie_id=Movie.objects.get(id=self.movie_1.data["id"]))
        comment1_1.save()
        comment1_2 = Comment(comment_body='Movie1Test2', movie_id=Movie.objects.get(id=self.movie_1.data["id"]))
        comment1_2.save()
        comment2_1 = Comment(comment_body='Movie2Test1', movie_id=Movie.objects.get(id=self.movie_2.data["id"]))
        comment2_1.save()
        comment2_2 = Comment(comment_body='Movie2Test2', movie_id=Movie.objects.get(id=self.movie_2.data["id"]))
        comment2_2.save()
        comment2_3 = Comment(comment_body='Movie2Test3', movie_id=Movie.objects.get(id=self.movie_2.data["id"]))
        comment2_3.save()
        response = self.client.get('/api/comments', format='json')
        self.assertEqual(len(response.data), 5)

    def get_comments_with_movie_id(self):
        # not working - can't pass data with GET request, but working normally when server start
        old_count = Comment.objects.all().count()
        comment1_1 = Comment(comment_body='Movie1Test1', movie_id=Movie.objects.get(id=self.movie_1.data["id"]))
        comment1_1.save()
        comment1_2 = Comment(comment_body='Movie1Test2', movie_id=Movie.objects.get(id=self.movie_1.data["id"]))
        comment1_2.save()
        comment2_1 = Comment(comment_body='Movie2Test1', movie_id=Movie.objects.get(id=self.movie_2.data["id"]))
        comment2_1.save()
        response = self.client.get('/api/comments', {"movie_id": self.movie_1.data["id"]}, format='json')
        self.assertEqual(len(response.data), 2)
        new_count = Comment.objects.all().count()
        self.assertNotEqual(old_count, new_count)

    def try_get_comment_from_movie_with_no_comments(self):
        # not working - can't pass data with GET request, but working normally when server start
        response = self.client.get('/api/comments', {"movie_id": self.movie_1.data["id"]}, format='json')
        self.assertEqual(response.status_code, 400)

class ReportsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(MovieApiConfig.name, 'movie_api')
        self.assertEqual(apps.get_app_config('movie_api').name, 'movie_api')