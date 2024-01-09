from functools import wraps
from . import main, redirect, request, url_for, flash, abort, session, requests,\
    user_model, assistant_model, auth_users, os, api_crud,\
        GOOGLE_CLIENT_ID, flow, app_id_token, app_cachecontrol, my_requests, secure_filename, UPLOAD_FOLDER

def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print("user" not in session)
        if "google_id" in session or "user" in session:
            return function()
        
        return abort(401)  # Authorization required

    return wrapper

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
        return redirect(url_for("main.login"))
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
    
    auth_user = {"pay_name": request.form["name"], "last name": request.form["surname"], "name": request.form["username"], "email" : request.form["email"], "pass" : request.form["password"]}
    if not auth_users.verify_signup(auth_user):
        flash("Invalid username, email or password. Please try again!")
        return redirect(url_for("main.signup"))
    return redirect(url_for("main.auth_signup", name = request.form["name"], surname = request.form["surname"], user = request.form["username"], email = request.form["email"], password = request.form["password"], ))

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
        "pay_name": request.args.get("name"),
        "last name": request.args.get("surname"),
        "username": request.args.get("user"),
        "email": request.args.get("email"),
        "password": request.args.get("password"),
    }
    user = user_model.User(user_auth["email"])
    resp = api_crud.create_customer(data=user_auth)
    if resp.is_error():
        print(resp.errors)
        flash("Internal error. Please try again!")
        return redirect("/login")
    if user.signup(user_auth):
        session.pop('_flashes', None)
        session["user"] = user.to_json()
        return redirect(url_for("main.dashboard"))
    
    flash("Invalid username. Please try again!")
    return redirect(url_for("main.signup"))

#________________________ User's Profile Page ________________________#
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
@main.route("/assistants/new/auth", methods = ["POST"])
@login_is_required
def new_assistant_auth():
    """
    Authenticates a new assistant.
    Returns:
        The URL to redirect to if the authentication is successful.
    """
    files: list
    if "user" not in session:
        return redirect("/login")
    user = user_model.from_json(session["user"])
    if request.method != "POST":
        flash("Internal problem. Please try again!")
        return redirect(url_for("main.new_assistant"))
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    print(file)
    if file and auth_users.verify_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        files = [filename]
    data = {
        "user_id" : str(user.id),
        "name" : request.form["name"],
        "gpt-model" : request.form["gpt-model"],
        "instructions" : request.form["instructions"],
        "files" : files
    }

    if not auth_users.verify_str(data):
        flash("Invalid data. Please try again!")
        return redirect(url_for("main.new_assistant"))

    return redirect(url_for("main.new_assistant_create", data = data))

@main.route("/assistants/new/create")
@login_is_required
def new_assistant_create():
    """
    Creates a new assistant.
    Returns:
        The URL to redirect to if the creation is successful.
    """
    if "user" not in session:
        return redirect("/login")
    data = eval(request.args.get("data"))
    assistant = assistant_model.Assistant()
    assistant.create_assistant(data)
    return redirect(f"/assistants/chat/{data['assistant_id']}")

@main.route("/assistants/delete")
@login_is_required
def delete_assistant():
    """
    Deletes an assistant.
    Returns:
        The URL to redirect to if the deletion is successful.
    """
    if "user" not in session:
        return redirect("/login")
    user = user_model.from_json(session["user"])
    assistant_id = request.args.get("assistant_id")
    for assistant in user.assistants:
        if assistant.assistant_id == assistant_id:
            assistant.delete_assistant()
            break
    return redirect("/assistants")