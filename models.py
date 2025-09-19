from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    status = db.Column(db.String(50))
    idade = db.Column(db.Integer)
    sexo = db.Column(db.String(20))
    foto = db.Column(db.String(200))
    alergias = db.Column(db.String(200))
    condicoes = db.Column(db.String(200))

class Timeline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))
    data = db.Column(db.String(20))
    evento = db.Column(db.String(200))