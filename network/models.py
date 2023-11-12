from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class post(models.Model):
    content = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.id} on {self.timestamp.strftime('%d %b %Y %H:%M:%S')}"
    
class follow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User,on_delete=models.CASCADE, related_name="following")

    def __str__(self) -> str:
        return f"{self.user} is following {self.following}"
    
class like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    lpost = models.ForeignKey(post,on_delete=models.CASCADE, related_name="post_like")

    def __str__(self) -> str:
        return f"{self.user} liked {self.lpost}"
