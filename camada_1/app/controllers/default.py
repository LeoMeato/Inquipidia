from app import app, render_template, redirect, request
import requests
from urllib.parse import unquote

@app.route("/")
def index():
    search = request.args.get('search', '')
    if search:
        url = f"http://127.0.0.1:8080/?search={search}"
    else:
        url = "http://127.0.0.1:8080/"
    response = requests.get(url)
    dados = response.json()
    return render_template("index.html", criar=dados["criar"] , artigos=dados["artigos"])

@app.route("/criar/<path:url>", methods=["GET", "POST"])
def criar(url):
    if request.method == "POST":
        novo_artigo = {"titulo": request.form['titulo'], "descricao": request.form["descricao"], "conteudo": request.form["conteudo"]}
        response = requests.post(unquote(url), json=novo_artigo)
        return redirect("/")
    else:
        return render_template("criar.html", url=url)
    
@app.route("/ver/<int:id>/<path:url>", methods=["GET"])
def ver(id, url):
    response = requests.get(unquote(url))
    dados = response.json()
    dados["artigo"]["id"] = id
    return render_template("ver.html", dados=dados)

@app.route("/editar/<int:id>/<path:url>", methods=["POST"])
def editar(id, url):
    artigo = {}
    artigo['titulo'] = request.form['titulo']
    artigo['descricao'] = request.form['descricao']
    artigo['conteudo'] = request.form['conteudo']
    response = requests.post(unquote(url), json=artigo)
    return redirect("/")

@app.route("/excluir/<int:id>/<path:url>")
def excluir(id, url):
    response = requests.post(unquote(url))
    return redirect("/")