from django.db import models



class Author(models.Model):
    name = models.CharField(max_length= 30)
    phone_no = models.CharField(max_length=11)
    email = models.EmailField()


    def __str__(self):
        return self.name

class Article(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author')
    category = models.CharField(max_length=10)


    def __str__(self):
        return self.category