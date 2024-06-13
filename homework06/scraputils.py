import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    tables = parser.table.findAll("table")
    news = tables[1]

    trs = news.findAll("tr")
    for i in range(0, 90, 3):
        current_new = {}

        tr = trs[i + 1]
        td = tr.findAll('td')[1]
        span = td.span
        spans = span.findAll('span')
        anchors = span.findAll('a')
        current_new["author"] = anchors[0].contents[0]
        current_new["points"] = int(spans[0].contents[0].split()[0])

        # comments exist not for all articles, so it is dificult to get number of it
        current_new["comments"] = 0
        
        tr = trs[i]
        td = tr.findAll('td')[2]
        span = td.span
        spans = span.findAll('span')
        anchors = span.findAll('a')
        current_new["title"] = anchors[0].contents[0]
        current_new["url"] = anchors[0].attrs["href"]

        news_list.append(current_new)

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    tables = parser.table.findAll("table")
    news = tables[1]
    tr = news.findAll("tr")[-1]
    td = tr.findAll("td")[-1]
    a = td.findAll("a")[0]
    url = a.attrs["href"]
    return url


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
