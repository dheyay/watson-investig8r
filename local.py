from util import *
import click

def get_notes_local(content_dict):
    """Generate detailed academic notes from a content dictionary using OpenAI's GPT-3.5 Turbo."""
    all_text = ""
    for cont in content_dict:
        text = ""
        text += f'\n The link for this article is: {cont} \n'
        text += content_dict[cont] + "\n"
        all_text += text 

    SYSTEM_MESSAGE = "You are a helpful assitant with teaching experience. Present the information as a summary on the given topic for a student to understand the topic." +  \
        "Make the text coherent and understandable. Cite sources at the end"
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": all_text},
        ],
    )
    return completion

@click.command()
@click.option('--topic', prompt='Enter your query', help='The query for generating academic notes.')
def main(topic):
    """Generate academic notes on a given topic by executing a series of content discovery, categorization, and note generation steps."""
    query = generate_query(topic)
    search_response = search_topic(query.choices[0].message.content)
    text_content, video_content = categorize_content(search_response.get_contents().contents)
    relevant_content = get_most_relevant_content(text_content, query)

    # For simplicity picking top 3 most relevent responses
    content = fetch_contents(relevant_content[:3])
    notes_response = get_notes_local(content)
    notes = notes_response.choices[0].message.content

    with open("generated_notes.txt", 'w') as file:
        file.write(notes)
    
    print(notes + "\n")
    print("Notes have been saved to text file: generated_notes.txt")

if __name__ == '__main__':
    main()