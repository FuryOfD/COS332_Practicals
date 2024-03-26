import socket
import random



class Question:
    def __init__(self, question, answers, correct_answer):
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer


# Function to read questions and answers from file
def read_questions(filename):
    questions = []
    question = None
    num_questions = 0
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('?'):
                if question:
                    questions.append(question)
                    num_questions += 1
                question = Question(line[1:], [], '')
            elif line.startswith('+'):
                question.correct_answer = line[1:]
                question.answers.append(line[1:])
            elif line.startswith('-'):
                question.answers.append(line[1:])
            elif line.strip() == "":
                continue
    return questions

# Function to select a random question
def select_question(questions):
    return random.choice(questions)

#global score, total  # Declare score and total as global variables
score = 0  # Initialize score
total = 0  # Initialize total

# Function to handle a client's connection
def handle_client_connection(client_socket, questions):
    global score, total  # Declare score and total as global variables
    
    selected_question = select_question(questions)
    question_text = selected_question.question
    answers = selected_question.answers
    client_socket.sendall(question_text.encode() + b'\n')
    for i, answer in enumerate(answers):
        client_socket.sendall(f"{chr(65 + i)}. {answer}\n".encode())
    
    question = b"Enter your answer (A/B/C/D"
    if len(answers) == 5:
        question += b"/E"
    question += b"): "
    client_socket.sendall(question)
    
    # Receive and process user's answer
    user_answer = client_socket.recv(1024).decode().strip().upper()
    
    if user_answer in ['A', 'B', 'C', 'D', 'E']:
        if answers[ord(user_answer) - ord('A')] == selected_question.correct_answer:
            client_socket.sendall(b"Correct answer!\n")
            score += 1
            total += 1
        else:
            client_socket.sendall(b"Incorrect answer!\n The correct answer is: " + selected_question.correct_answer.encode() + b"\n")
            total += 1
            
    else:
        client_socket.sendall(b"Invalid answer. Please enter A, B, C, or D.\n")
    
    # Ask if the user wants to continue
    client_socket.sendall(b"Do you want to answer another question? (y/n): ")
    response = client_socket.recv(1024).decode().strip().lower()
    if response == 'y':
        handle_client_connection(client_socket, questions)
    else:
        #client_socket.sendall(b"Your final score is: " + str(score).encode() +"/" + str(total).encode()+ b"\n")
        client_socket.sendall(f"Your final score is: {score}/{total}\n".encode())
        client_socket.sendall(b"Thank you for playing! Goodbye.\n")
        client_socket.close()

# Main function
def main():
    # Read questions from file
    questions = read_questions("questions.txt")

    for question in questions:
        print("Question:", question.question)
        print("Answers:", question.answers)
        print("Correct answer:", question.correct_answer)

    # Set up socket for Telnet connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 55555))
    server_socket.listen(1)
    print("Waiting for Telnet connection on port 55555...")

    # Accept Telnet connection
    while True:
        client_socket, address = server_socket.accept()
        print("Connection from:", address)
        handle_client_connection(client_socket, questions)

if __name__ == "__main__":
    main()
