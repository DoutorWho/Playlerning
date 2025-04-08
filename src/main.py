from os import getcwd
from flask import Flask
from models.database import db
from controllers.rotas import minhas_rotas
from config.verificacao import verificao
app = Flask(__name__, static_folder='../', static_url_path='/static')
app.config['SECRET_KEY'] = "43f66fb95103a2979e5f003bc1540282c1c69aba7cde38d48c3e291cc616ed0153a0eb05d2d2"
app.register_blueprint(minhas_rotas)
app.register_blueprint(verificao)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{getcwd()}/src/models/playlerning.sqlite3' #SQLALCHEMY_DATABASE_URI
db.init_app(app)


if __name__ == '__main__':
    with app.test_request_context():
        db.create_all()
    app.run(debug=True, host='localhost', port=5000)
 