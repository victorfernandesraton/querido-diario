from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class PeCabroboSpider(BaseDospSpider):
    TERRITORY_ID = "2603009"
    name = "pe_cabrobo"
    code = 3190
    start_date = date(2019, 4, 8)
