from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from colorama import Fore, Back, Style

def send_email(drink, date, email):
    try:
        subject = f"{drink} <-> Running Low"
        context = {'drink': drink, 'date': date}
        message = render_to_string('Email/email.html', context)
        sender_email = '629eaf004@smtp-brevo.com'
        recipient_email = email

        # Create the email
        email_message = EmailMessage(
            subject,
            message,
            sender_email,
            [recipient_email]
        )
        email_message.content_subtype = 'html'
        email_message.send()
    except Exception as e:
        print(f"{Fore.RED} Email sending failed: {e} {Style.RESET_ALL}")

if __name__ == "__main__":
    send_email(
        drink="Coca Cola",
        date="2024-11-03",
        email="churchilkodhiambo@gmail.com" 
    )
