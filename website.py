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
        if user is None or user == -1:
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

        reviews = test_database.getAllReviews(
            session["user_id"], sort_parameter, sort_method
        )

        return render_template(
            "reviews.html", reviews=reviews, sorted_status=sorted_status
        )
    else:
        session["redirect"] = "reviews"
        return redirect(url_for("login"))


@app.route("/purchase_history/", methods=["GET", "POST"])
def purchase_history():
    if "user_id" in session:
        query_parameter = ""
        sort_parameter = None
        sort_method = None

        if request.method == "POST":
            sort_parameter = request.form["sort_parameter"]
            sort_method = request.form.get("sort_method")
            sort_method = "🔼" if sort_method == "🔽" else "🔽"

            if "query" in request.form:
                query_parameter = request.form["query"]

        purchase_history = test_database.getAllPurchases(
            session["user_id"], sort_parameter, sort_method, query_parameter
        )

        return render_template(
            "purchases.html",
            products=purchase_history,
            sort_parameter=sort_parameter,
            sort_method=sort_method,
            query=query_parameter,
        )
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
        if "redirect" in session:
            return redirect(url_for(session["redirect"]))
        else:
            return redirect(url_for("home"))
    form = LoginForm()
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            session["user_id"] = form.validate_login(email, password)
            session["cart"] = list()
            if "redirect" in session:
                return redirect(url_for(session["redirect"]))
            else:
                return redirect(url_for("home"))
        except Exception as e:
            print(e)

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("home"))
    form = RegisterForm()
    if request.method == "POST":
        email = request.form["email"]
        first_name = request.form["first_name"]
        password = request.form["password"]
        try:
            form.validate_email(email)
            session["user_id"] = form.add_email(email, first_name, password)
            session["cart"] = list()
            return redirect(url_for("home"))
        except Exception as e:
            print(e)

    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/home", methods=["GET", "POST"])
def home():
    if "user_id" in session:
        query_parameter = ""
        sort_parameter = None
        sort_method = None

        if request.method == "POST":
            sort_parameter = request.form["sort_parameter"]
            sort_method = request.form.get("sort_method")
            sort_method = "🔼" if sort_method == "🔽" else "🔽"

            if "query" in request.form:
                query_parameter = request.form["query"]

        products = test_database.getAllProducts(
            sort_parameter, sort_method, query_parameter
        )

        return render_template(
            "main.html",
            products=products,
            sort_parameter=sort_parameter,
            sort_method=sort_method,
            query=query_parameter,
            cart=session["cart"],
        )
    else:
        session["redirect"] = "home"
        return redirect(url_for("login"))



@app.route("/product/<id>", methods=["GET", "POST"])
def product(id):
    if request.method == "POST":
        if request.form.get("add_cart_button") == "Add to Cart":
            adding_to_cart = session["cart"]
            adding_to_cart.append(id)
            session["cart"] = adding_to_cart
            return redirect(url_for("home"))
        elif request.form.get("back_button") == "Back":
            return redirect(url_for("home"))

    return render_template(
        "product.html", product=test_database.getProduct(id), cart=session["cart"]
    )


@app.route("/product/<id>/<customer_id>/", methods=["GET", "POST"])
def product_review(id, customer_id):
    rating_value = ""

    if request.method == "POST":
        if request.form.get("add_cart_button") == "Add to Cart":
            adding_to_cart = session["cart"]
            adding_to_cart.append(id)
            session["cart"] = adding_to_cart
            return redirect(url_for("home"))
        elif request.form.get("back_button") == "Back":
            return redirect(url_for("home"))
        elif request.form.get("rating"):
            rating_value = int(request.form.get("rating"))
        elif request.form.get("submit_rating_button"):
            print(request.form)
            add_database.add_review(
                id, customer_id, int(request.form.get("submit_rating_button"))
            )
            return render_template(
                "rating_submission.html", product=test_database.getProduct(id)
            ), {"Refresh": f"1.25; url={url_for('purchase_history')}"}

    return render_template(
        "product_review.html",
        product=test_database.getProduct(id),
        cart=session["cart"],
        rating=rating_value,
    )


@app.route("/cart", methods=["GET", "POST"])
def cart():
    cart_list = session["cart"]
    total = 0
    cart_dict = {}
    if cart_list:
        cart_dict = {
            i: [
                cart_list.count(i),
                test_database.getProduct(i)[0][1],
                test_database.getProduct(i)[0][2],
                test_database.getProduct(i)[0][2] * cart_list.count(i),
            ]
            for i in cart_list
        }
        for item in cart_dict:
            total += cart_dict[item][3]

    if request.method == "POST":
        if request.form.get("buy_cart_button") == "Purchase Cart":
            test_database.buyProduct(session["user_id"], cart_dict)
            session["cart"] = list()
            return redirect(url_for("home"))
        elif request.form.get("clear_cart_button") == "Clear Cart":
            session["cart"] = list()
            return redirect(url_for("cart"))

    return render_template("cart.html", cart=cart_dict, total=total)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == 'POST':
        if request.form.get('pur_hist_button') == "Purchase History":
            return redirect(url_for('purchase_history'))
        elif request.form.get('review_button') == "Reviews":
            return redirect(url_for('reviews'))
        elif request.form.get('update_acc_button') == "Update Name":
            return redirect(url_for('update_name'))
        elif request.form.get('delete_acc_button') == "Delete Account":
            return redirect(url_for('delete_account'))
        
    return render_template('settings.html', cart=session['cart'])

@app.route("/settings/update_name", methods=["GET", "POST"])
def update_name():
    if request.method == 'POST':
        if request.form.get('Cancel') == "Cancel":
            return redirect(url_for('settings'))
        elif request.form.get('Confirm') == "Confirm":
            test_database.changeName(session['user_id'], request.form['name'])
            return redirect(url_for('settings'))
    
    return render_template('update_name.html', cart=session['cart'])
        
@app.route('/settings/delete_account', methods=["GET", "POST"])
def delete_account():
    if request.method == 'POST':
        if request.form.get('Cancel') == "Cancel":
            return redirect(url_for('settings'))
        elif request.form.get('Confirm') == "Confirm":
            del_user = session['user_id']
            test_database.deleteUser(del_user)
            return redirect(url_for('logout'))

    return render_template('delete_acc.html', cart=session['cart'])
if __name__ == "__main__":
    app.run(debug=True)
