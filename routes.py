from flask import request, render_template, redirect, url_for, session, flash
from bson import ObjectId
from mongo import MongoDB
from auth import Auth
from google_storage import GoogleStorage
import forms
from stytch.core.response_base import StytchError
import os

def register_routes(app):
    stytch_client = app.stytch_client
    env = os.environ

    @app.route('/authenticate', methods=['GET'])
    def authenticate() -> str:
        token = request.args.get("token", None)
        token_type = request.args.get("stytch_token_type", None)

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
        return redirect(url_for('internal_articles'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = forms.Login()
        
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            if not email:
                flash("Email required", "error")
                return redirect(url_for('login'))

            try:
                resp = stytch_client.magic_links.email.login_or_create(
                    email=email,
                    login_magic_link_url=env.get('STYTCH_REDIRECT_URL'),
                    signup_magic_link_url=env.get('STYTCH_REDIRECT_URL')
                )
                flash("Email sent! Check your inbox!", "success")
                return redirect(url_for('login'))
            except StytchError as e:
                error_type = getattr(e, 'error_type', '')
                if error_type == 'inactive_email':
                    flash("This email address cannot receive messages. Please try a different email address or contact support.", "error")
                else:
                    print(f"Stytch Error: {str(e)}")  # Log the full error
                    flash("An error occurred sending the login link. Please try again.", "error")
                return redirect(url_for('login'))
            except Exception as e:
                print(f"Unexpected Error: {str(e)}")
                flash("An unexpected error occurred. Please try again.", "error")
                return redirect(url_for('login'))
        
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}", "error")
        
        return render_template('login.html', form=form)

    @app.route('/upload/image', methods=['POST'])
    def upload_image():
        file = request.files['image']

        if 'image' not in request.files:
            return 'No file uploaded', 400

        if file.filename == '':
            return 'No file selected', 400

        g = GoogleStorage()
        file_url = g.upload_to_gcs(file)
        return {'success': True, 'file_url': file_url}, 200

    @app.route('/internal/articles', methods=["GET"])
    def internal_articles() -> str:
        use = Auth()
        user = use.get_authenticated_user()
        filter_d = {}
        mn = MongoDB('posts')
        list = mn.find(filter=filter_d).to_list()

        ev = MongoDB('events')
        events = ev.find(filter=filter_d).to_list()

        form = forms.ImageForm()
        goog = GoogleStorage()
        files = goog.list_files_in_bucket()

        if not user:
            return redirect(url_for('internal_articles'))

        return render_template('internal_blogs_list.html', articles=list, events=events, form=form, files=files)

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
        return render_template('event.html', data=data)

    @app.route('/impact')
    def impact():
        return render_template('impact.html')

    @app.route('/events')
    def events():
        filter_d = {}
        mn = MongoDB('events')
        list = mn.find(filter=filter_d).to_list()
        return render_template('events.html', events=list)

    @app.route('/news/article/<id>')
    def article(id):
        mn = MongoDB('posts')
        data = mn.find_one({'_id': ObjectId(id)})
        return render_template('article.html', data=data)

    @app.route('/post/delete', methods=['GET'])
    def delete_post() -> str:
        post_id = request.args.get("post_id", None)
        query = {'_id': ObjectId(post_id)}
        mn = MongoDB('posts')
        mn.delete(query)
        return redirect(url_for('internal_articles'))

    @app.route('/event/delete', methods=['GET'])
    def delete_event() -> str:
        event_id = request.args.get("event_id", None)
        query = {'_id': ObjectId(event_id)}
        mn = MongoDB('events')
        mn.delete(query)
        return redirect(url_for('internal_articles'))

    @app.route('/event/edit', methods=['POST', 'GET'])
    def edit_event():
        use = Auth()
        user = use.get_authenticated_user()
        event_id = request.args.get('event_id')
        if not user:
            return url_for('login')

        if request.method == 'POST':
            data = request.form.to_dict()
            query = {'_id': ObjectId(event_id)}
            mn = MongoDB('events')
            mn.update_or_insert(document=data, filter=query)
        else:
            query = {'_id': ObjectId(event_id)}
            mn = MongoDB('events')
            event_data = mn.find(query).to_list()
            form = forms.NewNewsArticleForm(obj=event_data[0])
            form.title.data = event_data[0]['title']
            form.content.data = event_data[0]['content']
            return render_template('event_create.html', form=form, post_data=event_data[0], event_id=event_id)

        return redirect(url_for('internal_articles'))

    @app.route('/post/edit', methods=['POST', 'GET'])
    def edit_post():
        use = Auth()
        user = use.get_authenticated_user()
        post_id = request.args.get('post_id')
        if not user:
            return url_for('login')

        if request.method == 'POST':
            data = request.form.to_dict()
            query = {'_id': ObjectId(post_id)}
            mn = MongoDB('posts')
            mn.update_or_insert(document=data, filter=query)
        else:
            query = {'_id': ObjectId(post_id)}
            mn = MongoDB('posts')
            post_data = mn.find(query).to_list()
            if len(post_data) == 0:
                data = None
                content = None
                title = None
            else:
                data = post_data[0]
                content = data['content']
                title = data['title']

            form = forms.NewNewsArticleForm(obj=data or None)
            goog = GoogleStorage()
            files = goog.list_files_in_bucket()
            list = [(file['name'], file['url']) for file in files]
            form.image.choices = list
            form.title.data = title
            form.content.data = content
            return render_template('article_create.html', form=form, post_data=data, post_id=post_id)

        return redirect(url_for('internal_articles'))

    @app.route('/event/create', methods=['POST', 'GET'])
    def create_event():
        use = Auth()
        user = use.get_authenticated_user()

        if not user:
            return url_for('login')

        if request.method == 'POST':
            data = request.form.to_dict()
            mn = MongoDB('events')
            mn.insert_one(data)
        else:
            form = forms.NewNewsArticleForm()
            return render_template('event_create.html', form=form)

        return redirect(url_for('internal_articles'))

    @app.route('/news')
    def news():
        filter_d = {}
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

    # ... Add the rest of your routes here ...
    # (post/edit, event/edit, news, resources, team, partners, contact, etc.)

    # ... rest of your routes ... 