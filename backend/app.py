import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Atleta

app = Flask(__name__)
CORS(app)

# Configura il database (usa la variabile d'ambiente di Render)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Funzione per inizializzare il database automaticamente
def init_db():
    with app.app_context():
        db.create_all()

# API per ottenere atleti filtrati per disciplina e nazione
@app.route('/api/atleti', methods=['GET'])
def get_atleti():
    disciplina = request.args.get('disciplina')
    nazione = request.args.get('nazione')

    query = Atleta.query
    if disciplina:
        query = query.filter_by(disciplina=disciplina)
    if nazione:
        query = query.filter_by(nazione=nazione)

    atleti = query.all()
    return jsonify([a.to_dict() for a in atleti])

# Avvio dell'applicazione e inizializzazione automatica del database
if __name__ == '__main__':
    init_db()  # Esegui la creazione del database all'avvio
    app.run(debug=True)
