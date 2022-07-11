from api.models.api import Category, Comment, Genre, Review, Title
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("name", "slug")
        model = Category
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("name", "slug")
        model = Genre
        lookup_field = "slug"


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ("id", "name", "year", "genre", "rating",
                  "category", "description")
        read_only_fields = ("id", "rating")
        model = Title

    def get_rating(self, obj):
        all_reviews = obj.reviews.all()
        score_count = all_reviews.count()
        if score_count > 0:
            score_sum = sum(
                [value['score'] for value in all_reviews.values('score')])
            return int(score_sum / score_count)
        return None


class TitleWriteSerializer(TitleReadSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field="slug",
        many=True,
        required=False
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="slug",
        required=False
    )

    class Meta:
        fields = ("id", "name", "year", "genre",
                  "category", "description")
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        queryset=Review.objects.all(),
        required=False,
        slug_field='id',
    )

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.SlugRelatedField(
        queryset=Title.objects.all(),
        required=False,
        slug_field='id',
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if data == {}:
            raise serializers.ValidationError("Данные не должны быть пустыми!")
        return data
