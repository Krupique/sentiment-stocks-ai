# Imports
import argparse
import requests
import json
import yfinance as yf
import numpy as np
from openai import OpenAI
from newsapi import NewsApiClient 

class SentimentStockAI():

    def __init__(self):
        pass



if __name__ == "__main__":
    # Argument parser for dynamic input
    parser = argparse.ArgumentParser(description="Generate text using an LLM")
    parser.add_argument(
        "--company",
        type=str,
        required=True,
        help="Company name"
    )

    parser.add_argument(
        "--ticker",
        type=str,
        required=True,
        help="ticker"
    )

    args = parser.parse_args()
    
    
    print("\nProject AI Investing - Using LLMs for Investment Analytics")

    # Setting the secret keys
    secret_key = '../ignore/keys.json'

    # Open and read Json file
    with open(secret_key, 'r', encoding='utf-8') as file:
        key = json.load(file)

    client = OpenAI(api_key = key['gpt'])
    newsapi = NewsApiClient(api_key = key['news_api'])
        