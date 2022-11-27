from django.db import models
class ListWord(models.Model):
    word=models.CharField(max_length=50)
    meaning=models.TextField()
    sample = models.TextField()