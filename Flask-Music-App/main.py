from flask import Flask, render_template, redirect, url_for, request, session
from flask_login import LoginManager
from forms import LoginForm, RegisterForm
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__)
app.config["SECRET_KEY"] = "227c75baff5b86d11b0ad91b4983e5ca"
login_manager = LoginManager(app)
login_manager.init_app(app)

errors = [
    {
        "invalid_email": "The email already exists",
        "invalid_login": "Email or password is invalid",
        "invalid_query": "No result is  retrieved. Please query again",
    }
]


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    user_name = ""
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data, form.password.data)
        if user is None:
            return render_template(
                "login.html",
                form=form,
                title="Login",
                user_name=user_name,
                errors=errors,
                inv_login=True,
            )
        else:
            session["user_ID"] = form.email.data
            session["user_name"] = user["user_name"]
            user_name = session["user_name"]
            return redirect(url_for("query"))
    return render_template(
        "login.html",
        form=form,
        title="Login",
        user_name=user_name,
        errors=errors,
        inv_login=False,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    user_name = ""
    form = RegisterForm()
    if form.validate_on_submit():
        if isEmailUnique(form.email.data):
            createUser(form.email.data, form.user_name.data, form.password.data)
            return redirect(url_for("login"))
        else:
            return render_template(
                "register.html",
                form=form,
                title="Register",
                user_name=user_name,
                errors=errors,
                inv_email=True,
            )
    return render_template(
        "register.html",
        form=form,
        title="Register",
        user_name=user_name,
        errors=errors,
        inv_email=False,
    )


@app.route("/query", methods=["GET", "POST"])
def query():
    user_name = ""
    subscriptions = userSubscriptions()
    print(type(subscriptions))
    if "user_name" in session:
        user_name = session["user_name"]

    if request.method == "POST":
        if "query" in request.form:
            songs = querySongs(
                request.form["title"], request.form["artist"], request.form["year"]
            )
            print(songs)
            if songs is None or not songs:
                return render_template(
                    "query.html",
                    songs=songs,
                    user_name=user_name,
                    title="Query",
                    subscriptions=subscriptions,
                    errors=errors,
                    inv_query=True,
                )

            return render_template(
                "query.html",
                songs=songs,
                user_name=user_name,
                title="Query",
                subscriptions=subscriptions,
                errors=errors,
                inv_query=False,
            )

        if "subscribe" in request.form:
            if "user_ID" in session:
                addSubscription(
                    request.form["song_title"], request.form["song_artist"],
                )
                subscriptions = userSubscriptions()
                return render_template(
                    "query.html",
                    user_name=user_name,
                    title="Query",
                    subscriptions=subscriptions,
                    errors=errors,
                    inv_query=False,
                )
        if "remove" in request.form:
            removeSubscription(request.form["song_title"], request.form["song_artist"])
            subscriptions = userSubscriptions()
            return render_template(
                "query.html",
                user_name=user_name,
                title="Query",
                subscriptions=subscriptions,
                errors=errors,
                inv_query=False,
            )

    return render_template(
        "query.html",
        user_name=user_name,
        title="Query",
        subscriptions=subscriptions,
        errors=errors,
        inv_query=False,
    )


@app.route("/logout")
def logout():
    session.pop("user_ID", None)
    session.pop("user_name", None)
    return redirect(url_for("login"))


def get_user(email, password, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table("login")
    response = table.get_item(Key={"email": email})

    if int(response["ResponseMetadata"]["HTTPHeaders"]["content-length"]) > 2:
        if response["Item"]["password"] == password:
            return response["Item"]
        else:
            return None
    else:
        return None


def createUser(email, user_name, password, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table("login")
    response = table.put_item(
        Item={"email": email, "user_name": user_name, "password": password}
    )
    return response


def isEmailUnique(email, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table("login")
    response = table.query(KeyConditionExpression=Key("email").eq(email))
    if len(response["Items"]) != 0:
        return False
    else:
        return True


def querySongs(title, artist, year, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table("music")
    attr = {"title": title, "artist": artist, "year": year}
    filt = {}

    for value in attr:
        if attr[value]:
            filt.update({value: attr[value]})

    if len(filt) == 0:
        print("Please enter some values")
    elif len(filt) == 1:
        response = table.scan(
            FilterExpression=Attr(list(filt)[0]).eq(list(filt.values())[0])
        )
        return response["Items"]
    elif len(filt) == 2:
        response = table.scan(
            FilterExpression=Attr(list(filt)[0]).eq(list(filt.values())[0])
            & Attr(list(filt)[1]).eq(list(filt.values())[1])
        )
        return response["Items"]
    else:
        response = table.scan(
            FilterExpression=Attr(list(filt)[0]).eq(list(filt.values())[0])
            & Attr(list(filt)[1]).eq(list(filt.values())[1])
            & Attr(list(filt)[2]).eq(list(filt.values())[2])
        )
        return response["Items"]


def addSubscription(title, artist, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table("subscription")

    response = table.put_item(
        Item={"email": session["user_ID"], "song_title": title, "song_artist": artist,}
    )
    return response


def userSubscriptions(dynamodb=None):
    if "user_name" in session:
        if not dynamodb:
            dynamodb = boto3.resource("dynamodb")

        table_sub = dynamodb.Table("subscription")
        table_songs = dynamodb.Table("music")
        subscriptions = []

        response_sub = table_sub.scan(
            FilterExpression=Attr("email").eq(session["user_ID"])
        )
        for item in response_sub["Items"]:
            response_song = table_songs.scan(
                FilterExpression=Attr("artist").eq(item["song_artist"])
                & Attr("title").eq(item["song_title"])
            )
            subscriptions.append(response_song["Items"])
        return subscriptions
    else:
        return None


def removeSubscription(title, artist, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table("subscription")
    response = table.delete_item(Key={"email": session["user_ID"], "song_title": title})


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
