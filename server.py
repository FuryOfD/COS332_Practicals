import socket
import random
from urllib.parse import unquote

class Question:
    def __init__(self, question, answers, correct_answer):
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer

def read_questions(filename):
    questions = []
    question = None
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('?'):
                if question:
                    questions.append(question)
                question = Question(line[1:], [], '')
            elif line.startswith('+'):
                question.correct_answer = line[1:]
                question.answers.append(line[1:])
            elif line.startswith('-'):
                question.answers.append(line[1:])
            elif line.strip() == "":
                continue
    return questions

def select_question(questions):
    return random.choice(questions)

def generate_html(answers):
    html_answers = ""
    for answer in answers:
        html_answers += f'<input type="radio" name="answer" value="{answer}">{answer}<br>'
    return html_answers

questions = read_questions("questions.txt")

class QuizHandler:
    total = 0
    correct = 0
    previous_question = None
    
    def handle_request(self, request):
        if not request:
            return self.handle_get('/')

        print("--------------------------")
        print("Handle Request")
        print(request)
        print("--------------------------")

        method, path, headers, body = self.parse_request(request)

        if(path.find('?') != -1):
            path = path[:path.find('?')]
        
        print("--------------------------")
        print("Method: ", method)
        print("Path: ", path)
        print("Headers: ", headers)
        print("Body: ", body)
        print("--------------------------")


        if method == 'GET':
            return self.handle_get(path)
        elif method == 'POST':
            return self.handle_post(path, body)
        else:
            return self.not_allowed()

    def parse_request(self, request):
        if not request:
            return None, None, None, None

        lines = request.split('\r\n')
        method, path, _ = lines[0].split(' ')
        headers = {}
        for line in lines[1:]:
            if not line:
                break
            key, value = line.split(': ')
            headers[key] = value
        body = '\r\n'.join(lines[lines.index('') + 1:])
        return method, path, headers, body

    def handle_get(self, path):
        if path == '/':
            while True:
                question = select_question(questions)
                if question != QuizHandler.previous_question:
                    QuizHandler.previous_question = question
                    break
            
            html_answers = generate_html(question.answers)
            html_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html><html><head><title>COS 332 Assignment 4</title></head><body><h1>Quiz</h1><h2>{question.question}</h2><form method='POST'><input type='hidden' name='correct_answer' value='{question.correct_answer}'>{html_answers}<input type='submit' value='Submit'></form></body></html>"
            return html_response.encode()
        if path == '/endquiz':
            print("Correct answers: ", QuizHandler.correct, " out of ", QuizHandler.total)
            html_response =  f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html><html><head><title>COS 332 Assignment 4</title></head><body><h1>Quiz</h1><h2>Quiz ended</h2><h3>Correct answers: {QuizHandler.correct} out of {QuizHandler.total}</h3><form method='GET' action='/'><input type='submit' value='Start quiz'></form></body></html>"
            html_response = html_response.encode()
            QuizHandler.correct = 0
            QuizHandler.total = 0
            return html_response
        else:
            return self.not_found()

    def handle_post(self, path, body):
        if path == '/':
            if not body:
                return self.invalid_request()
            
            parsed_body = dict(x.split("=") for x in body.split("&"))

            if 'answer' not in parsed_body or 'correct_answer' not in parsed_body:
                return self.invalid_request()
            
            QuizHandler.total += 1
            
            user_answer = parsed_body['answer']
            correct_answer = parsed_body['correct_answer']

            if user_answer == correct_answer:
                response = "Correct!"
                QuizHandler.correct += 1
            else:
                correct_answer = unquote(correct_answer)
                correct_answer = correct_answer.replace("+", " ")
                response = "Incorrect! The correct answer is: " + correct_answer
            html_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html><html><head><title>COS 332 Assignment 4</title></head><body><h1>Quiz</h1><h2>{response}</h2><form method='GET' action='/'><input type='submit' value='Next Question'></form><form method='GET' action='/endquiz'><input type='submit' value='End quiz'></form></body></html>"
            return html_response.encode()
        else:
            return self.not_found()

    def not_allowed(self):
        return b"HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html><html><head><title>405 Method Not Allowed</title></head><body><h1>405 Method Not Allowed</h1><a href='/'>Go to home</a></body></html>"

    def not_found(self):
        return b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html><html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1><a href='/'>Go to home</a></body></html>"

    def invalid_request(self):
        return b"HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html><html><head><title>400 Bad Request</title></head><body><h1>400 Bad Request</h1><a href='/'>Go to home</a></body></html>"
    
    
def main():

    port = 8080

    quiz_handler = QuizHandler()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)
    print('Started server on http://localhost:' + str(port))
    while True:
        client_socket, _ = server_socket.accept()
        request = client_socket.recv(1024).decode()
        response = quiz_handler.handle_request(request)
        client_socket.sendall(response)
        client_socket.close()

if __name__ == "__main__":
    main()
