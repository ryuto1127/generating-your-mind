from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import random
from openai import OpenAI
import os
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler # type: ignore

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__, static_folder='static')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string="InstrumentationKey=c316a918-2301-4373-ba79-204e44f3d81a;IngestionEndpoint=https://japaneast-1.in.applicationinsights.azure.com/;LiveEndpoint=https://japaneast.livediagnostics.monitor.azure.com/;ApplicationId=b046141a-9771-4de3-8ed1-2e1842bec1b0"))

questions = [
    "What is your favorite color?",
    "Do you prefer mountains or the sea?",
    "What is your favorite time of day?",
    "What is your favorite animal?",
    "What kind of weather do you enjoy the most?",
    "What is your favorite season?",
    "Do you prefer coffee or tea?",
    "What is your favorite book?",
    "What is your favorite movie?",
    "What is your favorite genre of music?",
    "Do you prefer to work in the morning or at night?",
    "What is your favorite hobby?",
    "Do you like cats or dogs more?",
    "What is your favorite food?",
    "Do you prefer sweet or savory snacks?",
    "What is your favorite type of cuisine?",
    "Do you prefer to travel by plane, train, or car?",
    "What is your favorite sport?",
    "Do you like to read fiction or non-fiction?",
    "What is your favorite flower?",
    "What is your favorite type of art?",
    "Do you prefer hot or cold weather?",
    "Do you prefer city life or country life?",
    "What is your favorite holiday?",
    "Do you like the beach or the mountains more?",
    "What is your favorite drink?",
    "What is your favorite fruit?",
    "Do you prefer sunrise or sunset?",
    "What is your favorite type of clothing?",
    "Do you like rainy days or sunny days more?",
    "What is your favorite insect?",
]

@app.route("/", methods=["GET"])
def index():
    selected_questions = random.sample(questions, 3)
    logger.info(f"Selected questions: {selected_questions}")
    return render_template("index.html", questions=selected_questions)

@app.route("/submit", methods=["POST"])
def submit():
    try:
        user_answers = request.form.getlist("answer")
        logger.info(f"User answers: {user_answers}")
        prompt = "Create an abstract image based on these answers: " + ", ".join(user_answers)

        response = client.images.generate(
            model="dall-e-3",
            style="vivid",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        image_url = response.data[0].url
        return render_template("result.html", image_url=image_url)

    except Exception as e:
        logger.error(f"Exception on /submit: {e}")
        return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True)
