from flask import Flask, render_template, request, redirect, url_for
from google.cloud import datastore, storage
from datetime import datetime

datastore_client = datastore.Client.from_service_account_json('service.json')
storage_client = storage.Client.from_service_account_json('service.json')
session_user = ""
logged_in = False
user_image = ""
app = Flask(__name__)

# Erorr messages
errors = [
    {
        "invalid_id": "The ID already exists",
        "invalid_user_name": "The username already exists",
        "invalid_login": "ID or password is invalid",
        "password_incorrect": "The old password is incorrect"
    }
]

# Login Page
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get user entered ID and Password from login form
        id = request.form["id"]
        password = request.form["password"]

        # Validate the user
        if validate_login(id, password):

            # store_session(get_user_name(id))
            global session_user
            global user_image
            session_user = get_user_name(id)
            user_image = "https://storage.googleapis.com/forum-application-a1/user_images/" + id[(len(id))-1] + ".jpg"
            print(user_image)
            print(session_user)
            # If login information valid, redirect user to forum page
            return redirect(url_for("forum"))
        else:
            # Else display errors
            return render_template(
                "login.html", title="Login Page", errors=errors, inv_login=True
            )
    return render_template("login.html", title="Login Page", inv_login=False)


# Forum Page
@app.route("/forum", methods=["GET", "POST"])
def forum():
    # Load 10 most recent posts
    forums = get_forums()
    # Create new Post
    if request.method == "POST":
        subject = request.form["subject"]
        message = request.form["message-text"]
        image = request.files["post-image"]
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string)
        if image.filename != '':
            #Store image
            store_post_image(image, dt_string)
        create_forum(subject, message, dt_string)

    return render_template(
        "forum.html", forums=forums, title="Forum Page", user=session_user, user_image=user_image
    )


# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get user entered registration data
        id = request.form["id"]
        user_name = request.form["user_name"]
        password = request.form["password"]
        image = request.files["user-image"]
        # Validate data
        if validate_id(id) and validate_user_name(user_name):
            # Store user image
            store_user_image(image, id)
            # If ID and Username unique, create a new user
            create_user(id, user_name, password)
            # Redirect to login page
            return redirect(url_for("login"))
        # If both ID and Username invalid
        elif not validate_id(id) and not validate_user_name(user_name):
            # Display errors for both fields
            return render_template(
                "register.html",
                title="Register Page",
                errors=errors,
                inv_id=True,
                inv_user_name=True,
            )
        # If Username invalid
        elif not validate_user_name(user_name):
            # Display error for Username exist
            return render_template(
                "register.html",
                title="Register Page",
                errors=errors,
                inv_id=False,
                inv_user_name=True,
            )
        # If ID invalid
        else:
            # Display error for ID exist
            return render_template(
                "register.html",
                title="Register Page",
                errors=errors,
                inv_id=True,
                inv_user_name=False,
            )

    return render_template(
        "register.html",
        title="Register Page",
        errors=errors,
        inv_id=False,
        inv_user_name=False,
    )

# User profile page
@app.route("/user", methods=["GET", "POST"])
def user():
    # Get all user posts
    forums = get_user_forums(session_user)

    if request.method == "POST":
        # Update password
        if "update-pass" in request.form:
            user_name = session_user
            password = request.form["current-pass"]
            new_password = request.form["new-pass"]
            if update_password_valid(user_name, password):
                update_password(user_name, password, new_password)
                return redirect(url_for("login"))
            else:
                return render_template(
                "user.html", title="User Page", user=session_user, forums=forums, user_image=user_image, errors=errors, inv_pass=True
                )      
        # Edit user post
        elif "update-post" in request.form:
            subject = request.form["update-subject"]
            message = request.form["update-message-text"]
            date_time = request.form["date-time-hidden"]
            image = request.files["update-post-image"]
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            if image.filename != '':
                store_post_image(image, dt_string)
            update_post(subject, message, date_time, dt_string)
            return redirect(url_for("forum"))

    return render_template(
        "user.html", title="User Page", user=session_user, forums=forums, user_image=user_image, inv_pass=False
    )


