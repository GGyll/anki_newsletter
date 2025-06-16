import os

from mailjet_rest import Client

from settings import MAILJET_API_KEY, MAILJET_SECRET_KEY, MAILJET_SENDER_EMAIL


class MailService:
    def __init__(self):
        self.api_key = MAILJET_API_KEY
        self.api_secret = MAILJET_SECRET_KEY
        self.sender_email = MAILJET_SENDER_EMAIL

        if not self.api_key or not self.api_secret:
            raise ValueError(
                "Mailjet API keys (MAILJET_API_KEY_PUBLIC, MAILJET_API_KEY_PRIVATE) not set in environment variables."
            )
        if (
            not self.sender_email
            or self.sender_email == "your_verified_sender@example.com"
        ):
            print(
                "WARNING: MAILJET_SENDER_EMAIL is not set or uses default. Please configure a verified sender."
            )

        self.mailjet_client = Client(
            auth=(self.api_key, self.api_secret), version="v3.1"
        )

    def send_newsletter_email(
        self, recipient_email: str, subject: str, html_content: str
    ) -> bool:
        if not html_content:
            print("MailService: Cannot send empty HTML content.")
            return False

        data = {
            "Messages": [
                {
                    "From": {
                        "Email": self.sender_email,
                        "Name": "Vocabro Larry",
                    },
                    "To": [{"Email": recipient_email, "Name": "Language Learner"}],
                    "Subject": subject,
                    "HTMLPart": html_content,
                }
            ]
        }

        try:
            result = self.mailjet_client.send.create(data=data)
            if result.status_code == 200:
                print(
                    f"Mailjet: Email sent successfully! Status Code: {result.status_code}"
                )
                return True
            else:
                print(
                    f"Mailjet: Failed to send email. Status Code: {result.status_code}"
                )
                print(f"Mailjet: Error details: {result.json()}")
                return False
        except Exception as e:
            print(f"Mailjet: An error occurred while sending email: {e}")
            return False


mail_service = MailService()
