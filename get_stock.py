#!usr/bin/python

import os
import sys
import argparse
from workflow import Workflow3, web, ICON_WEB


def get_stock(stock):
    # get stock info here
    url = "https://api.iextrading.com/1.0/stock/{ticker}/batch?types=quote".format(
        ticker=stock
    )
    r = web.get(url)
    result = r.json()
    return result["quote"]


def get_news(stock):
    # get stock news articles here
    api_key = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "news_api_key.txt")
    f = open(api_key, "r")
    key = f.readline()
    f.close()
    url = "https://stocknewsapi.com/api/v1?tickers={ticker}&sortby=trending&type=article&items=5&token={token}".format(
        ticker=stock,
        token=key
    )
    r = web.get(url)
    result = r.json()
    return result["data"]


def main(wf):
    icon = "./icon.png"
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default=None)
    args = parser.parse_args(wf.args)

    quote = get_stock(args.query)
    wf.add_item(
        title="{company} ({ticker}): ${price} | {chg}%".format(
            company=quote["companyName"],
            ticker=quote["symbol"],
            price=quote["latestPrice"],
            chg=(quote["changePercent"]*100)
        ),
        subtitle="Day High: ${hi} | Day Low: ${lo}".format(
            hi=quote["high"],
            lo=quote["low"]
        ),
        icon=icon,
        valid=True,
        arg="https://finance.yahoo.com/quote/{ticker}".format(
            ticker=args.query)
    )

    def get_news_cache():
        return get_news(args.query)
    news = wf.cached_data(
        "news-{ticker}".format(ticker=args.query), get_news_cache, max_age=1800)
    for article in news:
        wf.add_item(
            title=article["title"],
            subtitle=article["text"],
            valid=True,
            arg=article["news_url"]
        )
    wf.send_feedback()
    return 0


if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
