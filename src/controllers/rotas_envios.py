from flask import Blueprint, abort, request, render_template, redirect, url_for, session, make_response

rotas_submit = Blueprint("rotas_submit", __name__, template_folder='../../src')
# Parte do submit, ou seja, envio de arquivos



@rotas_submit.route("/cadastro-submit", methods=['POST', 'GET']) # falta eu configurar aqui, principalmente a parte do professor
def cadastrar():
    from secrets import token_hex
    from os import path, getcwd, listdir, mkdir
    import json
    from models.database import db, Usuarios
    from config.seguranca import Basico

    # esses são comuns de dois
    nickname = request.form['nickname']
    email = request.form['email']
    senha = request.form['senha']

    # parte de indentificação
    tipo_usuario = request.form['tipo_usuario']

    retorno = Basico.cadastro(dados=[nickname, email, senha])

    # verificar se tá tudo bem no que ele mandou
    if retorno[0]: # Isso significa que tá tudo bem
        if tipo_usuario == 'aluno':
            session['email'] = email # Porque o email é comum dos dois
            session['cargo'] = 'aluno'
            session['nickname'] = nickname
            session['modo'] = 'claro'
            curso = request.form['curso']
            aluno = Usuarios(nickname, 'aluno', email, senha, curso) # completar aqui
            db.session.add(aluno)
            db.session.commit()
        else:
           # Aqui eu preciso verificar se ele não está floodando solicitação, pois se não vai ficar aparecendo vários json lá com o mesmo email.
           flood = Basico
           curriculo = request.files['curriculo']
           # tá dando erro quando é mt arquivo, usar um sistema para melhorar
           curriculo_salvar = Basico.nome_confiavel(nome_arquivo=curriculo.filename) # aqui é para garantir o save
           caminho_arquivo = path.join(getcwd() + '/temp/curriculos')
           quantidade_pastas = len(listdir(caminho_arquivo)) + 1

           with open("src/utils/base_professor.json", 'r+', encoding='utf-8') as base: #utils
               dados = json.load(base)
               dados['nickname'] = nickname
               dados['email'] = email
               dados['senha'] = senha
               dados['curriculo'] = curriculo_salvar
               while True:  # Isso aqui é que para se caso tiver um professor_2 e a quantidade pasta dê 2, ele não dê erro!
                try:
                    mkdir(caminho_arquivo + f"/professor_{quantidade_pastas}", mode=0o755)
                    break
                except:
                    quantidade_pastas += 1 # Isso aqui faz a mágica da soma, no caso!
                    continue

               with open(f"temp/curriculos/professor_{quantidade_pastas}/dados.json", 'w', encoding='utf-8') as arquivo:
                json.dump(dados, arquivo, indent=4, ensure_ascii=True)
                
           salvar = path.join(caminho_arquivo + f"/professor_{quantidade_pastas}", curriculo_salvar)
           curriculo.save(salvar)


           # Essa parte aqui é a confirmação, para que o usuário saiba que tudo ocorreu bem!
           token = token_hex(30)
           resposta = make_response(redirect(url_for("verificao.sucesso", token=token)))
           resposta.set_cookie("token", token, max_age=60)
           dados = {'titulo': 'Cadastro realizado com sucesso', 'descrição': 'Aguarde agora a aprovoção dos nossos administradores, você receberá uma notificação por email'}
           resposta.set_cookie("informacao", json.dumps(dados), max_age=60)
           return resposta
        return redirect(url_for("minhas_rotas.index")) # autoriza o acesso
    return render_template("páginas/cadastro.html", erro=retorno[1]) # Aqui é porque deu erro


@rotas_submit.route("/login-submit", methods=['POST', 'GET'])
def logar():
    from config.seguranca import Basico
    # Ou seja, se for post
    email = request.form['email']
    senha = request.form['senha']
    retorno = Basico.login(email, senha)
    if retorno[0]: # Ou seja, tudo está ocorrendo bem!
        session['email'] = email
        session['cargo'] = retorno[1]
        session['nickname'] = retorno[2]
        session['modo'] = retorno[3]
        print("O retorno é: ", retorno[4])
        session['curso'] = retorno[4]
        return redirect(url_for("minhas_rotas.index"))
    # se não é porque houve algum erro
    return render_template("páginas/login.html", erro=retorno[1]) # Aqui já executa toda a verificação e retorna o erro.

