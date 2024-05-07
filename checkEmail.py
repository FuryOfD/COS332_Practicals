import poplib
from email import parser

def checkingEmail():
    pop_server = 'pop.gmail.com'
    receiver_email = 'work.dharsh@gmail.com'
    password = 'brmo nosk unmr zglg'
    
    pop_con = poplib.POP3_SSL(pop_server)
    pop_con.user(receiver_email)
    pop_con.pass_(password)
    
    num_messages = len(pop_con.list()[1])
    
    # Printing the most recent email
    message = pop_con.retr(num_messages)[1]
    message = b'\n'.join(message).decode()
    message = parser.Parser().parsestr(message)
    
    print("Subject:", message['subject'])
    print("From:", message['from'])
    print("To:", message['to'])
    
    pop_con.quit()
    

checkingEmail()
    
    
    