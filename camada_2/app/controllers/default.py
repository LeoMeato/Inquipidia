from app import *
from app.models.tables import *

@app.route("/")
def index():
    search = request.args.get('search', '')
    if search:
        artigos = Article.query.filter(Article.title.ilike(f"%{search}%")).all()
    else:
        artigos = Article.query.limit(10).all()
    f_artigos = []
    for a in artigos:
        f_artigos.append({"id": a.id, "title": a.title, "description": a.description, "url": f"http://127.0.0.1:8080/artigo/{a.id}"})
    dados = {}
    dados["criar"] = {"url": "http://127.0.0.1:8080/artigo"}
    dados["artigos"] = f_artigos
    accept = request.headers.get('Accept', '')
    if not accept or 'application/json' in accept:
        return jsonify(dados)
    else:
        return Response("Formato não suportado", status=406)


@app.route("/artigo/<int:id>", methods=["GET", "DELETE", "PUT"])
@app.route("/artigo", methods=["POST"])
def artigo(id=None):
    if request.method == "GET":
        artigo = Article.query.get_or_404(id)
        dados = {}
        dados["artigo"] = {"title": artigo.title, "description": artigo.description, "content": artigo.content, "url": f"http://127.0.0.1:8080/artigo/{artigo.id}"}
        accept = request.headers.get('Accept', '')
        if not accept or 'application/json' in accept:
            return jsonify(dados)
        else:
            return Response("Formato não suportado", status=406)
    if request.method == "PUT":
        dados = request.get_json()
        title = dados.get("title")
        description = dados.get("description")
        content = dados.get("content")
        artigo = Article.query.get_or_404(id)
        artigo.title = title
        artigo.description = description
        artigo.content = content
        db.session.commit()
        return jsonify({})
    if request.method == "POST":
        dados = request.get_json()
        title = dados.get("title")
        description = dados.get("description")
        content = dados.get("content")
        novo_artigo = Article(title, description, content)
        db.session.add(novo_artigo)
        db.session.commit()
        return jsonify({})
    if request.method == "DELETE":
        artigo = Article.query.get_or_404(id)
        db.session.delete(artigo)
        db.session.commit()
        return jsonify({})