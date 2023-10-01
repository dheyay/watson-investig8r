from flask import Flask, render_template, request
from util import generate_academic_notes
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ''
    if request.method == 'POST':
        topic = request.form['topic']
        summary = generate_academic_notes(topic)
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
