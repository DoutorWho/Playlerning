class Controle:
    """
    Uma classe para controle

    Métodos
    -------
    adicionar_atividade():
        Método para adicionar atividades no Banco de Dados, esse método adiciona atividades.
    diretorio_correto():
        Esse método serve para verificar se um diretório está correto para enviar curso.
    """
    @staticmethod
    def adicionar_atividade(secao, disciplina, unidade, pergunta, respostas, alternativas=[]): # As alternativas tem que ser 1, 2, 3, 4, no caso, as opções
        """
        Enviar atividdades para o Banco de Dados.

        Parâmetros
        ----------
        secao : string
            Aqui você diz a seção. Pode ser Enem ou Informática.
        disciplina : string
            A disciplina depende, se você escolher Enem, pode ser naturais, humanas, etc. Se escolher informática, pode ser lógica.
        unidade : int
            A unidade pode ser 1, 2, 3, 4.
        pergunta : string
            A pergunta deve ser feita como string, com uma interogação.
        respostas : int
            A resposta deve ser o id da pergunta nas alternativas. Por exemplo, se no id (começando por 0) a alternativa é 2, a resposta deve ser 2.
        alternativas : list
            A alternativas é uma lista, que deve contér 4 alternativas.No caso as respostas, e as respostas devem estar contidas nas alternativas.
        
        Retorno
        -------
            Nenhum | Função sem retorno            
        
        Exemplo
        -------
        >>> adicionar_atividade('Enem', 'humanas', 1, 'O que é java?', 4, alternativas=['É um dogma', 'não é nada', 'é um programa', 'é uma linguaguem de programação'])
        
        """
        from models.database import db, Atividades
        # verificar se as disciplinas estão corretas

        secao = f"{secao}/{disciplina}" # Tem que ser nome/disciplina, no caso Enem/humanas
        atividade = Atividades(secao=secao, unidade=unidade, pergunta=pergunta, resposta=respostas, alternativa_1=alternativas[0], alternativa_2=alternativas[1], alternativa_3=alternativas[2], alternativa_4=alternativas[3])
        db.session.add(atividade)
        db.session.commit()
        print("Atividade adicionada com sucesso")

    @staticmethod
    def diretorio_correto(nome: str, disciplina: str, email: str):
        """
        Verificar se o diretorio está correto.

        Parâmetros
        ----------
        nome : string
            Aqui é se o nome pode ser Enem ou Informática.
        disciplina : string
            A disciplina depende, se você escolher Enem, pode ser naturais, humanas, etc. Se escolher informática, pode ser lógica.
        email : int
            Aqui é o email, do usuário. Serve para verificar as atividades que ele fez ou não e enviar a ele.
        
        Retorno
        -------
        list
            Uma lista contendo os seguintes itens:
            - status: bool
                Pode ser True ou False, e é o status, se foi bem ou maal.
            - curso : string
                Podendo ser Curso para o Enem ou Curso de Informática
            - disciplina : string
                A disciplina pode ser Humanas, Lógica de Programação, etc.
            - atividade_status : list
                Uma matriz com todas as atividades, se tiver True ele fez, se tiver False ele não fez. Pode ter outras listas dentro dessa matriz, 
                sendo a 1 equivalante a primeira unidade e assim sucessivamente. 
            - atividades : list
                Uma matriz e dentro dela uma lista, e dentro da lista um dicionário com a pergunta, resposta e alternativas. Lembrando que a primeira lista tem as atividades da primeira unidade, e assim sucessivamente, e dentro dessas listas como disse tem dicionários!
        
        
        Exemplo
        -------
        >>> diretorio_correto('enem', 'informatica', 'leandro@gmail.com')
        """
        import json
        from models.database import db, Usuarios, Atividades
        lista = [[], [], []] # nome do curso, disicplina e no final é um dicionário com as atividades, unidades, etc
        match nome:
            case 'enem':
                if disciplina in ['linguagens', 'naturais', 'humanas', 'exatas']:
                    if disciplina != 'linguagens':
                        lista[0] = f"Curso para o Enem" # type: ignore
                        lista[1] = f"Ciências {disciplina.title()}" # type: ignore
                    else:
                        lista[0] = f"Curso para o Enem" # type: ignore
                        lista[1] = f"Linguagens" # type: ignore
                else:
                    return [False]
            case 'informatica':
                if disciplina in ['logica', 'programacao', 'bancodedados']:
                    nomes_disciplinas = {'logica': 'Lógica de Programação', 'programacao': "Linguaguem de Programação em C", 'bancodedados': 'Banco de Dados'}
                    lista[0] = f"Curso de Informática" # type: ignore
                    lista[1] = nomes_disciplinas[disciplina] # type: ignore
                else:
                    return [False] # significa que algum está incorreto               
            case _: # Ou seja nenhum dos dois
                return [False]
        # se tudo ocorrer bem
        # é  bom lembrar que aqui mesmo eu faço a verificação das atividades
        user = Usuarios.query.filter_by(email=email).first()
        
        lista[2] = json.loads(user.atividades)
        # Aqui a partir da disciplina e do tipo, eu faço uma verificação, para mostrar somente os daquele exércicios
        for valores in lista[2]:
            print(valores) 
            if (valores['nome'] == nome) and (valores['disciplina'] == disciplina): # A verificação se ele fez ou não, está no json
                resultado = [valores['unidade_1']] # aqui é por unidade
                break
        
        secao = f'{nome}/{disciplina}' # Isso é para eu descobrir as perguntas, que está no banco de dados.
        # as atividades podem ser repetidas
        atividades_totais = [[]] # Lista de unidades, para descobrir o arquivo de texto, é pelo json. Como só tem uma unidade, só vai ter 1 listad de atividades
        
        # Aqui é das cinco unidades, que agora é 1, descobrir qual é a atividade
        for unidade in range(1, 5):
            atividades = Atividades.query.filter_by(secao=secao, unidade=unidade)
            for contagem, mostrar in enumerate(atividades, start=1):
                # Como são 4 unidades, ele vai passando e tira 10 de cada.
                atividades_totais[unidade-1].append({ 
                    'pergunta': mostrar.pergunta,
                    'resposta': mostrar.resposta,
                    'alternativas': [mostrar.alternativa_1, mostrar.alternativa_2, mostrar.alternativa_3, mostrar.alternativa_4]
                })
                if contagem == 10: # Para não lotar de perguntas
                    break
        
        print(resultado)
        return [True, lista[0], lista[1], resultado, atividades_totais]
        # falta a parte para redirecionar o usuário para atividade somente.


