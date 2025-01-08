from bson import ObjectId
from flask import Flask, request, render_template
from os import environ as env
import forms
from flask_bootstrap import Bootstrap5
from mongo import MongoDB
from os import environ as env

app = Flask(__name__)
app.secret_key = env.get('app_secret')
bootstrap = Bootstrap5(app)




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

@app.route('/news/article/<id>')
def article(id):

    mn = MongoDB('posts')
    data = mn.find_one({'_id': ObjectId(id)})
    print(data)


    return render_template('article.html', data = data)

@app.route('/post/create', methods=['POST','GET'])
def create_post():

    if request.method == 'POST':

        data = request.form.to_dict()
        mn =  MongoDB('posts')
        mn.insert_one(data)

        print(data)

    else:

        form = forms.NewNewsArticleForm()

        return render_template('article_create.html', form = form)




    return 'hello'


if __name__ == "__main__":
        app.run(host="0.0.0.0", port=env.get("PORT", 8080))

