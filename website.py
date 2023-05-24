from flask import Flask, render_template, request, redirect, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import test_database
import add_database



app = Flask(__name__)
app.secret_key = "temp"



class RegisterForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Length(min=4, max=50)],
        render_kw={"placeholder": "Email"},
    )
    first_name = StringField(
        validators=[InputRequired(), Length(min=1, max=50)],
        render_kw={"placeholder": "First Name"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=50)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Register")


    def validate_email(self, email):
        if not test_database.checkEmail(email):
            raise ValidationError(
                "That email already exists. Please choose a different one."
            )


    def add_email(self, email, first_name, password):
        return add_database.addCustomer(email, first_name, password)



class LoginForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Length(min=4, max=50)],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=50)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Login")

    def validate_login(self, email, password):
        user = test_database.loginCustomer(email, password)
        if user is None:
            raise ValidationError(
                "Login failed. Please check your email and password again."
            )
        else:
            return user



@app.route("/reviews/", methods=["GET", "POST"])
def reviews():
    if "user_id" in session:
        sorted_status = ["🔽", "🔽"]
        sort_parameter = None
        sort_method = None
        
        if request.method == "POST":
            sort_parameter = request.form["sort_parameter"]
            sort_method = request.form["sort_method"]

            match sort_parameter:
                case "price":
                    sorted_status = ["🔽" if "🔽" != sort_method else "🔼", "🔽"]
                case "num_stars":
                    sorted_status = ["🔽", "🔽" if "🔽" != sort_method else "🔼"]

        reviews = test_database.getAllReviews(session["user_id"], sort_parameter, sort_method)

        return render_template(
            "reviews.html", reviews=reviews, sorted_status=sorted_status
        )
    else:
        session["redirect"] = "reviews"
        return redirect(url_for("login"))



@app.route("/purchase_history/", methods=["GET", "POST"])
def purchase_history():
    if "user_id" in session:
        sorted_status = ["🔽", "🔽"]
        sort_parameter = None
        sort_method = None
        query_parameter = ""
        
        if request.method == "POST":
            sort_parameter = request.form["sort_parameter"]
            sort_method = request.form["sort_method"]

            match sort_parameter:
                case "price":
                    sorted_status = ["🔽" if "🔽" != sort_method else "🔼", "🔽", "🔽"]
                case "category_name":
                    query_parameter = request.form["query"]
                    print(query_parameter)
                    if not query_parameter:
                        sorted_status = ["🔽", "🔽" if "🔽" != sort_method else "🔼", "🔽"]
                case "product_quantity":
                    sorted_status = ["🔽", "🔽", "🔽" if "🔽" != sort_method else "🔼"]
        
        purchase_history = test_database.getAllPurchases(session["user_id"], sort_parameter, sort_method, query_parameter)

        return render_template("purchases.html", products=purchase_history, sorted_status=sorted_status, query=query_parameter)
    else:
        session["redirect"] = "purchase_history"
        return redirect(url_for("login"))



@app.route("/")
def start():
    if "user_id" in session:
        return redirect(url_for("home"))
    else:
        session["redirect"] = "home"
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("home"))
    form = LoginForm()
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            session["user_id"] = form.validate_login(email, password)
            session["cart"] = []
            return redirect(url_for(session["redirect"]))
        except Exception as e:
            print(e)

    return render_template("login.html", form=form)



@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("home"))
    form = RegisterForm()
    if request.method == "POST":
        print(request.form)
        email = request.form["email"]
        first_name = request.form["first_name"]
        password = request.form["password"]
        try:
            form.validate_email(email)
            session["user_id"] = form.add_email(email, first_name, password)
            session["cart"] = []
            return redirect(url_for("home"))
        except Exception as e:
            print(e)

    return render_template("register.html", form=form)



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



@app.route("/home")
def home():
    html_table_format = []
    raw = test_database.getAllProducts()
    # for x in raw:
    if "cart" in session:
        return render_template(
            "main.html",
            products=test_database.getAllProducts(),
            cartSize=session["cart"],
        )
    else:
        return render_template("main.html", products=test_database.getAllProducts())



if __name__ == "__main__":
    app.run(debug=True)