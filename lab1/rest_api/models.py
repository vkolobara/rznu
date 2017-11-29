from django.db import models

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User', related_name='posts', editable=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
    author = models.ForeignKey('auth.User', related_name='comments', editable=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', editable=False, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
