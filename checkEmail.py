import ssl
import socket
from email.parser import BytesParser
from email.header import decode_header

def decode_email_header(header):
    """Decode email header into readable string."""
    decoded = []
    for part, encoding in decode_header(header):
        if isinstance(part, bytes):
            # Decode bytes to str using specified encoding
            decoded.append(part.decode(encoding or 'utf-8'))
        else:
            decoded.append(part)
    return ''.join(decoded)

def retrieve_email_headers(username, password, host):
    try:
        # Connect to POP3 server over SSL
        context = ssl.create_default_context()
        with socket.create_connection((host, 995)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                # Receive server greeting
                print(ssock.recv(1024).decode())

                # Send username
                ssock.sendall(f"USER {username}\r\n".encode())
                print(ssock.recv(1024).decode())

                # Send password
                ssock.sendall(f"PASS {password}\r\n".encode())
                print(ssock.recv(1024).decode())

                # Send LIST command to get email count
                ssock.sendall(b"LIST\r\n")
                response = ssock.recv(1024).decode()
                print(response)

                # Parse email count from response
                num_emails = int(response.split()[1])

                if num_emails == 0:
                    print("No emails in the mailbox.")
                    return

                # Retrieve headers and body for all emails
                for i in range(1, num_emails + 1):
                    # Send TOP command to retrieve headers and part of the body
                    ssock.sendall(f"TOP {i} 0\r\n".encode())
                    response = ssock.recv(1024).decode()
                    print(response)

                    # Parse email headers and body
                    headers_text = b''
                    while True:
                        line = ssock.recv(1024)
                        headers_text += line
                        if b'\r\n.\r\n' in line:
                            break

                    # Parse email headers
                    headers = BytesParser().parsebytes(headers_text)

                    # Extract relevant header fields
                    subject = decode_email_header(headers.get('Subject', ''))
                    from_address = decode_email_header(headers.get('From', ''))
                    to_address = decode_email_header(headers.get('To', ''))
                    bcc_address = decode_email_header(headers.get('Bcc', ''))

                    # Retrieve the email body
                    ssock.sendall(f"RETR {i}\r\n".encode())
                    response = ssock.recv(1024).decode()
                    print(response)  # This will print the beginning of the body
                    
                    # Continue reading the body until the end marker
                    body_text = b''
                    while True:
                        line = ssock.recv(1024)
                        body_text += line
                        if b'\r\n.\r\n' in line:
                            break

                    # Decode the email body
                    body = BytesParser().parsebytes(body_text)

                    # Print email headers and body
                    print(f"Email {i} - Subject: {subject}, From: {from_address}, To: {to_address}")
                    if bcc_address:
                        print(f"Bcc: {bcc_address}")
                    print("Body:")
                    print(body.get_payload(decode=True).decode())

                # Quit session
                ssock.sendall(b"QUIT\r\n")
                print(ssock.recv(1024).decode())

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Replace these credentials with your own
    username = "u21459640@tuks.co.za"
    password = "glun ydwp hpmb zfaj"
    host = "pop.gmail.com"

    retrieve_email_headers(username, password, host)
