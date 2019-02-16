from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm
from django.views import generic
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializer import PostSerializer, CommentSerializer
import tweepy
from allauth.socialaccount.models import SocialToken
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required



class HomeView(LoginRequiredMixin, generic.ListView):
        model = get_user_model()
        template_name = 'blog/Home.html'
        context_object_name = 'users'
        redirect_field_name = 'blog:login'



class AccountArticleView(LoginRequiredMixin, generic.ListView):
        model = Post
        template_name = 'blog/account_article.html'
        paginate_by = 10
        context_object_name = 'posts'
        redirect_field_name = 'blogs:login'
        def get_queryset(self):
         user_id = self.kwargs['user_id']
         return Post.objects.filter(author_id=user_id)


class PostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class CommentView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    fields = ('name', 'text')
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_pk)

        comment = form.save(commit=False)
        comment.target = post
        comment.save()
        return redirect('blog:post_detail', pk=post_pk)




class NewPostView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    success_url ='blog:account_article'
    template_name = 'blog/post_new.html'

    def post_tweet(self):
        user = self.request.user
        access_token = SocialToken.objects.get(account__user=user, account__provider='twitter')
        ts = access_token
        access_token_secret = ts.token_secret
        access_token = str(access_token)
        access_token_secret = str(access_token_secret)
        consumer_key = 'E5rzyQyYfK80RJRWPNvLpOOi2'
        consumer_secret = 'ssAz6p6qvkej4vcr9KabAkhO15aetpYS47GiC1Slc3oPYJfjmH'
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        api.update_status("ブログを投稿しました")

    def form_valid(self, form):
        if form.is_valid():
            post = form.save(commit=False)
            post.author = self.request.user
            post.author.id = self.request.user.id
            post.post_date = timezone.now()
            post.published_date = timezone.now()
            post.save()
            self.post_tweet()
            return redirect('blog:post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})




@login_required()
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.author_id = request.user.id
            post.post_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required()
def post_remove(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:Home')


 #Djangorestframework

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



