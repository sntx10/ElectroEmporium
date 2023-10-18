from config.celery import app

from applications.electronics.models import RecommendImages, ParsedElectronic
from applications.electronics.parser import get_recommend_data


@app.task
def write_parsed_data():
    """
    записывает спаршенные с других сайтов товары в базу данных
    """
    RecommendImages.objects.all().delete()
    ParsedElectronic.objects.all().delete()
    res = []
    recommend_data = get_recommend_data()
    for data in recommend_data:
        res.append(ParsedElectronic(
            title=data['title'],
            price=data['price'],
        ))
    ParsedElectronic.objects.bulk_create(res)
    res = []
    for data in recommend_data:
        for img in data['images']:
            res.append(RecommendImages(
                electronic_recommend=ParsedElectronic.objects.get(title=data['title']),
                image=img
            ))
    RecommendImages.objects.bulk_create(res)
