import openai
import os
import logging
from tenacity import retry, stop_after_attempt

logger = logging.getLogger(__name__)
openai.api_key = os.environ["OPENAI_KEY"]


@retry(stop=stop_after_attempt(2))
def parse_text_to_menu(text):
    assert len(text) < 1000  # Cost
    assert len(text) > 150  # Not empty
    system_prompt = "Tu es un assistant dont le but est d'extraire et de formater des informations à partir de texte brut, bruité, afin de les rendre compréhensibles. Ces informations sont transmises par mail à une chaine de distribution."
    user_prompt = f"Le restaurant les 3 brasseurs publie chaque semaine une vidéo pour annoncer le plat du jour pour chaque jour de la semaine à venir. Cette vidéo a été traité par un modèle OCR et voici le texte extrait '{text}'.  Ce texte contient du bruit. En utilisant ce texte, écris un message pour faire connaître de manière claire les plats du jours de la semaine."
    messages = []
    messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, temperature=0, max_tokens=256
    )
    response_text = response.choices[0].message["content"]
    logger.info(f"Parsed menu {response_text}")
    return response_text