@rotas_submit.route("/configuracoes", defaults={'tipo': 'padrão'}, methods=['POST', 'GET'])
@rotas_submit.route("/configuracoes/<tipo>", methods=['POST', 'GET'])
def configuracoes(tipo):
    from config.usuarios import Usuario
    email = session.get("email", None)
    if email == None:
        abort(404)
    if request.method == 'POST': # aqui o tipo é padrão
        if tipo == 'padrão': # se no caso, isso for padrão. Ou seja, na parte de status
            nickname = request.form.get("nickname", None)
            curso = request.form.get("curso", None)
            tema = request.form.get("tema", None)
            imagem_usuario = request.files.get("imagem_usuario", None)
            if imagem_usuario.filename != '': # Aqui é para garantir que não vai da erro, caso não há. No caso ele envia com filee stronag e vázio 
                nome_imagem = imagem_usuario.filename
            else:
                nome_imagem = None

            retorno = Usuario.configuracoes('inicial', email, nickname, tema, nome_imagem) 
            if retorno[0]: # Se for true quer dizer que tem imagem
                imagem_usuario.save(retorno[1])
            if curso != None:
                session['curso'] = curso
            return redirect(url_for("minhas_rotas.status", nome="perfil"))
        # aqui é caso o tipo seja mudar ou excluor conta.
        if tipo == 'deleteconta':
            session.clear() 
            Usuario.configuracoes(tipo="excluir", email=email)
        if tipo == 'mudarsenha':
            senha = request.form['novasenha']
            confirmacao = request.form['confirmacao']
            session['senhachave'] = True # Pra ser um guia
            if senha != confirmacao:
                return redirect(url_for("minhas_rotas.rotas_submit.configuracoes", tipo="mudarsenha")) # Isso signiica que as senhas não estão corretas. E aqui vai pro get
            # se as senhas estão corretas então mudamos
            Usuario.configuracoes(tipo='mudarsenha', email=email, senha=senha)
        return redirect(url_for("minhas_rotas.index"))
    
    # aqui é a parte final de erro da senha
    if tipo == 'mudarsenha':
        senhachave = session.get("senhachave", None)
        if senhachave == None:
            abort(404)
        session.pop("senhachave", None)
        return render_template("páginas/configuracoes.html", status='mudar-senha', mensagem=True)

    # aqui é se não for post é porque é get e se for get, temos que saber os tipos
    if tipo == 'mudar-senha':
        return render_template("páginas/configuracoes.html", status="mudar-senha", mensagem=None)

    if tipo == 'excluir-conta':
        return render_template("páginas/configuracoes.html", status='excluir-conta')

    if tipo == 'sair-conta':
        session.clear()
        return redirect(url_for("minhas_rotas.index"))
    # se não for nenhum desses, então
    abort(404)


# Aqui é uma parte abaixo


@rotas_submit.route("/exercicio/<int:unidade>/<int:atividade_numero>", methods=['POST', 'GET'])
def exercicio(unidade, atividade_numero):
    email = session.get("email", None)
    # aqui eu gero o exercicio de acordo com a atividade
    curso = request.args.get("curso", None)
    disciplina = request.args.get("disciplina", None)

    #atividade = Atividades.diretorio_correto(nome=curso, disciplina=disciplina, email=email) seria atividade[4][0]
    return render_template("páginas/exercicios.html", curso=curso, disciplina=disciplina, atividade_numero=atividade_numero, unidade=unidade)


@rotas_submit.route("/envioatividades-submit", methods=['POST', 'GET'])
def envio_de_atividades():
    from datetime import datetime
    from models.database import db, Usuarios
    from config.usuarios import Usuario
    # SEM O GET PARA TESTE
    # Aqui é se foi o envio mesmo
    # preciso decretar aqui que o usuário fez essa atividade
    respostas = request.form['respostas'] # tá vindo como string
    curso = request.form['curso']
    disciplina = request.form['disciplina']
    atividade_numero = request.form['atividade_numero']
    unidade = request.form['unidade']
    email = session.get("email", None)
    Usuario.envio_atividade_configuracao(email=email, acerto=float(respostas), curso=curso, disciplina=disciplina, unidade=unidade, atividade=atividade_numero)
    # para aumentar as ofensivas
    usuario = Usuarios.query.filter_by(email=email).first()
    data_atual = datetime.now()
    ultimo_dia = datetime.combine(usuario.ultimo_dia_jogado, datetime.min.time()) # Conventer date para datetime
    if data_atual.date() != ultimo_dia.date():
        usuario.ofensiva += 1
        db.session.commit()

    return redirect(url_for("minhas_rotas.status", nome='perfil'))


