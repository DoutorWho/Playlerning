from flask import Blueprint, render_template, abort, request, session, redirect, url_for
from controllers.rotas_envios import rotas_submit
from controllers.api import api

# Criando o Blueprint e cadastrado blueprint
minhas_rotas = Blueprint("minhas_rotas", __name__, template_folder='../../src')
minhas_rotas.register_blueprint(rotas_submit)
minhas_rotas.register_blueprint(api)

# Parte Inicial

@minhas_rotas.route("/")
def index():
    email = session.get("email", None)
    cargo = session.get("cargo", None)
    if (email == None) or (cargo == 'professor'):
        return render_template("páginas/pagina_inicial.html", tipo=cargo)

    curso = session.get("curso", None)
    print("O curso é: ", curso)
    return render_template("páginas/modulos.html", tipo=curso)
    # é porque é professor, arqui eu vou da um abort por ele vai se transportado pro forum

@minhas_rotas.route("/cursos", defaults={'curso': 'padrão'})
@minhas_rotas.route("/cursos/<curso>")
def cursos(curso):  
    if curso.lower() not in ['padrão','enem', 'informatica']:
        abort(404)
    if curso.lower() in ['enem', 'informatica']:
        return render_template("páginas/tipos_cursos.html", curso=curso)
    return render_template("páginas/cursos.html")


# Parte do cadastro/login

@minhas_rotas.route("/cadastrar")
def cadastro():
    email = session.get("email", None)
    if email != None: # Ou seja, se ele já foi cadastrado
        return redirect(url_for("minhas_rotas.index"))
    
    return render_template("/páginas/cadastro.html", erro='')

@minhas_rotas.route("/login") 
def login():
    email = session.get("email", None)
    if email != None: # Ou seja, se ele já foi cadastrado
        return redirect(url_for("minhas_rotas.index"))

    return render_template("páginas/login.html", erro='')


# Parte do usuário já conectado

@minhas_rotas.route("/atividades/<nome>/<disciplina>") # se o nome deve ser enem ou informatica e lá sabemos qual disicplina está relacionada
def atividades(nome, disciplina):
    from config.atividades import Controle
    # verificar se ele tem conta, o sesion
    email = session.get('email', None)
    if email == None:
        abort(404)
    # usar o sistema de segurança para verificar se os nomes estão coretos, se tá tudo certo | Já tá sendo usado
    # aqui eu coloco pra retornar o valor de nome e disicplina, já com tudo editado e formato. | Já sendo usado
    atividade = Controle.diretorio_correto(nome=nome, disciplina=disciplina, email=email)
    if atividade[0]:
        return render_template("páginas/atividades.html", secao=nome, disicplina_nome=disciplina, nome_titulo=atividade[1], disciplina_titulo=atividade[2], secoes=atividade[3], enumerate=enumerate)
    abort(404)


# Parte de Status 


@minhas_rotas.route("/status", defaults={'nome': 'home'})
@minhas_rotas.route('/status/<nome>')
def status(nome):
    from config.usuarios import Status
    email = session.get("email", None)
    if email == None: # Não tem conta
        abort(404)
    
    if nome == 'home':
        return redirect(url_for("minhas_rotas.index")) # Eu tenho que resolver isso, para ao invés de aparecer, home ou informática, aparecer o curso que ele quer fazer. Isso também no Login, adapatar esse home aí.
    if nome not in ['perfil', 'missoes', 'rank', 'configuracoes']:
        abort(404)

    missao = Status.missoes(email=email) # aterar isso, pegar do sesion o email dele
    rank = Status.rank(email)
    perfil = Status.perfil(email)
    return render_template("páginas/status.html", titulo=nome.title(), status=nome, missao=missao, rank=rank, perfil=perfil)


# Parte do fórum

