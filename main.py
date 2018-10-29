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
    blog = db.Column(db.String(600))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, b_title, blog):
        self.b_title = b_title
        self.blog = blog

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(20))
    blog = db.relationship('Blog', backref='owner')

    def __init__(self, username, password, blog):
        self.username = username
        self.password = password
        self.blog = blog


def title_validate(b_title):
    if b_title is None:
        return "enter a title"
    else:
        return ""

def blog_validate(blog):
    if blog is None:
        return "please enter a paragraph"
    else:
        return ""



@app.route('/blog', methods=['GET', 'POST'])
def index():

    id = request.args.get('id')
    if id != None:
        info=Blog.query.filter_by(id=id).all()
        return render_template('blog.html', title=info[0].b_title, blog=info[0], one_post=True)
    else:
        info = Blog.query.all()
        return render_template('blog.html', title="Build A Blog", blog=info, one_post=False)



@app.route('/newpost', methods=['GET', 'POST'])
def new_blog():
    if request.method == 'POST':
        b_title = request.form.get('name')
        blog = request.form.get('content')
        if title_validate(b_title) or blog_validate(blog) != "":
            return render_template('newpost.html', title="Enter new blog", title_error=title_validate(b_title), c_error=blog_validate(blog), old_name=b_title, old_entry=blog)
        else:
            new_blog = Blog(b_title, blog)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog?id=' + str(new_blog.id))
    else:
        return render_template("newpost.html", title="New One")



if __name__ == '__main__':
    app.run()
