from django.test import TestCase
from .models import Movie, Rating, Comment
from .serializers import MovieSerializer, RatingSerializer, CommentSerializer
import requests



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
