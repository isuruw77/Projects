from botocore.paginate import ResultKeyIterator
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager
from werkzeug.wrappers import response
from forms import LoginForm, RegisterForm, ConfirmUser
import boto3
import botocore
from boto3.dynamodb.conditions import Key, Attr

queryText = ""
house_type = []
min_val = ""
max_val = ""
bedrooms = ""
bathrooms = ""
parking = ""
user_ID = ""
house_ID = ""


application = app = Flask(__name__)
app.config["SECRET_KEY"] = "227c75baff5b86d11b0ad91b4983e5cb"
login_manager = LoginManager(app)
login_manager.init_app(app)

cloudsearch = boto3.client(
    "cloudsearchdomain",
    endpoint_url="http://doc-real-estate-ckelza4573ngxteirivt3jfg5e.us-west-1.cloudsearch.amazonaws.com",
    region_name="us-west-1",
)

cognito = boto3.client("cognito-idp", region_name="us-west-1")

APP_CLIENT_ID = "2ibnafbpseoitalqhg2pnavo79"

errors = [
    {
        "invalid_email": "[The email already exists.]",
        "invalid_login": "[Email or password is invalid.]",
    }
]


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        if "search" in request.form:
            global queryText
            queryText = request.form["search-result"]
            return redirect(url_for("search"))
    return render_template("home.html", title="home")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if signUp(
            form.email.data,
            form.password.data,
            form.first_name.data,
            form.last_name.data,
        ):
            global user_ID
            user_ID = form.email.data
            return redirect(url_for("confirm"))
        else:
            return render_template(
                "register.html",
                form=form,
                title="register",
                errors=errors,
                inv_email=True,
            )
    return render_template(
        "register.html", form=form, title="register", errors=errors, inv_email=False
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if loginUser(form.email.data, form.password.data):
            global user
            user = form.email.data
            session["User"] = form.email.data

            return redirect(url_for("home"))
        else:
            return render_template(
                "login.html", form=form, title="login", errors=errors, inv_login=True
            )
    return render_template(
        "login.html", form=form, title="login", errors=errors, inv_login=False
    )


@app.route("/confirm", methods=["GET", "POST"])
def confirm():
    form = ConfirmUser()
    if form.validate_on_submit():
        if confirmSignUp(form.code.data):
            return redirect(url_for("login"))
    return render_template("confirm.html", form=form, title="confirm")


@app.route("/search", methods=["GET", "POST"])
def search():
    user = ""
    if "User" in session:
        user = session["User"]

    if request.method == "POST":
        if "search-bar" in request.form:
            global queryText
            queryText = request.form["search-result"]
            searchQuery = query()
            return render_template("search.html", title="search", results=searchQuery)

        elif "filter" in request.form:
            global house_type
            global min_val
            global max_val
            global bedrooms
            global bathrooms
            global parking
            min_val = request.form["min-value"]
            max_val = request.form["max-value"]
            bedrooms = request.form["bedrooms"]
            bathrooms = request.form["bathrooms"]
            parking = request.form["parking"]
            house_type = request.form.getlist("house-type")
            return render_template("search.html", title="search", results=query())

        elif "house-ID" in request.form:
            # print(request.form["ID"])
            global house_ID
            house_ID = request.form["ID"]
            return redirect(url_for("view"))
        elif "favourite" in request.form:
            addFavourite(request.form["favourite_ID"])
            searchQuery = query()
            return render_template("search.html", title="search", results=searchQuery)
    else:
        searchQuery = query()
        return render_template("search.html", title="search", results=searchQuery)


@app.route("/view")
def view():
    properties = getHouse()
    return render_template("view.html", title="view", properties=properties)


@app.route("/favourites")
def favourites():
    properties = userFavourites()
    print(properties)
    return render_template("favourites.html", title="favourites", properties=properties)


def signUp(email, password, first_name, last_name):
    try:
        response = cognito.sign_up(
            ClientId=APP_CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "given_name", "Value": first_name},
                {"Name": "family_name", "Value": last_name},
            ],
        )
    except botocore.exceptions.ClientError:
        return False
    else:
        return True


