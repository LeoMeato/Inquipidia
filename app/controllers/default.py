from app import app, db, render_template, redirect, request
from app.models.tables import *


@app.route("/")
def index():
    artigos = Article.query.limit(10).all()
    return render_template("index.html", artigos=artigos)

@app.route("/criar", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        novo_artigo = Article(request.form['titulo'], request.form['descricao'], request.form['conteudo'])
        db.session.add(novo_artigo)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("criar.html")