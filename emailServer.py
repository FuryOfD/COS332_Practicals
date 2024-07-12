import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, password, receiver_email, bcc_email, subject, message):
    try:
        # Establish a secure connection to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade the connection to a secure TLS connection
            server.login(sender_email, password)  # Log in to the SMTP server

            # Create a multipart message and set headers
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            if(bcc_email != ''):
                msg['Bcc'] = bcc_email
            msg['Subject'] = subject

            # Add message body
            msg.attach(MIMEText(message, 'plain'))

            if(bcc_email == ''):

                server.sendmail(sender_email, receiver_email, msg.as_string())
            else:
                server.sendmail(sender_email, [receiver_email, bcc_email], msg.as_string())

            print("Email sent successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    sender_email = "insert email here"
    password = "app password from Google"
    receiver_email = 'ruan@ufcons.com'
    bcc_email = 'u21459640@tuks.co.za'

    send_email(sender_email, password, receiver_email, bcc_email, 'I am the Bcc', 'This is a test email where I am the Bcc receiver.')
    send_email(sender_email, password, bcc_email, '', 'I am not the Bcc', 'This is a test email where I am only the receiver.')

