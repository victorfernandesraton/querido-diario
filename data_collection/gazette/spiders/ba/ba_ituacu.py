from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaItuacuSpider(BaseDoemSpider):
    TERRITORY_ID = "2917201"
    name = "ba_ituacu"
    state_city_url_part = "ba/ituacu"
    start_date = date(2015, 2, 4)
