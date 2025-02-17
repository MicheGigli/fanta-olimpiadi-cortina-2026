from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Usa l'URL del database da Render (assicurati che sia definita come variabile d'ambiente)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///fallback.db")

db = SQLAlchemy(app)

# Creazione delle tabelle (solo al primo avvio)
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Backend funzionante con il database!"

if __name__ == "__main__":
    app.run(debug=True)
