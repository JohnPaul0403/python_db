from functools import wraps
from . import main, abort, render_template, session, redirect, user_model, assistant_model

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

#________________________ About page  ________________________#
@main.route("/about")
def about():
    return render_template("about.html")

#________________________ Pricing page  ________________________#
@main.route("/pricing")
def pricing():
    return render_template("pricing.html")

#________________________ Blogs page  ________________________#
@main.route("/blogs")
def blogs():
    return render_template("blogs.html")

#________________________ Login page  ________________________#
@main.route("/login")
def login():
    return render_template("login.html")

#________________________ Signup page  ________________________#
@main.route("/signup")
def signup():
    return render_template("signup.html")

#________________________ Set Token page  ________________________#
@main.route("/signup/set-token")
@login_is_required 
def set_token_page():
    if "user" not in session:
        return redirect("/login")
    
    return render_template("set_token.html")

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
    assistant = assistant_model.Assistant()
    dict_assistant = assistant.read_assistant_by_id(assistant_id)
    session["assistant"] = {"assistant_id" : assistant_id, "name" : dict_assistant["name"]}

    return render_template("assistantchat.html", assistant_id = assistant_id)
