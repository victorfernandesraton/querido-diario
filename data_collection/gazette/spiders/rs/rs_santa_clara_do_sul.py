from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class RsSantaClaraDoSulSpider(BaseDospSpider):
    TERRITORY_ID = "4316758"
    name = "rs_santa_clara_do_sul"
    code = 4159
    start_date = date(2017, 9, 5)
