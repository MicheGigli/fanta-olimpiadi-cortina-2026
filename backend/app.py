import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configura il database con la variabile d'ambiente
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("postgresql://fantasolimpiadi_db_user:AYA0Fs15FRfKDZQT9mTKSrlyx1FoVCsu@dpg-cupn6m9u0jms73bpnpb0-a/fantasolimpiadi_db")  # Usa la stringa di connessione
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
