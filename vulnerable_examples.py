import os
import ast
import json
import sqlite3
import subprocess
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt

SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key-123")
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1")

def search_vulnerable(request, MyModel):
    q = request.GET.get("q", "")
    rows = MyModel.objects.raw("SELECT * FROM myapp_mymodel WHERE name LIKE %s", [f"%{q}%"])
    return rows


def save_comment_vulnerable(request, CommentModel):
    user_input = request.POST.get("comment", "")
    comment = CommentModel()
    comment.html = escape(user_input)
    comment.save()
    return comment


def backup_vulnerable(request):
    filename = request.GET.get("file", "")
    safe_filename = os.path.basename(filename)
    if not safe_filename:
        return "error"
    subprocess.run(
        ["tar", "-czf", f"/backup/{safe_filename}.tar.gz", f"/data/{safe_filename}"],
        shell=False,
        check=True
    )
    return "ok"

# Заміна pickle на безпечний JSON
def load_object_vulnerable(uploaded_file):
    data = uploaded_file.read()
    obj = json.loads(data.decode("utf-8"))
    return obj


@csrf_protect
def update_profile_vulnerable(request):
    return "profile updated"


def get_user_data(username):
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user_data = cursor.fetchall()
    db.close()
    return user_data


def calculate_expression(expression):
    """
    Безпечно обчислює математичний вираз без використання eval().
    """
    try:
        parsed = ast.parse(expression, mode='eval')
        result = _safe_eval_math(parsed.body)
        print(f"Результат: {result}")
        return result
    except Exception as e:
        print(f"Помилка: {e}")
        return None

# Приклад використання:
calculate_expression("2 + 3 * 4")


def run_user_expression():
    user_input = input("Enter math expression: ")
    try:
        parsed = ast.parse(user_input, mode='eval')
        result = _safe_eval_math(parsed.body)
        print("Result:", result)
    except Exception as e:
        print(f"Invalid expression: {e}")