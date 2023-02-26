from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSEKEY = "responses"


@app.route("/")
def root_route():
    """Return home page template"""

    

    return render_template("home.html", satisfaction_survey=satisfaction_survey)

@app.route("/start", methods=["POST"])
def start():
    """Clears responses"""
    session[RESPONSEKEY] = []
    return redirect("/question/0")

@app.route("/question/<int:question_id>")
def show_question(question_id):
    """Shows question that user is on"""
    
    response = session[RESPONSEKEY]

    if (len(response) != question_id):
        flash("Invalid question")
        return redirect(f"/question/{len(response)}")
    
    if (response == None):
        return redirect("/")

    if (len(response) == len(satisfaction_survey.questions)):
        response = RESPONSEKEY
        return redirect("/finish")

    question = satisfaction_survey.questions[question_id]

    return render_template("question.html", question_id=question_id, question=question)

@app.route("/answer", methods=["POST"])
def answer():
    """Append response and move to next question"""

    answer = request.form['answer']

    response = session[RESPONSEKEY]
    response.append(answer)
    session[RESPONSEKEY] = response

    if (len(response) == len(satisfaction_survey.questions)):
        return redirect("/finish")
    else:
        return redirect(f"/question/{len(response)}")

@app.route("/finish")
def finish():
    """Finished survey, show thanks."""

    return render_template("finish.html")