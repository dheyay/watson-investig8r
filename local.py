from util import *
import click

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
    notes_response = get_notes(content)
    notes = notes_response.choices[0].message.content

    with open("generated_notes.txt", 'w') as file:
        file.write(notes)
    
    print(notes + "\n")
    print("Notes have been saved to text file: generated_notes.txt")

if __name__ == '__main__':
    main()