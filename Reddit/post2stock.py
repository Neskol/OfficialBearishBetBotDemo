from textblob import TextBlob
from nltk.stem.snowball import EnglishStemmer

def nouns_array_of_txt(text:str):
    candidate_arr = TextBlob(text).noun_phrases
    ## print(candidate_arr)
    result_arr = []
    for candidate in candidate_arr:
        for word in candidate.split():
            result_arr.append(word)
    return result_arr

def nouns_array_of_stock(text:str):
    candidate_arr = text.split()
    result_arr = []
    for candidate in candidate_arr:
        for word in candidate.split(','):
            result_arr.append(word)
    return result_arr

def nouns_correlation(post_noun_arr,stock_noun_arr):
    stemmer = EnglishStemmer()
    # Pre-process stock_arr to reduce running time
    for s in stock_noun_arr:
        s = stemmer.stem(s)
    distinct_noun_count = 0
    total_noun_count = 0
    appeared_noun_arr = []
    for p_noun in post_noun_arr:
        stemmer.stem(p_noun) # reduces a word to its dictionary form
        for s_noun in stock_noun_arr:
            if p_noun.upper() == s_noun.upper():
                if not s_noun in appeared_noun_arr:
                    appeared_noun_arr.append(s_noun)
                total_noun_count += 1
    distinct_noun_count = len(appeared_noun_arr)
    # Distinct overlapped n. * (total overlapped n. / total n.) : n. is Post_noun
    if (len(post_noun_arr)>0): return distinct_noun_count * (total_noun_count / len(post_noun_arr))
    else: return 0

# txt = "NVIDIA may launch their new graphics card RTX5090 by next year. Do you guys think I should by its stock now and/or buy stock in technology sector as well?"
# stock = "NVDA, NVIDIA Corporation, Technology, Semiconductor"
# stock2 = "NVVA, NVE Corporation, Technology, Semiconductor"
# stock3 = "QUAD,Quad Graphics Inc, Consumer Discretionary,Publishing"
# txt = nouns_array_of_txt(txt)
# stock = nouns_array_of_stock(stock)
# stock2 = nouns_array_of_stock(stock2)
# stock3 = nouns_array_of_stock(stock3)
# print(txt)
# print(stock)
# print(stock2)
# print(stock3)
# print(nouns_correlation(txt,stock))
# print(nouns_correlation(txt,stock2))
# print(nouns_correlation(txt,stock3))
