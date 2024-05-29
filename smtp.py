import socket
import ssl
import base64

sender_email = "ruanrossouw58@gmail.com"
password = "lmst ztsm rflu udks"

def sendEmail(receiver_email, subject, message):
    server = "smtp.gmail.com"
    port = 587
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as smtpSocket:
        smtpSocket.connect((server, port))
        
        # Receive the server's banner
        response = smtpSocket.recv(1024).decode()
        print(response)

        # Send EHLO command
        smtpSocket.send(b"EHLO localhost\r\n")
        response = smtpSocket.recv(1024).decode()
        print(response)

        # Send STARTTLS command
        smtpSocket.send(b"STARTTLS\r\n")
        response = smtpSocket.recv(1024).decode()
        print(response)

        # Upgrade the socket to SSL/TLS
        context = ssl.create_default_context()
        smtpSocket = context.wrap_socket(smtpSocket, server_hostname=server)

        # Send EHLO again over SSL
        smtpSocket.send(b"EHLO localhost\r\n")
        response = smtpSocket.recv(1024).decode()
        print(response)

        # Send AUTH LOGIN command
        smtpSocket.send(b"AUTH LOGIN\r\n")
        response = smtpSocket.recv(1024).decode()
        print(response)
        if response[:3] != "334":
            print("Failed to authenticate with SMTP server")

        # Send base64-encoded username
        smtpSocket.send(base64.b64encode(sender_email.encode()) + b"\r\n")
        response = smtpSocket.recv(1024).decode()
        print(response)
        if response[:3] != "334":
            print("Failed to authenticate with SMTP server")
            
        # Send base64-encoded password
        smtpSocket.send(base64.b64encode(password.encode()) + b"\r\n")
        response = smtpSocket.recv(1024).decode()
        print(response)
        if response[:3] != "235":
            print("Failed to authenticate with SMTP server")
            
        # Send MAIL FROM command
        smtpSocket.send(f"MAIL FROM: <{sender_email}>\r\n".encode())
        response = smtpSocket.recv(1024).decode()
        print(response)
        if response[:3] != "250":
            print("Failed to send email")
            
        # Send RCPT TO command
        smtpSocket.send(f"RCPT TO: <{receiver_email}>\r\n".encode())
        response = smtpSocket.recv(1024).decode()
        print(response)
        if response[:3] != "250":
            print("Failed to send email")
            
        # Send DATA command
        smtpSocket.send(b"DATA\r\n")
        response = smtpSocket.recv(1024).decode()
        print(response)
        if response[:3] != "354":
            print("Failed to send email")
            
        # Send email headers and content
        smtpSocket.send(f"Subject: {subject}\r\n".encode())
        smtpSocket.send(f"From: {sender_email}\r\n".encode())
        smtpSocket.send(f"To: {receiver_email}\r\n".encode())
        smtpSocket.send(b"\r\n")
        smtpSocket.send(f"{message}\r\n".encode())

        # End the email with a period
        smtpSocket.send(b".\r\n")
        response = smtpSocket.recv(1024).decode()
        print(response)
        if response[:3] != "250":
            print("Failed to send email")
            
        # Send QUIT command
        smtpSocket.send(b"QUIT\r\n")
        response = smtpSocket.recv(1024).decode()
        print(response)
        if response[:3] != "221":
            print("Failed to send email")
        else:
            print("Email sent successfully")