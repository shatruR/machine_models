# News Summarizer Application

## Overview

The News Summarizer Application is a Flask-based web service that fetches, processes, and summarizes articles from multiple URLs. Using OpenAI's language model via LangChain, the application provides detailed and coherent summaries for articles, ensuring completeness and maintaining context.

## Features

- **Multiple URL Handling**: Accepts and processes multiple URLs in a single request, removing duplicates to optimize performance.
- **Detailed Summarization**: Provides nuanced and comprehensive and presentable summaries that cover major points and sub-points of the articles.
- **Error Handling**: Gracefully handles errors in fetching and summarizing articles, providing meaningful feedback for each URL.
- **Efficient Chunking**: Splits large texts into manageable chunks with overlaps while maintaining sentence boundaries to ensure summaries are not cut off mid-sentence and the context of the article isn't lost.
- **Sequential Processing**: Each article is processed sequentially, ensuring only one article is loaded into memory at a time.
- **Summarization Delay**: Added delays between API calls to avoid rate limiting and excessive memory spikes.

## Installation
- langchhain
- langchain_community
- python_dotenv
- bs4
- flask
### Prerequisites

- Python 3.8 or higher
- An OpenAI API key
- LANGCHAIN API KEY

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/news-summarizer-app.git
    cd news-summarizer-app
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    LANGCHAIN_API_KEY=your_langchain_api_key
    LANGHAIN_PROJECT_NAME= your_project_name
    ```

5. **Run the application**:
    ```bash
    python app.py
    ```

## Usage

### Endpoint

- **POST /summarize**

    **Description**: Summarizes articles from the provided URLs.

    **Request Body**:
    ```json
    {
        "urls": [
            "https://example.com/article1",
            "https://example.com/article2",
            ...
        ]
    }
    ```

    **Response**:
    ```json
    [
        {
            "url": "https://example.com/article1",
            "title": "Article 1 Title",
            "date": "2024-07-23T14:10:19.000Z",
            "summary": "Comprehensive summary of article 1...",
            "data": "Full text content of article 1..."
        },
        {
            "url": "https://example.com/article2",
            "title": "Article 2 Title",
            "date": "2024-07-23T14:10:19.000Z",
            "summary": "Comprehensive summary of article 2...",
            "data": "Full text content of article 2..."
        }
    ]
    ```

### Example

To summarize articles, you can use tools like `curl`:
```sh
curl -X POST http://127.0.0.1:5000/summarize -H "Content-Type: application/json" -d '{
    "urls": [
        "https://example.com/article1",
            "https://example.com/article2",
        "https://example.com/article2",
        "https://example.com/article3",
        "https://example.com/article4",
        "https://example.com/article5"
    ]
}'
