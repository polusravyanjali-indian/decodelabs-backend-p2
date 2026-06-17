from flask import Flask, request, jsonify
from models import db, User

app = Flask(__name__)

# SQLite database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Home route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to DecodeLabs REST API!"}), 200

# CREATE - POST /users
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or not data.get("email"):
        return jsonify({"status": "error", "message": "Email is required"}), 400
    
    existing = User.query.filter_by(email=data["email"]).first()
    if existing:
        return jsonify({"status": "error", "message": "Email already exists"}), 409
    
    user = User(email=data["email"], age=data.get("age"))
    db.session.add(user)
    db.session.commit()
    return jsonify({"status": "success", "data": user.to_dict()}), 201

# READ ALL - GET /users
@app.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    return jsonify({"status": "success", "total": len(users), "data": [u.to_dict() for u in users]}), 200

# READ ONE - GET /users/<id>
@app.route("/users/<int:user_id>", methods=["GET"])
def get_one_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404
    return jsonify({"status": "success", "data": user.to_dict()}), 200

# UPDATE - PUT /users/<id>
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404
    data = request.get_json()
    if "age" in data:
        user.age = data["age"]
    if "is_active" in data:
        user.is_active = data["is_active"]
    db.session.commit()
    return jsonify({"status": "success", "data": user.to_dict()}), 200

# DELETE - DELETE /users/<id>
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"status": "success", "message": "User deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)