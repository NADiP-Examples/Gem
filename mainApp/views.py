from django.shortcuts import render
from .models import Gem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def main(request):
    return render(request, 'index.html')


def listing(request):
    gems = Gem.objects.all()
    paginator = Paginator(gems, 3)
    page = request.GET.get('page')
    try:
        gems = paginator.page(page)
    except PageNotAnInteger:
        gems = paginator.page(1)
    except EmptyPage:
        gems = paginator.page(paginator.num_pages)

    return render(request,'list.html', {"gems": gems})