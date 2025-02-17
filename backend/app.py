import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Atleta

app = Flask(__name__)
CORS(app)  # Permette chiamate dal frontend

# Configura il database (usa l'URL di Render)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Usa la variabile d'ambiente
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# API per inizializzare il database (solo se necessario)
@app.route('/api/init_db', methods=['POST'])
def init_db():
    with app.app_context():
        db.create_all()
    return jsonify({"message": "Database creato con successo!"}), 200

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

# Esegui l'app solo in modalità locale
if __name__ == '__main__':
    app.run(debug=True)
