from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post, Category
from account.models import User
from django.urls import reverse
from account.utils import check_category_exists, check_username_exists
from django.db import IntegrityError
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def post_index(request):
    all_posts = Post.objects.all().order_by('id')
    paginator = Paginator(all_posts, 20 )
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver the last page
        posts = paginator.page(paginator.num_pages)

    context = {
        'all_posts': posts
    }

    return render(request, 'dashboard/post_index.html', context=context)

def edit_post(request, slug):
    all_categories = Category.objects.all()
    author_list = ['author', 'admin']
    all_authors = User.objects.filter(role__in=author_list)

    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":

        # Check if the image fields is empty in the form data
        if not request.FILES.get('image'):
            # if no new image is uploaded, retain the original image
            image = post.image
        else:
            # If no new image is uploaded, retain the orginal image
            image = request.FILES.get("image")

        # Extract form data from request.POST
        title = request.POST.get('title')
        body = request.POST.get('body')
        # image = request.FILES.get('image')
        category_slug = request.POST.get('category')
        user_id = request.POST.get('author')
        status = request.POST.get('status')

        # update post fields with new data
        post.title = title
        post.body = body
        post.image = image  # Assign the new or existing image
        # update category and author using related objects or IDs
        post.category.category_slug = category_slug
        post.user_id = user_id
        post.status = status
        # Save the updated post
        post.save()

        return redirect(reverse('dashboard:post'))
    edit = True
    context = {
        "post": post,
        "edit": edit,
        "all_categories": all_categories,
        "all_authors": all_authors,
    }
    return render(request, 'dashboard/post_create.html', context)

def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        # Delete the post
        post.delete()
        return redirect(reverse('dashboard:post'))
    return render(request, 'dashboard/post_index.html')

def create_post(request):
    all_categories = Category.objects.all()
    author_list = ['author', 'admin']
    all_authors = User.objects.filter(role__in=author_list)

    error = ''
    if request.method == "POST":
        data = request.POST
        file = request.FILES
        title = data.get('title')
        slug = slugify(title)
        body = data.get('body')
        image = file.get('image')
        category_slug = data.get('category')
        category_slug = slugify(category_slug)
        user_id = data.get('author')
        status = data.get('status')

        if title == '':
            error = "Please enter title"
        elif image == None:
            error = "Image field is required"
        elif body == '':
            error = "Body field is required"
        else:
            try:
                category = Category.objects.get(category_slug=category_slug)
                author = User.objects.get(id=user_id)

                Post.objects.create(title=title, slug=slug,
                                    body=body, image=image, category=category, user=author, status=status)
                return redirect(reverse('dashboard:post'))

            except IntegrityError:
                error = "There is an issue with the title"
    context = {
        "error": error,
        "all_categories": all_categories,
        "all_authors": all_authors,
    }
    return render(request, 'dashboard/post_create.html', context=context)


def manage_user(request):
    all_users = User.objects.all().order_by('id')
    paginator = Paginator(all_users, 20 )
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        users = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver the last page
        users = paginator.page(paginator.num_pages)

    context = {
        "users": users
    }
    return render(request, 'dashboard/user_index.html', context=context)

def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        # Check for password matching
        if password != data.get('passwordConf'):
            error = "Passwords didn't match"
        else:
            # Update user details
            user.username = username
            user.email = email
            if password:
                user.set_password(password)  # Hash the password
            user.role = role
            user.save()
            return redirect(reverse('dashboard:manage-user'))
    else:
        error = ''

    edit = True
    context = {
        "edit": edit,
        "user": user,
        "error": error
    }
    return render(request, 'dashboard/user_create.html', context)

def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        # Delete the post
        user.delete()
        return redirect(reverse('dashboard:manage-user'))
    return render(request, 'dashboard/user_index.html')

def create_user(request):
    error = ''
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        hashed_password = make_password(password)
        password_conf = data.get('passwordConf')
        role = data.get('role')

        if password != password_conf:
            error = "passwords didn't match"
        elif check_username_exists(username):
            error = "this username already exists"
        else:
            try:
                User.objects.create(
                    username=username, email=email, password=hashed_password, role=role)
                return redirect(reverse('dashboard:manage-user'))
            except Exception as e:
                error = f"{e}"
    context = {
        "error": error
    }
    return render(request, 'dashboard/user_create.html', context=context)


def manage_topic(request, edit_category_slug=None, delete_category_slug=None):
    all_topics = Category.objects.all().order_by('id')
    paginator = Paginator(all_topics, 20 )
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        topics = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver the last page
        topics = paginator.page(paginator.num_pages)
    context = {
        "all_topics": topics
    }
    return render(request, 'dashboard/topic_index.html', context=context)

def create_topic(request):
    error = ''
    if request.method == "POST":
        data = request.POST
        name = data.get('name', '')
        slug = slugify(name)
        if name.isalpha():
            name = name.title()
            try:
                Category.objects.create(name=name, category_slug=slug)
                return redirect(reverse('dashboard:manage-topic'))
            except IntegrityError:
                error = "This category/topic name already exists"
        else:
            error = "Invalid category/topic name"

    context = {
        "error": error
    }
    return render(request, 'dashboard/topic_create.html', context=context)

def edit_topic(request, category_slug):
    category = get_object_or_404(Category, category_slug=category_slug)
    if request.method == 'POST':
        data = request.POST

        # extract category from the data
        name = data.get('name')
        slug = slugify(name)

        # update the category field with the new data
        category.name = name
        category.category_slug = slug

        # save the updated category
        category.save()
        return redirect(reverse('dashboard:manage-topic'))
    edit = True
    context = {
        "edit": edit,
        "category": category
    }
    return render(request, 'dashboard/topic_create.html', context)

def delete_topic(request, category_slug):
    category = get_object_or_404(Category, category_slug=category_slug)
    if request.method == "POST":
        category.delete()
        return redirect(reverse('dashboard:manage-topic'))
    return render(request, 'dashboard/topic_index.html')
