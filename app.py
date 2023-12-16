from flask import Flask, request, render_template, redirect, flash, session
from flask_session import Session
from flask_debugtoolbar import DebugToolbarExtension
import os
import surveys

# Flask setup 
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
Session(app)

# Make the session permanent and set the lifetime to 1 day (in seconds)
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 1 day in seconds

# Define available surveys
all_surveys = surveys.surveys

@app.route("/")
def show_home_page():
    """The root page should show the user a list of surveys they can take"""

    # raise

    # Q: Should I instead only pass in the data that is used on this page? 
    #    survey title and slug. If so, how to associate the two? 
    return render_template("home.html", all_surveys=all_surveys)

@app.route("/start-survey/<slug>")
def show_start_survey_page(slug):
    """The start page should show the user the title of the survey they
       are taking along with a button that takes them to the survey."""
    
    # Get survey title and instructions based on the slug. 
    survey = all_surveys[slug]

    return render_template("start-survey.html", 
                           survey_title=survey.title, 
                           survey_instructions=survey.instructions, 
                           survey_slug=slug)

@app.route("/init-session/<slug>", methods=["POST"])
def init_session(slug):
    """
    This function:
       - Sets which survey is actively being taken
       - Checks to see if user session has provided responses for that survey
       - If so, it directs them to where they should be
       - If not, it initializes the user's response list for the sruvey, which we'll use to store their survey progess and answers.
    """

    # get which survey the user is taking
    survey = all_surveys[slug]
    count_questions = len(survey.questions)

    # set which survey the user is currently taking here
    session['current_survey'] = slug

    # check if responses for that survey already exists. 
    # if there are survey responses for any survey
    if session.get('survey_responses'):

        # if the user has a response list for current survey: 
        if session['survey_responses'].get(slug):

            # if we have answers for all questions, redirect to thanks page
            if len(session['survey_responses'][slug]) == count_questions:
                flash('We already have all of your answers. If this is incorrect, please clear your cookies.', 'warning')
                return redirect(f"/thanks")        
            else:
                # redirect user to question page, which has redirect logic to put them on correct question
                return redirect(f"/questions/0")
        
        # else they need a response list for a new survey
        else:
            session['survey_responses'][slug] = []
            return redirect(f"/questions/0")

    
    # else the user doesn't have a session with survey responses
    else: 

        # create an empty dict where user's survey responses will be recorded
        session['survey_responses'] = {}

        # create an empty list to store this suvey's reponses
        session['survey_responses'][slug] = []

        # redirect to the first question of the survey
        return redirect(f"/questions/0")


@app.route("/questions/<int:question_id>")
def show_survey_question_page(question_id): 
    """Show the survey question page based on question id provided"""

    session_id = session.sid

    # debug:
    print("")
    print(f"Start of Questions view. Session ID: {session_id} | Session Responses: {session['survey_responses']}")
    print("")

    # get which survey the user is working on
    survey_slug = session['current_survey']
    survey = all_surveys[survey_slug]

    # check which question should be answerd next based on the responses we have
    responses = session['survey_responses'][survey_slug]
    next_question_id = len(responses)   

    # debug:
    print("")
    print(f"Viewing Question {question_id}. Session Responses: {session['survey_responses']}")
    print("")
    

    # if user is on the correct question page, render the page. Else redirect them to correct page.
    if question_id == next_question_id:
        question = survey.questions[question_id]
        return render_template("survey-question.html", survey_title=survey.title, question_id=question_id, question_text=question.question, choices=question.choices)
    else:
        flash("Let's continue where you left off!", 'warning')
        return redirect(f"/questions/{next_question_id}")

@app.route("/answer", methods=["POST"])
def process_answer():
    """Show the survey question page based on question id provided"""

    session_id = session.sid

    # get which survey the user is working on
    survey_slug = session['current_survey']
    survey = all_surveys[survey_slug]

    # get data from query string
    answer = request.form.get("answer")
    last_question_id = int(request.form.get("question-id"))

    # and answer to responses list in the session
    current_survey_responses = session['survey_responses'][survey_slug]
    current_survey_responses.append(answer)
    session['survey_responses'][survey_slug] = current_survey_responses
    
    # debug:
    print("")
    print(f"Setting Answer in session. Session ID: {session_id} | Session Responses: {session['survey_responses']}")
    print("")

    # check to see what next question should be
    count_questions = len(survey.questions)
    next_question_id = last_question_id + 1

    # redirect to next question if there is one. else redirect to end survey page
    if next_question_id < count_questions:
        return redirect(f"/questions/{next_question_id}")
        # return redirect(f"/raise")
    else: 
        flash('Thank you!', 'success')
        return redirect(f"/thanks")
    
@app.route("/thanks")
def show_thanks_page():
    """Show the user a thank you message after completing the survey """

    return render_template("thanks.html")

@app.route("/raise")
def show_error():
    """Show the user a thank you message after completing the survey """

    # debug:
    print("")
    print(f"On raise page. Session ID: {session.sid} | Session Responses: {session['survey_responses']}")
    print("")

    raise
    return render_template("thanks.html")