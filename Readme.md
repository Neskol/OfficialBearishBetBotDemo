# Official Bear-ish-Bets-Bot
> Autonomous/interactive application for buying/trading stocks using Reddit Data

## Note: this repo is the archival of original repo. Copyrights hold by original members.
## Stock Prediction using Elasticsearch on [r/wallstreetbets](https://www.reddit.com/r/wallstreetbets/)
> This bot uses Elasticsearch to search and match posts from the wallstreetbets subreddit. It aims to search text in individual posts and use a variety of metrics, such as sentiment analysis, to correlate post text discussing stocks to positive or negative sentiment. This information will be used to guide a user to invest in certain stocks.

We'll be collecting text data from r/wallstreetsbets using Elasticsearch and saving the sentiment of the text in conjunction with the stock in question. The bot will draw inferences in this way as part of a stock investment strategy.

![r/wallstreetbets icon](https://a.thumbs.redditmedia.com/w-gbSE-QjkUuNjq2yPpekzEtN4CXRiL4tTO_XfloH80.png)

## Reddit API Changes
> [An Update Regarding Reddit's API](https://www.reddit.com/r/reddit/comments/12qwagm/an_update_regarding_reddits_api/): Effective July 1st, 2023, we will not be able to access the Reddit API for free. Spending money to support API access through PRAW is currently not in the scope of this project.

## Technologies
- <img src="https://user-images.githubusercontent.com/25181517/183569191-f32cdf03-673f-4ae3-809b-3a8b376bb8a2.png" width="20"> Elasticsearch
- <img src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png" width="20"> Python
- Python Libraries: Alpaca, PRAW, Transformers, Pillow, Ttkthemes, pygame.

## Installation

To install the required dependencies, follow the steps below:

1. [PRAW][1]:
   Install `praw` by running the following command:

```
pip install praw
```

2. Create a `praw.ini` file in the Reddit directory with the following format:

```ini
[BearishBetsBot]
client_id=your_client_id
client_secret=your_client_secret
user_agent=your_user_agent
```

3. [ALPACA][2]:
   Install the `Alpaca SDK` by running the following command:

```
pip install alpaca-py
```

4. Create an `alpaca.ini` file in the Alpaca directory with the following format:

```ini
[BearishBetsBot]
API_KEY=your_key_id
API_SECRET=your_secret_key
```

5. [Transformers][3]:
   Install `Transformers` by running the following command:

```
pip install transformers
```
6. [Pillow][4]:
   **Render Gifs in GUI** Install `Pillow` by running the following command:

```
pip install pillow
```
7. [ttkthemes][5]:
   **GUI** Install `ttkthemes` by running the following command:

```
pip install ttkthemes
```

7. [pygame]:
   **Sound Effects** Install `pygame` by running the following command:

```
pip install pygame
```

8. The Elasticsearch cluster should be setup on port 9200.

9. [TextBlob]:
   Install `TextBlob` by running the following command:

```
pip install textblob
```

10. [Download data]:
   Install `NLTK Language Model` by running the following command:

```
python -m textblob.download_corpora
```

11. [Docker][6]:
   Install `Docker`

12. [Elasticsearch][7]:
   Install `Elasticsearch` with Docker by running the following comands:

```
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.8.2
docker network create elastic
```

## Directories
Alpaca
- Trades.py - functions to buy and sell stocks on Alpaca

Data
- new_posts_2023-06-20_20-30-48.json - local json of Reddit data
- SortedStock.json - list of stock tickers/identifiers for ElasticSearch

ElasticSearchSequence
- Contains functions for initializing ElasticSearch data and queries for data
- Data with posts matched to stock/sentiment analysis

Reddit
- Read.py - functions for collecting Reddit data
- SentimentAnalysisPreprocessing.py - appends sentiment analysis to Reddit data
- StockPrice Determination

## Usage

User will define parameters for a strategy and can get recomendations by stock.

## Contributing

State if you are open to contributions and what your requirements are for accepting them.

## License
MIT License

Copyright (c) 2023 Bear-ish-Bets

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[1]: https://praw.readthedocs.io/en/stable/
[2]: https://alpaca.markets/docs/introduction/
[3]: https://pypi.org/project/transformers/
[4]: https://pillow.readthedocs.io/en/stable/
[5]: https://ttkthemes.readthedocs.io/en/latest/
[6]: https://docs.docker.com/engine/install/
[7]: https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html
