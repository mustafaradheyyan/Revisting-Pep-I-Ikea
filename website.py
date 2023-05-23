from flask import Flask, render_template, request, redirect, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import test_database
import add_database

app = Flask(__name__)
app.secret_key = 'temp'

class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={'placeholder': 'Email'})
    first_name = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={'placeholder': 'First Name'})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={'placeholder': 'Password'})
    submit = SubmitField("Register")

    def validate_email(self, email):
        if not test_database.checkEmail(email):
            raise ValidationError("That email already exists. Please choose a different one.")
    
    def add_email(self, email, first_name, password):
        return add_database.addCustomer(email, first_name, password)
        
class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={'placeholder': 'Email'})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={'placeholder': 'Password'})
    submit = SubmitField("Login")

@app.route("/")
def home():
    if 'user_id' in session:
        return render_template('main.html')
    else:
        return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        password = request.form['password']
        try:
            form.validate_email(email)
            form.add_email(email, first_name, password)
        except Exception as e:
            print(e)
            
    return render_template('register.html', form=form)

@app.route("/logout")
def logout():
    pass

if __name__ == '__main__':
    app.run(debug=True)