@rotas_submit.route("/forum-submit/<tipo_formulario>", methods=['POST', 'GET'])
def forumsubmit(tipo_formulario):
    from config.usuarios import Comentario

    # senão, significa que é do tipo post
    if tipo_formulario == 'adicionartopico': # adicioanar_topico
        topico_nome = request.form['nome']
        categoria = request.form['categoria']
        descricao = request.form['descricao']
        email = session.get("email", None)
        id = Comentario.adicionar_topico(email=email, nome=topico_nome, descricao=descricao, categoria=categoria) # nem precisa, porque ele não retorna nada.
        return redirect(f"/forum/comentarios?topico={id}")
    
    if tipo_formulario == 'encerartopico':  # vou fazer isso
        topico_id = request.form['topico_id']
        Comentario.encerar_topico(topico_id)
        return redirect(f"/forum/comentarios?topico={topico_id}")
    
    if tipo_formulario == 'excluirtopico':
        topico_id = request.form['topico_id']
        Comentario.excluir_topico(topico_id)
        return redirect(url_for("minhas_rotas.forum"))
    
    if tipo_formulario == 'apagarcomentario':
        idcomentario = request.form['comentario_id']
        topico_id = request.form['topico_id']
        Comentario.apagar_comentario(idcomentario)
        return redirect(f"/forum/comentarios?topico={topico_id}")
    
    if tipo_formulario == 'adicionarcomentario':
        email = session.get("email", None)
        topico_id = request.form['topico_id']
        comentario = request.form['comentario']
        Comentario.adicionar_comentario(email, topico_id, comentario)
        return redirect(f"/forum/comentarios?topico={topico_id}")
    
    abort(404)
    
    # senão, é porque, provalvamente o tipo é na parte de encerar topico, excluir comentario ou adicionar comentario

# Parte de Admin

@rotas_submit.route("/aprovarprofessor-submit", methods=['POST', 'GET'])
def aprovar_professor():
    from shutil import rmtree
    from os import getcwd, path
    import json
    from models.database import db, Usuarios
    botao = request.form['botao']
    email = request.form['email']
    print("O botão é ", botao)
    c = 0
    while True: # configurar isso para ele só pegar o que dados for igual ao email
        c += 1  
        try:
            with open(f"temp/curriculos/professor_{c}/dados.json", 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
                email_enviado_json = dados['email']
                if email == email_enviado_json:
                    # Significa que estamos na parte dele, vamos salvar a pasta para apagar
                    endereco = f"professor_{c}"
                    break
        except:
            continue
    print("A pasta é ", endereco)
    # se o botão for aprovar ou reprovar ele vai excluir a pasta de qualquer jeito
    caminho = path.join(getcwd() + f'/temp/curriculos/{endereco}')
    rmtree(caminho)
    # aqui é se ele for aprovado
    if botao == 'aprovar':
        professor = Usuarios(dados['nickname'], 'professor', email, dados['senha']) 
        db.session.add(professor)
        db.session.commit()
    # tanto faz, ele vai retornar para aqui!
    return redirect("/admin/aprovacao")
    
@rotas_submit.route("/banir-usuario-submit", methods=['GET', 'POST'])
def banir_usuario():
    from json import dumps
    from secrets import token_hex
    from config.seguranca import Admin
    forma = request.form['forma'] # Aqui pode ser email ou nickname
    motivo = request.form['motivo']
    status = request.form['status'] # Aqui é se o ban é permanente ou de dias, etc
    link = request.form['link'] # Aqui é a prova
    informacao = Admin.punir_usuario(forma=forma, status=status, motivo=motivo, link=link)

    # Já preparar o retorno
    token = token_hex(20)
    resposta = make_response(redirect(url_for("verificao.sucesso", token=token)))
    resposta.set_cookie("token", token, max_age=60)
    dados = {'titulo': informacao[0], 'descrição': informacao[1]}
    print("Os dados são: ", dados)
    resposta.set_cookie("informacao ", dumps(dados), max_age=60)
    # Independete se ocorrer bem ou ruim, a mensagem vai aparecer
    return resposta

