# Anki Newsletter: Personalized Anki Study Newsletter

![Project Icon/Banner (Optional - you can add a relevant image here)](https://placehold.co/600x200/cccccc/333333?text=Anki+Newsletter+-+AI+Powered)

Automate your language learning with AI-generated short stories based on your Anki "struggle cards," delivered directly to your inbox!

If this program proves useful, please consider giving the repository a star! ✨

## Table of Contents

- [About the Program](#about-the-program)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [AnkiConnect Setup (Crucial!)](#ankiconnect-setup-crucial)
  - [Installation](#installation)
  - [Configuration](#configuration)
    - [OpenRouter API Key](#openrouter-api-key)
    - [Mailjet API Keys](#mailjet-api-keys)
- [How to Run](#how-to-run)
- [Usage](#usage)
- [Contribution](#contribution)
- [License](#license)

## About the Program

This program is an automated system designed to enhance your Anki language learning experience. It connects to your Anki desktop application via AnkiConnect, identifies vocabulary words you're struggling with (based on your Anki card statistics), and then leverages powerful Large Language Models (LLMs) to generate unique, engaging, and personalized short stories incorporating those words. These stories, framed as "Seinfeld episodes" for a touch of humor, are then delivered as an HTML newsletter to your email inbox, providing context-rich exposure to challenging vocabulary.

The goal is to move beyond simple flashcards by immersing you in creative narratives that reinforce your learning, all powered by AI.

## Features

- **Intelligent Card Selection:** Identifies "struggle cards" based on lapses, ease factor, and recency, prioritizing actively learned vocabulary.
- **AI-Powered Story Generation:** Uses LLMs (via OpenAI API / OpenRouter) to craft unique short stories in your target language.
- **Seinfeld-Themed Narratives:** Stories are creatively styled as Seinfeld episodes for an entertaining learning experience.
- **HTML-Bolded Vocabulary:** Automatically bolds the learning vocabulary in both the target language and English translation for easy identification.
- **Dynamic Email Subject Generation:** An LLM generates a concise, Seinfeld-esque title for each newsletter.
- **Email Delivery:** Sends the personalized story newsletter to your inbox via Mailjet.
- **Configurable LLMs:** Supports various LLMs including GPT-3.5 Turbo, DeepSeek Free, and Gemini models via OpenRouter.

## Technologies Used

- **Python 3.9+**
- **Libraries:**
  - `requests`: For interacting with AnkiConnect and other APIs.
  - `openai`: For interacting with OpenAI and OpenRouter LLMs.
  - `mailjet-rest`: For sending emails.
  - `beautifulsoup4`: For HTML parsing.
  - `python-dotenv`: For managing environment variables.
  - (Optional: `replicate` for image generation, if re-enabled in future versions)

## Getting Started

Follow these steps to set up and run the program.

### Prerequisites

- **Anki Desktop Application:** Ensure you have Anki Desktop installed and running.
- **Python 3.9+:** Python must be installed on your system.
- **API Keys:** You will need API keys for your chosen LLM provider (OpenAI or OpenRouter) and Mailjet.

### AnkiConnect Setup (Crucial!)

The program communicates with your Anki desktop application via an add-on called AnkiConnect.

1.  **Install AnkiConnect:**

    - Open your Anki desktop application.
    - Go to **Tools -> Add-ons**.
    - Click on **"Get Add-ons..."**.
    - In the "Get Add-ons" window, paste the following code: `2055492159`
    - Click **"OK"**.
    - AnkiConnect will be downloaded and installed. **Restart Anki** when prompted for the changes to take effect.

2.  **Verify AnkiConnect is Running:**

    - With Anki running, open your web browser and go to `http://localhost:8765`.
    - If AnkiConnect is running correctly, you should see a message like `AnkiConnect is running!` or similar. If you get a "Page not found" or "Connection refused" error, ensure Anki is open and try restarting it.

3.  **Allow API Access (if prompted):** The first time the program attempts to connect to AnkiConnect, Anki might ask you to confirm whether you want to allow the connection. Click **"Yes"** or **"Allow"**.

### Installation

1.  **Clone the Repository:**

    ```bash
    git clone [https://github.com/your-github-username/anki-newsletter.git](https://github.com/your-github-username/anki-newsletter.git)
    cd anki-newsletter
    ```

    _(Remember to replace `your-github-username` with your actual GitHub username and `anki-newsletter` with your repo name)_

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    _(You'll need to generate a `requirements.txt` from your `pyproject.toml` or `poetry.lock` if you're using Poetry, or create one manually based on the libraries listed in "Technologies Used" section.)_
    Example `requirements.txt`:
    ```
    requests
    openai
    mailjet-rest
    beautifulsoup4
    python-dotenv
    # replicate (only if you re-enable image generation in config)
    ```

### Configuration

1.  **Create `.env` file:**
    Copy the provided example environment file:

    ```bash
    cp .env.example .env
    ```

2.  **Edit `.env` file:**
    Open the `.env` file you just created and fill in your API keys and other configurations. **Do not share this file publicly!**

    ```ini
    # .env

    # AnkiConnect
    ANKICONNECT_URL=http://localhost:8765
    # ANKICONNECT_AUTH_TOKEN=your_anki_connect_auth_token_here # Optional, if you have one set in AnkiConnect

    # LLM Configuration
    # Choose one of: gpt-3.5-turbo, deepseek/deepseek-r1:free, google/gemini-2.0-flash-001, google/gemini-2.5-pro-preview
    LLM_MODEL_TO_USE=deepseek/deepseek-r1:free # Or your preferred model

    # --- LLM API Key Setup ---

    ### OpenRouter API Key
    # You will need an OpenRouter API key.
    # 1. Go to OpenRouter.ai: [https://openrouter.ai/](https://openrouter.ai/)
    # 2. Sign up or log in.
    # 3. Navigate to your "Keys" or "API Keys" section.
    # 4. Create a new API key.
    # 5. Paste it here:
    OPENROUTER_API_KEY=sk-or-v1-YOUR_OPENROUTER_API_KEY # Replace with your OpenRouter API Key
    # OPENROUTER_BASE_URL=https://openrouter.ai/api/v1 # Default, uncomment if you need to override

    # --- Mailjet API Keys ---
    # Mailjet is used for sending the email newsletters. We use the free plan for this
    # 1. Go to Mailjet.com: [https://www.mailjet.com/](https://www.mailjet.com/)
    # 2. Sign up or log in.
    # 3. Navigate to your "API Key Management" or "REST API" section (often found under Account -> My API Key).
    # 4. You will find your Public API Key and Secret Key.
    # 5. Paste them here:
    MAILJET_API_KEY_PUBLIC=YOUR_MAILJET_PUBLIC_KEY # Replace with your Mailjet Public API Key
    MAILJET_API_KEY_PRIVATE=YOUR_MAILJET_PRIVATE_KEY # Replace with your Mailjet Private API Key
    MAILJET_SENDER_EMAIL=your_verified_sender@example.com # Crucial: This email MUST be verified in your Mailjet account!
    ```

## How to Run

Before running, ensure your Anki Desktop application is open and AnkiConnect is running (check `http://localhost:8765` in your browser).

1.  **Activate your virtual environment:**

    ```bash
    source venv/bin/activate
    ```

    _(On Windows: `.\venv\Scripts\activate`)_

2.  **Run the main script:**
    ```bash
    python main.py
    ```

The program will fetch cards, generate the story, and attempt to send the email. Watch the console for progress and success/failure messages.

## Usage

- **Target Deck:**
  Modify the `TARGET_DECK` variable in `main.py` to specify the exact name of the Anki deck you want to draw struggle cards from (e.g., `"My French Vocab"`).
- **Recipient Email:**
  Change `RECIPIENT_EMAIL` in `main.py` to the email address where you want to receive the newsletters.
- **Target Language:**
  Adjust the `TARGET_LANGUAGE` variable in `main.py` to match the language of your Anki cards (e.g., `"French"`, `"Spanish"`).
- **Struggle Card Criteria:**
  In `utils/card_helpers.py`, you can fine-tune the `get_struggle_cards` function parameters (`min_lapses`, `max_factor`, `recent_days`, `prioritize_active_learning`, `limit`) to customize which cards are identified as "struggles."

## Contribution

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
