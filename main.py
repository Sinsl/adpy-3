from pprint import pprint
import requests
from bs4 import BeautifulSoup as bs
import fake_headers
import json

def get_html(url: str) -> bytes:
    """Получаем страницу"""

    headers_gen = fake_headers.Headers(os='win', browser='chrome')
    response = requests.get(url, headers=headers_gen.generate()).content
    return response


def get_json(html) -> json:
    """Извлекает json из html"""

    soup = bs(html, "lxml")
    data = str(soup.find("noindex"))
    data = data.split('display:none')[1][2:-1].split("</template></noindex")[0]
    data_json = json.loads(data)
    return data_json

def read_json():
    with open('vacancies.json') as f:
        pprint(f.read())


def main(url: str) -> None:
    """главная"""

    html = get_html(url)
    result = get_json(html)
    res_list = []
    for vacancy in result['vacancySearchResult']['vacancies']:
        data = {
            'company_name': vacancy['company']['name'],
            'link': vacancy['links']['desktop'],
            'city': vacancy['area']['name'],
            'price': vacancy['compensation']
        }
        res_list.append(data)

    with open('vacancies.json', 'w') as f:
        f.write(json.dumps(res_list, ensure_ascii=False))

    read_json()


if __name__ == '__main__':
    hh_url = 'https://spb.hh.ru/search/vacancy?text=python%2C+django%2C+flask&area=1&area=2'
    main(hh_url)