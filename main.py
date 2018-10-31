from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '48957w9875kjsdhfkahsdkj'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    b_title = db.Column(db.String(50))
    body = db.Column(db.String(600))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, b_title, body, owner):
        self.b_title = b_title
        self.body = body
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password








@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blog_list']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')






@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            return redirect('/blog_list')
        if not user:
            return render_template('login.html', user_error='Invalid user')
        else:
            return render_template('login.html', pass_error='Invalid password')


    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data
        username_error =""
        pass_error = ""
        verify_error = ""
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            username_error = "User already exists"

        if len(username) > 10 or len(username) < 3 or " " in username:
            username_error = "Username must be between 3 and 10 characters and mut not contain spaces"

        if not password:
            pass_error = "You must enter a password"
        if " " in password:
            pass_error = "Password must not contain spaces"
        if len(password) < 3 or len(password) > 20:
            pass_error = "Your pass is too short or too long"

        if not verify:
            verify_error = "you must re-enter a password"
        if verify != password:
            verify_error = "Passwords must match"

        if not existing_user and not username_error and not pass_error and not verify_error:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            # TODO - user better response messaging
            return render_template('/signup.html', username_error=username_error, pass_error=pass_error, verify_error=verify_error)

    return render_template('signup.html')

@app.route('/index', methods=['GET', 'POST'])
def home():
    users = User.query.all()
    return render_template('signup.html', users=users)

@app.route('/singleUser', methods=['GET', 'POST'])
def singleUser():
    author = request.args.get('user')
    posts = Blog.query.filter_by(owner_id = author).all()
    return render_template('singleUser/html', blogs=posts)

@app.route('/blog_list', methods=['POST', 'GET'])
def blog_list():
    if request.args:

        id = request.args.get('id')
        search = request.args.get(id)
        return render_template('singlePost.html', post=search)
    else:
        search = Blog.query.all()
        return render_template('blog_list.html', blog=search)


@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        b_title = request.form['b_title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        title_error= ''
        body_error =''
        if not b_title:
            title_error="Enter a title"
        if not body:
            body_error="Enter a blog"
        if not title_error and not body_error:
            new_blog = Blog(b_title, body, owner)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog_list?id=' + str(new_blog.id))
        return render_template('newpost.html', title_error=title_error, body_error=body_error, owner=owner, body=body)
    else:
        return render_template("newpost.html")



@app.route('/logout')
def logout():
    del seesion['username']
    return redirect('/')

if __name__ == '__main__':
    app.run()
