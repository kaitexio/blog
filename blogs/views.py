from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializer import PostSerializer, CommentSerializer
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User
from django.conf import settings
import tweepy

class AccountView(generic.DetailView):
    template_name = 'blog/top.html'
    model = User
    slug_url_kwarg = "username"
    slug_field = "username"

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)
        auth = UserSocialAuth.objects.get(user=self.get_object())
        handler = tweepy.OAuthHandler(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET)
        handler.set_access_token(auth.tokens['oauth_token'], auth.tokens['oauth_token_secret'])
        api = tweepy.API(auth_handler=handler)
        data = api.get_user(screen_name=auth.user.username)
        # print(data)
        context['account'] = data
        return context


def top_page(request):
    user = UserSocialAuth.objects.get(user_id=request.user.id)
    return render(request, 'blog/top.html', {'user': user})



class HomeView(generic.ListView):
        model = get_user_model()
        template_name = 'blog/Home.html'
        context_object_name = 'users'



class AccountArticleView(generic.ListView):
        model = Post
        template_name = 'blog/account_article.html'
        paginate_by = 5
        context_object_name = 'posts'
        def get_queryset(self):

         user_id = self.kwargs['user_id']
         return Post.objects.filter(author_id=user_id)


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'




class CommentView(generic.CreateView):
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

class NewPostView(generic.CreateView):
    model = Post
    form_class = PostForm
    success_url ='blog:account_article'
    template_name = 'blog/post_new.html'

    def form_valid(self, form):
        if form.is_valid():
            post = form.save(commit=False)
            post.author = self.request.user
            post.author.id = self.request.user.id
            post.post_date = timezone.now()
            post.published_date = timezone.now()
            post.save()
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





class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



