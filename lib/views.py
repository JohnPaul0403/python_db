import requests
from functools import wraps
from flask import Blueprint, redirect, render_template, session, abort, request, url_for, flash
from .extensions import GOOGLE_CLIENT_ID, flow, app_id_token, app_cachecontrol, my_requests
from .users import auth_users
from .models import user_model

main = Blueprint('main', __name__)

#Login required decorator
def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print("user" not in session)
        if "google_id" in session or "user" in session:
            return function()
        
        return abort(401)  # Authorization required

    return wrapper

#________________________ Index page  ________________________#
@main.route("/")
def index():
    return render_template("index.html")

#________________________ Login page  ________________________#
@main.route("/login")
def login():
    return render_template("login.html")

#________________________ Signup page  ________________________#
@main.route("/signup")
def signup():
    return render_template("signup.html")

#________________________ Login Methods-________________________#
@main.route("/login/user", methods = ["POST"])
def get_user():
    """
    Login for user.
    Parameters:
        None.
    Returns:
        -url for auth_login
        -url to login again, in case of an error
    """
    if request.method != "POST":
        flash("Internal problem. Please try again!")
        return redirect(url_for("main.login"))
    
    user_auth: list = [request.form["username"], request.form["password"]]
    if not auth_users.verify_login({"name": user_auth[0], "pass" : user_auth[1]}):
        flash("Invalid username or password. Please try again!")
        return redirect(url_for("login"))
    return redirect(url_for("main.auth_login", user = user_auth[0], password = user_auth[1]))
    
@main.route("/login/user/auth_login")
def auth_login():
    """
    Login for user.
    Parameters:
        None.
    Returns:
        -template for the dashboard
        -url to login again, in case of an bad authentification
    """

    user_auth: list = [request.args.get("user"), request.args.get("password")]
    user: user_model.User = user_model.User(user_auth[0])
    print(user_auth)
    if user.login(user_auth[1]):
        session.pop('_flashes', None)
        session["user"] = user.to_json()
        return redirect("/dashboard")
    
    flash("Invalid username or password. Please try again!")
    return redirect(url_for("main.login"))
    

@main.route("/login/google")
def get_google_url():
    """
    Generate the Google URL for user login.
    Returns:
        str: The URL for user login.
    """
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@main.route("/callback")
def callback():
    """
    Callback function for the "/callback" route.
    This function is called when the user is redirected to the "/callback" endpoint after
    completing the authorization process. It fetches the token using the authorization
    response from the request URL.
    Parameters:
        None.
    Returns:
        None.
    Raises:
        None.
    """
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = app_cachecontrol.CacheControl(request_session)
    token_request = my_requests.Request(session=cached_session)

    id_info = app_id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    if not auth_users.verify_google_login(id_info):
        print("error")
        return abort(500)

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    return redirect("/login/auth_google_login")

@main.route("/login/auth_google_login")
def auth_google_login():
    """
    Login for user.
    Parameters:
        None.
    Returns:
        -template for the dashboard
        -url to login again, in case of an error
    """
    user: user_model.User = user_model.User(session["email"])
    if user.login_google(session["name"]):
        session.pop('_flashes', None)
        session["user"] = user.to_json()
        return redirect("/dashboard")
    
    flash("Invalid username. Please try again!")
    return redirect(url_for("main.login"))

@main.route("/logout")
def logout():
    """
    Logout for user.
    Parameters:
        None.
    Returns:
        -template for the index
    """
    user = user_model.from_json(session["user"])
    user.logout(session)
    session.clear()
    return redirect("/")

#________________________ Signup user method  ________________________#
@main.route("/signup/user", methods = ["POST"])
def signup_user():
    """
    Creates a new user account when a POST request is made to "/signup/user" endpoint.
    Returns:
        - If the request method is not "POST", it flashes an error message saying "Internal problem. Please try again!" and redirects to the "signup" page.
        - If the user details provided in the request form are not valid, it flashes an error message saying "Invalid username, email or password. Please try again!" and redirects to the "signup" page.
        - If the user details provided in the request form are valid, it redirects to the "auth_signup" page passing the username, email, and password as parameters.
    """
    if request.method != "POST":
        flash("Internal problem. Please try again!")
        return redirect(url_for("main.signup"))
    
    auth_user = {"name": request.form["username"], "email" : request.form["email"], "pass" : request.form["password"]}
    if not auth_users.verify_signup(auth_user):
        flash("Invalid username, email or password. Please try again!")
        return redirect(url_for("main.signup"))
    return redirect(url_for("main.auth_signup", user = request.form["username"], email = request.form["email"], password = request.form["password"], ))

