from flask import Flask, jsonify, request, Blueprint
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from config import confgig
from datetime import datetime
from function_jwt import write_token #validate_token

app = Flask(__name__)
conexion = MySQL(app)

@app.route("/registration", methods = ['POST']) #registra los usuarios a la base de datos 
def user_registration():

     cursor = conexion.connection.cursor()
     created_at = datetime.now()

     sql = """INSERT INTO users (name, last_name, pasword, email, phone_number, created_at) 
     VALUES ('{0}', '{1}', '{2}', '{3}', {4},'{5}')""".format(request.json['name'], request.json['last_name'],
     request.json['pasword'], request.json['email'], request.json['phone_number'], created_at)
     
     cursor.execute(sql)
     conexion.connection.commit()
      
     return jsonify({'Message': "User Registered Successfully"})

@app.route("/autentication", methods=["POST"]) # crea token
def user_autentication():
    data = request.get_json()
    email = data['email']
    password = data['pasword']

    cursor = conexion.connection.cursor()

    sql = "SELECT email,pasword FROM users"
    cursor.execute(sql)
    datos = cursor.fetchall()

    for user in datos:
        if user == (email, password):
            return write_token(data=request.get_json())
        else:
            continue

    return jsonify({'Message': "User no found :("})
                          
@app.route("/movies") #enlista todas las pelicualas
def list_movies():

    cursor = conexion.connection.cursor()

    sql =  """SELECT m.id, m.title, m.image, m.clasification,m.idFuncion, f.date
    FROM movies AS m
    INNER JOIN function_movie AS f
    ON m.idFuncion = f.id"""
    
    cursor.execute(sql)
    data = cursor.fetchall()
    movies = []

    for fila in data:
        movie = {'id':fila[0], 'title':fila[1], 'image':fila[2],
         'clasification':fila[3], 'idFuncion':fila[4], 'date': fila[5] }
        movies.append(movie)

    return jsonify({'movies:':movies, 'message': "List movies"})

@app.route("/shoping", methods = ['POST']) # compra de boletos
def buy_tikets():

     cursor = conexion.connection.cursor()
     id = request.json['id']
     movie = request.json['id_movie']
     seat =  int(request.json['id_seat'])
     created_at = datetime.now()

     sql = "SELECT id_seat FROM shopping"
     cursor.execute(sql)
     data = cursor.fetchall()
     
     for id_seat in data:  
        if id_seat[0] == seat:
            return jsonify({'Message': "Seat not available:("})
        
     sql2 = """INSERT INTO shopping (id,id_movie, id_seat,created_at) 
     VALUES ('{0}', '{1}','{2}', '{3}')""".format(id,movie, seat, created_at)

     cursor.execute(sql2)
     conexion.connection.commit()

     return jsonify({'Message': "Successful purchase"})
    
@app.route("/checkTickets") #lista de boletos comprados
def check_tickets():

    cursor = conexion.connection.cursor()

    sql =  """SELECT shopping.id, st.seat, m.idFuncion, f.date, shopping.id_movie, m.title, m.image, m.clasification
    FROM shopping
    INNER JOIN seats as st ON shopping.id_seat = st.id
    INNER JOIN  movies as m ON shopping.id_movie = m.id
    INNER JOIN  function_movie as f ON m.idFuncion = f.id
    ORDER BY shopping.id;;"""
    
    cursor.execute(sql)
    data = cursor.fetchall()
    tickets = []

    for fila in data:
        ticket = {'id':fila[0], 'seat':fila[1], 'idFuncion':fila[2],
         'date':fila[3], 'id_movie':fila[4], 'title': fila[5], 'image': fila[6], 'clasification': fila[7]}
        tickets.append(ticket)

    return jsonify({'Tickets:':tickets, 'message': "List Tickets"})

@app.route("/cancelTicket/<id_ticket>", methods = ['DELETE'] ) #elimina boletos
def delete_ticket(id_ticket):

     cursor = conexion.connection.cursor()

     sql = """SELECT f.date
     FROM shopping
     INNER JOIN  movies as m ON shopping.id_movie = m.id
     INNER JOIN  function_movie as f ON m.idFuncion = f.id
     WHERE shopping.id = '{0}'
     ORDER BY shopping.id;""".format(id_ticket)
     cursor.execute(sql)
     data = cursor.fetchall()

     now = datetime.now()

     for date in data:
        if now > date[0]:
           return jsonify({'Message': "You cannot delete an expired ticket"})

        else:
            sql2 = "DELETE FROM shopping WHERE id = '{0}'".format(id_ticket)
            cursor.execute(sql2)
            conexion.connection.commit()
            return jsonify({'Message': "TICKET REMOVED"})
        
def page_not_found(error):
    return "<h1> The page you're trying to search for doesn't exist...<h1>" ,404

if __name__ == '__main__':
    load_dotenv()
    app.config.from_object(confgig['development'])
    app.register_error_handler(404,page_not_found)
    app.run()
