class Usuario:
    """
    # Introdução
    -------
    Uma classe para extrair e mostrar informações das configurações do usuário

 
    Métodos
    -------
    * configuracoes(cls, tipo, email=None, nickname=None, tema=None, nome_imagem=None, senha=None):
        Isso aqui são as configurações na parte de status, que pode excluir conta, mudar senha, alterar modo e alterar nickname.

    **Chamada em:** Na rota 

    * envio_atividade_configuracao(cls, email, acerto: float, curso, disciplina, unidade, atividade):
        Ela retorna as configurações do usuário como último dia jogado, dias jogados, quantidade de ofensiva e xp.

    **Chamada em:** Na rota /envioatividades-submit

    """
    from models.database import db, Usuarios, Topico, Comentarios

    @classmethod
    def configuracoes(cls, tipo, email=None, nickname=None, tema=None, nome_imagem=None, senha=None):
        """
        Definir as configurações do usuário
        
        """
        from os import getcwd, path, remove
        from sqlalchemy import text
        from config.seguranca import Basico
        usuario = cls.Usuarios.query.filter_by(email=email).first()
        if tipo == 'inicial':
            if (nickname != None) and (nickname != ''):
                # alterar o nickname
                nickname_antigo = usuario.nickname  # type: ignore
                usuario.nickname = nickname # type: ignore
                # alterar os tópicos e comentário para o novo nickname dele
                cls.db.session.execute(text(""" 
                    Update Topico 
                        Set autor = :novo_autor 
                        where autor = :nickname_antigo"""), {'novo_autor': nickname, 'nickname_antigo': nickname_antigo })
                
                cls.db.session.execute(text(""" 
                    Update Comentarios 
                        Set autor = :novo_autor 
                        where autor = :nickname_antigo"""), {'novo_autor': nickname, 'nickname_antigo': nickname_antigo })
                cls.db.session.commit()
            if tema != None:
                usuario.modo = tema # type: ignore

            if nome_imagem != None:
                # já configuro isso
                nome = Basico.nome_confiavel(nome_imagem) # aqui ele me retorna um nome confiável
                # aqui eu tenho que pegar o id pra salvar
                foto_de_perfil = usuario.foto_perfil # type: ignore
                if foto_de_perfil != 'padrao_usuario.png': # Aqui é, se ele tem uma foto com esse nome, vou excluir para adicionar a próxima
                    caminho = path.join(getcwd() + '/uploads/user-pictures/' + foto_de_perfil)
                    remove(caminho)
                    
                nome = f"{usuario.idUsuarios}_{nome}" # type: ignore
                usuario.foto_perfil = nome # type: ignore
                nome = path.join(getcwd() + '/uploads/user-pictures/' + nome)
                cls.db.session.commit()
                return [True, nome]
            cls.db.session.commit() 
            
        if tipo == 'mudarsenha':
            usuario.senha = senha # type: ignore
            cls.db.session.commit()

        if tipo == 'excluir':
            # Eu também tenho que excluir os comentários e os tópicos criados por ele.
            nickname = usuario.nickname # type: ignore
            comentarios = cls.Comentarios.query.filter_by(autor=nickname).first()
            topicos = cls.Topico.query.filter_by(autor=nickname).first()
            foto_usuario = usuario.foto_perfil # type: ignore
            if foto_usuario != "padrao_usuario.png": # Significa que ele não mudou de foto, se caso ele tenha mudado vamos excluir
                caminho = path.join(getcwd() + '/uploads/user-pictures/' + foto_usuario)
                remove(caminho)

            cls.db.session.delete(usuario)
            if (comentarios != None): # Pra não da erro
                cls.db.session.delete(comentarios)
            if topicos != None:
                cls.db.session.delete(topicos)
            cls.db.session.commit()
        return [False]


    @classmethod
    def envio_atividade_configuracao(cls, email, acerto: float, curso,  disciplina, unidade, atividade):
        """Definir as configurações do usuário"""
        from datetime import date
        import json
        from math import ceil
        usuario = cls.Usuarios.query.filter_by(email=email).first()
        ultimo_dia_jogado = usuario.ultimo_dia_jogado # type: ignore
        data_atual = date.today()

        if (ultimo_dia_jogado == None) or (data_atual > ultimo_dia_jogado): # Isso significa que hoje ele não jogou. O última dia == None tem que tá na frente porque se não da erro, na outra setença aqui, ele simplismente executa a primeira.
            print("Cheguei nisso, significa que tá safe")
            usuario.ultimo_dia_jogado = data_atual # type: ignore
            usuario.quantidade_dias_jogados = usuario.quantidade_dias_jogados + 1 # type: ignore # Pra dizer que ele tem mais um dia jogado
            usuario.ofensiva = usuario.ofensiva = 1 # type: ignore
            # vamos fazer o cálculo para o xp
            xp = ceil((6 * acerto) / 50)
            usuario.xp = usuario.xp + xp
            # depois eu dou um db para salvar
        # agora aqui eu tenho que colocar o nome, a atividade e a unidade
        atividades_feitas = json.loads(usuario.atividades)
        unidade_feita = f'unidade_{unidade}' # Aqui é a unidade que ele fez a atividade
        for valor in atividades_feitas:
            if (valor['nome'] == curso) and (valor['disciplina'] == disciplina):
                valor[unidade_feita][int(atividade)-1] = True # Significa que ele já fez, -1 porque atividade tá 1, no caso, tá na parte 0 no indice
        usuario.atividades = json.dumps(atividades_feitas) # Aqui pra salvar tudo no database
        cls.db.session.commit()
        print(atividades_feitas[4]['unidade_1']) 




