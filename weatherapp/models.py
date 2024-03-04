from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Emergency(models.Model):
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    address = models.TextField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    image=models.ImageField(upload_to='emergency_images/', blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='posts/')
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    location=models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    
    reports_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        """
        Report the post and remove it if it has reached a threshold of reports.
        """
        report_threshold = 3  # Adjust the threshold as needed

        # Check if the post has reached the report threshold
        if self.reports_count >= report_threshold:
            self.status = False
            super().save(update_fields=['status'], *args, **kwargs)  # Update only the 'status' field
        else:
            super().save(*args, **kwargs)

        def __str__(self):
            return self.title
        
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'