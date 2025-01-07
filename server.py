from flask import Flask, request, render_template
from os import environ as env


app = Flask(__name__)

@app.route('/')
def index():

    return render_template('home.html')

@app.route('/about')
def about():

    return render_template('about.html')

@app.route('/projects')
def projects():

    return render_template('projects.html')

@app.route('/events')
def events():

    return render_template('events.html')
@app.route('/impact')
def impact():

    return render_template('impact.html')
@app.route('/news')
def news():

    return render_template('news.html')
@app.route('/resources')
def resources():

    return render_template('resources.html')
@app.route('/team')
def team():

    return render_template('team.html')
@app.route('/partners')
def partners():

    return render_template('partners.html')
@app.route('/contact')
def contact():

    return render_template('contact.html')

@app.route('/privacy')
def privacy():

    return render_template('privacy.html')

@app.route('/cookie')
def cookie():

    return render_template('cookie.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))

