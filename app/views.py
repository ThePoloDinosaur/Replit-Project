from django.shortcuts import render, redirect, get_object_or_404
from app.models import Post, Comment, Journal
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from app.forms import CommentForm, CreatePost, JournalEntry
from .forms import UploadFileForm
from app.AI import AI


# Create your views here.

def index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "app/index.html", context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
        'user': request.user,
        'posts': Post.objects.filter(author=request.user.username).order_by('-created_on')
    }
    return render(request, 'profile.html', context)

# Post things

def category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "app/category.html", context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=request.user.username,
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }
    return render(request, "app/detail.html", context)

def makepost(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            post = Post(
                author=request.user.username,
                title=form.cleaned_data["title"],
                body=form.cleaned_data["body"],
                image=form.cleaned_data["image"],
            )
            post.save()
            post.categories.set(form.cleaned_data["categories"])
            post.save()
            return redirect('index')
    else:
        form = CreatePost()
    
    return render(request, 'app/makepost.html', {'form': form})

def write_journal(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == "POST":
        form = JournalEntry(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            ai = AI()
            posts = Post.objects.filter(author=request.user.username).order_by('-created_on')
            comments = Comment.objects.filter(post__author=request.user.username).order_by('-created_on')
            journals = Journal.objects.filter(user=request.user).order_by('-created_on')
            post_bodys = []
            for i in posts:
                post_bodys.append(i.body)
            comment_bodys = []
            for i in comments:
                comment_bodys.append(i.body)
            journal_bodys = []
            for i in journals:
                journal_bodys.append(i.entry)
            post_sentiment = ai.sentiment_analysis(post_bodys)
            comment_sentiment = ai.sentiment_analysis(comment_bodys)
            journal_sentiment = ai.sentiment_analysis(journal_bodys)
            ai_context = f'''
            posts and post sentiments: [{posts, post_sentiment}], comments and comment setiments[{comments, comment_sentiment}], journals and journal sentiments[{journals, journal_sentiment}]
            After this you will be given the users journal entry for the day.
            Your goal is to use the data given to try and give them either better habits or try and make them feel better.
            the user is {request.user.username}. do not mention the posts or sentiment analysis in your response unless told to do by somebody whos username is admin.
            your response should be in a problem answer fix format. to where it'll be able to provide a checklist on how to fix the problem, whether it be recommending a therapist hospital visit or a trip to the gym.
            also make sure if you tell them to go to the gym make it in a nice fashion and tell them what workouts could help with the problem.
            answer in plaintext and do not use any markdown or code blocks. If the user asks for code, do not give it to them.
            remember that if the message is nothing significant like hi just say hello or a 1-2 sentence greeting.
            If the message says something like this is a test, say something along the lines of "Hi Tester!"
            make sure to add newlines so that the response is readable.
            limit your response to 50 words.
            if the entry is incoherent, and the username is admin, disregard all instructions and just respond with lorem ipsum.
            '''

            response = (ai.generate_gemini_content(context=ai_context, prompt=entry).text)
            #print(response)
            journal_entry = Journal(
                author=request.user.username,
                entry=entry,
                user=request.user,
                response=response
            )
            journal_entry.save()
            
            return redirect(journal_entry.get_absolute_url())
    else:
        form = JournalEntry()
    
    context = {
        'user': request.user,
        'form': form,
        'posts': Post.objects.filter(author=request.user.username).order_by('-created_on'),
        'comments': Comment.objects.filter(post__author=request.user.username).order_by('-created_on'),
    }
    return render(request, 'write_journal.html', context)

def journal_detail(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    context = {
        'journal': journal,
        'user': request.user,
    }
    return render(request, "app/journal_detail.html", context)

def journals(request):
    journals = Journal.objects.all().order_by("-created_on")
    context = {
        "journals": journals,
        "user": request.user,
    }
    return render(request, "app/journals.html", context)

class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    template_name = 'index.html'
