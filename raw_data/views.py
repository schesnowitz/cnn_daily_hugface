from django.shortcuts import render
from .models import NewsData
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
import datasets



# def load_news(news_data):
#   """ Loads N articles from the 'cnn_dailymail' dataset, in streaming mode """

#   dataset = datasets.load_dataset(news_data, split="train", streaming=False) 
#   # data = dataset.take(1)
#   print(len(dataset))


def vectorizie(data):
    embeddings = OpenAIEmbeddings()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = splitter.create_documents(data)  # creates Document objects from the text in the articles
    document_chunks = splitter.split_documents(documents)  # splits the Documents into chunks
    print(document_chunks)
    print("hello  ")

def index(request):
  news = NewsData.objects.all()
  # for item in news:
  #   news_content = item.content.replace("  ", "")
  #   load_news(news_content)  
  news_loop(news)

  return render(request, 'raw_data/index.html')


def news_loop(news):
  for item in news:
    news_content = item.content.replace("  ", "")
    vectorizie(news_content)

    # print(news_content)