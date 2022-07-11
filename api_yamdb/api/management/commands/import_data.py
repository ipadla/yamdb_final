from csv import DictReader

from api.models.api import Category, Comment, Genre, Review, Title
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Import data from csv files'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Importing users'))
        for row in DictReader(
            open(f'{settings.STATICFILES_DIRS[0]}/data/users.csv')
        ):
            user = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                password=make_password(None)
            )
            user.save()

        self.stdout.write(self.style.SUCCESS('Importing categories'))
        for row in DictReader(
            open(f'{settings.STATICFILES_DIRS[0]}/data/category.csv')
        ):
            category = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            category.save()

        # Import Genres
        self.stdout.write(self.style.SUCCESS('Importing genres'))
        for row in DictReader(
            open(f'{settings.STATICFILES_DIRS[0]}/data/genre.csv')
        ):
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            genre.save()

        self.stdout.write(self.style.SUCCESS('Importing titles'))
        for row in DictReader(
            open(f'{settings.STATICFILES_DIRS[0]}/data/titles.csv')
        ):
            title = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(pk=row['category']),
            )
            title.save()

        self.stdout.write(self.style.SUCCESS('Importing genre - title'))

        self.stdout.write(self.style.SUCCESS('Importing reviews'))
        for row in DictReader(
            open(f'{settings.STATICFILES_DIRS[0]}/data/review.csv')
        ):
            review = Review(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                score=row['score'],
                pub_date=row['pub_date']
            )
            review.save()

        self.stdout.write(self.style.SUCCESS('Importing comments'))
        for row in DictReader(
            open(f'{settings.STATICFILES_DIRS[0]}/data/comments.csv')
        ):
            comment = Comment(
                id=row['id'],
                review=Review.objects.get(id=row['review_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                pub_date=row['pub_date']
            )
            comment.save()
