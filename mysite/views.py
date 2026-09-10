from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render
from django.templatetags.static import static
from django.shortcuts import get_object_or_404
from django.urls import reverse

from places.models import Place, Image
from mysite import settings


def get_object_by_id(request, id):
    place = get_object_or_404(Place, pk=id)
    images = place.images.all()
    paths = []
    for image in images:
        path = str(image.file.url)
        paths.append(path)
    details_url = {
        "title": place.title,
        "imgs": paths,
        "description_short":  place.description_short,
        "description_long":  place.description_long,
        "coordinates": {
            "lng": place.longitude,
            "lat": place.latitude
        }
    }
    return JsonResponse(
        details_url,
        safe=False,
        json_dumps_params={'ensure_ascii': False, 'indent': 2}
    )


def index(request):
    places = Place.objects.all()
    features = []
    for place in places:
        print(place.title)
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.longitude, place.latitude]
            },
            "properties": {
                "title": place.title,
                "placeId": place.place_id,
                "detailsUrl": reverse("place_detail", args=[place.pk])
            }
        }
        features.append(feature)
    print(features)

    places_on_page = {
      "type": "FeatureCollection",
      "features": features
    }
    return render(request, 'index.html', context={'places_on_page': places_on_page})


