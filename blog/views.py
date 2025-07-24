from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from .models import Post, Comment, Like
from .forms import CommentForm  # We will create this form next
from django.views.generic import TemplateView

class HomePageView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()

    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()

    # Check if user is a subscriber
    is_subscriber = False
    if request.user.is_authenticated:
        is_subscriber = request.user.subscription.is_active

    comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'like_count': post.likes.count(),
        'is_subscriber': is_subscriber,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Security check: only active subscribers can comment
    if not request.user.subscription.is_active:
        return HttpResponseForbidden("You must be an active subscriber to comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=post.slug)
    return redirect('post_detail', slug=post.slug)


@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        # If the like already existed, remove it (unlike)
        like.delete()

    # For a real application, this should be an AJAX call returning JSON
    return redirect('blog/post_detail', slug=post.slug)

class TermsOfServiceView(TemplateView):
    template_name = "terms_of_service.html"

class PrivacyPolicyView(TemplateView):
    template_name = "privacy_policy.html"