@main.route("/signup/user/auth_signup")
def auth_signup():
    """
    Route for authenticating and signing up a user.
    Args:
        None
    Returns:
        None
    """
    user_auth = {
        "username": request.args.get("user"),
        "email": request.args.get("email"),
        "password": request.args.get("password"),
    }
    user = user_model.User(user_auth["email"])
    if user.signup(user_auth):
        session.pop('_flashes', None)
        session["user"] = user.to_json()
        return redirect(url_for("main.dashboard"))
    
    flash("Invalid username. Please try again!")
    return redirect(url_for("main.signup"))

#________________________  User's Dashboard  ________________________#
@main.route("/dashboard")
@login_is_required
def dashboard():
    """
    Renders the dashboard page for the authenticated user.
    Parameters:
        None
    Returns:
        The rendered dashboard.html template with the user's name and email.
    Raises:
        Redirect: If the user is not logged in, redirects to the login page.
    """
    if "user" not in session:
        return redirect("/login")
    user = user_model.from_json(session["user"])
    return render_template("dashboard.html", name = user.name, email = user.email)

@main.route("/dashboard/chat/")
@login_is_required
def chat_assistant():
    """
    Route decorator for the "/dashboard/chat/" endpoint.
    Requires the user to be logged in.
    
    Parameters:
        None
        
    Returns:
        Flask redirect object or Flask render_template object
            - If the user is not in the session, redirects to "/login"
            - Otherwise, renders the "assistantchat.html" template
    """
    if "user" not in session:
        return redirect("/login")
    return render_template("assistantchat.html")

#________________________ User's Profile Page ________________________#
# User's Profile Page
@main.route("/profile")
@login_is_required
def profile():
    """
    Renders the profile page for the authenticated user.
    This function is decorated with `@app.route("/profile")` to specify the URL route for accessing the profile page.
    The `@login_is_required` decorator ensures that only authenticated users can access this page.
    Returns:
        A rendered HTML template of the profile page with the user's session information.
        If the user is not logged in, they will be redirected to the login page.
    """
    if "user" not in session:
        return redirect("/login")
    return render_template("profile.html", user=session["user"])

#Change user data
@main.route("/profile/change_data", methods=["POST"])
@login_is_required
def change_data():
    """
    A function to handle the "/profile/change_data" route with the "POST" method.
    It requires the user to be logged in.
    ---
    Returns:
        - If the user is not logged in, it redirects to the "/login" page.
        - If the request method is not "POST", it flashes an error message and redirects to the "profile" page.
        - If the user data is successfully updated, it updates the session, flashes a success message, and redirects to the "profile" page.
        - If the user data update fails, it flashes an error message and redirects to the "profile" page.
    """
    if "user" not in session:
        return redirect("/login")
    if request.method != "POST":
        flash("Internal problem. Please try again!")
        return redirect(url_for("main.profile"))
    user = user_model.from_json(session["user"])
    print(user.assistants)
    data = {
        "name": request.form["name"],
        "email": request.form["email"]
    }
    if not auth_users.verify_update(data):
        flash("Invalid username or character. Please try again!")
        return redirect(url_for("main.profile"))
    if user.update_user(data):
        session.pop('_flashes', None)
        session["user"] = user.to_json()
        flash("User data updated successfully!")
    else:
        flash("Failed to update user data.")
    return redirect(url_for("main.profile"))

