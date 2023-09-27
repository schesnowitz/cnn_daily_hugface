
import datasets

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Cassandra
from langchain.document_loaders import TextLoader


def load_articles(n=4):
    """ Loads N articles from the 'cnn_dailymail' dataset, in streaming mode """
    dataset = datasets.load_dataset("cnn_dailymail", '3.0.0', split="train", streaming=True)
    data = dataset.take(n)
    return [d['article'] for d in data]

articles = load_articles()
print(type(articles))



text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.create_documents(str(articles))  # creates Document objects from the text in the articles
document_chunks = text_splitter.split_documents(documents) 



embedding_function = OpenAIEmbeddings(openai_api_key='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')



# embedding = OpenAIEmbeddings(openai_api_key='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')
# splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# documents = splitter.create_documents(articles)  # creates Document objects from the text in the articles
# document_chunks = splitter.split_documents(documents)  # splits the Documents into chunks


from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json


ASTRA_DB_SECURE_BUNDLE_PATH = 'vector_db_connect/secure-connect-vector-db.zip'
ASTRA_DB_TOKEN_JSON_PATH = 'vector_db_connect/vector_db-token.json'
ASTRA_DB_KEYSPACE = 'vector_db_keyspace'
print(f"ASTRA_DB_TOKEN_JSON_PATH:  {type(ASTRA_DB_TOKEN_JSON_PATH)}")
cloud_config= {
  "secure_connect_bundle": ASTRA_DB_SECURE_BUNDLE_PATH
}

with open(ASTRA_DB_TOKEN_JSON_PATH) as f:
    secrets = json.load(f)
    
# Extract the token into another constant:
ASTRA_DB_APPLICATION_TOKEN = secrets["token"]



auth_provider = PlainTextAuthProvider("token", ASTRA_DB_APPLICATION_TOKEN)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
connect_session = cluster.connect()

# check our session ID
print(connect_session.session_id)

the_vectorstore = Cassandra.from_documents(
    documents=document_chunks,
    embedding=embedding_function,
    session=connect_session,
    keyspace='vector_db_keyspace',
    table_name='cnn_daily_vectors'
)
