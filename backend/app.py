from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Atleta

app = Flask(__name__)
CORS(app)  # Permette chiamate dal frontend

# Configura il database (usa l'URL di Render)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://user:password@host:port/dbname"
db.init_app(app)

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

