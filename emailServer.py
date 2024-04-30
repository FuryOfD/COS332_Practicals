import socket
import ssl
import base64
import datetime


def emailPerson(message, name):
    server = "smtp.gmail.com"
    # port = 25
    port = 587
    time = datetime.datetime.now()
    # message = "Check your email for the quiz results."
    # name = "Dharsh"
    
    sender_email ="work.dharsh@gmail.com" 
    receiver_email = "u21637386@tuks.co.za"
    password = "ForWork2504;"
    
    message = f"Subject: COS 332 Assignment 6\n\n{message}"
    
    smtpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    smtpSocket.connect((server, port))
    
    response = smtpSocket.recv(1024).decode()
    print(response)
    
    smtpSocket.send(f"EHLO localhost\r\n".encode())
    response = smtpSocket.recv(1024).decode()
    print(response)

    smtpSocket.send("STARTTLS\r\n".encode())
    response = smtpSocket.recv(1024).decode()
    print(response)
    
    smtpSocket = ssl.wrap_socket(smtpSocket)
    
    smtpSocket.send(f"EHLO {name}\r\n".encode())
    response = smtpSocket.recv(1024).decode()
    print(response)
    
    smtpSocket.send(f"AUTH LOGIN\r\n".encode())
    response = smtpSocket.recv(1024).decode()
    print(response)
    
    b64_user = base64.b64encode(sender_email.encode()).decode()   
    b64_password = base64.b64encode(password.encode()).decode()
    
    smtpSocket.send(f"{b64_user}\r\n".encode())
    response = smtpSocket.recv(1024).decode()
    
    smtpSocket.send(f"{b64_password}\r\n".encode())
    response = smtpSocket.recv(1024).decode()
    
    smtpSocket.send(f"MAIL FROM: <{sender_email}>\r\n".encode())
    response = smtpSocket.recv(1024).decode()
    print(response)
    
    smtpSocket.send(f"RCPT TO: <{receiver_email}>\r\n".encode())
    response = smtpSocket.recv(1024).decode()
    print(response)
    
    smtpSocket.send("DATA\r\n".encode())
    response = smtpSocket.recv(1024).decode()
    print(response)
    
    smtpSocket.send(f"Subject: COS 332 Assignment 6 {time}\r\n".encode())
    smtpSocket.send(b'\r\n')
    smtpSocket.send(f"{message}\r\n".encode())
    smtpSocket.send(b'\r\n')
    smtpSocket.send(f"From : {sender_email}\r\n".encode())
    
    response = smtpSocket.recv(1024).decode()
    print(response)
    
    smtpSocket.send("QUIT\r\n".encode())
    response = smtpSocket.recv(1024).decode()
    print(response)
    
    smtpSocket.close()
    print("Email sent successfully")
    
    