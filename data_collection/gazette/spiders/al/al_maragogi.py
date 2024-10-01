import locale
from datetime import date, datetime
from urllib.parse import ParseResult, parse_qs, urlencode, urlparse

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
            "per-page": 30,
            "page": 1,
        }
        url = f"{self.start_urls[0]}/busca?{urlencode(params, encoding='utf-8')}"
        yield scrapy.Request(
            url,
        )

    @staticmethod
    def __get_edition_number(parts: list, extra_edition: bool) -> str:
        edition_number = parts[-2] if extra_edition else parts[-1]
        edition_number = edition_number.split("/")[0]
        if extra_edition:
            edition_number = edition_number + "-A"

        return edition_number

    @staticmethod
    def __has_page_params(url: ParseResult) -> str | None:
        query_params = parse_qs(url.query)
        return query_params.get("BuscaSearch[page]", [None])[0]

    @staticmethod
    def __get_total_pages(query: str) -> int:
        params = parse_qs(query)
        return int(params.get("page", ["0"])[0])

    def parse(self, response):
        publications = response.css("div.publicacao > div.box-publicacao")
        for publication in publications:
            extra_edition = False
            title_el = publication.css("h4 a::text").get()
            data_el = publication.css("div div div::text").getall()[1]
            title_parts = title_el.strip().split(" ")
            extra_edition = title_parts[-1] == "Extra"
            edition_number = self.__get_edition_number(title_parts, extra_edition)

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

        if not self.__has_page_params(urlparse(response.url)):
            has_last_page = response.css(
                "div.publicacao ul > li.last > a::attr(href)"
            ).get()
            last_page = self.__get_total_pages(has_last_page.split("/")[-1])
            for page in range(2, last_page + 1):
                params = {
                    "BuscaSearch[data_inicio]": self.start_date.strftime("%Y-%m-%d"),
                    "BuscaSearch[data_fim]": self.end_date.strftime("%Y-%m-%d"),
                    "BuscaSearch[sort]": "data_new",
                    "BuscaSearch[modulo]": "diario-oficial",
                    "page": page,
                    "per-page": 30,
                }
                url = (
                    f"{self.start_urls[0]}/busca?{urlencode(params, encoding='utf-8')}"
                )
                yield scrapy.Request(
                    url,
                )
