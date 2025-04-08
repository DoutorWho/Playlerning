from flask import Blueprint, abort, request, session

api = Blueprint("api", __name__, template_folder='../../src')

# Parte da base
@api.route("/api/modoclaroouescuro", methods=['POST', 'GET'])
def api_modo():
    from flask import jsonify
    from models.database import db, Usuarios
    email = session.get("email", None)
    if email == None:
        abort(403)
    tipo = request.args.get("tipo", None)
    usuario = Usuarios.query.filter_by(email=email).first()
    if tipo == 'enviar':
        print("Entrei aqui rapaziada!")
        modo_recebido = request.args.get("modo", None)
        print("O modo é: ", modo_recebido)
        usuario.modo = modo_recebido
        db.session.commit()
    modo_usuario = usuario.modo.value
    modo = {"modo": modo_usuario}
    return jsonify(modo)


@api.route("/api/informacoesusarios", methods=['GET', 'POST'])
def informacoes_usuarios():
    from flask import jsonify
    cargo = session.get("cargo")
    return jsonify({'nome': cargo})

# Outras partes
@api.route("/api/atividadesapi", methods=['GET', 'POST'])
def api_atividades():
    from flask import jsonify
    from config.atividades import Controle
    email = session.get("email", None) # organizar isso para evitar que eles acessem mesmo sem ter EMAIL
    if email == None:
        abort(403)
    curso = request.args.get("curso", None)
    disciplina = request.args.get("disciplina", None)
    if (curso == None) or (disciplina == None):
        abort(404)
    print("A unidade é ", curso)
    print("A atividade é ", disciplina) # linguaguens linguagens
    atividade = Controle.diretorio_correto(nome=curso, disciplina=disciplina, email=email)
    return jsonify(atividade[4][0])

@api.route("/api/pesquisartopico", methods=['GET', 'POST'])
def pesquisar_topico():
    from datetime import datetime
    from flask import jsonify
    from models.database import db, Comentarios, Topico as Topicos_lista
    email = session.get("email", None)
    # edição aqui
    ''''pesquisa = session.get("pesquisa", None)
    session.pop("pesquisa", None)
    print("A pesquisa é ", pesquisa)'''
    pesquisa = request.args.get("pesquisa", None)
    # continação
    if (email == None) or (pesquisa == None) or (pesquisa == ''):
        abort(404)
    pesquisa = pesquisa.strip()
    # Caso não seja
    idsTopicos = []
    pesquisa = str(pesquisa).upper()
    topicos = Topicos_lista.query.all()
    for topico in topicos:
        if (pesquisa in str(topico.nome).upper()) or (pesquisa in str(topico.descricao).upper()):
            data = datetime.strftime(topico.data, "%d/%m/%Y")
            comentario = Comentarios.query.filter_by(idTopico=topico.idTopico).count()
            idsTopicos.append({'idTopico': topico.idTopico, 'nome': topico.nome, 'data': data, 'quantidade_comentarios': comentario, 'autor': topico.autor, 'categoria': topico.categoria.value, 'status': topico.status.value})
    return jsonify(idsTopicos)


@api.route("/api/buscardadosusuario", methods=['GET', 'POST'])
def buscarDadosUsuario():
    from flask import jsonify
    from models.database import Usuarios
    nome = request.args.get("nome", None)
    usuario = Usuarios.query.filter_by(nickname=nome).first()
    if usuario == None:
        return jsonify()
    dados = {'cargo': usuario.cargo.value, 'rank': 'bronze', 'email': usuario.email, 'xp': usuario.xp} # configurar o rank dps atráves do xp
    print("Os dados são: ",dados)
    return jsonify(dados)
    

