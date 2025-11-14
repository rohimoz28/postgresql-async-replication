from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
import sys

# Inisialisasi Flask dan konfigurasi
app = Flask(__name__)
app.config.from_object(Config)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Inisialisasi database
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))


@app.route('/')
def home():
    return jsonify({
        "message": "Flask API is working!",
        "status": "success",
        "endpoints": {
            "health": "/health",
            "books": "/books"
        }
    })


@app.route('/health')
def health():
    return jsonify({"status": "healthy", "database": "connected"})


# GET all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    result = [
        {
            "id": book.id,
            "name": book.name
        }
        for book in books
    ]
    return jsonify(result)


# ADD new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    if not data or not all(k in data for k in ('name',)):
        return jsonify({"ERROR : Missing data fields"}), 400

    new_book = Book(name=data['name'])
    db.session.add(new_book)
    db.session.commit()

    all_books = [
        {"id": book.id, "name": book.name}
        for book in Book.query.all()
    ]

    return jsonify({
        "message": "Book added successfully",
        "all_books": all_books
    }), 201


# UPDATE book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Missing field 'name'"}), 400

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    # update
    book.name = data['name']
    db.session.commit()
    book_dict = {"id": book.id, "name": book.name}

    return jsonify({
        "message": f"Book {book_id} updated successfully",
        "book": book_dict
    }), 200


# DELETE book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)

    if not book:
        return jsonify({"ERROR : Book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    all_books = [
        {"id": book.id, "name": book.name}
        for book in Book.query.all()
    ]

    return jsonify({
        "message": "Book deleted successfully",
        "books": all_books
    }), 200


def initialize_database():
    try:
        with app.app_context():
            db.create_all()
            print("✅ Database tables created")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False


if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    print(f"📡 Server will run on: http://0.0.0.0:5000")
    print(f"🌐 Access from host: http://localhost:5001")

    if initialize_database():
        try:
            app.run(
                host='0.0.0.0',  # Critical: allow external connections
                port=5000,  # Container port
                debug=False,  # Must be False
                threaded=True
            )
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            sys.exit(1)
    else:
        sys.exit(1)
