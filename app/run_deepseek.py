# Imports
import argparse
import requests
import json
import yfinance as yf
import numpy as np
from newsapi import NewsApiClient 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms.ollama import Ollama

class SentimentStockAI():

    def __init__(self, company, ticker):
        self.company = company
        self.ticker = ticker

    # Function to get news about a specific company
    def collect_news(self):
        # Makes a request to the NewsAPI to get articles about the company, in Portuguese and sorted by relevance
        all_articles = newsapi.get_everything(q = self.company, language = 'en', sort_by = 'relevancy', page_size = 20)

        # Initializes a list to store the news titles
        news_list = []

        # Goes through all the articles returned by the API
        for article in all_articles['articles']:
            # Extracts the title of each article
            title = article['title']

            # Checks if the title is not empty and if it does not contain '[Removed]'
            if title and '[Removed]' not in title:
                # Adds the valid title to the news list
                news_list.append(title)

        # Returns the list of news titles
        return news_list
    

    # Function to get stock data using the yfinance library
    def collect_stock_data(self):

        # Creates a Ticker object for the specified stock
        stock = yf.Ticker(self.ticker)

        # Gets historical stock data for the last month
        data = stock.history(period='1mo')

        # Returns historical stock data
        return data
    

    # Function to analyze the sentiment of a list of news items
    def analyze_sentiment(self, news_list):

        # Initialize a list to store the sentiments of the news items
        sentiments = []

        # Creating the parser for the language model output
        output_parser = StrOutputParser()

        # Loop through each news item in the news item list
        for news in news_list:

            # Set a prompt for the Llama model to analyze the sentiment of the news headline
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", f"Classify the sentiment of the following news item title about {self.company} as 'positive', 'negative', or 'neutral': "),
                    ("user", "question: {question}")
                ]
            )

            # Execution chain definition: prompt -> LLM -> output_parser
            chain = prompt | llm | output_parser

            # Execute the string with the given prompt and get the response
            response = chain.invoke({'question': news})

            # Convert to lowercase
            sentiment = response.strip().lower()

            # Check if sentiment is 'positive', 'negative' or 'neutral' and adds it to the list
            if sentiment in ['positive', 'negative', 'neutral']:
                sentiments.append(sentiment)
            else:
                # Add 'neutral' if sentiment is not identified
                sentiments.append('neutral')

        # Returns the list of sentiments
        return sentiments
    

    # Function to convert text sentiments to numeric values
    def convert_sentiment_to_numerical(self, sentiments):

        # Initialize a list to store numeric sentiment scores
        sentiment_scores = []

        # Loop through each sentiment in the sentiment list
        for sentiment in sentiments:

            # Assign 1 for 'positive'
            if 'positive' in sentiment:
                sentiment_scores.append(1)

            # Assign -1 for 'negative'
            elif 'negative' in sentiment:
                sentiment_scores.append(-1)

            # Assign 0 for 'neutral'
            else:
                sentiment_scores.append(0)

        # Returns the list of numeric scores
        return sentiment_scores
    

    # Function to make a decision based on stock data and sentiment
    def make_decision(self, stock_data, sentiment_scores):

        # Calculates the daily percentage change in the stock's closing price
        stock_data['Pct_Change'] = stock_data['Close'].pct_change()

        # Get the most recent percentage change
        recent_change = stock_data['Pct_Change'].iloc[-1]

        # Calculates the average of sentiments if there are values ​​in the list
        if sentiment_scores:
            avg_sentiment = np.mean(sentiment_scores)
        else:
            # Sets 0 as default value if the list is empty
            avg_sentiment = 0

        # Sets the decision based on sentiment values ​​and price change
        if avg_sentiment > 0 and recent_change > 0:
            decision = 'Buy'
        elif avg_sentiment < 0 and recent_change < 0:
            decision = 'Sell'
        else:
            decision = 'Keep'

        # Returns the final decision
        return decision
    

    def run(self):
        # Get the news about Apple
        news = self.collect_news()

        # Display the number of news items retrieved and the list of news items
        print(f"\nNumber of news items retrieved: {len(news)}")
        print("\nThe AI ​​Investing Robot is Working. Please wait!\n")

        # Check for news to analyze
        if not news:
            # Set 'Keep' as default decision if there is no news
            print("No news was retrieved.")
            decision = 'Keep'

            return decision, None, None

        else:
            # Analyze the sentiment of the news
            sentiments = self.analyze_sentiment(news_list=news)

            # Display the analyzed sentiments
            for i in range(len(sentiments)):
                print("Sentiment: {} \t {}".format(sentiments[i], news[i]))

            # Convert the sentiments into numeric values
            sentiment_scores = self.convert_sentiment_to_numerical(sentiments)

            # Make a decision based on the stock data and sentiments
            decision = self.make_decision(self.collect_stock_data(), sentiment_scores)

           

            return decision, sentiments, sentiment_scores


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
    secret_key = 'ignore/keys.json'

    # Open and read Json file
    with open(secret_key, 'r', encoding='utf-8') as file:
        key = json.load(file)

    # Instanciação do LLM Llama3.2 através do Ollama
    llm = Ollama(model = "deepseek-r1:7b")
    newsapi = NewsApiClient(api_key = key['news_api'])

    sentiment_stock_ai = SentimentStockAI(args.company, args.ticker)
    decision, sentiments, sentiment_scores = sentiment_stock_ai.run()

    # Display the final decision
    print(f"\nInvestment Decision: {decision}")
    print("\nThanks for Using Sentiment Stocks AI - Come Back Soon!\n")
        