from flask import Flask, render_template, request, redirect, url_for
from models import db, Paciente, Timeline

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pacientes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chave_secreta'

db.init_app(app)
# Depois adicionar opção de pegar os dados do paciente selecionado ao invés de pôr dados mockados. Necessitando de uma tela pra selecionar o paciente.
def cria_banco():
    db.create_all()
    if not Paciente.query.first():
        paciente = Paciente(
            nome="João da Silva",
            status="Em Atendimento",
            idade=58,
            sexo="Masculino",
            foto="/static/img/placeholder.jpg",
            alergias="Dipirona",
            condicoes="Hipertensão,Diabetes Tipo II"
        )
        db.session.add(paciente)
        db.session.commit()
        eventos = [
            {"data": "15/09/2025", "evento": "Consulta Dr. Ana (Cardiologia)"},
            {"data": "12/09/2025", "evento": "Exame de Sangue (Hemograma)"},
            {"data": "05/09/2025", "evento": "Consulta Dr. João (Clínico Geral)"},
            {"data": "20/08/2025", "evento": "Raio-X Tórax"}
        ]
        for ev in eventos:
            db.session.add(Timeline(paciente_id=paciente.id, data=ev["data"], evento=ev["evento"]))
        db.session.commit()

@app.route("/", methods=["GET", "POST"])
def dashboardmed():
    paciente = Paciente.query.first()
    if request.method == "POST":
        if "status" in request.form:
            paciente.status = request.form["status"]
            db.session.commit()
        if "data" in request.form and "evento" in request.form and "ala" in request.form:
            novo_evento = Timeline(
                paciente_id=paciente.id,
                data=request.form["data"],
                evento=f"{request.form['evento']} (Ala: {request.form['ala']})"
            )
            db.session.add(novo_evento)
            db.session.commit()
        return redirect(url_for("dashboardmed"))

    timeline = Timeline.query.filter_by(paciente_id=paciente.id).order_by(Timeline.id.desc()).all()
    paciente_dict = {
        "nome": paciente.nome,
        "status": paciente.status,
        "idade": paciente.idade,
        "sexo": paciente.sexo,
        "foto": paciente.foto,
        "alergias": paciente.alergias,
        "condicoes": paciente.condicoes.split(","),
        "timeline": [{"data": t.data, "evento": t.evento} for t in timeline]
    }
    return render_template("index.html", paciente=paciente_dict)

if __name__ == "__main__":
    with app.app_context():
        cria_banco()
    app.run(debug=True)