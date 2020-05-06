from app import app, photos, db
from model import User, Tweet, followers
from forms import RegisterForm, LoginForm, TweetForm
from flask import  render_template, redirect, url_for,request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import login_user, login_required, current_user, logout_user

@app.route('/')
def index():
    form = LoginForm()

    return render_template('index.html', form = form, logged_in_user = current_user)

#aici se face login-ul propriu zis
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            return render_template('index.html', form = form, message = 'Login Failed')

        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('profile'))
        else:
            return render_template('index.html', form = form, message = 'Login Failed')

    else:
        return render_template('index.html', form = form)


@app.route('/profile', defaults={'username' : None})
@app.route('/profile/<username>')
def profile(username):
    if username:
        user = User.query.filter_by(username = username).first()
        if not user:
            abort(404)
        #user_id = user.id
        
    else:
        user = current_user
        #user_id = current_user.id
    
    tweets = Tweet.query.filter_by(user=user).order_by(Tweet.date_created.desc()).all()

    current_time = datetime.now()

    followed_by = user.followed_by.all()

    display_follow = True
    if current_user == user:
        display_follow = False
    else:
        if current_user in followed_by:
            display_follow = False

    #aduc 4 useri random din baza de date
    who_to_watch = User.query.filter(User.id != user.id).order_by(db.func.random()).limit(4).all()

    
    return render_template('profile.html', current_user=user, tweets = tweets, current_time = current_time, followed_by = followed_by, display_follow = display_follow, who_to_watch = who_to_watch, logged_in_user = current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        image_filename = photos.save(form.image.data)
        image_url = photos.url(image_filename)

        #salvam in baza de date cu sql_alchemy
        new_user = User(name=form.name.data, username=form.username.data, password=generate_password_hash(form.password.data), image=image_url, join_date=datetime.now())
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        return redirect(url_for('profile'))
    return render_template('register.html', form=form)


@app.route('/timeline', defaults={'username' : None}) # punem pe default nimic la route
@app.route('/timeline/<username>')
def timeline(username):
    form = TweetForm()
    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
        #user_id = user.id
        #selectez dupa id si ordonez
        tweets = Tweet.query.filter_by(user=user).order_by(Tweet.date_created.desc()).all()
        total_tweets = len(tweets)
    else:
        user = current_user
        #user_id = current_user.id
        tweets = Tweet.query.join(followers, followers.c.followee_id == Tweet.user_id).filter(followers.c.follower_id == current_user.id).order_by(Tweet.date_created.desc()).all()
        total_tweets = Tweet.query.filter_by(user=user).order_by(Tweet.date_created.desc()).count()


    current_time = datetime.now()
    who_to_watch = User.query.filter(User.id != user.id).order_by(db.func.random()).limit(4).all()

    followed_by_count = user.followed_by.count() 

    return render_template('timeline.html', form=form, tweets = tweets, current_time=current_time, current_user=user,total_tweets=total_tweets, who_to_watch = who_to_watch, logged_in_user = current_user, followed_by_count = followed_by_count)


@app.route('/post_tweet',methods=['POST'])
@login_required
def post_tweet():
    form = TweetForm()
    if form.validate():
        #inseram in baza de date
        tweet = Tweet(user_id=current_user.id, text = form.text.data, date_created = datetime.now())
        db.session.add(tweet)
        db.session.commit()
        # ma intorc pe aceasi pagina
        return redirect(url_for('timeline'))
        
    return 'Something went wrong'

@app.route('/follow/<username>')
@login_required
def follow(username):
    user_to_follow = User.query.filter_by(username = username).first()
    
    current_user.following.append(user_to_follow)

    db.session.commit()

    return redirect(url_for('profile')) 
