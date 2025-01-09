from bson import ObjectId
from flask import Flask, request, render_template
from os import environ as env
import forms
from flask_bootstrap import Bootstrap5
from mongo import MongoDB
from os import environ as env
from flask import Flask, request, redirect, url_for, session
from stytch import Client
from stytch.core.response_base import StytchError
from auth import Auth

app = Flask(__name__)
app.secret_key = env.get('app_secret')
bootstrap = Bootstrap5(app)
### AUTH ROUTES ####
stytch_client = Client(
          project_id=env.get("STYTCH_PROJECT_ID"),
          secret=env.get("STYTCH_SECRET"),
          environment=env.get('envrionment_v')
        )
@app.route('/login_or_create_user', methods=['POST'])
def login_or_create_user() -> str:

  data = request.form.to_dict()
  email = data['email']
  if not email:
    return "Email required"

  try:


      resp = stytch_client.magic_links.email.login_or_create(
        email=email
        )
  except StytchError as e:
    return e.details.original_json

  return "Email sent! Check your inbox!"

@app.route('/authenticate', methods=['GET'])
def authenticate() -> str:
  token = request.args.get("token", None)
  token_type = request.args.get("stytch_token_type", None)

  # Distinct token_type for each auth flow
  # so you know which authenticate() method to use
  if token_type != 'magic_links':
    return f"token_type: {token_type} not supported"

  try:
    resp = stytch_client.magic_links.authenticate(
      token=request.args["token"],
      session_duration_minutes=60
    )
  except StytchError as e:
    return e.details.original_json

  session['stytch_session_token'] = resp.session_token
  return f"Hello {resp.user.emails[0].email}"

@app.route('/internal/articles', methods=["GET"])
def internal_articles() -> str:
  use = Auth()
  user = use.get_authenticated_user()
  filter_d={}
  mn = MongoDB('posts')
  list = mn.find(filter=filter_d).to_list()

  ev = MongoDB('events')
  events = ev.find(filter=filter_d).to_list()

  print('the list of articles: ', list)
  if not user:
    return "Log in to view this page."

  return render_template('internal_blogs_list.html',articles=list, events=events)


@app.route('/post/create', methods=['POST','GET'])
def create_post():
    use = Auth()
    user = use.get_authenticated_user()

    if not user:
        return url_for('login')


    if request.method == 'POST':

        data = request.form.to_dict()
        mn =  MongoDB('posts')
        mn.insert_one(data)

        print(data)

    else:

        form = forms.NewNewsArticleForm()

        return render_template('article_create.html', form = form)




    return redirect(url_for('internal_articles'))
@app.route('/event/create', methods=['POST','GET'])
def create_event():
    use = Auth()
    user = use.get_authenticated_user()

    if not user:
        return url_for('login')
    if request.method == 'POST':

        data = request.form.to_dict()
        mn =  MongoDB('events')
        mn.insert_one(data)

        print(data)

    else:

        form = forms.NewNewsArticleForm()

        return render_template('event_create.html', form = form)




    return redirect(url_for('internal_articles'))


### NON AUTH ROuTES

@app.route('/login')
def login():
    form = forms.Login()
    return render_template('login.html', form = form)

@app.route('/')
def index():

    return render_template('home.html')

@app.route('/about')
def about():

    return render_template('about.html')

@app.route('/projects')
def projects():

    return render_template('projects.html')

@app.route('/event/<id>')
def event(id):

    mn = MongoDB('events')
    data = mn.find_one({'_id': ObjectId(id)})

    return render_template('event.html',data=data)
@app.route('/impact')
def impact():

    return render_template('impact.html')@app.route('/impact')


@app.route('/events')
def events():

    filter_d = {}
    mn = MongoDB('events')
    list = mn.find(filter=filter_d).to_list()

    return render_template('events.html', events = list)

@app.route('/news')
def news():

    filter_d={}
    mn = MongoDB('posts')
    list = mn.find(filter=filter_d).to_list()


    return render_template('news.html', articles=list)
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


    return render_template('article.html', data = data)



if __name__ == "__main__":
        app.run(host="0.0.0.0", port=env.get("PORT", 8090))

