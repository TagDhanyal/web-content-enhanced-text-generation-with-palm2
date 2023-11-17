from flask import Flask, render_template, request
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import WebBaseLoader
from langchain.llms import GooglePalm
import os
from dotenv import load_dotenv

# Load environment variables from config.env
load_dotenv('config.env')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    query = request.form['query']

    google_api_key = os.getenv('GOOGLE_API_KEY')
    llm = GooglePalm(google_api_key=google_api_key)
    llm.temperature = 0.1

    urls = ["https://blogs.nasa.gov/artemis/"]
    loader = WebBaseLoader(urls)
    documents = loader.load_and_split()

    chain = load_qa_chain(llm=llm, chain_type="stuff", verbose=True)
    answer = chain.run(input_documents=documents, question=query)

    return render_template('index.html', query=query, answer=answer)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')