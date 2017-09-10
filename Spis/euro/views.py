from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect

from .models import EuroAuchanNames
from .forms import EAForm

def index(request):
    if request.method == 'POST':
        form = EAForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('Index')
    else:
        form = EAForm()
    return render(request, 'euro/index.html', {'form': form})

def names(request):
    return HttpResponse('Tabela z nazwami Euro-Auchan')

