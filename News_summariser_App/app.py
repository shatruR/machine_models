import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, abort
import requests
from bs4 import BeautifulSoup
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import time

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

app = Flask(__name__)

# Initialize the OpenAI model with LangChain
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model = OpenAI(api_key=openai_api_key, model_name="gpt-3.5-turbo-instruct")

# Define prompt templates for detailed summaries
prompt_template0 = PromptTemplate(
    input_variables=["text"],
    template="""Read the complete text, process it providing a coherent and concise summary of the text. Ensure that the summary does not get cut off in between: {text}"""
)

prompt_template1 = PromptTemplate(
    input_variables=["text"],
    template="""Read the complete article, process it providing a coherent and concise summary by breaking it into exactly 5 major points with up to 3 sub-points each. Ensure no point is cut off in between: {text}"""
)

# Create LLMChains for summarization
summarization_chain0 = LLMChain(llm=openai_model, prompt=prompt_template0)
summarization_chain1 = LLMChain(llm=openai_model, prompt=prompt_template1)

def fetch_article_content(url):
    """Fetches and parses article content from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else 'No Title'
        date = soup.find('meta', {'property': 'article:published_time'})
        date = date['content'] if date else 'No Date'
        
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text() for p in paragraphs])
        
        return {'title': title, 'date': date, 'content': content}
    except requests.RequestException as e:
        print(f"Error fetching article: {e}")
        return None

def chunk_text(text, max_tokens=1000, overlap=200):
    """Splits text into chunks with overlap to maintain context."""
    tokens = text.split()
    for start in range(0, len(tokens), max_tokens - overlap):
        end = min(start + max_tokens, len(tokens))
        chunk = tokens[start:end]
        yield ' '.join(chunk)

def summarize_chunks(chunks):
    """Summarizes each chunk of text."""
    for chunk in chunks:
        summary = summarization_chain0.run(text=chunk)
        time.sleep(5)  # To avoid rate limiting
        yield summary

def combine_and_summarize(summaries):
    """Combines chunk summaries and performs a final summarization."""
    combined_summary = ' '.join(summaries)
    final_summary = summarization_chain1.run(text=combined_summary)
    time.sleep(5)  # To avoid rate limiting
    return final_summary

def summarize_large_text(text):
    """Handles large text by chunking, summarizing, and combining summaries."""
    chunk_generator = chunk_text(text)
    chunk_summaries = list(summarize_chunks(chunk_generator))
    final_summary = combine_and_summarize(chunk_summaries)
    return final_summary

@app.route('/summarize', methods=['POST'])
def summarize_articles():
    """Endpoint to summarize multiple articles."""
    data = request.get_json()
    urls = data.get('urls', [])

    if not urls:
        abort(404, description="No URLs provided")

    # Remove duplicate URLs
    unique_urls = list(set(urls))

    results = []

    for url in unique_urls:
        article_data = fetch_article_content(url)
        time.sleep(5)  # To avoid rate limiting
        if article_data:
            try:
                summary = summarize_large_text(article_data['content'])
                time.sleep(5)  # To avoid rate limiting
                results.append({
                    'url': url,
                    'title': article_data['title'],
                    'date': article_data['date'],
                    'summary': summary,
                    'data': article_data['content']
                })
            except Exception as e:
                print(f"Error summarizing article from {url}: {e}")
                time.sleep(5)  # To avoid rate limiting
                results.append({
                    'url': url,
                    'title': article_data['title'],
                    'date': article_data['date'],
                    'summary': 'Error processing the article',
                    'data': article_data['content']
                })
        else:
            results.append({
                'url': url,
                'title': 'No Title',
                'date': 'No Date',
                'summary': 'Error fetching article content',
                'data': 'No content'
            })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
