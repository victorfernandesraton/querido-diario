from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpGuaracaiSpider(BaseDospSpider):
    TERRITORY_ID = "3517802"
    name = "sp_guaracai"
    code = 4853
    start_date = date(2018, 9, 27)
