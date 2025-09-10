from flask import Flask, request, render_template_string
import csv
import os
import random
import string

app = Flask(__name__)

data_file = 'data.csv'

# Certifique-se de que o arquivo data.csv existe
if not os.path.exists(data_file):
    with open(data_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['email', 'password'])

# HTML base
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auth System</title>
    <style>
        body {
            background-color: Yellow;
            color: black;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        input, button {
            margin: 5px;
        }
    </style>
</head>
<body>
    <h1>Auth System</h1>
    <form method="post">
        <input type="email" name="email" placeholder="Email" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit" name="action" value="create">Create Account</button>
        <button type="submit" name="action" value="login">Login</button>
    </form>
    {% if message %}
    <p>{{ message }}</p>
    {% endif %}
</body>
</html>
"""

# Função para gerar um código aleatório de 32 caracteres
def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        action = request.form.get('action')

        with open(data_file, 'r') as file:
            reader = csv.DictReader(file)
            users = list(reader)

        if action == 'create':
            # Verificar se o email já existe
            if any(user['email'] == email for user in users):
                message = "Email already exists."
            else:
                # Criar nova conta
                code = generate_code()
                with open(data_file, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([email, password])
                message = f"Account created successfully. Your code: {code}"

        elif action == 'login':
            # Verificar login
            user = next((user for user in users if user['email'] == email), None)
            if user and user['password'] == password:
                message = "Login successful!"
            else:
                message = "Invalid email or password."

    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    app.run(debug=True)

