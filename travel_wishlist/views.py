from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required
def place_list(request):
    # Renders the non-visited place list for a user and adds a new place if a correctally filled out POST request is made.
    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False)
            # witholds committng the save until the user ID is attached to the form data and the data is validiated.   
        place.user = request.user
        if form.is_valid():
            place.save()
            return redirect('place_list')

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form':new_place_form})

@login_required
def visited(request):
    # Get's a user's visited places and renders the visited page with them.
    places = Place.objects.filter(user=request.user).filter(visited = True).order_by('name')

    return render(request, 'travel_wishlist/visited.html', {'places': places})

@login_required
def place_was_visited(request, place_pk):
    # changes a place's visited status to true and returns to the place list.
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list')

@login_required
def place_details(request, place_pk):
    # Renders the place detail page for a place assuming that a place belongs to a user. Adds review notes upon acurate completion of a form. 
    place = get_object_or_404(Place, pk=place_pk)
    if place.user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip info updated.')
        else:
            messages.eror(request, form.errors)
        return redirect('place_details', place_pk=place_pk)
    else:
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_details.html', {'place' : place, 'review_form' : review_form})
        else:
            return render(request, 'travel_wishlist/place_details.html', {'place': place})
        



@login_required
def delete_place(request, place_pk):
    place=get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()

