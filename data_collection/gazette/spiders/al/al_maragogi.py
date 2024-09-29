import locale
from datetime import date, datetime
from urllib.parse import urlencode

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class AlMaragogiSpider(BaseGazetteSpider):
    name = "al_maragogi"
    TERRITORY_ID = "2704500"
    allowed_domains = ["diario.maragogi.al.gov.br"]
    start_date = date(2024, 4, 17)
    start_urls = ["https://diario.maragogi.al.gov.br"]

    def start_requests(self):
        params = {
            "BuscaSearch[data_inicio]": self.start_date.strftime("%Y-%m-%d"),
            "BuscaSearch[data_fim]": self.end_date.strftime("%Y-%m-%d"),
            "BuscaSearch[sort]": "data_new",
            "BuscaSearch[modulo]": "diario-oficial",
        }
        url = f"{self.start_urls[0]}/busca?{urlencode(params, encoding='utf-8')}"
        yield scrapy.Request(
            url,
            callback=self.get_last_page,
        )

    def get_last_page(self, response):
        last_page = 1
        has_last_page = response.css(
            "div.publicacao ul > li.last > a::attr(data-page)"
        ).get()
        if has_last_page:
            last_page = int(has_last_page)

        for page in range(1, last_page + 1):
            params = {
                "BuscaSearch[data_inicio]": self.start_date.strftime("%Y-%m-%d"),
                "BuscaSearch[data_fim]": self.end_date.strftime("%Y-%m-%d"),
                "BuscaSearch[sort]": "data_new",
                "BuscaSearch[modulo]": "diario-oficial",
                "BuscaSearch[page]": page,
            }
            url = f"{self.start_urls[0]}/busca?{urlencode(params, encoding='utf-8')}"
            yield scrapy.Request(
                url,
            )

    def parse(self, response):
        publications = response.css("div.publicacao > div.box-publicacao")
        for publication in publications:
            extra_edition = False
            title_el = publication.css("h4 a::text").get()
            data_el = publication.css("div div div::text").getall()[1]
            edition_number = title_el.strip().split(" ")[-1]
            if edition_number == "EXTRA":
                edition_number = title_el.strip().split(" ")[-2]
                extra_edition = True

            item_date = None

            locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
            date_str = data_el.split(",")[-1].strip()
            item_date = datetime.strptime(date_str, "%d de %B de %Y").date()

            file_id = publication.css("h4 > a::attr(href)").get().strip().split("/")[-1]
            url = f"{self.start_urls[0]}/diario-oficial/versao-pdf/{file_id}"

            yield Gazette(
                date=item_date,
                edition_number=edition_number,
                is_extra_edition=extra_edition,
                file_urls=[url],
                power="executive",
            )
