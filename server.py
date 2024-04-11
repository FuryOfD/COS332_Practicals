from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import random

class Question:
    def __init__(self, question, answers, correct_answer):
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer

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

def select_question(questions):
    return random.choice(questions)

# html_template = """<!DOCTYPE html>
# <html>
#     <head>
#         <title>COS 332 Assignment 4</title>
#     </head>
#     <body>
#         <h1>Quiz</h1>
#         <h2>{question}</h2>
#         <form method="post" action="/questionpage">
#             {answers}
#             <input type="submit" value="Submit">
#         </form>
#     </body>
# </html>
# """

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Quiz</title>
</head>
<body>
    <h1>Quiz</h1>
    <form method="post" action="/submit">
        <p>{question}</p>
        {answers}
        <input type="submit" value="Submit">
    </form>
    <form method="get" action="/page">
        <input type="submit" value="Go to Another Page">
    </form>
</body>
</html>
"""

html_response = """
            <!DOCTYPE html>
            <html>
                <head>
                    <title>COS 332 Assignment 4</title>
                </head>
                <body>
                    <h1>Quiz</h1>
                    <h2>{response}</h2>
                    <form method = "get" action = "/responsepage">
                        <input type="submit" value="Next Question">
                </body>
"""

def generate_html(answers):
    html_answers = ""
    for answer in answers:
        html_answers += f'<input type="radio" name="answer" value="{answer[0]}">{answer}<br>'
    return html_answers

questions = read_questions("questions.txt")

class QuizHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        #questions = read_questions("questions.txt")
        question = select_question(questions)
        
        #answers = [(i, answer) for i, answer in enumerate(question.answers)]
        answers_html = generate_html(question.answers)
        html = html_template.format(question=question.question, answers=answers_html)
        self.wfile.write(html.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        parsed_data = parse_qs(post_data)
        user_answer = parsed_data['answer'][0]
        
        if user_answer == "correct":
            response = "Correct!"
        else:
            response = "Incorrect!"
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        
        self.wfile.write(response.encode())

def main():
    #questions = read_questions("questions.txt")
    question = select_question(questions)

    for question in questions:
        print("Question:", question.question)
        print("Answers:", question.answers)
        print("Correct answer:", question.correct_answer)
        
    try :
        server = HTTPServer(('localhost', 8080), QuizHandler)
        print('Started server on http://localhost:8080')
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()
        print('Server stopped')

   

if __name__ == "__main__":
    main()