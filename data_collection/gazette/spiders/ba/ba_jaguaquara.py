from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaJaguaquaraSpider(BaseDoemSpider):
    TERRITORY_ID = "2917607"
    name = "ba_jaguaquara"
    state_city_url_part = "ba/jaguaquara"
    start_date = date(2021, 4, 5)
