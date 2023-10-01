from flask import Flask, render_template, request
from util import generate_academic_notes, get_embedded_links
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ''
    embedded_links = []
    if request.method == 'POST':
        topic = request.form['topic']
        summary, video_urls = generate_academic_notes(topic)
        embedded_links = get_embedded_links(video_urls[:2])
    return render_template('index.html', summary=summary, embedded_links=embedded_links)

if __name__ == '__main__':
    app.run(debug=True)
