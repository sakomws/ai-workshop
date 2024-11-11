# Welcome to the Vector Database Workshop!


In this workshop, we're going to use Weaviate to explore and learn about the power of vector search. Here are three challenges that will get you started with the basics of retrieval for LLM applications that leverage vector search for RAG.


## Challenge 0: Generate a vector embedding using OpenAI API

Try out this "get_embedding()" function. You can create a vector embedding for any text using this function.

```python 
from openai import OpenAI
client = OpenAI(api_key="INSERT YOUR API KEY")

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

vector = get_embedding("A piece of text that we're going to vectorize")

print(vector)
```

This embedding is a 1536 (by default) dimensional vector that semantically represents your input text. When you vectorize all of your chunks and you store them in Weaviate, they'll be plotted into an HNSW vector index which allows us to do vector search on all of our data to find semantically related data to our query.

This is the magic RAG, and ultimately Agentic RAG.

The great thing about Weaviate is that we have direct integrations to various model providers and inference platforms like OpenAI, Google, FriendlAI, and many more.

When you store a chunk in Weaviate, you can automatically have the client library generate a vector of your chunk before it gets stored in the Weaviate cluster.

## Challenge 1: Create a Weaviate Cluster and a Chunk Collection

### Create a Weaviate Cluster and Create a Chunk Collection
Alright, we're in a chunking workshop today to learn about text splitting strategies, but first, we'll need a place to store those chunks and then do vector search over them.

