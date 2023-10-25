from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrations.db'
db = SQLAlchemy(app)


class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']

    # Создаем новую запись в базе данных внутри контекста приложения
    with app.app_context():
        new_registration = Registration(name=name, email=email)
        db.session.add(new_registration)
        db.session.commit()

    return redirect(url_for('success'))


@app.route('/success')
def success():
    return 'Регистрация прошла успешно!'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаем таблицы в базе данных перед запуском приложения
    app.run(debug=True)