#Change user password
@main.route("/profile/change_password", methods=["POST"])
@login_is_required
def change_password():
    """
    This function is used to handle the change password functionality for the user's profile.
        
    Parameters:
        - No parameters
        
    Returns:
        - No return value
        
    Description:
        - This function is decorated with the `@app.route` decorator to map the URL "/profile/change_password" to this function.
        - It is also decorated with the `@login_is_required` decorator to ensure that the user is logged in before accessing this functionality.
        - If the "user" key is not present in the session, the user is redirected to the login page.
        - If the HTTP method is not "POST", a flash message is displayed and the user is redirected to the profile page.
        - The user object is extracted from the session and stored in the `user` variable.
        - The `data` dictionary is created with the values of "old_password" and "new_password" extracted from the request form.
        - If the entered password does not match the user's current password, a flash message is displayed and the user is redirected to the profile page.
        - If the password is successfully updated, a flash message is displayed and the user is redirected to the profile page.
        - Otherwise, a flash message indicating the failure to update the password is displayed.
        - No value is returned.
    """
    if "user" not in session:
        return redirect("/login")
    if request.method != "POST":
        flash("Internal problem. Please try again!")
        return redirect(url_for("main.profile"))
    user = user_model.from_json(session["user"])
    data = {
        "old_password": request.form["old_password"],
        "new_password": request.form["new_password"]
    }
    if not auth_users.verify_password(data):
        flash("Invalid password. Please try again!")
        return redirect(url_for("main.profile"))
    if user.update_password(data):
        session.pop('_flashes', None)
        flash("Password updated successfully!")
    else:
        flash("Failed to update password.")
    return redirect(url_for("main.profile"))

#__________________________ Assistants Page __________________________#
#Assistant page
@main.route("/assistants")
@login_is_required
def assistants():
    """
    Renders the assistants page for the authenticated user.
    This function is decorated with `@app.route("/assistants")` to specify the URL route for accessing the assistants page.
    The `@login_is_required` decorator ensures that only authenticated users can access this page.
    Returns:
        A rendered HTML template of the assistants page.
        If the user is not logged in, they will be redirected to the login page.
    """
    if "user" not in session:
        return redirect("/login")
    print(session["user"])
    user = user_model.from_json(session["user"])
    session["user"] = user.to_json()
    return render_template("assistants.html", user = session["user"])

#Create new assistant
@main.route("/assistants/new")
@login_is_required
def new_assistant():
    """
    Renders the new assistant page for the authenticated user.
    This function is decorated with `@app.route("/assistants/new")` to specify the URL route for accessing the new assistant page.
    The `@login_is_required` decorator ensures that only authenticated users can access this page.
    Returns:
        A rendered HTML template of the new assistant page.
        If the user is not logged in, they will be redirected to the login page.
    """
    if "user" not in session:
        return redirect("/login")
    return render_template("create_new_assistant.html")

@main.route("/assistants/new/auth")
@login_is_required
def new_assistant_auth():
    """
    Renders the new assistant page for the authenticated user.
    This function is decorated with `@app.route("/assistants/new/auth")` to specify the URL route for accessing the new assistant page.
    The `@login_is_required` decorator ensures that only authenticated users can access this page.
    Returns:
        A rendered HTML template of the new assistant page.
        If the user is not logged in, they will be redirected to the login page.
    """
    if "user" not in session:
        return redirect("/login")
    return render_template("create_new_assistant_auth.html")

@main.route("/assistants/new/create")
@login_is_required
def new_assistant_create():
    """
    Renders the new assistant page for the authenticated user.
    This function is decorated with `@app.route("/assistants/new/create")` to specify the URL route for accessing the new assistant page.
    The `@login_is_required` decorator ensures that only authenticated users can access this page.
    Returns:
        A rendered HTML template of the new assistant page.
        If the user is not logged in, they will be redirected to the login page.
    """
    if "user" not in session:
        return redirect("/login")
    return render_template("create_new_assistant_create.html")

#Chat with the assistant 
@main.route("/assistants/chat/<assistant_id>")
def chat(assistant_id):
    """
    Route decorator for the chat endpoint.
    Parameters:
        assistant_id (str): The ID of the assistant.
    Returns:
        redirect: Redirects to the login page if the user is not in session.
        render_template: Renders the assistant chat template with the assistant ID.
    """
    if "user" not in session:
        return redirect("/login")
    return render_template("assistantchat.html", assistant_id = assistant_id)
