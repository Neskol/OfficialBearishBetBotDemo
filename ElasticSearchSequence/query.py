from elasticsearch import Elasticsearch
import json
from Alpaca.MakeTrade import make_trade_decision

# Helper iterator: iterates all documents under given index
def es_iterate_all_documents(es, index, pagesize=250, **kwargs):
    """
    Helper to iterate ALL values from
    Yields all the documents.
    """
    offset = 0
    while True:
        result = es.search(index=index, **kwargs, body={
            "size": pagesize,
            "from": offset
        })
        hits = result["hits"]["hits"]
        # Stop after no more docs
        if not hits:
            break
        # Yield each entry
        yield from (hit['_source'] for hit in hits)
        # Continue from there
        offset += pagesize

def query_posts_for_stock(es,ticker, callback=None):
  if ticker == None or ticker == '':
       print("It looks like you didn't input anything. Here are some suggestions")
       if(callback):
          callback("It looks like you didn't input anything. Here are some suggestions")
       es = Elasticsearch(hosts=["http://localhost:9200"])
       for entry in es_iterate_all_documents(es, 'related_stock'):
          print(entry['ticker'])
          if(callback):
            callback(entry['ticker'])
  else:
    try:
      # Get stock item to search posts
      sorted_stock_json = open("Data/SortedStock.json")
      sorted_stock_obj = json.load(sorted_stock_json)
      stock = next(stock for stock in sorted_stock_obj if stock['ticker'] == ticker)
      # print(stock)

      # Parse identifiers
      stock_identifiers = str(str(stock['ticker']) + ' ' + str(stock['name']) + ' ' + str(stock['industry']) + ' ' + str(stock['sector']))
      # print(stock_identifiers)

      query = {
          "query": {
            "match": {
              "stock-related": ticker
            }
          }
      }

      # Return query
      results = es.search(index='user_post', body=query)
      # print("Got %d Hits:" % results['hits']['total']['value'])
      posts = []
      avg_score = 0.0
      avg_emotion_score = 0.0
      avg_correlation = 0.0
      hits =0
      for hit in results['hits']['hits']:
          # reddit_score, emotion_score, emotion_type, ticker, correlation_to_stock
          # print("Score: ", hit["_source"]["score"],
          #       "Emotion-score: ", hit["_source"]["emotion-score"],
          #       "Emotion-type: ", hit["_source"]["emotion-type"],
          #       "Stock-related: ", hit["_source"]["stock-related"],
          #       "Correlation: ", hit["_source"]["correlation"])

          avg_score+=int(hit["_source"]["score"])
          if hit["_source"]["emotion-type"] == "POSITIVE":
            avg_emotion_score += float(hit["_source"]["emotion-score"])
          elif hit["_source"]["emotion-type"] == "NEGATIVE":
            avg_emotion_score -= float(hit["_source"]["emotion-score"])
          avg_correlation += int(hit["_source"]["correlation"])
          hits += 1

          posts.append(
                        {
                        "source" : hit["_source"]["score"],
                        "emotion-score" : hit["_source"]["emotion-score"],
                        "emotion-type" : hit["_source"]["emotion-type"],
                        "stock-related" : hit["_source"]["stock-related"],
                        "correlation" : hit["_source"]["correlation"]
                        }
                      )
      if (hits > 0):
        avg_score/=hits
        avg_correlation/=hits
        avg_emotion_score/=hits
        emotion_type = "POSITIVE"
        if avg_emotion_score < 0: emotion_type = "NEGATIVE"
        print(f"The final result for stock {ticker} is Avg_score: {avg_score}, Emotion type: {emotion_type}, Avg_Emotion_Score: {abs(avg_emotion_score)}, Avg_Correlation: {avg_correlation}")
        if callback:
          callback(f"The final result for stock {ticker} is Avg_score: {avg_score}, Emotion type: {emotion_type}, Avg_Emotion_Score: {abs(avg_emotion_score)}, Avg_Correlation: {avg_correlation}")
        # TRADE DECISION PROCESS
        make_trade_decision(avg_score, avg_emotion_score, emotion_type, ticker, avg_correlation, callback=callback)
      else:
        print(f"The stock {ticker} does not return hits and will be ignored for transaction")
        if callback:
          callback(f"The stock {ticker} does not return hits and will be ignored for transaction")
      return posts
    except Exception as e:
      print(f"Sorry but there was a problem trading with {ticker}... maybe it was for the best")
      if(callback):
          callback(f"Sorry but there was a problem trading with {ticker}... maybe it was for the best")

# test
# es = Elasticsearch(hosts=["http://localhost:9200"])
# for entry in es_iterate_all_documents(es, 'related_stock'):
#     print(entry['ticker'])
#     query_posts_for_stock(es,entry['ticker'])

