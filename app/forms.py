from django import forms
from .models import Category, Post
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CommentForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment!"}
        )
    )

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class CreatePost(forms.Form):   
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Title"}
        ),
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Body"}
        )
    )
    is_private = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"}
        ),
        label="Make this a journal entry (private post)"
    )
    categories = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "form-control"}
        )
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "accept": "image/*",
            }
        ),
        label="Upload Image",
    )

class CreateCategory(forms.Form):
    name = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "New Category"})
        )
    
class UserRegisterForm(UserCreationForm):
    grade = forms.ChoiceField(choices=['None', 'Middle School', 'High School', 'Collage'], required=False)
    class Meta:
        model = User
        fields = ['username', 'grade', 'password1', 'password2']


class JournalEntry(forms.Form):
    
    entry = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.Textarea()
    )