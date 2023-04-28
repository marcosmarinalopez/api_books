from flask import Flask, g, jsonify, request
import psycopg2

app = Flask(__name__)

def fx__get_db():
    
    db = getattr(g, '_database', None)

    if db is None:
        db = psycopg2.connect(
            user = "postgres",
            password = "PIKqPhxx35Ymhm3MIgdR",
            host="containers-us-west-17.railway.app",
            port="5679",
            database ="railway")

    return db


@app.teardown_appcontext
def fx__close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET'])
def home():
    conn = fx__get_db()
    cursor = conn.cursor()
    cursor.execute("select * from books_table")
    totalRows = cursor.fetchall()
    num_libros = len(totalRows)

    cursor.close()

    home_display = f"""
    <h1> API libros</h1>
    <p> Esta es una API que contiene {num_libros} libros. </p>
    """

    return home_display


@app.route('/books', methods=['GET'])
def get_books():
    conn = fx__get_db()
    cursor = conn.cursor()
    cursor.execute("select * from books_table")
    totalRows = cursor.fetchall()
    cursor.close()
    
    return jsonify(totalRows)


# hay que meter un body con json
@app.route('/resources/book/add', methods=['POST'])
def add_book():
    message = "El libro se ha añadido correctamente"
    book = request.get_json()

    author = book['author']
    year = book['year']
    title = book['title']
    description = book['description']
    id_book = book['id']
    conn = fx__get_db()

    try:
        conn = fx__get_db()
        cursor = conn.cursor()
        cursor.execute('insert into books_table (author, year, title, description, id) values (%s, %s, %s, %s, %s)', (author, year, title, description, id_book))
        conn.commit()
        cursor.close()
        
    except Exception as ex: 
        conn.rollback()
        message = "Error al añadir el libro \r\n" + str(ex)
    finally:
        cursor.close()
    return jsonify({'message':message})


# Si quisiéramos añadir un libro desde el código hay que enviar el json
# body = { "id": 6,
#     "title": "La Biblia",
#      "author": "Profetas",
#      "description": "En el principio creó Dios los cielos y la tierra",
#      "year": "2022"}

# request.post('htpp://127.0.0.1:5000/resoruces/book/add',json=body)

@app.route('/resources/book/delete/<int:id>', methods=['DELETE'])
def delete_book(id):
    message = "El libro se ha borrado correctamente"
        
    try:
        conn = fx__get_db()
        cursor = conn.cursor()
        cursor.execute('delete from books_table where id = %s', (id,))
        conn.commit()
                
    except Exception as ex: 
        conn.rollback()
        message = "Error al borrar el libro \r\n" + str(ex)
    finally:
        cursor.close()
    return jsonify({'message':message})



@app.route('/resources/book/update', methods=['PUT'])
def update_book():
    message = "El libro se ha actualizado correctamente"
    title= request.args['title']
    year= request.args['year']

    try:
        conn = fx__get_db()
        cursor = conn.cursor()
        cursor.execute('update books_table set year = %s where title = %s', (year,title))
        conn.commit()
                
    except Exception as ex: 
        conn.rollback()
        message = "Error al actualizar el libro \r\n" + str(ex)
    finally:
        cursor.close()
    return jsonify({'message':message})



if __name__ == '__main__':
    app.run(debug=True)