
from flask import Flask, request, redirect, url_for, render_template_string, send_from_directory
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

uploads_list = []

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email.endswith('@siddhartha.co.in') and password:
        return redirect('/dashboard')
    return "Invalid credentials", 401

@app.route('/login/google')
def google_login():
    return "Google login placeholder (implement OAuth2 here)"

@app.route('/dashboard')
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE, files=uploads_list)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    desc = request.form.get('description')
    if file:
        filename = datetime.now().strftime('%Y%m%d%H%M%S_') + secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        uploads_list.append({'url': f'/uploads/{filename}', 'description': desc})
    return redirect('/dashboard')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SITS CSE(se) - Dashboard</title>
  <style>
    body {
      background: #000;
      color: #0ff;
      font-family: 'Arial', sans-serif;
      padding: 40px;
    }
    h1 { color: #0ff; }
    input, textarea {
      display: block;
      margin: 10px 0;
      padding: 10px;
      background: #000;
      color: #0ff;
      border: 2px solid #0ff;
      border-radius: 5px;
    }
    button {
      background: #0ff;
      border: none;
      padding: 10px;
      font-weight: bold;
      border-radius: 5px;
      cursor: pointer;
    }
    .uploads img {
      max-width: 100%;
      margin-top: 10px;
      border: 1px solid #0ff;
      border-radius: 10px;
    }
  </style>
</head>
<body>
  <h1>Welcome to SITS CSE(se) Dashboard</h1>
  <form action="/upload" method="post" enctype="multipart/form-data">
    <input type="text" name="description" placeholder="Description" required />
    <input type="file" name="file" accept="image/*" required />
    <button type="submit">Upload</button>
  </form>
  <div class="uploads">
    {% for file in files %}
      <div><p>{{file.description}}</p><img src="{{ file.url }}" alt="Uploaded"/></div>
    {% endfor %}
  </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
