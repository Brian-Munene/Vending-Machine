from .models import ProductType
import datetime


def generate_slug(title):
    slug = ''.join(title.split(' '))
    if ProductType.objects.filter(slug=slug).exists():
        slug = slug + '_' + str(datetime.datetime.now().timestamp())
    return slug
