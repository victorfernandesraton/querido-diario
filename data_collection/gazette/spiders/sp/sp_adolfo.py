from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpAdolfoSpider(BaseDospSpider):
    TERRITORY_ID = "3500204"
    name = "sp_adolfo"
    code = 4650
    start_date = date(2015, 5, 14)
