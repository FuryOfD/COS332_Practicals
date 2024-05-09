import ssl
import socket
import time

from emailServer import send_email

def read_email(username, password, host):
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
                    # Send RETR command to retrieve the entire email
                    ssock.sendall(f"RETR {i}\r\n".encode())

                    # Read the entire email content until we find the end marker
                    email_content = b''
                    while True:
                        line = ssock.recv(1024)
                        if not line:
                            break
                        email_content += line

                        # Check if we reached the end of the email
                        if email_content.endswith(b'\r\n.\r\n'):
                            break

                    # Convert email_content to string for processing
                    email_content_str = email_content.decode()

                    # Check for Bcc field containing the username
                    if 'Bcc:' in email_content_str:
                        bcc_start_index = email_content_str.index('Bcc:') + 4
                        bcc_end_index = email_content_str.find('\r\n', bcc_start_index)
                        bcc_field = email_content_str[bcc_start_index:bcc_end_index]

                        # Check if username is in the Bcc field
                        if username in bcc_field:
                            print(f"Username '{username}' found in Bcc field of Email {i}.")
                            send_email(username, password, username, '', 'You have have been Bcc', f"Username '{username}' found in Bcc field of Email {i}.")

                # Quit session
                ssock.sendall(b"QUIT\r\n")
                print(ssock.recv(1024).decode())

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    username = "u21459640@tuks.co.za"
    password = "glun ydwp hpmb zfaj"
    host = "pop.gmail.com"

    while True:
        read_email(username, password, host)
        #sleep for 10 seconds
        time.sleep(10)
