from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' #обращ-ся к словарю и указ-ем с какой БД работаем и ее назв-е
db = SQLAlchemy(app)

class Article(db.Model): # созд-и табл с полями ниже:
    id = db.Column(db.Integer, primary_key=True)# ид
    title = db.Column(db.String(100),nullable=False)# назвние
    intro = db.Column(db.String(300), nullable=False)# краткое описание
    text = db.Column(db.Text, nullable=False)# полный текст
    date = db.Column(db.DateTime, default=datetime.utcnow)# дата созд-я,если не ук-ли сами,созд-ся автом-ки

#когда будем выбирать обьект на основе этого класса,будет выдаваться сам обьект,
    #который представляет определенную запись в БД и ее id
    def __repr__(self):
        return '< Article %r>' % self.id


@app.route('/')# переход по / на главную страницу
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about') # переход по /about на втор-ю стр
def about():
    return render_template('about.html')


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("posts_detail.html", article=article)


@app.route('/posts/<int:id>/del')
def posts_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении записи произошла ошибка!"


@app.route('/posts/<int:id>/update', methods=['POST','GET'])
def posts_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При редактировании статьи произошла ошибка!'

    else:
        article = Article.query.get(id)
        return render_template('posts-update.html', article=article)



@app.route('/create-article', methods=['POST','GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title,intro=intro,text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При добавлении статьи произошла ошибка!'

    else:
        return render_template('create-article.html')



if __name__  == '__main__':
    app.run(debug=True)
