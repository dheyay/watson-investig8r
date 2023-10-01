# watson-investig8r
Search support for LLM's to find what you want. Generates short notes on a search topic, gives the LLM power to find recent information on new topics or any topic in general and present it as notes to you. 

## Setup to run locally

Create a keys.py file to add your own OPENAI api key and METAPHOR api key.

```python
METAPHOR_KEY = 'your-metaphor-key-here'
OPENAI_KEY = 'your-openai-key-here'

```
In your terminal, install the required packages.

```python
pip install -r requirements.txt
```

Setup the FLASK env variable.
```python
export FLASK_APP=app.py
```

Run the Flask app.
```python
flask run
```

Follow the link in the terminal or Open your web browser and go to http://127.0.0.1:5000.

## Using CLI

If you don't want to go through the pain of setting up a Flask UI, you can also run the notes generator locally. 
Navigate to this folder in your terminal and run the local.py file.

```python
python local.py
```
