#!usr/bin/python

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
        icon=icon
    )
    wf.send_feedback()
    return 0


if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
