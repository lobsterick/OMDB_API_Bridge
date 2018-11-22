from django.test import TestCase
from .models import Movie, Rating, Comment

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