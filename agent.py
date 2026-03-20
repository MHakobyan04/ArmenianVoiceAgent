import asyncio
from dotenv import load_dotenv
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, cli, AutoSubscribe
from livekit.plugins import openai, silero

# Load environment variables (API keys)
load_dotenv()


class BankingAssistant(Agent):
    """
    Defines the persona and rules for our AI assistant.
    """

    def __init__(self):
        super().__init__(
            instructions=(
                "Դուք Հայաստանի առաջատար բանկերից մեկի հոգատար, պրոֆեսիոնալ և բանիմաց "
                "հաճախորդների սպասարկման ձայնային օգնականն եք: Ձեր նպատակն է օգնել հաճախորդներին "
                "իրենց հաշիվների, վարկերի, քարտերի և այլ բանկային պրոդուկտների հետ կապված հարցերում: "
                "Պատասխանեք բացառապես հայերենով: Եղեք քաղաքավարի, հստակ և հակիրճ, քանի որ սա "
                "բանավոր ձայնային խոսակցություն է:"
            )
        )


async def entrypoint(ctx: JobContext):
    print("Banking Voice Agent successfully connected to the server.")

    # Connect to the room, subscribing only to audio tracks
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    print("Waiting for a customer to connect...")

    # Build the AI session pipeline (VAD, STT, LLM, TTS)
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(model="gpt-4o"),
        tts=openai.TTS(voice="nova")
    )

    # Bring the agent into the room
    await session.start(agent=BankingAssistant(), room=ctx.room)

    # Proactively greet the customer as soon as they join
    session.generate_reply(
        instructions="Introduce yourself in Armenian as a banking assistant and ask how you can help.")


if __name__ == "__main__":
    # Run the agent application
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))