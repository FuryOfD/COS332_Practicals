import socket 
import ssl
from email.parser import Parser

def checkingEmail(username, password):
    pop_server = "pop.gmail.com"
    pop_port = 995
    
    # Establish a socket connection to the POP server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as popSocket:
        popSocket.connect((pop_server, pop_port))
        
        # Upgrade the socket to SSL/TLS
        context = ssl.create_default_context()
        pop_socket_ssl = context.wrap_socket(popSocket, server_hostname=pop_server)
        
        # Receive the server's banner
        response = pop_socket_ssl.recv(4096).decode()
        print(response)
        
        # Send username
        pop_socket_ssl.sendall(f'USER {username}\r\n'.encode())
        print(pop_socket_ssl.recv(4096).decode())

        # Send password
        pop_socket_ssl.sendall(f'PASS {password}\r\n'.encode())
        print(pop_socket_ssl.recv(4096).decode())

        # # Send STAT command to get the total number of messages and the total size of the mailbox
        # pop_socket_ssl.sendall(b'STAT\r\n')
        # response = pop_socket_ssl.recv(4096).decode()
        # num_messages, _ = response.split()[1:]

        # # Fetch the most recent email
        # pop_socket_ssl.sendall(f'RETR {num_messages}\r\n'.encode())
        # email_data = b''
        # while True:
        #     data = pop_socket_ssl.recv(4096)
        #     if not data:
        #         break
        #     email_data += data

        # # Parse the email
        # email_text = email_data.decode()
        # msg = Parser().parsestr(email_text)

        # # Process the most recent email
        # print("Subject:", msg['Subject'])
        # print("From:", msg['From'])
        # print("To:", msg['To'])
        
        # Fetch headers of the first 5 messages
        for i in range(1, 3):
            pop_socket_ssl.sendall(f'TOP {i} 0\r\n'.encode())  # Get only the headers
            headers_data = b''
            while True:
                data = pop_socket_ssl.recv(4096)
                if not data or b'\r\n\r\n' in data:  # End of headers
                    break
                headers_data += data
            
            # Parse and process the headers
            headers_text = headers_data.decode()
            msg = Parser().parsestr(headers_text)
            print(f"Message {i} - Subject: {msg['Subject']}, From: {msg['From']}, To: {msg['To']}")


        # Close connection
        pop_socket_ssl.sendall(b'QUIT\r\n')
        pop_socket_ssl.close()
        
checkingEmail("work.dharsh@gmail.com","brmo nosk unmr zglg")