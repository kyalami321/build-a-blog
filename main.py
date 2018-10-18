from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogpass@localhost:3307/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(120))
    post_text = db.Column(db.String(500))
    
    def __init__(self, post_title, post_text):        
        self.post_title = post_title
        self.post_text = post_text

@app.route('/', methods=['GET'])
def index():

    return redirect('/blog')

@app.route('/blog', methods=['GET'])
def blogs():

    posts = Post.query.all()
    return render_template('blog.html',title="Welcome to the Blog!", posts=posts)

@app.route('/newpost', methods=['GET','POST'])
def newpost():
    if request.method == 'POST':
        post_title = ''
        post_text = ''
        post_title = request.form['blog_post_title']
        post_text = request.form['blog_post_text']
        if post_title == '' or post_text == '':
            post_error = "You left one of the fields blank. Try, try again."
            return render_template('newpost.html', blog_post_title=post_title,blog_post_text=post_text,blank_input=post_error)
        newPost = Post(post_title, post_text)
        db.session.add(newPost)                
        db.session.commit()        
        return render_template('post.html',blog_post_title = post_title,blog_post_text=post_text)


    return render_template('newpost.html')

@app.route('/display_post', methods=['GET', 'POST'])
def display_post():
    blog_id = request.args.get('swag')
    blog_content = Post.query.filter_by(id=blog_id).first()
    blog_title = blog_content.post_title
    blog_text = blog_content.post_text
    return render_template('post.html',blog_post_title = blog_title,blog_post_text=blog_text)

    




    ###use query parameter (/?xxxxx) to display only one blog post. request.args.get ('v=XXXX)
    ###https://www.myblog.com/post?title=Inception
if __name__ == "__main__":
    app.run()