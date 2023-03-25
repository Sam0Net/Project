import sqlite3

# Creamos la conexión con base de datos
def create_connection():
    connection = sqlite3.connect("brain.db") 
    return connection

# Hacemos la conexión y obtenemos la tabla de nuestra base de datos
def get_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM preguntas_y_respuestas") 
    return cursor.fetchall() 

bot_list = list() 
def get_preguntas_respuestas():
    rows = get_table() 
    for row in rows:
        bot_list.extend(list(row)) 
    return bot_list 