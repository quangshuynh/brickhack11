from flask import Flask, render_template, request, jsonify
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)