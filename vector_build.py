"""

1: Chunk the Data UP / split up pypdf
2: Chunks to Embeddings
3: Store in Vector DB
4: RAG-  Query + embedding
"""

import os
from dotenv import load_dotenv
load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import chromadb

from sentence_transformers import SentenceTransformer
from functools import lru_cache


from pypdf import PdfReader

class db():
    def __init__(self,question:str):
        self.question_ = question

#Split → Embed → Store → Search → Send to LLM

    def func(self):


        data = [
            {"role": "assistant", "content": "Hello, how are you doing?"},
            {"role": "user", "content": "Hello! I am Yousaf. I am testing this device. I love to code! and I attend TJHSST"},
            {"role": "user", "content": "Can I go to the hackathon?"},
            {"role": "user", "content": "What school do I go to? after college?"},
            {"role": "user", "content": "I need a new laptop because my current laptop is broken"},
            {"role": "user", "content": "What is the best laptop for coding?"}
        ]
    


        #2

        model = SentenceTransformer("all-MiniLM-L6-v2")


        # #3
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection(name="vectordb_for_rag")




        for i in range(len(data)):
            page_text = data[i]["content"]
            embedding = model.encode(page_text).tolist()
            collection.upsert(
                documents=[page_text],
                metadatas=[{"source": f"page_{i}"}],
                ids=[f"id_{i}"],
                embeddings=[embedding]
            )
            
            
            
        question = self.question_
            
        convert = model.encode(question).tolist()



        result = collection.query(
            query_embeddings=[convert],
            n_results=2, # change this based on how many results
            include=["documents", "metadatas"]
            
            
        )

        import os
        from llama_api_client import LlamaAPIClient

        client = LlamaAPIClient(
            api_key=os.environ["LLAMA_API_KEY"],
            base_url="https://api.llama.com/v1/",
        )


        docs = result["documents"][0]
        metas = result["metadatas"][0]
                
                
                
        response = client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[
                {"role": "user", "content": question + "\n\n" + "Here are the relevnt information:\n" + "\n".join(docs) + "\n\n" + "Metadata:\n" + "\n".join([str(m) for m in metas])},
            ],
        )

        # print(response.completion_message.content.text)

        
        results_data = {
            "question": question,
            "retrieved_docs": docs,
            "retrieved_metas": metas,
            "llm_response": response.completion_message.content.text
        }
        
        return results_data
        
from functools import lru_cache
@lru_cache(maxsize=128)
def get_results(question):
    obj = db(question)
    return obj.func()

results_data = get_results("what school does yousaf go to?")
print(results_data)