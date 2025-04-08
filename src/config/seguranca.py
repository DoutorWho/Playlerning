class Basico:
    """
    Uma classe para o básico, que são as funções básicas para o site.

    Métodos
    -------
    nome_confiavel():
        Método para verificar se um nome de um arquivo está correto, para não gerar erro!
    cadastro():
        Esse método serve para cadastrar um usuário no servidor.
    login():
        Esse método serve para entrar no servidor. 
    """
    @staticmethod
    def nome_confiavel(nome_arquivo):
        """
        Verificar se o nome enviado está tudo certo ou não.

        Parâmetros
        ----------
        nome_arquivo : string
            Aqui é enviado o nome do arquivo.
        Retorno
        -------
            O nome do arquivo do tipo string, só que seguro! Sem problemas para enviar-los ao servidor.      
        
        Exemplo
        -------
        >>> nome_confiavel('imagem_da_boa')
        """
        import unicodedata
        from werkzeug.utils import secure_filename
        
        curriculo = unicodedata.normalize('NFKD', nome_arquivo) # Normalizar caracteres, tipo "é" se torna 'e'
        curriculo = curriculo.encode('ascii', 'ignore').decode('ascii') # arquivo o arquivo é codificado em ascii e ignorando o que não são codificados em anscii
        return secure_filename(curriculo) # aqui verifica se o arquivo é seguro é manda 

    @staticmethod
    def cadastro(dados=[]):
        """
        Função para cadastrar um novo usuário.

        Parâmetros
        ----------
        dados : list
            - nickname
                Aqui é o nome do usuário, no caso o nickname.
            - email
                Aqui é o e-mail do usuário!  
            - senha
                Aqui é a senha do usuário!
        Retorno
        -------
            Aqui ele retorna uma lista, que pode contér True/False ou None/Mensagem de erro. Se for True é porque está correto, se for False é porque está errado e uma mensagem será apresentado no 2 item da lista.   
        
        Exemplo
        -------
        >>> cadastro(dados=['leandro', 'email', 'senha'])
        """
        import json
        from models.database import db, Usuarios
        nickname = str(dados[0]).strip().capitalize()
        email_completo = dados[1]
        email = str(email_completo).split('@')
        email = email[1]
        senha = str(dados[2]) 
        # verificação, e eu tenho que fazer essa verificação no back, pra vê se ele não tá usando um nickname de outro
        # manter legalidade; '/, ''

        usuario_email = Usuarios.query.filter_by(email=email_completo).first()
        nickname_usuario = Usuarios.query.filter_by(nickname=nickname).first()

        if (usuario_email != None) or (nickname_usuario != None): # Se ele for diferente de None, é porque já existe algum email ou nickname assim!
            return [False, f'Email ou nickname já existe']


        # verificar a legalidade dos nomes, nicknames, email e senhas
        with open("src/utils/cadastros_proibidos.json", "r", encoding='utf-8') as arquivo:
            dados_carregados = json.load(arquivo)
            nicknames = dados_carregados['nicknames_proibidos']
            email_permetido = dados_carregados['email_permetido']
            if any(palavra in nickname for palavra in nicknames):
                print("Nickname inválido")
                return [False, f'O nickname {nickname} é inválido ou indisponível!']
            if (email.lower() not in email_permetido):
                print("Email inválido", email)
                return [False, f'Esse email é inválido ou indisponível!']
            if len(senha) < 8:
                return [False, f"Sua senha é muito curta, ela tem que ter pelo menos 8 caracteres!"]
            return [True, None]
            #json.dump(dados, (arquivo, ensure_ascii=False, indent=4)
            # aqui é duas ou uma, se ele retornar um erro, eu tenho que colocar uma mensagem de erro na tela, se não, eu não coloco


    @staticmethod
    def login(email, senha):
        """
        Função para entrar no site.

        Parâmetros
        ----------
        email : str
            O e-mail do usuário.
        senha : str
            A senha do usuário.

        Retorno
        -------
        list
            Retorna uma lista com True/False.
            - Se for False, apresenta uma mensagem de erro.
            - Se for True, o retorno varia de acordo com o cargo do usuário:
                - Para 'ceo', 'administrador' ou 'aluno': [True, cargo, nickname, modo, curso]
                - Para 'professor': [True, cargo, nickname, modo, None]

        Exemplo
        -------
        >>> entrar_no_site('email@example.com', 'senha')
        """
        from models.database import db, Usuarios
        usuario = Usuarios.query.filter_by(email=email).first() # leandro@gmail.com
        if usuario == None:
            return [False, 'Este email não existe']
        
        if (usuario.senha != senha):
            return [False, 'A senha está incorreta!']
        # acesso 
        cargo = usuario.cargo.value
        print("O cargo é: ", cargo)
        if cargo in ['ceo', 'administrador', 'aluno']:
            return [True, cargo, usuario.nickname, usuario.modo.value, usuario.curso.value]
        return [True, cargo, usuario.nickname, usuario.modo.value, None]


