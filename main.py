import random 
import string
import json
from flask import Flask, request, render_template, redirect, url_for, Request
app = Flask(__name__)
shortened_urls = {}
def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(length))
    return short_url
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = generate_short_url()
        while short_url in shortened_urls:
            short_url = generate_short_url()
        shortened_urls[short_url] = long_url
        with open('shortened_urls.json', 'w') as f:
            json.dump(shortened_urls, f)
            return f"Short URL is: {request.host_url}{short_url}"
    return render_template('index.html')
@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    return "URL not found", 404
if __name__ == '__main__':
    try:
        with open('shortened_urls.json', 'r') as f:
            shortened_urls = json.load(f)
    except FileNotFoundError:
        shortened_urls = {}
    app.run(debug=True)
