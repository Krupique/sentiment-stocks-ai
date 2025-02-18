# Sentiment Stocks AI

## Overview  

**Sentiment-Stocks-AI** is a project that utilizes sentiment analysis techniques on real-time news to assist in stock investment decision-making. The system collects news about a specific company, analyzes the sentiment of these news articles using language models (LLMs), and combines this analysis with historical stock price data to recommend an investment decision: **Buy**, **Hold**, or **Sell**.  

The project is divided into two main versions:  
1. **DeepSeek Version**: Uses the **DeepSeek** model (via Ollama) for sentiment analysis.  
2. **GPT Version**: Uses the **GPT-4** model (from OpenAI) for sentiment analysis.  

Both versions follow the same logic but differ in the choice of the language model, allowing a comparison of performance and costs between a proprietary LLM (GPT) and an open-source LLM (DeepSeek).  

---  

## Project Structure  

The project is organized as follows:  

```
Sentiment-Stocks-AI/
├── app/
│   ├── run_deepseek.py       # Script for analysis with DeepSeek
│   └── run_gpt.py            # Script for analysis with GPT
├── notebooks/
│   └── exploratory_analysis.ipynb  # Exploratory data analysis
├── ignore/
│   └── keys.json             # File containing API keys (NewsAPI and OpenAI)
├── .gitignore                # File to ignore sensitive files
├── poetry.lock               # Poetry lockfile for dependencies
├── pyproject.toml            # Poetry configuration
└── README.md                 # Project documentation
```  

---  

## Algorithm Workflow  

The algorithm follows a well-defined workflow, summarized in five main steps:  

### 1. News Collection  
- **Source**: Uses **NewsAPI** to collect real-time news about the target company.  
- **Filters**:  
  - News in English (`language='en'`).  
  - Sorted by relevance (`sort_by='relevancy'`).  
  - Limit of 20 news items (`page_size=20`).  
- **Output**: A list of news headlines.  

### 2. Stock Data Collection  
- **Source**: Uses the **yfinance** library to obtain historical stock data.  
- **Period**: Last month (`period='1mo'`).  
- **Collected Data**: Closing price (`Close`) and daily percentage change (`Pct_Change`).  

### 3. Sentiment Analysis  
- **Language Model**:  
  - **DeepSeek**: Uses the `deepseek-r1:7b` model via Ollama.  
  - **GPT**: Uses the `gpt-4o` model from OpenAI.  
- **Prompt**: The model receives the news headline and classifies the sentiment as **positive**, **negative**, or **neutral**.  
- **Prompt Example**:  
  ```plaintext
  Classify the sentiment of the following news item title about {company} as 'positive', 'negative', or 'neutral': "{news_title}"
  ```
- **Output**: A list of sentiment classifications corresponding to the news articles.  

### 4. Sentiment Conversion to Numerical Values  
- **Mapping**:  
  - `positive` → `1`  
  - `neutral` → `0`  
  - `negative` → `-1`  
- **Output**: A list of numerical scores representing the sentiments.  

### 5. Decision-Making  
- **Inputs**:  
  - Recent stock price percentage change (`recent_change`).  
  - Average sentiment score (`avg_sentiment`).  
- **Decision Logic**:  
  - **Buy**: If `avg_sentiment > 0` and `recent_change > 0`.  
  - **Sell**: If `avg_sentiment < 0` and `recent_change < 0`.  
  - **Hold**: Otherwise.  

---  

## Technical Details  

### Dependencies  
The project uses the following Python libraries:  
- **requests**: For making HTTP requests to NewsAPI.  
- **yfinance**: For retrieving stock data.  
- **numpy**: For numerical calculations.  
- **langchain**: For integrating the DeepSeek model via Ollama.  
- **openai**: For integrating with GPT-4.  
- **newsapi**: For accessing the news API.  

### Configuration  
- **API Keys**:  
  - The NewsAPI and OpenAI keys are stored in the `ignore/keys.json` file.  
  - Example `keys.json` file:  
    ```json
    {
        "news_api": "your_newsapi_key",
        "gpt": "your_openai_key"
    }
    ```
- **Installation**:  
  - The project uses **Poetry** for dependency management. To install dependencies, run:  
    ```bash
    poetry install
    ```  

### Execution  
- **DeepSeek**:  
  ```bash
  poetry run python app/run_deepseek.py --company "Apple" --ticker "AAPL"
  ```  
- **GPT**:  
  ```bash
  poetry run python app/run_gpt.py --company "Apple" --ticker "AAPL"
  ```  

---  

## Example Output  

When executing the script, the program displays:  
1. Number of collected news items.  
2. Sentiment analysis results for each news item.  
3. Final investment decision.  

**Example**:  
```
Number of news items retrieved: 15

The AI Investing Robot is Working. Please wait!

Sentiment: positive     Apple launches new iPhone
Sentiment: neutral      Apple CEO attends tech conference
Sentiment: negative     Apple faces lawsuit over privacy concerns
...

Investment Decision: Buy

Thanks for Using Sentiment Stocks AI - Come Back Soon!
```  

---  

## Final Considerations  

### When to Use DeepSeek vs. GPT  
- **DeepSeek**:  
  - Ideal for scenarios where cost is a concern, as it is an open-source model.  
  - Can be run locally without reliance on external APIs.  
- **GPT**:  
  - Offers higher accuracy and consistency in sentiment analysis.  
  - Requires a paid OpenAI API key.  

### Limitations  
- **News Quality**: Depends on the relevance and accuracy of news collected via NewsAPI.  
- **Model Accuracy**: Sentiment analysis results may vary depending on the chosen model.  
- **Market Volatility**: Decisions based solely on news and recent stock prices may not capture long-term trends.  

### Future Improvements  
- Add support for more news sources.  
- Implement sentiment analysis on full news articles (not just headlines).  
- Integrate machine learning techniques for price prediction.  

---  

## Conclusion  

**Sentiment-Stocks-AI** is a powerful tool for investors looking to incorporate sentiment analysis into their decision-making strategies. By combining real-time news, market data, and advanced language models, the project offers an innovative approach to investment analysis.