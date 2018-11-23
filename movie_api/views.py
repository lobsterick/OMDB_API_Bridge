import requests
from .serializers import MovieSerializer, CommentSerializer
from .models import Movie, Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse


def welcome(request):
    return HttpResponse("Hello! I'm working :)")


class MoviesView(APIView):

    def get(self, request):
        if request.data.get("order"):
            if request.data["order"] == "dsc":
                print("working dsc")
                movies = Movie.objects.all().order_by("id").reverse()
            else:
                return Response(data={"Error": "You can only sort id with order equal to dsc (for descending)"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):

        if request.data.get("title"):
            title = request.data["title"]
        else:
            return Response(data={"Error": "You must provide title in POST request with key named title"}, status=status.HTTP_400_BAD_REQUEST)

        my_api_key = '28cb1743'
        url = f'http://www.omdbapi.com/?t={title}&type=movie&apikey={my_api_key}'
        response = requests.get(url)
        if response.status_code == requests.codes.ok and response.json()['Response'] == 'True':
            if not Movie.objects.filter(Title=response.json()['Title']).exists():
                serializer = MovieSerializer(data=response.json())
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    print(serializer.errors)
                    return Response(data={"Error": "Problem with serializing data from external API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                movie_from_database = Movie.objects.get(Title=response.json()['Title'])
                movie_from_database_serialized = MovieSerializer(movie_from_database)
                return Response(movie_from_database_serialized.data)
        else:
            return Response(data={"Error": "No movie with that title"}, status=status.HTTP_204_NO_CONTENT)


class CommentsView(APIView):
    def get(self, request):
        if request.data.get("movie_id"):
            comments = Comment.objects.filter(movie_id=request.data["movie_id"])
            if comments.count() == 0:
                return Response(data={"Error": "We don't have movie of this ID in database."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not (request.data.get("comment_body") and request.data.get("movie_id")):
            return Response(data={"Error": "You must provide comment and movie_id in POST request"}, status=status.HTTP_400_BAD_REQUEST)

        if Movie.objects.filter(id=request.data["movie_id"]).exists():
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"Error": "No movie with that id"}, status=status.HTTP_400_BAD_REQUEST)
