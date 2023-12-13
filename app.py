from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import surveys

# Flask setup 
app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# List to store survey responses
responses = []


@app.route("/")
def show_start_survey_page():
    """The root page should show the user the title of the survey they
       are taking along with a button that takes them to the survey."""

    survey = surveys.surveys["satisfaction"]

    return render_template("root.html", survey_title=survey.title, survey_instructions=survey.instructions)


@app.route("/questions/<int:question_id>")
def show_survey_question_page(question_id): 
    """Show the survey question page based on question id provided"""

    survey = surveys.surveys["satisfaction"]
    question = survey.questions[question_id]

    return render_template("survey-question.html", survey_title=survey.title, question_id=question_id, question_text=question.question, choices=question.choices)

@app.route("/answer", methods=["POST"])
def process_answer():
    """Show the survey question page based on question id provided"""

    # get data from query string
    answer = request.form.get("answer")
    last_question_id = int(request.form.get("question-id"))

    # and answer to responses list
    responses.append(answer)

    # check to see what next question should be
    survey = surveys.surveys["satisfaction"]
    count_questions = len(survey.questions)
    next_question_id = last_question_id + 1

    # redirect to next question if there is one. else redirect to end survey page
    if next_question_id < count_questions:
        return redirect(f"/questions/{next_question_id}")
    else: 
        return redirect(f"/thanks")
    
@app.route("/thanks")
def show_thanks_page():
    """Show the user a thank you message after completing the survey """
    return render_template("thanks.html")