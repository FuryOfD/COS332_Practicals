import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    sender_email = "ruanrossouw58@gmail.com"
    password = "lmst ztsm rflu udks"
    receiver_email = 'ruan@ufcons.com'
    bcc_email = 'u21459640@tuks.co.za'
    subject = 'Test Email'
    message = 'This is a test email sent from a Python script.'

    try:
        # Establish a secure connection to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade the connection to a secure TLS connection
            server.login(sender_email, password)  # Log in to the SMTP server

            # Create a multipart message and set headers
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Bcc'] = bcc_email
            msg['Subject'] = subject

            # Add message body
            msg.attach(MIMEText(message, 'plain'))

            # Send email
            server.sendmail(sender_email, [receiver_email, bcc_email], msg.as_string())

            print("Email sent successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to send an email
send_email()