class Status:
    """
    # Introdução
    -------
    Uma classe para extrair e mostrar informações das configurações do usuário

    Métodos
    -------
    * perfil(cls, emai):
        Isso aqui retorna um dicionário contendo o nickname, rank, cargo, xp, ofensiva e foto do usuário.

    **Chamada em:** Na rota 

    * missoes(cls, emai):
        Isso aqui ele pega as missões existentes, verifica se o usuário completou cada missão, e retorna as uma lista, com as True para dizer que tá tudo bem e em seguida com uma lista que nela tem as conquistas realizadas e as não realizadas. 

    **Chamada em:** Na rota 

    * rank(cls, emai):
        Isso aqui retorna a posição do usuário, a foto dele, o top 10 de todos os usuários com maior número de xp, as ofensivas, as quantidades de dias que ele usou o site e o último dia que usou.

    **Chamada em:** Na rota

    """
    import json
    from models.database import db, Usuarios
    with open("src/utils/ranks.json", 'r', encoding='utf-8') as rank: #type: ignore
        rank_controle = json.load(rank)

        

    @classmethod
    def perfil(cls, email):
        """Mostrar o perfil do usuário"""
        from datetime import datetime, timedelta
        usuario = cls.Usuarios.query.filter_by(email=email).first()
        
        xp = usuario.xp
        for nome_rank, controle in cls.rank_controle.items():
            if xp >= controle['xp']:
                rank = nome_rank
                break
                
        
        # Último dia jogado
        dia_para_reset = datetime.now()
        try:
            ultimo_dia_jogado = datetime.strftime(usuario.ultimo_dia_jogado, "%d/%m/%Y")
        except:
            ultimo_dia_jogado = "Usuário ainda não estudou"


        # corrigir aqui! 
        # verificação de ofensiva
        ofensiva = usuario.ofensiva  
        if (ofensiva != 0):
            if ultimo_dia_jogado != 'Usuário ainda não estudou':
                ultimo_dia = usuario.ultimo_dia_jogado 
                ultimo_dia = datetime.combine(ultimo_dia, datetime.min.time()) # Conventer date para datetime
                if (ultimo_dia.date() < dia_para_reset.date()): # No se caso o último dia foi 22/11/2024 e o dia do reset for 22/11/2024, ele vai confirmar é o usuário ofensiva vai virar 0! Esse date é para comprar somente data, se fosse hora/minuto/segundo é time!
                    usuario.ofensiva = 0
                    cls.db.session.commit()
            

        dicionario = {'nickname': usuario.nickname, 'rank': rank, 'cargo': str(usuario.cargo.value).title(), 'xp': usuario.xp, 'ofensiva': usuario.ofensiva, 'quantidade_dias_jogados': usuario.quantidade_dias_jogados, 'ultimo_dia_jogado': ultimo_dia_jogado, 'foto': str(usuario.foto_perfil)}
        return dicionario
        # retorna nome, foto_perfil, rank, xp, ofensiva, dias jogados, último login.


    @classmethod
    def missoes(cls, email):
        
        # tenho que fazer a verificação pra vê se o usuário fez a missão ou não
        with open("src/utils/conquistas.json", 'r', encoding='utf-8') as arquivo:
            conquistas = cls.json.load(arquivo)
            usuario = cls.Usuarios.query.filter_by(email=email).first()
            quantidade_dias = usuario.quantidade_dias_jogados

            # vamos fazer os requesitos aqui
            conquistas['1']['faltando'] = format(((quantidade_dias)/100) * 100, ".2f")
            conquistas['2']['faltando'] = format(((quantidade_dias)/300) * 100, ".2f") # Não esquecer de usar o .format lá no front-end ou aqui mesmo
            if usuario.conquistas == None: # aqui é duas ou uma, ele pode ser none significando que ele n tem nenhuma, ou ele pode ter algum número
                # aqui continua normal
                #print(conquistas) 
                #print(f"As conquistas são ", conquistas)
                return [None, conquistas] # Se o retorno for none, ele vai mandar um None lá e significa que não há conquistas

            
            salvar = [[], []] # Isso aqui é para salvar as conquistas que ele tem ou não
            conquista_usuario = usuario.conquistas # Se ele tiver alguma conquista, temos que descobrir qual é, aí é usar o in, pra vê se existe aquele valor na string
            for chave in conquistas.keys(): # aqui ele vai puxar conquistas, se o usuário tiver nas conquistas 1, 2, 3 significa que essas conquistas estão completadas!
                if chave in conquista_usuario:
                    salvar[0].append(conquistas[chave])
                else:
                    salvar[1].append(conquistas[chave])



            return [True, salvar]

    @classmethod
    def rank(cls, email=None):
        from sqlalchemy import desc
        todos_usuarios = cls.Usuarios.query.filter(~cls.Usuarios.cargo.in_(['professor', 'administrador', 'ceo'])).order_by(desc(cls.Usuarios.xp), desc(cls.Usuarios.nickname)).limit(10).all() # O ~ é negação!
        # agora eu tenho que colocar isso em uma lista
        # depois eu faço um para aparecer eu, passando o meu email como parâmetro
        lista = [[], []]
        lista[1] = [{'usuario': user.nickname, 'xp': user.xp, 'foto_perfil': user.foto_perfil} for user in todos_usuarios]
        # minha parte
        usuario = cls.Usuarios.query.filter_by(email=email).first() 
        lista[0] = [{'usuario': usuario.nickname, 'xp': usuario.xp, 'foto_perfil': usuario.foto_perfil}] 
        # adicionar o rank
        for c in range(2):
            for chaves, rank in enumerate(lista[c]):
                for rank_nome, controle in cls.rank_controle.items():
                    if rank['xp'] >= controle['xp']:
                        lista[c][chaves]['rank'] = rank_nome
                        break

        # descobrir a posição do usuário
        cargo = usuario.cargo.value
        print(cargo)
        if cargo in ['professor', 'administrador', 'ceo']: # se ele for na staff, tirar isso!
            lista[0][0]['posicao'] = f'Não definida, você é {str(cargo).capitalize()}!'
            return lista

        todos_usuarios = cls.Usuarios.query.filter(~cls.Usuarios.cargo.in_(['professor', 'administrador', 'ceo'])).order_by(desc(cls.Usuarios.xp), desc(cls.Usuarios.nickname)).all()
        #todos_usuarios = cls.Usuarios.query.order_by(desc(cls.Usuarios.xp), desc(cls.Usuarios.nickname)).all()
        for pos, user in enumerate(todos_usuarios, start=1):
            if usuario.email == user.email:
                posicao = pos
                break
        lista[0][0]['posicao'] = posicao # Para retornar a posição
        return lista
        # faltar configurar para aparecer o último feito


