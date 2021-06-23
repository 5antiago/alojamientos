from flask import Flask, render_template, url_for, request
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="alojamientos"
)

mycursor = mydb.cursor()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/Alojamientos", methods=["POST", "GET"])
def alojamientos():
    #Realiza la consulta de nombre y dirección de los alojamientos
    if request.method == "POST" and request.form["cantidad"]:
        mycursor.execute('SELECT alojamientos.Nombre, alojamientos.Direccion FROM alojamientos WHERE alojamientos.Capacidad >= '+ request.form["cantidad"])
    else:
        mycursor.execute('SELECT alojamientos.Nombre, alojamientos.Direccion FROM alojamientos')
    response = mycursor.fetchall()
    return render_template("Alojamientos.html", listado = response)


@app.route("/Actividades", methods=["POST", "GET"])
def actividades():
    #Consulta las acticvidades de hasta nivel 5
    if request.method == "POST" and request.form["dificultad"]:
        mycursor.execute('SELECT actividades.Nombre, actividades.Descripcion FROM actividades WHERE actividades.Dificultad <= '+ request.form["dificultad"])
    else:
        mycursor.execute('SELECT actividades.Nombre, actividades.Descripcion FROM actividades')
    response = mycursor.fetchall()
    return render_template("Actividades.html", listado = response)

@app.route("/Dias", methods=["POST", "GET"])
def diaActividad():
    #Consulta las actividades de un día específico
    if request.method == "POST" and request.form["dia"]:
        mycursor.execute('SELECT alojamientos.Nombre, actividades.Nombre, actividades.Descripcion FROM realizan, actividades, alojamientos WHERE realizan.Dia = "'+ request.form["dia"] +'" AND realizan.Actividades_idActividades = actividades.idActividades and realizan.alojamientos_idalojamientos = alojamientos.idalojamientos')
    else:
        mycursor.execute('SELECT alojamientos.Nombre, actividades.Nombre, actividades.Descripcion FROM realizan, actividades, alojamientos WHERE realizan.Actividades_idActividades = actividades.idActividades and realizan.alojamientos_idalojamientos = alojamientos.idalojamientos')
    response = mycursor.fetchall()
    return render_template("Dias.html", listado = response, title="Actividades")


if __name__ == "__main__":
    app.run(debug=True)
