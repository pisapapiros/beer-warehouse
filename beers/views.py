import random

from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
from beers.models import Beer, Company


def first_view(request):
    # return HttpResponse("Saludos")

    everybody_value = "todas"
    context = {
        'everybody_var': everybody_value,
        'my_list': [1, 3, 88889]
    }

    return render(request, 'beers.html', context)

@login_required
def beer_list_view(request):
    beer_list = Beer.objects.all()

    # TESTING ZONE
    print("beer_list", beer_list)

    beer_list_count = beer_list.count()
    print("beer_list_count", beer_list_count)

    if Company.objects.filter(tax_number=98989).exists():
        company = Company.objects.filter(tax_number=98989).first()
    else:
        company = Company.objects.create(name="Compañía", tax_number=98989)

    new_beer = Beer(name=random.randint(1,100), company=company)
    new_beer.save()
    print("beer_list", beer_list)

    beer_list_sorted = Beer.objects.all().order_by('name')
    print("beer_list_sorted", beer_list_sorted)

    beer_list_filtered = Beer.objects.filter( Q(name__startswith="E") | Q(abv__gte=5))
    print("beer_list_filtered", beer_list_filtered)

    beer_list_filtered = Beer.objects.filter(company__name__startswith='C', abv__lte=1)
    print("beer_list_filtered", beer_list_filtered)

    # beer_list_filtered.delete()
    print("beer_list_filtered", beer_list_filtered)

    return render(request, 'beer_list.html', {'beers': beer_list, 'beer_list_filtered': beer_list_filtered})

def beer_detail_view(request, pk):
    return render(request, 'beer_detail.html', {'beer': Beer.objects.get(pk=pk)})