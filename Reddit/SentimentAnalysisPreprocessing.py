from transformers import pipeline
from post2stock import *
import json
import csv

def SentimentAnalysisPreprocessing(reddit_json):
	# Load in the reddit hot posts from json
	data = open(reddit_json)
	# Perform sentiment analysis on the reddit data
	pipe = pipeline("sentiment-analysis")
	json_data = json.load(data)
	json_list = []

	with open('Data/SortedStock.json', 'r') as file:
		stock_data = json.load(file)

	stock_list = SelectStockOnText()
	mentioned_stock_list = []
	mentioned_stock_json_list = []

	earliest_time = ''
	latest_time = ''

	total_case = len(json_data)
	current_case = 0
	with open('Data/CorrelatedPost2Stock_75.json', 'w') as file:
		for entry in json_data:
			# compare earliest time
			if earliest_time == '': earliest_time = entry['created_utc']
			elif earlier_time(earliest_time,entry['created_utc']): earliest_time = entry['created_utc']

			# compare latest time
			if latest_time  == '': latest_time = entry['created_utc']
			elif earlier_time(entry['created_utc'],latest_time): latest_time = entry['created_utc']

			pipe_result = pipe(entry['title'])

			keywords = nouns_array_of_txt(entry['title'] + entry['selftext'])
			best_correlation = 0
			best_stock = []
			for stock in stock_list:
				stock_noun_candidate = nouns_array_of_stock(stock)
				current_correlation = nouns_correlation(keywords,stock_noun_candidate)
				if current_correlation >= best_correlation and current_correlation > 0.75 and len(best_stock)<3:
					best_correlation = current_correlation
					best_stock.append(stock.split()[0])
					if not stock.split()[0] in mentioned_stock_list :
						mentioned_stock_list.append(stock.split()[0])
						for stock_json in stock_data:
							if stock_json['ticker'] == stock.split()[0]: mentioned_stock_json_list.append(stock_json)

			post_dict = {
				"score" : entry['score'],
				"title" : entry['title'],
				"self-text" : entry['selftext'],
				"time-stamp" : entry['created_utc'],
				"emotion-score" : pipe_result[0]['score'],
				"emotion-type" : pipe_result[0]['label'],
				# Keywords will be an array from function
				"keywords": keywords,
				"stock-related":best_stock,
				"correlation":best_correlation
			}

			# print(post_dict)
			current_case+=1
			print(f"Case {current_case} out of {total_case} with valid cases of {len(json_list)}, earliest = {earliest_time}, latest = {latest_time}, mentioned stock = {len(mentioned_stock_list)}")

			if (len(best_stock)>0): json_list.append(post_dict)

		# Write the list of dictionaries to a JSON file
		json.dump(json_list, file, indent=4)
	with open('Reddit/mentioned_stock.json','w') as file:
		json.dump(mentioned_stock_json_list, file, indent=4)
	print(mentioned_stock_list)
	return json_list

def stock_preprocessing():
	csv_file = 'Data/stocks.csv'
	json_file = 'Data/SortedStock.json'

	# Read the CSV file and convert it to a list of dictionaries
	csv_data = []
	with open(csv_file, 'r') as file:
		csv_reader = csv.DictReader(file)
		for row in csv_reader:
			# Extract the required attributes from each row
			ticker = row['Symbol']
			name = row['Name']
			industry = row['Industry']
			sector = row['Sector']

			# Create a dictionary for each row
			json_data = {
				'ticker': ticker,
				'name': name,
				'industry': industry,
				'sector': sector
			}

			# Append the dictionary to the list
			csv_data.append(json_data)

	# Write the list of dictionaries to a JSON file
	with open(json_file, 'w') as file:
		json.dump(csv_data, file, indent=4)

def SelectStockOnText():
	json_file = 'Data/SortedStock.json'
	# Read the JSON file
	with open(json_file, 'r') as file:
		data = json.load(file)
	result = []
	# Iterate over the objects in the JSON data
	for obj in data:
		# Access the attributes for each object
		ticker = obj['ticker']
		name = obj['name']
		industry = obj['industry']
		sector = obj['sector']
		result.append(f"{ticker} {name} {industry} {sector}")
	return result

# return true if current_time is earlier than best_time
def earlier_time(best_time,current_time):
	best_time_array = best_time.split()
	current_time_array = current_time.split()
	best_date_array = best_time_array[0].split('-')
	current_date_array = current_time_array[0].split('-')
	best_tick_array = best_date_array[1].split(':')
	current_tick_array = current_date_array[1].split(':')
	for i in range(len(best_date_array)):
		if current_date_array[i] < best_date_array[i]: return True
	for i in range(len(best_tick_array)):
		if current_tick_array[i] < best_tick_array[i]: return True
	return False

SentimentAnalysisPreprocessing('Data/new_posts_2023-06-20_20-30-48.json')
