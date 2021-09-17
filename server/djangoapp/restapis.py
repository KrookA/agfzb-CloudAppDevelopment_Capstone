import requests
import json
import os
from dotenv import load_dotenv
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

load_dotenv()
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, apikey, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if apikey:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', apikey))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cloudant(url, **kwargs):
    results = []
    if "state" in kwargs:
        json_result = get_request(url, False, state=kwargs["state"])
    elif "dealerId" in kwargs:
        json_result = get_request(url, False, dealerId=kwargs["dealerId"])
    else:
        json_result = get_request(url, False)

    if json_result:
        dealers = json_result["entries"]
        for dealer in dealers:
            dealer_obj = CarDealer(dealer)
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cloudant(url, dealerId):
    results = []
    json_result = get_request(url, "", dealerId=dealerId)

    if json_result:
        reviews = json_result["entries"]
        for review in reviews:
            review_obj = DealerReview(review)
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = os.getenv("NLU_URL")
    apikey = os.getenv("NLU_APIKEY")
    text = text
    version = "2021-08-01"
    return_analyzed_text = True
    features = "sentiment"
    result = get_request(url, apikey, text=text, version=version, return_analyzed_text=return_analyzed_text, features=features)
    return result["sentiment"]["document"]["label"]