class Comentario:
    from models.database import db, Usuarios, Topico, Comentarios

    @classmethod
    def todos_topico(cls):
        from datetime import date, datetime, timedelta
        from sqlalchemy import desc
        mes = {
            '01': 'janeiro',
            '02': 'fevereiro',
            '03': 'março',
            '04': 'abril',
            '05': 'maio',
            '06:': 'junho',
            '07': 'julho',
            '08': 'agosto',
            '09': 'setembro',
            '10': 'outubro',
            '11': 'novembro',
            '12': 'dezembro' 
        }
        # precisa do nome, quem fez, a seção se tá ativa ou não e a quantidade de comentários.
        data_atual_menos_3_messes = date.today() - timedelta(days=90)
        print("A data é: ", data_atual_menos_3_messes)
        #topicos = Topico.query.order_by(desc(Topico.comentarios)).filter(Topico.data >= data_atual_menos_3_messes).limit(10).all()
        topicos = cls.Topico.query.filter(cls.Topico.data >= data_atual_menos_3_messes).order_by(desc(cls.Topico.comentarios), desc(cls.Topico.data)).all() # Não precisa do all mas eu coloquei!
        #topicos = cls.Topico.query.all()
        # 23/09/2023 <= 23/07/2024
        listas = []
        for topico in topicos: # aqui eu preciso do id do topico, nome, quem fez, seção e quantidade de comentários
            data = datetime.strftime(topico.data, "%d/%m/%Y") # Aqui não da erro, porque eu estou passando o valor, e não a função
            data = data.split('/')
            data = f"{data[0]} de {mes[data[1]]}, {data[2]}"
            quantidade_comentario = cls.Comentarios.query.filter_by(idTopico=topico.idTopico).count()
            print("Os comentários são: ", topico.comentarios)
            comentario = f"{quantidade_comentario} comentario" if quantidade_comentario == '1' else f"{quantidade_comentario} comentarios"
            dicionario = {"idTopico": topico.idTopico, "nome": topico.nome, "descricao": topico.descricao, "autor": topico.autor, "data": data, "comentario": comentario, "status": topico.status.value}

            listas.append(dicionario)
        return listas 
    
    @classmethod
    def ver_topico(cls, idTopico):
        from datetime import datetime
        # foto do usuário, nome do usuário, cargo, título do tópico, descrição, categoria e data.

        # Também na parte de comentários desses tópicos. Deve ter, comentario, usuário, foto de perfil, cargo e data.

        # A parte de apagar comentário temos que visualizar no front.
        topico = cls.Topico.query.get(idTopico) # aqui pega por id
        try:
            # Aqui é a parte do tópico
            data = datetime.strftime(topico.data, "%d/%m/%Y")
            nickname = topico.autor
            usuario = cls.Usuarios.query.filter_by(nickname=nickname).first()
            foto_perfil = usuario.foto_perfil
            cargo = str(usuario.cargo.value).title()
            topico = {'idTopico': topico.idTopico, 'status': topico.status.value, 'descrição': topico.descricao, 'categoria': str(topico.categoria.value).title(), 'data': data, 'nickname': nickname, 'cargo': cargo, 'foto_perfil': foto_perfil}
            # aqui é a parte de comentários
            comentario = [] # Para ir adicionando os comentários
            comentarios = cls.Comentarios.query.filter_by(idTopico=idTopico).all()
            if comentarios != []:
                for comentar in comentarios:
                    nickname = comentar.autor
                    data = datetime.strftime(comentar.data, "%d/%m/%Y")
                    usuario = cls.Usuarios.query.filter_by(nickname=nickname).first()
                    foto_perfil = usuario.foto_perfil
                    cargo = str(usuario.cargo.value).title()
                    comentario.append({'idComentario': comentar.idComentario, 'nickname': nickname, 'cargo': cargo, 'foto_perfil': foto_perfil, 'descrição': comentar.comentario, 'data': data})
            else:
                comentario = 'None'
        except AttributeError: # poderia usar o hasattr também, mas ele não funcionaria bem nesse caso
            return [False] # Aqui da um abort 
        
        print("Este é o comentário", comentario)
        return [True, topico, comentario] # Significa que tudo ocorreu bem bem

    @classmethod
    def adicionar_topico(cls, email, nome, descricao, categoria):
        from datetime import date
        usuario = cls.Usuarios.query.filter_by(email=email).first()
        autor = usuario.nickname
        data_atual = date.today()
        add_topico = cls.Topico(nome, categoria, descricao, autor, data_atual, 0)
        cls.db.session.add(add_topico)
        cls.db.session.commit()
        print("Adicionado com sucesso")
        return add_topico.idTopico

    @classmethod
    def encerar_topico(cls, topico_id):
        topico = cls.Topico.query.filter_by(idTopico=topico_id).first()
        topico.status = 'Encerada'
        cls.db.session.commit()
        print("Encerrado tópico")

    @classmethod
    def excluir_topico(cls, topico_id):
        topico = cls.Topico.query.filter_by(idTopico=topico_id).first()
        cls.db.session.delete(topico)
        cls.db.session.commit()
        print("Excluído tópico!")

    @classmethod
    def adicionar_comentario(cls, email, idTopico, comentario):
        from datetime import date
        usuario = cls.Usuarios.query.filter_by(email=email).first()
        autor = usuario.nickname
        data = date.today()
        add_comentario = cls.Comentarios(idTopico, comentario, autor, data)
        # aqui é para adicionar que lá em tópicos, tem comentários para ele retornar.
        cls.db.session.add(add_comentario)
        cls.db.session.commit()


    @classmethod
    def apagar_comentario(cls, idComentario):

        """
        tipo pode ser apagar
        """
        comentario = cls.Comentarios.query.get(idComentario)
        cls.db.session.delete(comentario)
        cls.db.session.commit()