class Admin:
    """
    Uma classe para o Administrador/Ceo.

    Métodos
    -------
    informacoes_gerais():
        Esse método mostra as informações gerais de todos os usuário.
    aprovacao_lista():
        Esse método mostra todos os professores pendentes, esperando para serem ou não aprovados.
    punir_usuario():
        Esse método serve para banir os usuários.
    """
    @staticmethod
    def informacoes_gerais(): # terminar essa docstring e as de baixo
        """
        Mostrar as informações essenciais do site.

        Parâmetros
        ----------
        Nenhum
        
        Retorno
        -------
            Aqui ele retorna uma lista, que pode contér True/False.
            Se for False, ele apresenterá uma mensagem de erro, se for True ele se dividirá em dois.
            Se o cargo dele for ceo, administrador ou aluno, o retorno é: True (o próprio), cargo, nickname, modo, curso. 
            Se caso o cargo dele for professor, que é o único que falta, ele retornará: True, cargo, nickname, modo e None (Para informar que não há curso).
        Exemplo
        -------
        >>> cadastro(dados=['leandro', 'email', 'senha'])
        """
        from models.database import Usuarios, Banidos, Topico, Comentarios
        # verificar total de usuarios, banidos, topicos e comentarios.
        total_usuarios = Usuarios.query.count()
        total_banidos = Banidos.query.count()
        total_topicos = Topico.query.count()
        total_comentarios = Comentarios.query.count()
        return {'total_usuarios': total_usuarios, 'total_banidos': total_banidos, 'total_topicos': total_topicos, 'total_comentarios': total_comentarios}
    @staticmethod
    def aprovacao_lista():
        """
        Função para entrar no site.

        Parâmetros
        ----------
        email : string
            Aqui é o nome do usuário, no caso o nickname.
        senha: string
            Aqui é o e-mail do usuário!  
        Retorno
        -------
            Aqui ele retorna uma lista, que pode contér True/False.
            Se for False, ele apresenterá uma mensagem de erro, se for True ele se dividirá em dois.
            Se o cargo dele for ceo, administrador ou aluno, o retorno é: True (o próprio), cargo, nickname, modo, curso. 
            Se caso o cargo dele for professor, que é o único que falta, ele retornará: True, cargo, nickname, modo e None (Para informar que não há curso).
        Exemplo
        -------
        >>> cadastro(dados=['leandro', 'email', 'senha'])
        """
        import json
        from os import path, getcwd, listdir
        caminho_arquivo = path.join(getcwd() + '/temp/curriculos')
        quantidade_pastas = len(listdir(caminho_arquivo))
        # abrir o arquivo para pegar os dados
        lista_dados = [] # Esse quantidade_pasta números que é a contagem das pastas, podendo ser 5, mas eu ter o professor_8, que ele não vai pegar
        for contagem in range(1, quantidade_pastas + 1):
            c = contagem
            while True:# Já resolvi se caso eu aprovar o professor 1, e ainda tiver 2... Ele usa o try e vai indo!
                try:
                    with open(f"temp/curriculos/professor_{c}/dados.json", 'r', encoding='utf-8') as dados:
                        arquivos = json.load(dados)
                        arquivos['curriculo'] = f"temp/curriculos/professor_{c}/" + arquivos['curriculo']
                        lista_dados.append(arquivos)
                        break
                except:
                    c += 1
                    continue
        # aqui ele já vai retornar todos os dados do professor, 
        return lista_dados

    @staticmethod
    def punir_usuario(forma, status, motivo, link):
        """
        Função para entrar no site.

        Parâmetros
        ----------
        email : string
            Aqui é o nome do usuário, no caso o nickname.
        senha: string
            Aqui é o e-mail do usuário!  
        Retorno
        -------
            Aqui ele retorna uma lista, que pode contér True/False.
            Se for False, ele apresenterá uma mensagem de erro, se for True ele se dividirá em dois.
            Se o cargo dele for ceo, administrador ou aluno, o retorno é: True (o próprio), cargo, nickname, modo, curso. 
            Se caso o cargo dele for professor, que é o único que falta, ele retornará: True, cargo, nickname, modo e None (Para informar que não há curso).
        Exemplo
        -------
        >>> cadastro(dados=['leandro', 'email', 'senha'])
        """
        from datetime import datetime, date, timedelta
        from models.database import db, Usuarios, Banidos
        # Eu preciso verificar se o email ou nickname existe
        if '@' in forma:
            usuario = Usuarios.query.filter_by(email=forma).first()
        else:
            usuario = Usuarios.query.filter_by(nickname=forma).first()
        
        if usuario == None:
            print("To aqui!")
            return ['Nick ou email inválido!', f'O nickname ou email {forma} não existe em nosso banco de dados!']
        # Aqui é se tudo ocorrer bem, para realizar o ban
        idUsuario = usuario.idUsuarios
        data = date.today()
        duracao = {'permanente': 'Permanente', '2_dias': datetime.strftime((data + timedelta(days=10)), "%d/%m/%Y"), '15_dias': datetime.strftime((data + timedelta(days=15)), "%d/%m/%Y"), '30_dias': datetime.strftime((data + timedelta(days=30)), "%d/%m/%Y"), '1_ano': datetime.strftime((data + timedelta(days=365)), "%d/%m/%Y")}
        print("A duração é: ", duracao[status])
        banido = Banidos(idUsuario=idUsuario, motivo=motivo, status=duracao[status], prova=link) # verificar se é ano bissexto ou não, pra fazer a soma se o ban for de 1 ano!
        db.session.add(banido)
        db.session.commit()
        return ['Usuário banido com sucesso!', f'O usuário que possuí o email ou a senha {forma} foi banido corretamente até/por {duracao[status]}!']
    
    