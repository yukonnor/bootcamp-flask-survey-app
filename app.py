from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import surveys

# Flask setup 
app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# List to store survey responses
responses = []


@app.route("/")
def show_template_select_form():
    """The root page should show the user the title of the survey they
       are taking along with a button that takes them to the survey."""

    survey = surveys.surveys["satisfaction"]

    return render_template("root.html", survey_title=survey.title, survey_instructions=survey.instructions)