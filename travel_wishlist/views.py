from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


@login_required
def place_list(request):

    '''If this is a POST request, the user clicked the Add button
    in the form. Check if the new place is valid, if so, save a
    new place to the database, and redirect to this same page.
    This creates a GET request to the same route.

    If not a POST route, or Place is not valid, display a page with
    a list of places and a form to add to a new place.
    '''

    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False)     # Creates a new Place from the form
        place.user = request.user
        if form.is_valid():     # Checks against DB constraints, for example, are required fields present?
            place.save()        # Saves to the database
            return redirect('place_list')       # redirects to GET view with name place_list - which is the same view

    ''' If not a POST, or the form is not valid, render the page
    with the form to add a new place, and list the places'''
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})


@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


def about(request):
    author = 'Tom'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})


@login_required
def place_was_visited(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        place = get_object_or_404(Place, pk=pk)
        print(place.user, request.user)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list')


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    return render(request, 'travel_wishlist/place_detail.html', {'place': place} )


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()
