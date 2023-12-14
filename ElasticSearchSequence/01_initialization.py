from elasticsearch import Elasticsearch
import json

# Connect to the local Elasticsearch server
es = Elasticsearch(hosts=["http://localhost:9200"])

# Check if the "user_post" index exists
if not es.indices.exists(index="user_post"):
    # Create the "user_post" index
    es.indices.create(index="user_post")
    print("Created index 'user_post'")

# Check if the "related_stock" index exists
if not es.indices.exists(index="related_stock"):
    # Create the "related_stock" index
    es.indices.create(index="related_stock")
    print("Created index 'related_stock'")

# Check if "user_post" index is empty
user_post_count = es.count(index="user_post")["count"]
if user_post_count == 0:
    try:
        # Search for "CorrelatedPost2Stock_75.json" and import records into "user_post" index
        with open("ElasticSearchSequence/Data/CorrelatedPost2Stock.json") as file:
            data = json.load(file)
            for record in data:
                es.index(index="user_post", body=record)
        print(f"Uploaded {len(data)} records to 'user_post' index")
    except FileNotFoundError:
        print("CorrelatedPost2Stock.json not found")
    except Exception as e:
        print(f"Error occurred while uploading records to 'user_post' index: {str(e)}")

# Check if "related_stock" index is empty
related_stock_count = es.count(index="related_stock")["count"]
if related_stock_count == 0:
    try:
        # Search for "Input_Stock.json" and import records into "related_stock" index
        with open("ElasticSearchSequence/Data/mentioned_stock.json") as file:
            data = json.load(file)
            for record in data:
                es.index(index="related_stock", ignore=400, body=record)
        print(f"Uploaded {len(data)} records to 'related_stock' index")
    except FileNotFoundError:
        print("mentioned_stock.json not found")
    except Exception as e:
        print(f"Error occurred while uploading records to 'related_stock' index: {str(e)}")

# Prompt the user for the number of records uploaded and any errors that occurred
user_post_count = es.count(index="user_post")["count"]
related_stock_count = es.count(index="related_stock")["count"]

print(f"\n--- Summary ---")
print(f"Number of records uploaded to 'user_post' index: {user_post_count}")
print(f"Number of records uploaded to 'related_stock' index: {related_stock_count}")
