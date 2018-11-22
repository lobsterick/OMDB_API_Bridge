from rest_framework import serializers
from .models import Movie, Comment, Rating
from drf_writable_nested import WritableNestedModelSerializer


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("Source", "Value")


class MovieSerializer(WritableNestedModelSerializer):
    Ratings = RatingSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
