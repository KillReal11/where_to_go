from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse

from where_to_go.models import Place, Image


def get_object_by_id(request, id):
    place = get_object_or_404(Place.objects.prefetch_related('images'), pk=id)
    images = place.images.all()
    paths = []
    [paths.append(str(image.file.url)) for image in images]
    place_details = {
        'title': place.title,
        'imgs': paths,
        'description_short':  place.short_description,
        'description_long':  place.long_description,
        'coordinates': {
            'lng': place.longitude,
            'lat': place.latitude
        }
    }
    return JsonResponse(
        place_details,
        safe=False,
        json_dumps_params={'ensure_ascii': False, 'indent': 2}
    )


def index(request):
    places = Place.objects.all()
    features = []
    for place in places:
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.longitude, place.latitude]
            },
            'properties': {
                'title': place.title,
                'placeId': place.pk,
                'detailsUrl': reverse('place_detail', args=[place.pk])
            }
        }
        features.append(feature)

    places_on_page = {
      'type': 'FeatureCollection',
      'features': features
    }
    return render(request, 'index.html', context={'places_on_page': places_on_page})
