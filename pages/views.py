from django.shortcuts import render
from consultants.models import Consultant
from choices import state_choices
import random

# TODO: convert to class-based views, https://docs.djangoproject.com/en/3.0/topics/class-based-views/


def index(request):
    consultants = random.sample(list(Consultant.objects.all().values()), 3)
    context = {
        'consultants': consultants,
        'states': state_choices,
        'values': request.GET
    }
    return render(request, 'pages/index.html', context)


def about(request):
    return render(request, 'pages/about.html')


def blog(request):
    return render(request, 'blog/blog.html')
