import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.agents import Agent, AgentSession
from livekit.agents.llm import function_tool
from livekit.plugins import openai, silero

load_dotenv()

# Connect to our local vector database
db_path = "./chroma_db"
chroma_client = chromadb.PersistentClient(path=db_path)

# Use the exact same HuggingFace model we used to build the database
hf_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)

# Load the existing collection
collection = chroma_client.get_collection(
    name="armenian_banks_knowledge",
    embedding_function=hf_ef
)


# Define the tool (skill) our voice agent can use
@function_tool
def search_bank_info(query: str) -> str:
    """Search the local database for specific information about Armenian banks (e.g., deposits, loans, branches, rates)."""
    print(f"Agent is searching database for: {query}")

    # Search the vector database for the top 3 most relevant chunks
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    # If nothing is found, inform the agent
    if not results["documents"] or not results["documents"][0]:
        return "No relevant information found in the database. Please tell the user you don't have this specific information."

    # Combine the found chunks into a single text block
    retrieved_info = "\n\n".join(results["documents"][0])
    print("Agent found relevant information.")
    return retrieved_info


async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Set up the AI Agent with our custom instructions and the search tool
    agent = Agent(
        instructions=(
            "Դու հայկական բանկերի աջակցման պրոֆեսիոնալ ձայնային օգնական ես: "
            "ՔՈ ԿԱՆՈՆՆԵՐԸ:"
            "1. ԽՈՍԻՐ ՄԻԱՅՆ ՀԱՅԵՐԵՆ: "
            "2. ՊԱՏԱՍԽԱՆԻՐ ՄԻԱՅՆ հետևյալ թեմաներով՝ ՎԱՐԿԵՐ (Credits), ԱՎԱՆԴՆԵՐ (Deposits) և ՄԱՍՆԱՃՅՈՒՂԵՐԻ ՀԱՍՑԵՆԵՐ (Branch Locations): "
            "3. ՕԳՏԱԳՈՐԾԻՐ 'search_bank_info' գործիքը յուրաքանչյուր հարցի համար: Մի՛ հորինիր թվեր կամ տոկոսադրույքներ: "
            "4. ՍԱՀՄԱՆԱՓԱԿՈՒՄ. Եթե օգտատերը հարցնում է այլ թեմաների մասին (օրինակ՝ քաղաքականություն, եղանակ, կամ այլ բանկային ծառայություններ), "
            "քաղաքավարի մերժիր և ասա, որ դու մասնագիտացված ես միայն վարկերի, ավանդների և մասնաճյուղերի հարցերում: "
            "5. Եղիր հակիրճ, բնական, օգնող և քաղաքավարի:"
        ),
        tools=[search_bank_info]
    )

    # Create the real-time session with VAD, STT, LLM, and TTS models
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
    )

    # Start the session and greet the user
    await session.start(agent=agent, room=ctx.room)
    await session.say("Բարև ձեզ: Ես հայկական բանկերի վիրտուալ օգնականն եմ: Ինչպե՞ս կարող եմ օգնել ձեզ այսօր:",
                      allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))