from flask import Flask, render_template, request, flash, url_for, redirect
import urllib.parse
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from animal import Animal
from avaliacao import Avaliacao
from sqlalchemy.orm import sessionmaker
from textblob import TextBlob

app = Flask(__name__)
app.secret_key = 'sdaghbdujighasuidhasidjioasghdui'

user = "root"
password = urllib.parse.quote_plus("senac")
host = "localhost"
database = "zooflask"

connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'

"""
A função create_engine cria uma interface 
que permite a comunicação entre o aplicativo web
e o banco de dados

"""
engine = create_engine(connection_string)

metadata = MetaData()
metadata.reflect(engine)


"""
-- Cria uma classe base que vai mapear 
-- Automaticamente as tabelas do banco de dados 
-- Que estão descritas no objeto metadata.

"""
Base = automap_base(metadata=metadata)

"""
--Esse método realiza o mapeamento das tabelas para classes Python, 
--Gera uma classe para cada tabela 
--Pode ser usada para interagir com os dados diretamente.
"""
Base.prepare()

# Ligando com a classe
Animal =  Base.classes.animal
Avaliacao = Base.classes.avaliacao

# Criar a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/avaliacao')
def avaliacao():
    return render_template('avaliacao.html')

@app.route('/novoanimal', methods=['POST'])
def inserir_animal():
    nome_popular = request.form['nome_popular']
    nome_cientifico = request.form['nome_cientifico']
    habitos_noturnos = request.form['habitos_noturnos']
    
    session = Session()
    
    
    animal = Animal(nome_popular=nome_popular, nome_cientifico=nome_cientifico, habitos_noturnos=habitos_noturnos)
    
    try:
        session.add(animal)
        session.commit()
        flash('Animal criado com sucesso!')
    except Exception as e:
        session.rollback()
        flash('Erro ao criar o animal: ' + str(e))
    finally:
        session.close()
    
    return redirect(url_for('home'))

@app.route('/addavalia',methods=['POST','GET'])
def inserir_avaliacao():
    session_a = Session() 
    texto = request.form['texto']
    blob_pt = TextBlob(texto)
    polaridade = blob_pt.sentiment.polarity
    avaliacao = Avaliacao(texto=texto,polaridade=polaridade) 
    try:
       session_a.add(avaliacao)
       session_a.commit() 
    except:
       session_a.rollback() 
    finally:
       session_a.close() 
    return redirect(url_for('listar_avalia'))


@app.route("/listavalia")
def listar_avalia():
    session_db = Session()
    avaliacoes = session_db.query(Avaliacao).all()
    return render_template("listavalia.html",avaliacoes=avaliacoes)

if __name__ == '__main__':
    app.run(debug=True)

