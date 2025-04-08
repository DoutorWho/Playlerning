from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

# Definindo a numeração para o Cargo e as Disciplinas
class Cargo(enum.Enum):
    ceo = 'ceo'
    administrador = 'administrador'
    professor = 'professor'
    aluno = 'aluno'
class Disciplinas_professor(enum.Enum):
    linguaguens = 'linguagens'
    ciencias_exatas = 'ciências_exatas'
    ciencias_naturais =  'ciências_naturais'
    ciencias_humanas =  'ciências_humanas'
    informatica = 'informática'


class Disciplinas_tipos(enum.Enum):
    enem = 'enem'
    informatica = 'informatica'

class Modo(enum.Enum):
    escuro = 'escuro'
    claro = 'claro'

# Parte de comentários

class Categoria_Topico(enum.Enum):
    enem = 'enem'
    informatica = 'informatica'
    ajuda = 'ajuda'

class Status_comentario(enum.Enum):
    Ativa = 'Ativa'
    Encerada = 'Encerada'

# Criação do banco de dados

class Usuarios(db.Model):
    __tablename__ = 'Usuarios'
    
    idUsuarios = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.Text, unique=True, nullable=False)
    cargo = db.Column(db.Enum(Cargo), nullable=False)
    email = db.Column(db.String(80), unique=True,  nullable=False)
    senha = db.Column(db.String(20), nullable=False)
    curso = db.Column(db.Enum(Disciplinas_tipos), nullable=True)
    modo = db.Column(db.Enum(Modo), nullable=True)
    foto_perfil = db.Column(db.Text, nullable=True)
    conquistas = db.Column(db.String(50), nullable=True)
    ofensiva = db.Column(db.Integer, default=0, nullable=True)
    quantidade_dias_jogados = db.Column(db.Integer, default=0, nullable=True)
    ultimo_dia_jogado = db.Column(db.Date, nullable=True)
    atividades = db.Column(db.Text, nullable=True) # Concatena string. Que nem em conquistas, um monte de string que representa uma atividade
    xp = db.Column(db.Integer, default=0,  nullable=True) # pra descobrir o top é só ordenar por XP
    disciplina = db.Column(db.Enum(Disciplinas_professor), nullable=True)

    def __init__(self, nickname, cargo, email, senha, curso=None, modo='claro', foto_perfil=None, conquistas=None, ofensiva=0, quantidade_dias_jogados=0, ultimo_dia_jogado=None, atividades=None, xp=0, disciplina=None):
        import json
        self.nickname = nickname
        self.cargo = cargo
        self.email = email
        self.senha = senha
        self.curso = curso
        self.modo = modo
        self.foto_perfil = "padrao_usuario.png"
        self.conquistas = conquistas
        self.ofensiva = ofensiva
        self.quantidade_dias_jogados = quantidade_dias_jogados
        self.ultimo_dia_jogado = ultimo_dia_jogado
        with open("src/utils/atividades.json", 'r', encoding='utf-8') as atividade:
            dados = json.load(atividade)
            self.atividades = json.dumps(dados)
        self.xp = xp
        self.disciplina = disciplina

class Atividades(db.Model):
    __tablename__ = 'Atividades'

    idAtividade = db.Column(db.Integer, primary_key=True, autoincrement=True)
    secao = db.Column(db.String, nullable=False) # Isso quer dizer a Seção, que pode ser "Enem/humanas"
    unidade = db.Column(db.Integer, nullable=False) # Isso quer dizer a unidade, que pode ser 1, pois só te mela.
    pergunta = db.Column(db.Text, nullable=False) # A pergunta
    alternativa_1 = db.Column(db.Text, nullable=False)
    alternativa_2 = db.Column(db.Text, nullable=False)
    alternativa_3 = db.Column(db.Text, nullable=False)
    alternativa_4 = db.Column(db.Text, nullable=False)
    resposta = db.Column(db.Text, nullable=False) # A resposta deve ser uma das alternativas

    def __init__(self, secao, unidade, pergunta, alternativa_1, alternativa_2, alternativa_3, alternativa_4, resposta):
        self.secao = secao
        self.unidade = unidade
        self.pergunta = pergunta
        self.alternativa_1 = alternativa_1
        self.alternativa_2 = alternativa_2
        self.alternativa_3 = alternativa_3
        self.alternativa_4 = alternativa_4
        self.resposta = resposta 

# Parte dos comentários

class Topico(db.Model): 
    __tablename__ = 'Topico'

    idTopico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    categoria = db.Column(db.Enum(Categoria_Topico), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    autor = db.Column(db.String, nullable=True) # Tenho que configurar para que se caso ele troque de nick, o autor aqui tbm troque.
    data = db.Column(db.Date, nullable=True)
    comentarios = db.Column(db.Integer, nullable=True, default=0) # É a quantidade de comentários. Aqui eu posso excluir!
    status = db.Column(db.Enum(Status_comentario), nullable=True)

    def __init__(self, nome, categoria, descricao, autor, data, comentarios, status='Ativa'):
        self.nome = nome
        self.categoria = categoria
        self.descricao = descricao
        self.autor = autor
        self.data = data
        self.comentarios = comentarios
        self.status = status


class Comentarios(db.Model):
    __tablename__ = 'Comentarios'

    idComentario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idTopico = db.Column(db.Integer)
    comentario = db.Column(db.Text, nullable=True)
    autor = db.Column(db.String, nullable=True)
    data = data = db.Column(db.Date, nullable=True) 

    def __init__(self, idTopico, comentario, autor, data):
        self.idTopico = idTopico
        self.comentario = comentario
        self.autor = autor
        self.data = data

class Banidos(db.Model):
    idBanidos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuario = db.Column(db.Integer) # A partir do email, eu pego o id do usuário para banir-ló. 
    data_punicao = db.Column(db.Date, nullable=True)
    status =  db.Column(db.String, nullable=True) # Aqui seria a data que acaba a punição ou se a punição é eterna. 
    motivo = db.Column(db.String, nullable=True)
    prova = db.Column(db.String, nullable=True)

    def __init__(self, idUsuario, status, motivo, prova):
        from datetime import date
        self.idUsuario = idUsuario
        self.data_punicao = date.today()
        self.status = status
        self.motivo = motivo
        self.prova = prova


# Para descobrir a quantidade ce comentários, da um len no comentário relacionado aquele tópico e pronto.

# Sobre excluir comentário ele vai enviar o id do comentário, aí é só excluir, e sobre o tópico, vai enviar o id do tópico, aí é só excluir o tópico e todos os comentarios relacionados aquele tópico, para saber disso, temos o id do topico no comentário.