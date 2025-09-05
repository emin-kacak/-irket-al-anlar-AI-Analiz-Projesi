from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
from qdrant_client.models import PointStruct

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient("localhost", port=6333)



def create_collection(documents):
    vectors = model.encode(documents)
    client.recreate_collection(
        collection_name="personel",
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
    )
    points = [
        PointStruct(id=i, vector=vectors[i], payload={"text": documents[i]})
        for i in range(len(documents))
    ]
    client.upsert(
        collection_name="personel",points=points)
def search_documents(query, limit=3    
                     ):
    query_vector = model.encode([query])[0]
    results = client.search(
        collection_name="personel",
        query_vector=query_vector,
        limit=limit
    )
    if not results:
        return ["No relevant information found."]
    return [r.payload["text"] for r in results]
