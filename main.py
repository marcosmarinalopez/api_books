from flask import Flask, g
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

if __name__ == '__main__':
    app.run()