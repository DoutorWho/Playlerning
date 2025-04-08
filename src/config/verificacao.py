from flask import Blueprint, render_template, request, abort, session, make_response

# criando o Bluepirnt
verificao = Blueprint("verificao", __name__, template_folder='../../src')


# Parte de sucesso, base

@verificao.route("/sucesso")
def sucesso():
    import json
    cookie_arg = request.args.get('token', None)
    cookie_gerado = request.cookies.get("token", None)
    if ((cookie_arg == cookie_gerado) and ((cookie_arg != None) and (cookie_gerado != None))):
        dados = request.cookies.get('informacao', None)
        resposta = json.loads(dados)
        return render_template("componentes/sucesso.html", titulo=resposta['titulo'], descricao=resposta['descrição'])
    abort(404)

# Parte de verificação
@verificao.before_app_request
def verificar_solicitacoes(): # Isso evita mt autentificação nas rotas
    # verificar os comandos
    url = request.path
    email = session.get("email")
    cargo = session.get("cargo")
    if request.method == 'GET': # Aqui é se caso ele for get vamos verificar algumas coisas
        if url.startswith("/api"): # Ele não pode acessar uma API via GET
            abort(403)

        if url in ['/cadastro-submit',' /login-submit', '/configuracoes', '/configuracoes/', '/envioatividades-submit', '/forum-submit/', '/exercicio/']:
            abort(403) # Aqui da erro porque acesso get não pode entrar nesses sites

        if (email == None) and (url.startswith(('/status', '/forum', '/status/', '/admin'))): # Aqui ele nem tem conta e quer acessar essas url
            abort(403)
        
        if (cargo == 'professor') and (url.startswith(('/atividades/', '/status/', '/configuracoes'))): #  vou add mais
            abort(403)
        

    
# criando os erros

# 400 Bad Request: A solicitação não pôde ser entendida pelo servidor devido a sintaxe incorreta.
# 401 Unauthorized: A solicitação requer autenticação do usuário.
# 403 Forbidden: O servidor entendeu a solicitação, mas se recusa a autorizá-la.
# 404 Not Found: O servidor não encontrou o recurso solicitado.
# 503 Service Unavailable: O servidor não está disponível para atender a solicitação no momento.
# 301 Moved Permanently: O recurso solicitado foi movido permanentemente para uma nova URL.

@verificao.app_errorhandler(404)
def pagina_nao_encontrada(error):
    codigo = error.code
    descricao = "Página não encontrada"
    descricao_detalhada = "Não conseguimos encontrar a página que você está procurando."
    return render_template("componentes/erros.html", codigo=codigo, descricao=descricao, descricao_detalhada=descricao_detalhada), 404

@verificao.app_errorhandler(403)
def acesso_nao_autorizado(error):
    codigo = error.code
    descricao = "Acesso não autorizado"
    descricao_detalhada = "Você não tem acesso a essa página"
    return render_template("componentes/erros.html", codigo=codigo, descricao=descricao, descricao_detalhada=descricao_detalhada), 403

@verificao.app_errorhandler(400)
def erro_sem_retorno(error):
    codigo = error.code
    descricao = "Servidor não conseguiu processar a solicitação"
    descricao_detalhada = "Você não tem acesso a essa solicitação ou essa solicitação não retorna nada"
    return render_template("componentes/erros.html", codigo=codigo, descricao=descricao, descricao_detalhada=descricao_detalhada), 400