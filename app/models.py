from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    
class Post(models.Model):
    author = models.CharField(max_length=100, default='admin')
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to="media/")    
    body = models.TextField(default="")
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    is_private = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title + "\n" + self.body
    
class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.post}'"
    
class Journal(models.Model):
    author=models.CharField(max_length=60)
    created_on = models.DateTimeField(auto_now_add=True)
    entry = models.TextField()
    response = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Journal"
        verbose_name_plural = "Journals"

    def __str__(self):
        return f"{self.author}'s Journal Entry on {self.created_on.strftime('%Y-%m-%d')}"

    def get_absolute_url(self):
        return reverse("journal_detail", kwargs={"pk": self.pk})

class Calender(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=100, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ], default='Monday')
    created_on = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = "Calender"
        verbose_name_plural = "Calenders"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Calender_detail", kwargs={"pk": self.pk})


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    mental_health_score = models.IntegerField(name = "Mental Health Score", default=0)
    grade = models.CharField(max_length=20, choices=[
        ('None', 'None'),
        ('Middle School', 'Middle School'),
        ('High School', 'High School'),
        ('College', 'College')
    ], default='None')
    def __str__(self):
        return self.user.username