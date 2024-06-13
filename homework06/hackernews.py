import string

from homework06.bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from homework06.db import News, session
from homework06.scraputils import get_news


def clean(s):
    translator = str.maketrans("", "", string.punctuation)

    return s.translate(translator)


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    id = request.query["id"]
    label = request.query["label"]

    s = session()
    news = s.query(News).get({"id": id})
    news.label = label
    s.commit()

    # redirect("/news")


@route("/update")
def update_news():
    s = session()
    news_list = get_news("https://news.ycombinator.com/newest")

    for article in news_list:
        flag = s.query(News).filter(News.author == article["author"] and News.title == article["title"]).first()
        if flag:
            continue
        news = News(**article)
        s.add(news)
        s.commit()

    # redirect("/news")


@route("/classify")
def classify_news():
    bayes = NaiveBayesClassifier()
    s = session()

    news_cl = s.query(News).filter(News.label != None).all()
    X = []
    ys = []
    for news in news_cl:
        X.append(clean(news.title).lower())
        ys.append(news.label)
    bayes.fit(X, ys)

    news_not_cl = s.query(News).filter(News.label == None).all()
    X = []
    for news in news_not_cl:
        X.append(clean(news.title).lower())
    ys = bayes.predict(X)
    for y, news in zip(ys, news_not_cl):
        news.label = y
    s.commit()

    answer = []
    classes = ["good", "maybe", "never"]
    for cl in classes:
        for news in news_not_cl:
            if news.label == cl:
                answer.append(news)
    return answer


@route("/recommendations")
def recommendations():
    classified_news = classify_news()
    return template("recs_template", rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