@minhas_rotas.route("/forum", defaults={'nome': 'padrão'})
@minhas_rotas.route("/forum/<nome>")
def forum(nome):
    from main import app
    from config.usuarios import Comentario
    # forum ou comentario
    # configurar depois pq vai ser forum/alguma coisa, vai ter args pra saber qual é o tópico, etc
    # parte de pesquisa
    pesquisa = request.args.get("pesquisa", None)
    if pesquisa != None: # Simplismente se pesquisa for diferente de None, é porque ele tá fazendo uma pesquisa, que ficará na url none e irá gerar esse render template, para uma página de pesquisa!
        return render_template("páginas/forum_topicos.html") # usar um redirect, é mais fácil!

    # parte normal
    print("Exeutei")
    if nome == 'padrão':
        topicos = Comentario.todos_topico()
        return render_template("páginas/forum.html", secao='forum', topicos=topicos)
    
    if nome == 'comentarios':
        print("Entrei aqui")
        # é porque ele escolheu algum tópico
        topico_id = request.args.get('topico', None)
        if topico_id == None: # A final, ele deu /topico e o não tem o args
            abort(404)
        retorno = Comentario.ver_topico(topico_id)
        print(retorno[0])
        # aqui vamos verificar se o tópico existe
        if retorno[0]:
            nickname = session.get("nickname", None)
            return render_template("páginas/forum.html", enumerate=enumerate, secao='comentario', nickname_usuario=nickname, topico=retorno[1], comentarios=retorno[2])
        abort(404)


# Rodapé
@minhas_rotas.route("/politica")
def politica_privacidade():
    return render_template("páginas/politicas_de_privacidade.html")

@minhas_rotas.route("/termodeuso")
def termo_de_uso():
    return render_template("páginas/termos_de_uso.html")

@minhas_rotas.route("/sobrenos")
def sobrenos():
    return render_template("páginas/sobre_nos.html")

@minhas_rotas.route("/contato")
def contato():
    return render_template('/páginas/contato.html')

@minhas_rotas.route("/servicos")
def servicos():
    return render_template("/páginas/servicos.html")


# Parte de admin

@minhas_rotas.route("/admin", defaults={'nome': 'padrão'})
@minhas_rotas.route("/admin/<nome>")
def admin(nome):
    from config.seguranca import Admin
    if nome == 'padrão': # quer acessar o admin normal
        cargo = session.get("cargo", None)
        return render_template("páginas/admin.html", cargo=cargo)
    if nome == 'geral':
        # Pegar uma informação, via api, sobre total usuarios, usuarios banidos, total topicos e total comentatarios
        dados = Admin.informacoes_gerais()
        return render_template('páginas/admin_partes.html', status="geral", dados=dados)
    if nome == "punicao":
        return render_template('páginas/admin_partes.html', status="punição")
    if nome == "aprovacao":
        dados = Admin.aprovacao_lista()
        return render_template('páginas/admin_partes.html', status="aprovação", dados=dados)
    # parte de atividades
    if nome == "adicionaratividades":
        return render_template('páginas/admin_partes.html', status="adicionar_atividade")
    # Isso é a parte de admin para mostrar todas as atividades
    if nome == 'todasatividades':
        secao = request.args.get('secao', None)
        if (secao == None) or (secao not in ['informatica', 'enem']):
            abort(400)
        return render_template("páginas/admin_partes_atividades.html", secao=secao)



# Teste


@minhas_rotas.route("/pesquisar", methods=['POST', 'GET'])
def pesquisar():
    from main import app
    pesquisa = request.form.get("pesquisa", None)
    with app.test_client() as client:
        response = client.get(f'/api/pesquisartopico?pesquisa={pesquisa}')
        print(response)
    # colocar pra se caso for get ele sair

    return render_template("páginas/forum_topicos.html")

'''    with app.test_client() as client:
        response = client.get(f'/api/pesquisartopico?pesquisa={pesquisa}')''' # Para fazer um teste no client, eu tenho que importar o app também!

