from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from cs50 import SQL
from tempfile import mkdtemp
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required, error, success

app = Flask(__name__)
# Configure the app's session
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set database and use sqlite database
db = SQL("sqlite:///storage.db")


@app.route("/", methods=["GET"])
@login_required
def index():
    #
    # Shows the user the index/home page
    #

    # Query the database for all the details of the items
    items = db.execute("SELECT * FROM items WHERE user_id = ?", session["user_id"])
    # Displays all the details of the items in the index page
    return render_template("index.html", items=items)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    #
    # Creates an item and adds it to the user's storage
    #

    if request.method == "POST":
        # Get label and description
        label = request.form.get("label").strip()
        description = request.form.get("description").strip()
        # Ensures that there is a label
        if not label:
            return error("Must provide label", "/create")
        # Ensures that there is a description
        if not description:
            return error("Must provide description", "/create")

        # Adds item to the database
        db.execute("INSERT INTO items (user_id, label, description) VALUES (?, ?, ?)", session["user_id"], label, description)

        return redirect("/")
    else:
        return render_template("create.html")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    #
    # Edits the item/s the user wants to edit
    #

    if request.method == "POST":
        # Query the database for the total amount of items owned by the corresponding user_id
        rows = db.execute("SELECT COUNT(id) FROM items WHERE user_id = ? GROUP BY user_id", session["user_id"])
        # Ensures that the user has items
        if not rows:
            return error("No items available", "/edit")
        # Set the count of the items
        total_items = rows[0]["COUNT(id)"]
        
        # Loop until the count of the total items
        for i in range(1, total_items + 1):
            label = request.form.get(f"{i}-label")
            # Ensures that the user wants the current label to be changed
            if label:
                db.execute("UPDATE items SET label = ? WHERE id = ? AND user_id = ?", label, i, session["user_id"])

            description = request.form.get(f"{i}-desc")
            # Ensures that the user wants the current description to be changed
            if description:
                db.execute("UPDATE items SET description = ? WHERE id = ? AND user_id = ?", description, i, session["user_id"])

        return redirect("/")
    else:
        # Query the database for all the details of the items
        items = db.execute("SELECT * FROM items WHERE user_id = ?", session["user_id"])
        return render_template("edit.html", items=items)


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    #
    # Deletes the item/s the user wants to delete
    #

    if request.method == "POST":
        # Query the database for the total amount of items owned by the corresponding user_id
        rows = db.execute("SELECT id, COUNT(id) FROM items WHERE user_id = ? GROUP BY user_id", session["user_id"])
        print(rows)
        # Ensures that the user has items
        if not rows:
            return error("No items available", "/edit")
        # Set the count of the items
        total_items = rows[0]["COUNT(id)"]
        # Set the starting point
        start = rows[0]["id"]

        # Loop until the count of the total items
        for i in range(start, start + total_items + 1):
            # Gets the value of item checkboxes
            selected = request.form.get(f"{i}-select")
            # If it is checked delete it from the database
            if selected:
                db.execute("DELETE FROM items WHERE id = ? AND user_id = ?", i, session["user_id"])

        return redirect("/")
    else:
        # Query the database for all the details of the items
        items = db.execute("SELECT * FROM items WHERE user_id = ?", session["user_id"])
        return render_template("delete.html", items=items)


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    #
    # Changes the password of the user
    #

    if request.method == "POST":
        # Get username, current password, new password, and confirmation of new password
        username = request.form.get("username").strip()
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        new_password_again = request.form.get("new_password_again")
        # Ensures that there is a username, and a current password
        if not username:
            return error("Must provide username", "/change_password")
        if not current_password:
            return error("Must provide current password", "/change_password")
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        # Ensures that username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], current_password) or not rows[0]["id"]:
            return error("Invalid username and/or password", "/change_password")

        # Ensures that there is a new password, and a confirmation of the new password
        if not new_password:
            return error("Must provide new password", "/change_password")
        if not new_password_again:
            return error("Must provide confirmation of new password", "/change_password")
        # Ensures that password and confirmation password matches
        if not new_password == new_password_again:
            return error("Both new password, and confirmation of new password are not the same", "/change_password")
        # Ensures that the length of the new password is greater than 3 characters
        if len(new_password) <= 3:
            return error("New password must be greater than 3 characters", "/change_password")
        # Ensures that the new password is not the same as the current password
        if new_password == current_password:
            return error("New password is the same as the current password", "/change_password")
        
        # Get user id
        user_id = rows[0]["id"]

        # Generate a hashed new password
        hashed_new_password = generate_password_hash(new_password)
        # Update the current password of the user to the new password
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_new_password, user_id)

        return success("Successfully changed password!", "/")
    else:
        return render_template("change_password.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    #
    # Registers user
    #

    if request.method == "POST":
        # Get username, password, and confirmation password
        username = request.form.get("username").strip()
        password = request.form.get("password")
        password_again = request.form.get("password_again")

        # Ensures that there is a username, password, and confirmation password provided
        if not username:
            return error("Must provide username", "/register")
        if not password:
            return error("Must provide password", "/register")
        if not password_again:
            return error("Must provide confirmation password", "/register")
        # Ensures that password and confirmation password matches
        if not password == password_again:
            return error("Both passwords are not the same", "/register")
        # Ensures that the length of the password is greater than 3 characters
        if len(password) <= 3:
            return error("Password must be greater than 3 characters", "/register")

        # Ensures that username is unique
        rows = db.execute("SELECT username FROM users WHERE username = ?", username)
        if not len(rows) == 0:
            return error("Username is already taken", "/register")

        # Inserts/registers user to the database with a hashed password
        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

        return success("Registered successfully!", "/")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    #
    # Logs In user
    #

    # Returns an error when the user is already logged in
    if "user_id" in session:
        return error("You are already logged in", "/")

    if request.method == "POST":
        # Get username and password
        username = request.form.get("username").strip()
        password = request.form.get("password")
        # Ensures that there is a username, and a password
        if not username:
            return error("Must provide username", "/login")
        if not password:
            return error("Must provide password", "/login")

        # Query the database for all the info with the provided username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # If there's no info or the password is incorrect, return an error
        if not len(rows) > 0 or not check_password_hash(rows[0]["hash"], password):
            return error("Invalid username/password", "/login")

        # Set the current user's session the user_id and username
        session["user_id"] = rows[0]["id"]
        session["username"] = username

        return success("Successfully Logged In!", "/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    #
    # Log user out
    #

    # Forget any user_id
    session.clear()

    # Redirect to login page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)