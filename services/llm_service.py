import os

from openai import OpenAI

from settings import USE_MODEL


class LLMService:
    def __init__(self):
        self.model_name = USE_MODEL
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    def generate_story(self, language: str, cards: list[tuple[str, str]]) -> str:
        PROMPT = """
        You are an expert language tutor and creative writer. Your task is to generate a short, engaging text in {language} that effectively incorporates a list of provided vocabulary words or phrases, and the english translation of that text as well. Ensure that the words or phrases that the user is learning is html-bolded in both versions somehow. Make the story somehow be a Seinfeld episode lmao

        ---
        **Input Details:**
        **1. Target Language:** {language}
        **2. Vocabulary Words (first element in tuple is the English word/phrase usually, and second is usually the {language} word/phrase):**
            {cards}
        **3. Desired Text Characteristics:**
            - **Type:** Short story
            - **Topic/Theme:** A scene in Seinfeld, reimagined with a story to fit the words
            - **Tone:** Peaceful, slightly reflective, try to incorporate dry humor and puns if possible
            - **Length:** Approximately 200-350 words.
            - **Key Requirement:** Each of the provided vocabulary words MUST be used naturally and correctly within the generated text.
        ---
        **Output Instructions:**
        1.  Generate the complete text in {language}.
        2.  Generate the translation of the text to English.
        3.  Do NOT include any definitions or translations in the generated text itself.
        4.  Do NOT include any conversational filler or meta-commentary. Just provide the text wrapped in html.
        5.  Do NOT include anything like ```html to make it markdown readable, just provide the text wrapped in html.
        6.  Wrap the entire text in html and format it to be as readable as possible
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": PROMPT.format(language=language, cards=cards),
                    },
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"LLM story generation failed: {e}")

    def generate_title(self, episode_text: str) -> str:
        TITLE_PROMPT = """
        You are an expert at titling Seinfeld episodes. Your goal is to create a concise, funny, and memorable title (typically 2-5 words) for a new episode, given its script or summary.

        Focus on:
        1.  **The core conflict or problem:** What's the main dilemma, especially for George or Elaine?
        2.  **A unique character quirk or bizarre incident:** Is there a strange side plot, a specific phrase, or a peculiar habit that defines the episode?
        3.  **Humor and absurdity:** Seinfeld titles often use alliteration, puns, or highlight the ridiculousness of everyday situations.

        Avoid:
        * Generic or overly descriptive titles.
        * Titles that give away the entire plot.

        Here is the text version of the Seinfeld episode:
        ---
        [Insert Episode Text Here]
        ---
        Based on the text, what's the best title for this Seinfeld episode? Provide only the title, no additional commentary.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": TITLE_PROMPT.format(episode_text=episode_text),
                    },
                ],
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"LLM title generation failed: {e}")


llm_service = LLMService()
