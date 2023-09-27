from django.shortcuts import render
import datasets
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_articles(n=5):
    """ Loads N articles from the 'cnn_dailymail' dataset, in streaming mode """
    dataset = datasets.load_dataset("cnn_dailymail", '3.0.0', split="train", streaming=True)
    data = dataset.take(n)
    return [d['article'] for d in data]

articles = load_articles()
print(articles[0])

def vectorizie(articles):
    embeddings = OpenAIEmbeddings()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = splitter.create_documents(articles)  # creates Document objects from the text in the articles
    document_chunks = splitter.split_documents(documents)  # splits the Documents into chunks
    print(document_chunks[0])
    print("hello  ")

def index(request):

  return render(request=request, template_name="cnn_daily/index.html")
