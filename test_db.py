import chromadb
from chromadb.utils import embedding_functions


def test_retrieval():
    # Connect to the local database
    client = chromadb.PersistentClient(path="./chroma_db")

    # Use the same multilingual model as in build_db.py
    hf_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="paraphrase-multilingual-MiniLM-L12-v2"
    )

    # Defensive programming block to handle missing database or collection
    try:
        collection = client.get_collection(
            name="armenian_banks_knowledge",
            embedding_function=hf_ef
        )
    except Exception as e:
        print(f"[Error] Database or collection not found. Make sure build_db.py has been executed. Details: {e}")
        return

    # Allow dynamic input for testing
    print("\n--- Bank Data Retrieval Test ---")
    query_text = input("Enter your query (or press Enter for the default query): ")

    if not query_text.strip():
        query_text = "Ինչպիսի՞ ավանդներ կան և որքա՞ն է տոկոսադրույքը:"

    print(f"\n[Search] Looking for: '{query_text}'\n")

    results = collection.query(
        query_texts=[query_text],
        n_results=2
    )

    print("--- Retrieved Chunks ---")
    if results['documents'] and results['documents'][0]:
        for idx, doc in enumerate(results['documents'][0]):
            # Print the first 500 characters of each chunk
            print(f"\n[Chunk] {idx + 1}:")
            print(doc[:500] + "...")
    else:
        print("[Result] Unfortunately, nothing was found.")


if __name__ == "__main__":
    test_retrieval()
