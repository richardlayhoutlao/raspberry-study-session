from openai import OpenAI
from dotenv import load_dotenv

from utils.stats_summary import summarize_data

load_dotenv()

client = OpenAI()

def evaluate_batch(data_list):
    summary = summarize_data(data_list)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "Tu analyses un environnement d'étude basé sur des moyennes et variations. "
                    "Règles: "
                    "- Température idéale: 20-24°C "
                    "- Lumière: >60 bon, <40 trop sombre "
                    "- Bruit: 0 = silence (excellent), >60 = bruyant "
                    "Donne un message global (max 2 phrases) + conseils concrets."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Données résumées:\n{summary}\n\n"
                    "Est-ce un bon environnement pour étudier sur la durée ? "
                    "Explique avec conseils."
                )
            }
        ]
    )
    return response.output_text
