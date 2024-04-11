from .models import User
from blog.models import Category


def check_username_exists(username):
    a = User.objects.filter(username=username).exists()
    return a

def check_category_exists(name):
    a = Category.objects.filter(name=name).exists()
    return a