import requests
from bs4 import BeautifulSoup

from .assets.database import db_session
from .assets.models import Data

import datetime


def get_udemy_info():
    url = 'https://scraping-for-beginner.herokuapp.com/udemy'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    name = soup.select('.card-title')[0].string

    n_subscribers = int(soup.select('.subscribers')[0].string.split('：')[1])
    n_reviews = int(soup.select('.reviews')[0].string.split('：')[1])

    results = {
        'name': name,
        'n_subscribers': n_subscribers,
        'n_reviews': n_reviews}

    return results


def write_data():

    date = datetime.date.today()
    # 新規データ
    _results = get_udemy_info()

    # 書き込みデータ
    subscribers = _results['n_subscribers']
    reviews = _results['n_reviews']

    row = Data(date=date, subscribers=subscribers, reviews=reviews)

    db_session.add(row)
    db_session.commit()


if __name__ == '__main__':
    write_data()