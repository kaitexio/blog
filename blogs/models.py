from django.db import models
from django.utils import timezone
from stdimage.models import StdImageField
from django.contrib.auth import get_user_model




class Post (models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    post_date = models.DateTimeField(blank=True, null=True)
    origin = StdImageField(upload_to='image//%y/%m/%d/', verbose_name='添付ファイル', blank=True, null=True, variations={
        'large': (600, 400), 'thumbnail': (100, 100, True), 'medium': (300, 200), })



    def publish(self):
        self.published_date = timezone.now()
        self.save()


    def __str__(self):
        return self.title




class Comment (models.Model):
    name = models.CharField(max_length=200, blank=True)
    text = models.TextField()
    target = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

