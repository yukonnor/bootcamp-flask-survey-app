from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

# Flask setup 
app = Flask(__name__)
app.config['SECRET_KEY'] = "TO_BE_A_SECRET_KEY"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
debug = DebugToolbarExtension(app)

# Define current survey we're working with
survey = surveys.surveys["satisfaction"]

# List to store survey responses
responses = []


@app.route("/")
def show_start_survey_page():
    """The root page should show the user the title of the survey they
       are taking along with a button that takes them to the survey."""

    return render_template("root.html", survey_title=survey.title, survey_instructions=survey.instructions)


@app.route("/init-session", methods=["POST"])
def init_session():
    """Initialize the user's session, which we'll use to store their survey progess and answers."""

    # create an empty list where user's responses will be recorded
    session['responses'] = []

    # redirect to the beginning of the survey
    return redirect(f"/questions/0")

@app.route("/questions/<int:question_id>")
def show_survey_question_page(question_id): 
    """Show the survey question page based on question id provided"""

    # double check which question should be answerd next based on the responses we have
    next_question_id = len(responses)   

    # if user is on the correct question page, render the page. Else redirect them to correct page.
    if question_id == next_question_id:
        question = survey.questions[question_id]
        return render_template("survey-question.html", survey_title=survey.title, question_id=question_id, question_text=question.question, choices=question.choices)
    else:
        flash('Please complete survey questions in order.', 'warning')
        return redirect(f"/questions/{next_question_id}")

@app.route("/answer", methods=["POST"])
def process_answer():
    """Show the survey question page based on question id provided"""

    # get data from query string
    answer = request.form.get("answer")
    last_question_id = int(request.form.get("question-id"))

    # and answer to responses list
    responses.append(answer)

    # check to see what next question should be
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