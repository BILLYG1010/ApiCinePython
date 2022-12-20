from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import confgig

app = Flask(__name__)
conexion = MySQL(app)

@app.route("/registration", methods = ['POST']) #registra los usuarios a la base de datos 
def user_registration():

     cursor = conexion.connection.cursor()

     sql = """INSERT INTO users (name, last_name, pasword, email, phone_number, created_at) 
     VALUES ('{0}', '{1}', '{2}', '{3}', {4},'{5}')""".format(request.json['name'], request.json['last_name'],
     request.json['pasword'], request.json['email'], request.json['phone_number'], request.json['created_at'])
     
     cursor.execute(sql)
     conexion.connection.commit()
      
     return jsonify({'Message': "User Registered Successfully"})

@app.route("/movies") #enlista todas las pelicualas
def list_movies():

    cursor = conexion.connection.cursor()

    sql = "SELECT id,title,image,clasification,created_ad,idFuncion FROM movies"
    cursor.execute(sql)
    datos = cursor.fetchall()
    movies =  []

    for fila in datos:
        movie = {'id':fila[0], 'title':fila[1], 'image':fila[2],
         'clasification':fila[3], 'created_ad':fila[4], 'idFuncion':fila[5]  }
        movies.append(movie)

    return jsonify({'movies':movies, 'mensaje': "Peliculas listadas"})


def page_not_found(error):
    return "<h1> La pagina que intentas buscar no existe...<h1>" ,404


if __name__ == '__main__':
    app.config.from_object(confgig['development'])
    app.register_error_handler(404,page_not_found)
    app.run()