* Weaviate Quickstart 
* [Weaviate Cloud Console](https://console.weaviate.cloud/)
* Create a free Weaviate Cluster and use the Weaviate Cloud Console to create a `chunk` Collection
![create a collection](collection_creation.png)

**Note** This is a naive collection object with a single attribute. As you get comfortable with collections in Weaviate, you can create collections with multiple attributes, create vectors for individual attributes called [named vectors](https://weaviate.io/developers/weaviate/config-refs/schema/multi-vector) to enhance searchability experiences.

For today, we'll keep things simple and just create a collection with the single `content` attribute which will take on our chunks.

### Let's chunk!

```python
text = '''🛠️ What to Expect:
Inspiring Keynotes: Hear from some of the most influential voices in the tech world, sharing insights on the latest in AI, machine learning, mobile development, cloud computing, and more.

Hands-On Workshops: Roll up your sleeves and dive into hands-on sessions designed to enhance your skills with Google technologies, such as Flutter, TensorFlow, Google Cloud, and Android development.

Tech Talks: Get an inside look at the latest trends, innovations, and best practices from industry experts and Google Developer Experts (GDEs).

Networking Opportunities: Connect with like-minded developers, industry leaders, and hiring managers. Whether you're looking for collaboration opportunities, career advice, or just want to share your passion for technology, this is the place to be!'''
# Create a list that will hold your chunks
chunks = []

chunk_size = 35 # Characters

# Run through the a range with the length of your text and iterate every chunk_size you want
for i in range(0, len(text), chunk_size):
    chunk = text[i:i + chunk_size]
    chunks.append(chunk)

for chunk in chunks:
    print(chunk)
```

Congrats! You've just chunked the text from the "What to expect" from GDG DevFest intro. This is just the beginning. You can always be in control of your chunking strategy in this way, however just like throughout software tools, we have abstractions so you don't have to write all of this yourself.

Notice the chunks that are printed out are split exactly by some character count and have no overlap? This is a fairly naive chunking strategy and shouldn't be used in production. It's good for testing quickly, but usually not very good for recall. Remember the purpose of chunking is to improve our ability to retrieve highly relevant chunks to our queries.

When you add some overlap, you might capture semantic meaning from a prior chunk of the following chunk within the chunk itself, but there's not too much fanciness and enhancements to your retrievals when using character based text splitting.

### Recursive Chunking with LangChain

Recursive chunking is a great first place to evaluate your chunks for retrieval, after character level text splitting. This would be a great place to start chunking for real, and potentially in production.

The idea behind recursive text splitting is that we have a list of (definable) separators. For simplicity, we'll pick the following which is also outlined in Greg Kamradt's 5 Levels of Chunking Jupyter notebook.

- "\n\n" - Double new line, or most commonly paragraph breaks
- "\n" - New lines
- " " - Spaces
- "" - Characters

This approach first chunks the text by the first separator, "\n\n". Once complete, it evaluates all the chunks to see if the text is short enough to fit the defined chunk size. If the chunk is too large, it'll then go through the chunks that are too large and separate by the next separator "\n". It keeps doing this with all the chunks until all chunks are the appropriate size.

Let's execute a recursive chunking with langchain. First we need to install some dependencies, ideally to a python virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
pip install langchain
```

```python

from langchain.text_splitter import RecursiveCharacterTextSplitter

text = """Google has its origins in "BackRub", a research project that was begun in 1996 by Larry Page and Sergey Brin when they were both PhD students at Stanford University in Stanford, California.[2] The project initially involved an unofficial "third founder", Scott Hassan, the lead programmer who wrote much of the code for the original Google Search engine, but he left before Google was officially founded as a company;[3][4] Hassan went on to pursue a career in robotics and founded the company Willow Garage in 2006.[5][6] Craig Nevill-Manning was also invited to join Google at its formation but declined and then joined a little later on.[7]

In the search of a dissertation theme, Larry Page had been considering among other things exploring the mathematical properties of the World Wide Web, understanding its link structure as a huge graph.[8] His supervisor, Terry Winograd, encouraged him to pick this idea (which Larry Page later recalled as "the best advice I ever got"[9]) and Larry Page focused on the problem of finding out which web pages link to a given page, based on the consideration that the number and nature of such backlinks was valuable information about that page (with the role of citations in academic publishing in mind).[8] Page told his ideas to Hassan, who began writing the code to implement Page's ideas.[3]

The research project was nicknamed "BackRub", and it was soon joined by Brin, who was supported by a National Science Foundation Graduate Fellowship.[10] The two had first met in the summer of 1995, when Page was part of a group of potential new students that Brin had volunteered to give a tour around the campus and nearby San Francisco.[8] Both Brin and Page were working on the Stanford Digital Library Project (SDLP). The SDLP's goal was "to develop the enabling technologies for a single, integrated and universal digital library" and it was funded through the National Science Foundation, among other federal agencies.[10][11][12][13] Brin and Page were also part of a computer science research team at Stanford University that received funding from Massive Digital Data Systems (MDDS), a program managed for the Central Intelligence Agency (CIA) and the National Security Agency (NSA) by large intelligence and military contractors.[14]

Page's web crawler began exploring the web in March 1996, with Page's own Stanford home page serving as the only starting point.[8] To convert the backlink data that is gathered for a given web page into a measure of importance, Brin and Page developed the PageRank algorithm.[8] While analyzing BackRub's output which, for a given URL, consisted of a list of backlinks ranked by importance, the pair realized that a search engine based on PageRank would produce better results than existing techniques (existing search engines at the time essentially ranked results according to how many times the search term appeared on a page).[8][15]

Convinced that the pages with the most links to them from other highly relevant Web pages must be the most relevant pages associated with the search, Page and Brin tested their thesis as part of their studies and laid the foundation for their search engine.[16] The first version of Google was released in August 1996 on the Stanford website. It used nearly half of Stanford's entire network bandwidth.[17]
"""


# the larger chunks means 
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 450, chunk_overlap=0) 


chunked_text = text_splitter.create_documents([text])

for chunk in chunked_text:
    print(chunk)

```

We'll be using these chunks in Weaviate for RAG, however know there are many other forms of chunking beyond recursive chunking that will better fit other formats of data. For example, document level splitting -- which takes into account the structure of the document, such as tables in a PDF. There are tools like Unstructured which gives you the ability to extract data from a PDF, or embedding models like CoPali which leverage a a vision model to evaluate the shape and size of the document to help generate embeddings.

More recently, the industry has been exploring semantic chunking which evaluates the distances of each chunk to determine similarity, and ensures that chunks that are similar to one another are chenked together. And further looking, agentic chunking has become an interesting topic as well.


## Challenge 3: Store the chunks in Weaviate and apply RAG

Great, let's store the chunks in Weaviate and execute a simle RAG, or Generative Search query. 

For each chunk that was created above, let's store them in our `chunk` collection in Weaviate.

Follow the Weaviate Quickstart to download the Weaviate python client library, `weaviate-client`. Then grab the Cluster URL and the Cluster API key of the cluster you created in challenge 1. 


### Add your chunks

```python

import weaviate
from weaviate.classes.init import Auth
import requests, json, os

# Best practice: store your credentials in environment variables
wcd_url = os.environ["WCD_URL"]
wcd_api_key = os.environ["WCD_API_KEY"]
openai_api_key = os.environ["OPENAI_APIKEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,                                    # Replace with your Weaviate Cloud URL
    auth_credentials=Auth.api_key(wcd_api_key),             # Replace with your Weaviate Cloud key
    headers={"X-OpenAI-Api-Key": openai_api_key},           # Replace with your OpenAI API key
)



chunk_collection = client.collections.get("Chunk")

with chunk_collection.batch.dynamic() as batch:
    for chunk in chunks: #Note these chunks come from the recursive chunking step in challenge 2
        batch.add_object({
            "content": chunk,
        })

client.close()  # Free up resources
```


Congrats, you've loaded the vector database and generated vectors automatically for each of the chunks. Let's do a generative search, or RAG query. 


```python


import weaviate
from weaviate.classes.init import Auth
import os

# Best practice: store your credentials in environment variables
wcd_url = os.environ["WCD_URL"]
wcd_api_key = os.environ["WCD_API_KEY"]
openai_api_key = os.environ["OPENAI_APIKEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,                                    # Replace with your Weaviate Cloud URL
    auth_credentials=Auth.api_key(wcd_api_key),             # Replace with your Weaviate Cloud key
    headers={"X-OpenAI-Api-Key": openai_api_key},           # Replace with your OpenAI API key
)

chunk_collection = client.collections.get("Chunk")

response = chunk_collection.generate.near_text(
    query="google history",
    limit=3,
    single_prompt="Summarize google's history based on the context."

)

print(response.generated)  # Inspect the generated text

client.close()  # Free up resources

```


## Congrats! 

You've just executed a RAG on your recursively chunked text. To go further, try loading any document into your Weaviate cluster using the recursive chunking strategy and see good the summaries are. 

At the end of the day, we need to ensure our chunks are optimized for the best possible retrievals. This is why evaluations are important when we are chunking our documents, but chunking is not part of todays workshop, if you'd like to learn more, connect with me on LinkedIn! https://linkedin.com/in/itsajchan.

Thanks for building with me today!