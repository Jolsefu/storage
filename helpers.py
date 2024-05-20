from functools import wraps
from flask import redirect, session, flash

# A function that requires the user to be logged in to access decorated app routes
def login_required(f):
    # Decorate routes to require login
    # https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def error(message, route):
    #
    # Displays an error message to the passed route
    #

    flash(message, "error")
    return redirect(route)

def success(message, route):
    #
    # Displays a success message to the passed route
    #

    flash(message, "success")
    return redirect(route)