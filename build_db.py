import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter


def main():
    # Initialize the local vector database
    db_path = "./chroma_db"
    print(f"Initializing ChromaDB at {db_path}...")
    client = chromadb.PersistentClient(path=db_path)

    # Set up the HuggingFace multilingual embedding model (Free & Local)
    # This model is specifically good at understanding Armenian
    hf_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="paraphrase-multilingual-MiniLM-L12-v2"
    )

    # Create or get a collection
    collection = client.get_or_create_collection(
        name="armenian_banks_knowledge",
        embedding_function=hf_ef
    )

    # Prepare the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " "]
    )

    data_dir = "data"
    if not os.path.exists(data_dir):
        print("Data directory not found. Please run scraper.py first.")
        return

    # Read all text files from the data directory
    for filename in os.listdir(data_dir):
        if filename.endswith("_info.txt"):
            bank_name = filename.split("_info.txt")[0].capitalize()
            file_path = os.path.join(data_dir, filename)

            print(f"Processing data for {bank_name}...")

            with open(file_path, "r", encoding="utf-8") as f:
                text_content = f.read()

            # Split the text into smaller chunks
            chunks = text_splitter.split_text(text_content)

            # Prepare data for the database
            documents = []
            metadatas = []
            ids = []

            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append({"bank": bank_name, "source": filename})
                ids.append(f"{bank_name}_chunk_{i}")

            # Add the chunks to the vector database
            if documents:
                collection.upsert(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )

            print(f"Added {len(chunks)} chunks for {bank_name} to the database.")

    print("\nKnowledge base successfully built using HuggingFace The vector database is ready.")


if __name__ == "__main__":
    main()