@login_manager.user_loader
def load_user(token):
    try:
        response = cognito.get_user(AccessToken=token)
    except botocore.exceptions.ClientError:
        return None
    return response


@app.route("/logout")
def logout():
    session.pop("User_ID", None)
    session.pop("User_name", None)
    return redirect(url_for("login"))


def resendVerification():
    response = cognito.resend_confirmation_code(
        ClientId=APP_CLIENT_ID, Username="kiborl77@gmail.com",
    )
    print(response)


def confirmSignUp(code):
    try:
        response = cognito.confirm_sign_up(
            ClientId=APP_CLIENT_ID, Username=user_ID, ConfirmationCode=code
        )
    except botocore.exceptions.ClientError:
        return False
    else:
        return True


def loginUser(username, password):
    try:
        response = cognito.initiate_auth(
            ClientId=APP_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": password},
        )
    except botocore.exceptions.ClientError:
        return False
    else:
        getUser(response["AuthenticationResult"]["AccessToken"])
        return True


def getUser(token):
    try:
        response = cognito.get_user(AccessToken=token)
    except botocore.exceptions.ClientError:
        print("ERROR")
    else:
        for attr in response["UserAttributes"]:
            if attr["Name"] == "email":
                session["User_ID"] = attr["Value"]
            elif attr["Name"] == "given_name":
                session["User_Name"] = attr["Value"]


def query():
    response = cloudsearch.search(
        query=queryConstructor(), queryParser="structured", size=10, start=0,
    )
    # print(queryConstructor())
    # print(response['hits'])
    results = response["hits"]["hit"]
    # print(results)
    return results


def queryConstructor():
    text = queryText
    query = "(and (or (phrase '{}') (prefix '{}') ) {} {} {} {} {})".format(
        text, text, houseType(), priceRange(), bedroomNum(), bathNum(), carNum()
    )
    return query


def houseType():
    s = ""
    for type in house_type:
        s += "type:'{}' ".format(type)

    if not house_type:
        q = ""
    else:
        q = "(or {})".format(s)

    return q


def priceRange():

    if not min_val and not max_val:
        q = ""
    elif not min_val:
        q = "(range field=price [0, {}])".format(max_val)
    elif not max_val:
        s = "(range field=price [{},".format(min_val)
        q = s + "})"
    else:
        q = "(range field=price [{}, {}])".format(min_val, max_val)

    return q


def bedroomNum():
    if not bedrooms:
        q = ""
    elif bedrooms == "on":
        q = ""
    else:
        s = "(range field=bedroom2 [{},".format(bedrooms)
        q = s + "})"

    return q


def bathNum():
    if not bathrooms:
        q = ""
    elif bathrooms == "on":
        q = ""
    else:
        s = "(range field=bathroom [{},".format(bathrooms)
        q = s + "})"

    return q


def carNum():
    if not parking:
        q = ""
    elif parking == "on":
        q = ""
    else:
        s = "(range field=car [{},".format(parking)
        q = s + "})"

    return q


def getHouse(dynamodb=None):

    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", region_name="us-west-1")

    table = dynamodb.Table("housing")
    response = table.query(KeyConditionExpression=Key("ID").eq(house_ID.strip()))
    print(response["Items"])
    return response["Items"]


def addFavourite(house_ID, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", region_name="us-west-1")

    table = dynamodb.Table("favourites")
    if house_ID and "User_ID" in session:
        response = table.put_item(
            Item={"email": session["User_ID"], "house_ID": house_ID,}
        )
        return response
    else:
        return None


def userFavourites(dynamodb=None):
    if "User_ID" in session:
        if not dynamodb:
            dynamodb = boto3.resource("dynamodb", region_name="us-west-1")

        table_fav = dynamodb.Table("favourites")
        table_property = dynamodb.Table("housing")
        subscriptions = []

        response_sub = table_fav.scan(
            FilterExpression=Attr("email").eq(session["User_ID"])
        )
        for item in response_sub["Items"]:
            response_fav = table_property.scan(
                FilterExpression=Attr("ID").eq(item["house_ID"].strip())
            )

            subscriptions.append(response_fav["Items"])
        # print(subscriptions)
        return subscriptions
    else:
        return None


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
