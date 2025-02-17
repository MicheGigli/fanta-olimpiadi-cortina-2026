import os
from sqlalchemy import text
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Atleta, Disciplina, Nazione

app = Flask(__name__)
CORS(app)

# Configura il database usando la variabile d'ambiente di Render
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Creazione delle tabelle
with app.app_context():
    db.create_all()

@app.route('/api/atleti/columns', methods=['GET'])
def get_atleti_columns():
    query = text("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'atleta'
    """)
    result = db.session.execute(query)
    columns = [{"column_name": row[0], "data_type": row[1]} for row in result]
    return jsonify(columns)

# API per ottenere tutte le discipline
@app.route('/api/discipline', methods=['GET'])
def get_discipline():
    discipline = Disciplina.query.all()
    return jsonify([{"id": d.id, "nome": d.nome} for d in discipline])

# API per ottenere tutte le nazioni
@app.route('/api/nazioni', methods=['GET'])
def get_nazioni():
    nazioni = Nazione.query.all()
    return jsonify([{"id": n.id, "nome": n.nome} for n in nazioni])

# API per ottenere atleti filtrati
@app.route('/api/atleti', methods=['GET'])
def get_atleti():
    disciplina_id = request.args.get('disciplina')
    nazione_id = request.args.get('nazione')

    query = Atleta.query
    if disciplina_id:
        query = query.filter_by(disciplina_id=disciplina_id)
    if nazione_id:
        query = query.filter_by(nazione_id=nazione_id)

    atleti = query.all()
    return jsonify([a.to_dict() for a in atleti])

# API per aggiungere una disciplina
@app.route('/api/discipline', methods=['POST'])
def add_disciplina():
    data = request.json
    if not data or "nome" not in data:
        return jsonify({"error": "Dati mancanti"}), 400

    nuova_disciplina = Disciplina(nome=data["nome"])
    db.session.add(nuova_disciplina)
    db.session.commit()

    return jsonify({"message": "Disciplina aggiunta con successo!", "id": nuova_disciplina.id}), 201

# API per aggiungere una nazione
@app.route('/api/nazioni', methods=['POST'])
def add_nazione():
    data = request.json
    if not data or "nome" not in data:
        return jsonify({"error": "Dati mancanti"}), 400

    nuova_nazione = Nazione(nome=data["nome"])
    db.session.add(nuova_nazione)
    db.session.commit()

    return jsonify({"message": "Nazione aggiunta con successo!", "id": nuova_nazione.id}), 201


# API per aggiungere un atleta
@app.route('/api/atleti', methods=['POST'])
def add_atleta():
    data = request.json
    if not data or "nome" not in data or "disciplina_id" not in data or "nazione_id" not in data:
        return jsonify({"error": "Dati mancanti"}), 400

    nuova_disciplina = Disciplina.query.get(data["disciplina_id"])
    nuova_nazione = Nazione.query.get(data["nazione_id"])

    if not nuova_disciplina or not nuova_nazione:
        return jsonify({"error": "Disciplina o nazione non trovata"}), 404

    nuovo_atleta = Atleta(nome=data["nome"], disciplina_id=data["disciplina_id"], nazione_id=data["nazione_id"])
    db.session.add(nuovo_atleta)
    db.session.commit()

    return jsonify({"message": "Atleta aggiunto con successo!"}), 201

@app.route('/api/atleti/<int:atleta_id>', methods=['DELETE'])
def delete_atleta(atleta_id):
    atleta = Atleta.query.get(atleta_id)
    if not atleta:
        return jsonify({"error": "Atleta non trovato"}), 404
    
    db.session.delete(atleta)
    db.session.commit()
    return jsonify({"message": "Atleta eliminato con successo!"}), 200

@app.route('/api/nazioni/<int:nazione_id>', methods=['DELETE'])
def delete_nazione(nazione_id):
    nazione = Nazione.query.get(nazione_id)
    if not nazione:
        return jsonify({"error": "Nazione non trovata"}), 404
    
    db.session.delete(nazione)
    db.session.commit()
    return jsonify({"message": "Nazione eliminata con successo!"}), 200

@app.route('/api/discipline/<int:disciplina_id>', methods=['DELETE'])
def delete_disciplina(disciplina_id):
    disciplina = Disciplina.query.get(disciplina_id)
    if not disciplina:
        return jsonify({"error": "Disciplina non trovata"}), 404

@app.route('/api/atleti', methods=['DELETE'])
def delete_all_atleti():
    try:
        num_deleted = db.session.query(Atleta).delete()
        db.session.commit()
        return jsonify({"message": f"Eliminati {num_deleted} atleti!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    
    db.session.delete(disciplina)
    db.session.commit()
    return jsonify({"message": "Disciplina eliminata con successo!"}), 200


@app.route("/api/reset_atleti", methods=["POST"])
def reset_atleti():
    try:
        # Drop tabella se esiste
        drop_query = text("DROP TABLE IF EXISTS atleta CASCADE;")
        db.session.execute(drop_query)

        # Creazione nuova tabella
        create_query = text("""
            CREATE TABLE atleta (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                disciplina_id INTEGER REFERENCES disciplina(id) ON DELETE CASCADE,
                nazione_id INTEGER REFERENCES nazione(id) ON DELETE CASCADE
            );
        """)
        db.session.execute(create_query)

        db.session.commit()
        return jsonify({"message": "Tabella atleta resettata con successo!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
