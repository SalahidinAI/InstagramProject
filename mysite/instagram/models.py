from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class UserProfile(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    user_image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'

    def get_post_quantity(self):
        return self.user_posts.count()

    def get_following_quantity(self):
        folloings = self.user_following.all()
        result = len([i.following for i in folloings])
        return result

    def get_follower_quantity(self):
        followers = self.user_follower.all()
        result = len([i.follower for i in followers])
        return result


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_follower')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_following')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.follower} < {self.following}'

    class Meta:
        unique_together = ('follower', 'following')


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_posts')
    post_image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    hashtag = models.CharField(max_length=64, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def get_like_quantity(self):
        likes = self.post_likes.all()
        result = [i.like for i in likes]
        return len(result)

    def clear(self):
        super().clean()
        if not self.post_image and not self.video:
            raise ValidationError('Оба поля post_image и video не могут быть пустыми!')


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} > {self.post}'

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_likes_quantity(self):
        return self.comment_likes.count()


class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
    like = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')


class Story(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='story_images/', null=True, blank=True)
    video = models.FileField(upload_to='story_videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clear(self):
        super().clean()
        if not self.image and not self.video:
            raise ValidationError('Оба поля image и video не могут быть пустыми!')


class Saves(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class SaveItem(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    save_cart = models.ForeignKey(Saves, on_delete=models.CASCADE, related_name='saved_items')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.save_cart} {self.post}'

    class Meta:
        unique_together = ('post', 'save_cart')


class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField(auto_now_add=True)


class Message(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    video = models.FileField(upload_to='chat_videos/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if not self.text and not self.image and not self.video:
            raise ValidationError('Error, sent text, image or video!')
