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
    
@app.route("/ver/<int:id>", methods=["GET"])
def ver(id):
    artigo = Article.query.get_or_404(id)
    return render_template("ver.html", artigo=artigo)

@app.route("/editar/<int:id>", methods=["POST"])
def editar(id):
    artigo = Article.query.get_or_404(id)
    artigo.title = request.form['titulo']
    artigo.description = request.form['descricao']
    artigo.title = request.form['titulo']
    db.session.commit()
    return redirect("/")

@app.route("/excluir/<int:id>")
def excluir(id):
    artigo = Article.query.get_or_404(id)
    db.session.delete(artigo)
    db.session.commit()
    return redirect("/")