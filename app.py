from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para usar session

@app.route("/", methods=["GET", "POST"])
def dashboardmed():
    if "paciente" not in session:
        session["paciente"] = {
            "nome": "João da Silva",
            "status": "Em Atendimento",
            "idade": 58,
            "sexo": "Masculino",
            "foto": "/static/img/placeholder.jpg",
            "alergias": "Dipirona",
            "condicoes": ["Hipertensão", "Diabetes Tipo II"],
            "timeline": [
                {"data": "15/09/2025", "evento": "Consulta Dr. Ana (Cardiologia)"},
                {"data": "12/09/2025", "evento": "Exame de Sangue (Hemograma)"},
                {"data": "05/09/2025", "evento": "Consulta Dr. João (Clínico Geral)"},
                {"data": "20/08/2025", "evento": "Raio-X Tórax"}
            ]
        }
    paciente = session["paciente"]

    if request.method == "POST":
        if "status" in request.form:
            paciente["status"] = request.form["status"]
        if "data" in request.form and "evento" in request.form and "ala" in request.form:
            novo_evento = {
                "data": request.form["data"],
                "evento": f"{request.form['evento']} (Ala: {request.form['ala']})"
            }
            paciente["timeline"].insert(0, novo_evento)
        session["paciente"] = paciente
        return redirect(url_for("dashboardmed"))

    return render_template("index.html", paciente=paciente)

if __name__ == "__main__":
    app.run(debug=True)