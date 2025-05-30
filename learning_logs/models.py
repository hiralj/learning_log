from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """A narrow topic user wants to understand and remember about."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Topic name"""
        return self.text


class Entry(models.Model):
    """Is it just cumulative or a sub-topic?"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'
    
    def __str__(self):
        """Short representation of entry within a topic"""
        if len(self.text) <= 50:
            return self.text
        else:
            return f"{self.text[:50]}..."