@api.route("/api/listadebanidos", methods=['GET', 'POST'])
def lista_de_banidos():
    from datetime import datetime
    from flask import jsonify
    from models.database import Usuarios, Banidos
    nickname = request.args.get("pesquisa", None)
    usuario = Usuarios.query.filter_by(nickname=nickname).first()
    if usuario == None:
        dados = {'indentificao': 'Usuário não encontrado'}
        return jsonify(dados)
    # Aqui é se ele não foi banido
    banido = Banidos.query.filter_by(idUsuario=usuario.idUsuarios).first()
    if banido == None:
        dados = {'indentificao': 'Usuário não está banido'}
        return jsonify(dados)
    # Aqui é se tudo ocorrer bem
    data = datetime.strftime(banido.data_punicao, "%d/%m/%Y")
    dados = {'indentificao': 'tudo ok', 'data': data, 'status': banido.status, 'motivo': banido.motivo, 'prova': banido.prova, 'nome': usuario.nickname, 'email': usuario.email}
    return dados

# Parte de atividades nas API

@api.route("/api/veraatividades", methods=['GET', 'POST'])
def atividade_todas_visualizar():
    from flask import jsonify
    from models.database import Atividades
    enem = Atividades.query.filter(Atividades.secao.like('%enem%')).count()
    informatica = Atividades.query.filter(Atividades.secao.like('%informatica%')).count()
    dados = {'informatica': informatica, 'enem': enem}
    return jsonify(dados)

@api.route("/api/envio-atividades-submit", methods=['POST','GET'])
def envio_atividades():
    from config.atividades import Controle
    dados = request.form
    print("O dados são: ", dados)
    # dados comuns
    unidade = request.form['unidade']
    pergunta = request.form['pergunta']
    questao = []
    questao.extend([request.form['questao1'], request.form['questao2'], request.form['questao3'], request.form['questao4']])
    print("As questões são: ", questao)
    resposta_correta = int(request.form['resposta_correta']) - 1 # Para pegar o id
    # dados para avaliar
    categoria = request.form['categoria']
    if categoria == 'enem': 
        disciplina = str(request.form['disciplina']).replace('-', '_')
    else:
        disciplina = 'logica'

    print("Cheguei aqui é é ", categoria)
    Controle.adicionar_atividade(secao=categoria, disciplina=disciplina, unidade=unidade, pergunta=pergunta, respostas=resposta_correta, alternativas=questao)
    # Essa função não retorna nada, pós, ela praticamente, só envia as atividades e pronto! No caso, ela só envia os dados para o banco de dados.

@api.route("/api/atividades-logicas-submit", methods=['GET', 'POST'])
def todas_atividades():
    from models.database import Atividades
    todas_atividades = []
    # Aqui é para descobrir qual secao o usuário quer e o que ele está procurando
    nome = str(request.args.get("nome", None)).lower()
    unidade = int(request.args.get("unidade", None))
    print("O nome é : ", nome)
    print("A unidade é: ", unidade)
    atividades_solicitadas = Atividades.query.filter(Atividades.secao.ilike(f"%{nome}%") & Atividades.unidade == unidade).all()
    # aqui ele vai mostrar várias atividades, então, tenho que importar todas em uma lista
    for atividade in atividades_solicitadas:
        alternativa = [atividade.alternativa_1, atividade.alternativa_2, atividade.alternativa_3, atividade.alternativa_4]
        todas_atividades.append({'unidade': atividade.unidade, 'pergunta': atividade.pergunta, 'resposta': atividade.resposta, 'alternativas': alternativa})
    print("Preciso todas as respostas: ", todas_atividades)
    return todas_atividades


@api.route("/api/atividades-progresso", methods=['GET', 'POST'])
def atividade_progresso():
    # ou aqui eu pego um método
    import json
    from flask import jsonify
    from models.database import Usuarios
    curso = request.args.get("tipo_curso", None)
    if curso == None:
        print("Erro, deu none!")
        abort(402) # Houve um erro ao processar essa operação
    # Aqui eu preciso descobrir o progresso
    # vamos entrar no loop aqui
    email = session.get("email", None)
    usuario = Usuarios.query.filter_by(email=email).first()
    atividades = json.loads(usuario.atividades)
    disiciplinas = []
    for valor in atividades:
        if (valor['nome'] == curso):
            unidade_1_concluida = valor['unidade_1'].count(True) # 3 de 5
            porcentagem = format(((unidade_1_concluida / 5) * 100), ".2f") + "%"

            dicionario = {"disiplina": valor['disciplina'], "porcentagem": porcentagem} 
            disiciplinas.append(dicionario)

    return jsonify(disiciplinas)


