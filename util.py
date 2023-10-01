import numpy as np
import openai
from metaphor_python import Metaphor
from transformers import pipeline
import re
from sentence_transformers import SentenceTransformer, util
import requests

# Here but can move to a seperate file
METAPHOR_KEY = ''
OPENAI_KEY = ''
openai.api_key = OPENAI_KEY
metaphor = Metaphor(METAPHOR_KEY)



def generate_query(topic):
    """Generate a query string for a given topic using OpenAI's GPT-3.5 Turbo."""
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": f"Generate a short search query for the topic: {topic}"},
    ],
    )
    return response

def search_topic(topic):
    """Conduct a search on a given topic using the Metaphor API."""

    response = metaphor.search(
        topic,
        num_results=10,
        use_autoprompt=True,
    )
    return response

def get_notes(content_dict):
    """Generate detailed academic notes from a content dictionary using OpenAI's GPT-3.5 Turbo."""
    all_text = ""
    for cont in content_dict:
        text = ""
        text += f'\n The link for this article is: {cont} \n'
        text += content_dict[cont] + "\n"
        all_text += text 

    SYSTEM_MESSAGE = "You are an academic researcher. Present the information as a summary for academic notes on the given topic for a student to understand the topic." +  \
        "Make the text coherent and understandable. Cite all sources at the end of the article."

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": all_text},
        ],
    )
    return completion

def categorize_content(content_list):
    """Categorize a list of content into text and video based on their URLs."""
    text_cont = []
    video_cont = []
    for content in content_list:
        if re.search(r"youtube\.com", content.url):
            video_cont.append(content)
        else:
            text_cont.append(content)
    return text_cont, video_cont

def get_most_relevant_content(text_content, query):
    """Find the most relevant content from a list of text content using a paraphrasing sentence transformer and embeddings."""
    titles = [content.title for content in text_content]
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    titles_plus_query = titles + [query]
    embeddings = model.encode(titles_plus_query, convert_to_tensor=True)
    query_embedding = embeddings[-1]
    scores = util.pytorch_cos_sim(query_embedding, embeddings[:-1])[0]
    relevant_indices = scores.argsort(descending=True)
    relevant_content = [text_content[i] for i in relevant_indices]
    return relevant_content

def fetch_contents(contents):
    """Fetch and organize content extracts from a list of content objects into a dictionary based on URLs."""
    url_dict = {}
    for cont in contents:
        url_dict[cont.url] = cont.extract
    return url_dict


def generate_academic_notes(topic):
    """Generate academic notes on a given topic by executing a series of content discovery, categorization, and note generation steps."""
    query = generate_query(topic)
    print("Query: ")

    search_response = search_topic(query.choices[0].message.content)
    print(search_response.get_contents().contents)

    text_content, video_content = categorize_content(search_response.get_contents().contents)

    relevant_content = get_most_relevant_content(text_content, query)

    # For simplicity picking top 3 most relevent responses
    content = fetch_contents(relevant_content[:3])
    notes_response = get_notes(content)
    notes = notes_response.choices[0].message.content
    return notes