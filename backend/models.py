from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)

class Nazione(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)

class Atleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=False)
    nazione_id = db.Column(db.Integer, db.ForeignKey('nazione.id'), nullable=False)

    disciplina = db.relationship('Disciplina', backref=db.backref('atleti', lazy=True))
    nazione = db.relationship('Nazione', backref=db.backref('atleti', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "disciplina": self.disciplina.nome,
            "nazione": self.nazione.nome
        }
