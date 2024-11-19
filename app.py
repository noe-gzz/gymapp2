import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

# Configuración de la aplicación
app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/gymapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de la base de datos
db = SQLAlchemy(app)

# Modelos de base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    training_goal = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    body_weight_kg = db.Column(db.Float, nullable=False)
    body_fat_percentage = db.Column(db.Float, nullable=False)
    height_cm = db.Column(db.Float, nullable=False)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    exercise_name = db.Column(db.String(100), nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    muscle_group = db.Column(db.String(100), nullable=False)

# Generador de datos para poblar la base de datos
# Definición de listas necesarias para los datos generados
training_goals = ["disminuir grasa corporal", "aumentar masa muscular", "mantenerse activo", "resistencia", "fuerza"]

usa_states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

mexico_states = [
    "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua",
    "Ciudad de México", "Coahuila", "Colima", "Durango", "Estado de México", "Guanajuato", "Guerrero",
    "Hidalgo", "Jalisco", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla",
    "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas",
    "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
]

def generate_user():
    username = f"user{random.randint(1,9999)}"
    password = "password123"
    training_goal = random.choice(training_goals)
    country = random.choice(["USA", "México"])
    state = random.choice(usa_states if country == "USA" else mexico_states)
    gender = random.choice(["Male", "Female"])
    height_cm = round(random.uniform(150, 200), 1)
    body_weight_kg = round(random.uniform(50, 120), 1)
    body_fat_percentage = round(random.uniform(10, 30), 1)
    return (
        username, password, training_goal, country, state, gender,
        body_weight_kg, body_fat_percentage, height_cm
    )

def generate_exercise(user_id):
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    exercise_name = random.choice(["Bench Press", "Squats", "Deadlift", "Pull Ups", "Push Ups"])
    weight_kg = round(random.uniform(10, 100), 1)
    reps = random.randint(5, 15)
    sets = random.randint(3, 5)
    muscle_group = random.choice(["Chest", "Legs", "Back", "Arms", "Shoulders"])
    return (
        user_id, date.strftime("%d/%m/%Y"), exercise_name, weight_kg, reps, sets, muscle_group
    )

# Rutas de la aplicación
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/populate")
def populate_database():
    db.drop_all()
    db.create_all()

    # Crear usuarios
    for _ in range(5):
        user_data = generate_user()
        user = User(
            username=user_data[0], password=user_data[1], training_goal=user_data[2],
            country=user_data[3], state=user_data[4], gender=user_data[5],
            body_weight_kg=user_data[6], body_fat_percentage=user_data[7], height_cm=user_data[8]
        )
        db.session.add(user)
        db.session.commit()

        # Crear ejercicios para el usuario
        for _ in range(10):
            exercise_data = generate_exercise(user.id)
            exercise = Exercise(
                user_id=exercise_data[0], date=exercise_data[1], exercise_name=exercise_data[2],
                weight_kg=exercise_data[3], reps=exercise_data[4], sets=exercise_data[5], muscle_group=exercise_data[6]
            )
            db.session.add(exercise)
        db.session.commit()

    return "Base de datos poblada con datos de ejemplo."

if __name__ == "__main__":
    print(f"Base de datos conectada en: {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.run(debug=True)
