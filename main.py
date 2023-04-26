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


@app.route('/resources/book/add', methods=['POST'])
def add_book():
    message = "El libro se ha añadido correctamente"
    book = request.get_json()

    author = book['author']
    year = book['year']
    title = book['title']
    description = book['description']
    conn = fx__get_db()

    try:
        conn = fx__get_db()
        cursor = conn.cursor()
        cursor.execute('insert into books_table (author, year, title, description) values (%s, %s, %s, %s), (author, year, title, description)')
        cursor.close()
        conn.commit()
    except Exception as ex: 
        conn.rollback()
        message = "Error al añadir el libro"
    
    return jsonify({message})


if __name__ == '__main__':
    app.run(debug=True)