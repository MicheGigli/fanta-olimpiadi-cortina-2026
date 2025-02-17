from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Atleta

app = Flask(__name__)
CORS(app)  # Permette chiamate dal frontend

@app.route('/api/init_db', methods=['POST'])
def init_db():
    db.create_all()
    return jsonify({"message": "Database creato con successo!"}), 200

# Configura il database (usa l'URL di Render)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://fantasolimpiadi_db_user:AYA0Fs15FRfKDZQT9mTKSrlyx1FoVCsu@dpg-cupn6m9u0jms73bpnpb0-a/fantasolimpiadi_db"
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

