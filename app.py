from flask import Flask,request,redirect,url_for
from flask import  render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from flask_bootstrap import Bootstrap


from sqlalchemy.sql import func

app= Flask(__name__)

students=[{"id":"1","name":"ali","track":"iti"},{"id":"2","name":"ali","track":"iti"},{"id":"3","name":"ali","track":"iti"}]

#connect to database

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db=SQLAlchemy(app)






# @app.route('/')
# def helloworld():
#     # no need to return with http response ---> return with it automatically
#     return  render_template("index.html",students=students)

# @app.route('/student/<id>')
# def get_info(id):
#     returned_student = filter(lambda std: std['id'] == id, students)
#     returned_student = list(returned_student)
#     if returned_student:
#         # print(returned_student[0])
#         # return returned_student[0]
#         student = returned_student[0]
#         return render_template("student/show.html", student=student)
#     # return "not found", 404
#     return render_template("pagenotefound.html"), 404

def li():
    lis=["py","django","css","oddo"]
    return lis

app.add_url_rule("/li",view_func=li)

@app.route("/say/<name>")
def sayhello(name):
    return f"<h1 style='color:red; text-align:center'>info {name}</h1>"

@app.errorhandler(404)
def notfound(error):
    return "eror 404"


#model section
class Post (db.Model):
    __tablename__="posts"
    id =db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)

@app.route('/posts',endpoint="posts.index")
def show_posts():
    posts=Post.query.all()
    return render_template("post/show.html",posts=posts)    


@app.route("/posts/<int:id>",endpoint="posts.show")
def get_post(id):
    post= Post.query.get_or_404(id)
    return render_template("post/showpost.html",post=post)

@app.route("/posts/<int:id>/delete",endpoint="posts.delete")
def delete_post(id):
    post= Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    url=url_for("posts.index")
    return redirect(url)

@app.route("/posts/create",endpoint="posts.create",methods=["GET","POST"])
def create_post():
    ## request method POST
    if request.method == "POST":
        print(request.form)
        post_title = request.form["title"]
        post_body = request.form["body"]
        post = Post(title=post_title, body=post_body)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('posts.index'))

    ## request method GET ?
    return render_template("post/create.html")

@app.route("/posts/<int:id>/update",endpoint="posts.update",methods=["GET","POST"])
def update_post(id):
    post= Post.query.get_or_404(id)
    if request.method == "POST":
        post_title = request.form["title"]
        post_body = request.form["body"]
        post.title=post_title
        post.body=post_body
        db.session.commit()
        return redirect(url_for('posts.index'))
    return render_template("post/update.html",post=post)

if __name__ == '__main__':
    app.run(debug=True)
