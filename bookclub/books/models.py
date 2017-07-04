from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    book_name = models.CharField(max_length=300)
    book_author = models.CharField(max_length=300)
    book_comment = models.TextField(blank=True)
    pub_date = models.DateTimeField()
    user_name = models.ForeignKey(User)
    recommend_total = models.IntegerField(default=1)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %d %Y')

    def date_read_pretty(self):
        return self.data_read.strftime('%b %Y')

# Create your models here.
class Recommender(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)

class BooksAlreadyRead(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    read_at = models.DateTimeField()



class BooksWantRead(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    priority = models.IntegerField(default=1)

# Book.filter(bookalreadread__user_id = 9)
