from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '48957w9875kjsdhfkahsdkj'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    blog = db.Column(db.String(600))


    def __init__(self, name, blog):
        self.name = name
        self.blog = blog

def blog_name_validate(name):
    if name == "":
        return "enter a title"
    else:
        return ""

def blog_body_validate(content):
    if content == "":
        return "please enter a paragraph"
    else:
        return ""



@app.route('/blog', methods=['GET', 'POST'])
def index():

    id = request.args.get('id')
    if id != None:
        data=Blog.query.filter_by(id=id).all()
        return render_template('blog.html', title=data[0].name, blog=data[0], one_post=True)
    else:
        data = Blog.query.all()
        return render_template('blog.html', title="Build A Blog", blogs=data, one_post=False)



@app.route('/newpost', methods=['GET', 'POST'])
def new_blog():
    if request.method == 'POST':
        blog_name = request.form.get('name')
        blog_body = request.form.get('content')
        if blog_name_validate(blog_name) or blog_body_validate(blog_body) != "":
            return render_template('newpost.html', title="Enter new blog", title_error=blog_name_validate(blog_name), content_error=blog_body_validate(blog_body), old_name=blog_name, old_entry=blog_body)
        else:
            new_blog = Blog(blog_name, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog?id=' + str(new_blog.id))
    else:
        return render_template("newpost.html", title="New One")




if __name__ == '__main__':
    app.run()