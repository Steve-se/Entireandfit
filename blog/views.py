from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, Category
from django.db.models import Q
from difflib import SequenceMatcher
from hitcount.views import HitCountDetailView
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mass_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def index(request):

    # Filtering by category
    all_categories = Category.objects.all()[:10]
    error = ''
    data = ''

    selected_category = request.GET.get("category")
    all_posts = Post.objects.filter(status='published')
    paginator = Paginator(all_posts, 20)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver the last page
        posts = paginator.page(paginator.num_pages)
    trending = Post.objects.filter(status='published').order_by(
        '-hit_count_generic__hits')[:10]

    if selected_category:
        all_posts = Post.objects.filter(
            category__name__icontains=selected_category)

    # Search
    if "search" in request.GET:

        data = request.GET.get("search")
        if data == '':
            error = "please enter a valid search"
        else:
            multiple_queries = Q(Q(title__icontains=data) | Q(
                category__name__icontains=data) | Q(body__icontains=data))
            all_posts = Post.objects.filter(multiple_queries)

    context = {
        "post": posts,
        'page':page,
        'all_categories': all_categories,
        'selected_category': selected_category,
        'trending': trending,
        'error': error,
        'data': data
    }
    return render(request, 'index.html', context)


class PostDetailView(HitCountDetailView):
    count_hit = True
    model = Post
    template_name = 'detail.html'
    context_object_name = 'trending_posts'

    def get(self, request, slug, *args, **kwargs):
        trending = Post.objects.order_by('-hit_count_generic__hits')[:10]

        all_categories = Category.objects.all()[:10]
        post = get_object_or_404(Post, slug=slug, status='published')

        # Get posts with the same category as the current post
        similar_posts = Post.objects.filter(category=post.category)

        # Filter out the current post from the similar posts
        similar_posts = similar_posts.exclude(slug=post.slug)

        # Compute similarity based on title
        similarity_threshold = 0.4

        similar_posts_filtered = []

        for x in similar_posts:
            similarity_ratio = SequenceMatcher(
                None, post.title, x.title).ratio()
            if similarity_ratio >= similarity_threshold:
                similar_posts_filtered.append(x)
        similar_posts_filtered = similar_posts_filtered[:7]

        context = {
            'item': post,
            'all_categories': all_categories,
            'similar_posts': similar_posts_filtered,
            'trending': trending

        }
        return render(request, 'detail.html', context)


def contact_us(request):
    sent = False
    success_message = ''
    if request.method == 'POST':
        message = request.POST.get('message')
        email = request.POST.get('email')
        subject = "Inquiry from Entire and Fit"

        # second part of the email
        second_subject = "Getting back to you"
        second_message = "Thank you for contacting us at Entire and Fit. We'll get back to you soon."
        sender_email = settings.EMAIL_HOST_USER
        recipient = [email]

        data_tuple = (
            (subject, message, email, [
             settings.EMAIL_HOST_USER, 'ejemstephen@gmail.com']),
            (second_subject, second_message, sender_email, recipient)
        )

        sent = send_mass_mail(data_tuple, fail_silently=False)
        if sent:
            success_message = "sent"

        return redirect('blog:homepage')
    context = {
        "success_message": success_message
    }

    return render(request, 'base.html', context)
