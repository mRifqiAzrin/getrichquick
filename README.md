# Hello, dear user! 
This is an experimental program that employs two separate APIs to make a "calculated" guess of which stocks are our best bets:

## Keywords to note:
1. Volatile - the degree or the measure of how much a stock's price fluctuates over time.
2. Sentiment - the general attitude of investors regarding a stock.
3. Subreddit - a niche community on Reddit.
4. WallStreetBets - a subreddit that discusses topics related to trading, most notoriously known for the GameStop incident in 2021. 
+ you can learn the gist of it through this https://en.wikipedia.org/wiki/GameStop_short_squeeze 
5. Bullish - the belief or (hope) that the price of a stock will rise in the future.
6. Bearish - the belief or (hope) that the price of a stock will fall in the future

## How it works:
This program employs two APIs, one to extract data from the TTM Squeeze Index and one to gather sentiments from the WallStreetBets subreddit.

The idea is to use the data from the TTM Squeeze Index to determine which stocks are volatile. However, just knowing if the stock is volatile is not enough to make proper decisions as we do not know the direction it will be heading. For example,
if a stock happens to be volatile, we may predict that it will go on a bullish run and you may be tempted to buy more shares, but it's too possible that it will end up going on a bearish run and you, the investor, just lost a bunch of money in the stock market.

Therefore, we employ the use of the sentiment analysis is the deduce the direction to decide whether to make a buy or sell order based on the general perceptions of users in the WallStreetBets subreddit.

After finding the stocks that overlap with both indexes, we run them through another API to verify if they actually went on a bullish or bearish run. 

That's pretty much it.

## Further reading:
If you wish to know how the TTM Squeeze index determine which stocks are volatile, you can visit this site and learn more about the algorithm employed:
https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/ttm-squeeze

and, if you wish to know more about the sentiment analysis, you can visit this site:
https://tradestie.com/apps/reddit/api/

test out the API for yourself and perhaps e-mail the creator at johnludhi@outlook.com.

## Possible developments that could've happen but did not:

The use of a third API, perhaps Aletheia API, but we chose not to because of the data constraints. It is already difficult to find the overlap between the TTM Squeeze Index and the WSB sentiment analysis, adding a third indicator will almsot eradicate all of the output.

## Limitations:
1. There is missing data on some dates, typically more recent ones. Making it a good theoretical tool but less of a practical one.
2. 

## Disclaimer:
This is merely an experimental program and is highly inaccurate most of the time and thus, the creator does not assume responsibility for any financial decisions.
