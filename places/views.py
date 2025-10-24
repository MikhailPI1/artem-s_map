import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Place


def index(request):
    places = Place.objects.all()

    features = []
    for place in places:
        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [place.lng, place.lat]},
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": f"/places/{place.id}/",
            },
        }
        features.append(feature)

    geojson_data = {"type": "FeatureCollection", "features": features}

    context = {"places_geojson": json.dumps(geojson_data, ensure_ascii=False)}

    return render(request, "index.html", context)


def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)

    images = [request.build_absolute_uri(img.image.url) for img in place.images.all()]

    data = {
        "title": place.title,
        "imgs": images,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {"lng": str(place.lng), "lat": str(place.lat)},
    }

    return JsonResponse(data)
