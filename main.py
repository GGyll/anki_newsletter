import sys

from services.anki_connect import anki_service
from services.llm_service import llm_service
from services.mail_service import mail_service
from settings import RECIPIENT_EMAIL
from utils.card_helpers import get_struggle_cards
from utils.html_helpers import html_to_text


def run_newsletter_generation(
    deck_name: str, recipient_email: str, language: str = "Portuguese"
):
    """
    Orchestrates the process of fetching struggle cards, generating a story,
    and sending it as an email newsletter.
    """
    print(f"Starting newsletter generation for deck '{deck_name}'...")

    try:
        # 1. Fetch cards from AnkiConnect
        print("Fetching card IDs...")
        card_ids = anki_service.find_cards_in_deck(deck_name)
        if not card_ids:
            print(f"No cards found in deck '{deck_name}'. Exiting.")
            return False

        print(f"Found {len(card_ids)} cards. Getting card info...")
        all_cards_info = anki_service.get_cards_info(card_ids)

        # 2. Identify struggle cards
        print("Identifying struggle cards...")
        struggle_cards = get_struggle_cards(
            all_cards_info, min_lapses=1, prioritize_active_learning=True
        )
        if not struggle_cards:
            print("No struggle cards found matching criteria. Exiting.")
            return False

        print(f"Selected {len(struggle_cards)} struggle cards.")
        print(f"Struggle Cards: {struggle_cards}")

        # 3. Generate short story with LLM
        print("Generating short story with LLM...")
        story_html_content = llm_service.generate_story(
            language=language, cards=struggle_cards
        )
        if not story_html_content:
            print("LLM failed to generate story content. Exiting.")
            return False

        # 4. Generate email subject/title
        print("Generating email subject/title...")
        # Assuming story_html_content is HTML and needs to be converted to plain text for title generation
        story_plain_text = html_to_text(story_html_content)
        subject = llm_service.generate_title(story_plain_text)
        if not subject:
            print("LLM failed to generate email subject. Using default.")
            subject = f"Your {language} Vocabro Story"

        # 5. Send email newsletter
        print(
            f"Sending newsletter email to {recipient_email} with subject: '{subject}'..."
        )
        # Ensure the HTML content is wrapped in basic HTML tags if not already by LLM
        final_html_body = f"<html><body>{story_html_content}</body></html>"
        email_sent = mail_service.send_newsletter_email(
            recipient_email, subject, final_html_body
        )

        if email_sent:
            print("Newsletter process completed successfully!")
            return True
        else:
            print("Newsletter process failed.")
            return False

    except ValueError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        return False
    except ConnectionError as e:
        print(f"Network/AnkiConnect Error: {e}", file=sys.stderr)
        return False
    except RuntimeError as e:
        print(f"Runtime Error (LLM/Mailjet): {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    # --- Example Usage ---
    # Customize these parameters
    TARGET_DECK = "My portuguese"
    RECIPIENT_EMAIL = RECIPIENT_EMAIL
    TARGET_LANGUAGE = "Portuguese"

    # Run the main process
    success = run_newsletter_generation(
        deck_name=TARGET_DECK, recipient_email=RECIPIENT_EMAIL, language=TARGET_LANGUAGE
    )
    if success:
        print("\nScript finished successfully!")
    else:
        print("\nScript finished with errors.")
