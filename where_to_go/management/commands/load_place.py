import os
import time
import requests
from urllib.parse import unquote, urlsplit

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from where_to_go.models import Place, Image

NETWORK_RETRY_DELAY_SECONDS = 5


class Command(BaseCommand):
    help = 'Load places from JSON files'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_url',
            nargs='+',
            type=str,
            help='URL of the raw JSON file containing place data'
        )

    def handle(self, *args, **options):
        for place_json_url in options['json_url']:
            try:
                place = load_place(place_json_url, self.stderr)
            except (requests.exceptions.HTTPError) as error:
                self.stderr.write(f'Пропущено место {place_json_url}: сервер ответил ошибкой ({error})')
                continue
            except requests.exceptions.ConnectionError as error:
                self.stderr.write(f'Пропущено место {place_json_url}: сеть недоступна ({error})')
                time.sleep(NETWORK_RETRY_DELAY_SECONDS)
                continue
            self.stdout.write(self.style.SUCCESS(place.title))


def load_place(place_json_url, stderr):
    response = requests.get(place_json_url)
    response.raise_for_status()
    place_fields = response.json()

    place, created = Place.objects.update_or_create(
        title=place_fields['title'],
        defaults={
            'short_description': place_fields['description_short'],
            'long_description': place_fields['description_long'],
            'latitude': place_fields['coordinates']['lat'],
            'longitude': place_fields['coordinates']['lng']
        }
    )

    image_urls = place_fields['imgs']
    place.images.all().delete()
    for position_number, image_url in enumerate(image_urls):
        try:
            response_image = requests.get(image_url)
            response_image.raise_for_status()
        except requests.exceptions.HTTPError as error:
            stderr.write(f'Пропущена картинка {image_url}: сервер ответил ошибкой ({error})')
            continue
        except requests.exceptions.ConnectionError as error:
            stderr.write(f'Пропущена картинка {image_url}: сеть недоступна ({error})')
            time.sleep(NETWORK_RETRY_DELAY_SECONDS)
            continue
        Image.objects.create(
            place=place,
            position_number=position_number,
            file=ContentFile(
                response_image.content,
                name=os.path.basename(urlsplit(image_url).path),
            )
        )
    return place
