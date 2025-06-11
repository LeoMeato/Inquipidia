from app import *
from app.models.tables import *
from urllib.parse import quote


@app.route("/")
def index():
    search = request.args.get('search', '')
    if search:
        artigos = Article.query.filter(Article.title.ilike(f"%{search}%")).all()
    else:
        artigos = Article.query.limit(10).all()
    f_artigos = []
    for a in artigos:
        f_artigos.append({"id": a.id, "title": a.title, "description": a.description, "url": quote(f"http://127.0.0.1:8080/ver/{a.id}")})
    dados = {}
    dados["criar"] = {"url": quote("http://127.0.0.1:8080/criar")}
    dados["artigos"] = f_artigos
    return jsonify(dados)

@app.route("/criar", methods=["POST"])
def criar():
    dados = request.get_json()
    titulo = dados.get("titulo")
    descricao = dados.get("descricao")
    conteudo = dados.get("conteudo")
    novo_artigo = Article(titulo, descricao, conteudo)
    db.session.add(novo_artigo)
    db.session.commit()
    return jsonify({})
    
@app.route("/ver/<int:id>", methods=["GET"])
def ver(id):
    artigo = Article.query.get_or_404(id)
    dados = {}
    dados["artigo"] = {"title": artigo.title, "description": artigo.description, "content": artigo.content}
    dados["editar"] = quote(f"http://127.0.0.1:8080/editar/{artigo.id}")
    dados["excluir"] = quote(f"http://127.0.0.1:8080/excluir/{artigo.id}")
    return jsonify(dados)

@app.route("/editar/<int:id>", methods=["POST"])
def editar(id):
    dados = request.get_json()
    titulo = dados.get("titulo")
    descricao = dados.get("descricao")
    conteudo = dados.get("conteudo")
    artigo = Article.query.get_or_404(id)
    artigo.title = titulo
    artigo.description = descricao
    artigo.content = conteudo
    db.session.commit()
    return jsonify({})

@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    print("id")
    artigo = Article.query.get_or_404(id)
    db.session.delete(artigo)
    db.session.commit()
    return jsonify({})