# Method for checking if ID already exists in Datastore
def validate_id(id):
    # Specify kind
    query = datastore_client.query(kind="user")
    # Filter to get an ID in Datastore that equals to ID entered by user
    query.add_filter("id", "=", id)
    # Fetch the results
    results = list(query.fetch())
    # If no results found, ID is valid hence return True
    if not results:
        print("Doesnt Exist")
        return True
    # If results found, ID is invalid hence return False
    else:
        print("Exist")
        return False

# Method for checking if user_name already exists in Datastore
def validate_user_name(user_name):
    # Specify kind
    query = datastore_client.query(kind="user")
    # Using filter to check if user name exists in the datastore
    query.add_filter("user_name", "=", user_name)
    results = list(query.fetch())
    # Return false if doesn't exist, else true
    if not results:
        return True
    else:
        return False

# Check user id and password matches informations stored in datastore
def validate_login(id, password):
    query = datastore_client.query(kind="user")
    # Using queries to check if the user exist in datastore
    query.add_filter("id", "=", id)
    query.add_filter("password", "=", password)
    results = list(query.fetch())
    # Return false if no user found, else return true
    if not results:
        return False
    else:
        return True

# Create a new user
def create_user(id, user_name, password):
    entity = datastore.Entity(key=datastore_client.key("user"))
    entity.update({"id": id, "user_name": user_name, "password": password})
    datastore_client.put(entity)

# Get username of user given the id
def get_user_name(id):
    query = datastore_client.query(kind="user")
    # Using queries to find a matching id
    query.add_filter("id", "=", id)
    results = query.fetch()
    # Return the username of the given id
    for result in results:
        return result["user_name"]

# Get 10 most recent posts
def get_forums():
    query = datastore_client.query(kind="forum")
    # Order by date-time to get latest posts
    query.order = ["-date-time"]
    results = query.fetch(limit=10)
    return results

# Get posts for currently logged in user
def get_user_forums(user_name):
    query = datastore_client.query(kind="forum")
    query.add_filter("user_name", "=", user_name)
    results = query.fetch()
    return results

# Create new post
def create_forum(subject, message, date_time):
    entity = datastore.Entity(key=datastore_client.key("forum"))
    entity.update(
        {
            "date-time": date_time,
            "message-text": message,
            "subject": subject,
            "user_name": session_user,
        }
    )
    datastore_client.put(entity)

# Check if current password is correct
def update_password_valid(user_name, password):
    query = datastore_client.query(kind="user")
    # Query to check if password matches the one stored in the datastore
    query.add_filter("user_name", "=", user_name)
    query.add_filter("password", "=", password)
    results = list(query.fetch())
    # Return false if password is wrong, true if correct
    if not results:
        return False
    else:
        return True

# update current password
def update_password(user_name, password, new_password):
    query = datastore_client.query(kind="user")
    # Query to get entity with current password
    query.add_filter("user_name", "=", user_name)
    query.add_filter("password", "=", password)
    results = list(query.fetch())
    entity = results[0]
    # Update entity with new password
    entity['password'] = new_password
    # Update datstore with new password
    datastore_client.put(entity)
   
# Update user post
def update_post(subject, message, date_time, new_date_time):
    query = datastore_client.query(kind="forum")
    # Query to get post to update
    query.add_filter("user_name", "=", session_user)
    query.add_filter("date-time", "=", date_time)
    results = list(query.fetch())
    entity = results[0]
    # Update all the required fields with new information
    entity['subject'] = subject
    entity['message-text'] = message
    entity['date-time'] = new_date_time
    # Save it in datastore
    datastore_client.put(entity)

# Store image uploaded in a post
def store_post_image(image, date_time):
    bucket = storage_client.get_bucket('forum-application-a1')
    # Unique name for image using created date-time + user number
    image_name = "p" + session_user[(len(session_user))-1] + date_time + ".jpg"
    filename = "%s/%s" % ("post_images", image_name)
    blob = bucket.blob(filename)
    # Store image in cloud storage
    blob.upload_from_string(image.read())

# Store user image
def store_user_image(image, id):
    bucket = storage_client.get_bucket('forum-application-a1')
    # Name as user number
    image_name = id[(len(id))-1] + ".jpg"
    filename = "%s/%s" % ("user_images", image_name)
    blob = bucket.blob(filename)
    # Store image in cloud storage
    blob.upload_from_string(image.read())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

