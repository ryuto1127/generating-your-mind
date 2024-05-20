from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import random
import openai
import os
import logging

app = Flask(__name__, static_folder='static')

logging.basicConfig(level=logging.DEBUG)

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
    "Do you prefer hot or cold weather?",
    "What is your favorite type of art?",
    "Do you prefer city life or country life?",
    "What is your favorite holiday?",
    "Do you like the beach or the mountains more?",
    "What is your favorite drink?",
    "What is your favorite fruit?",
    "Do you prefer sunrise or sunset?",
    "What is your favorite type of clothing?",
    "Do you like rainy days or sunny days more?",
    "What is your favorite insect?",
    "What is your favorite kind of tree?",
    "Do you prefer indoor or outdoor activities?",
    "What is your favorite TV show?",
    "What is your favorite way to relax?",
    "Do you prefer to be alone or with friends?",
    "What is your favorite type of exercise?",
    "Do you like to cook or eat out more?",
    "What is your favorite dessert?",
    "What is your favorite childhood memory?",
    "Do you prefer to give or receive gifts?",
    "What is your favorite board game?",
    "Do you like to plan things out or be spontaneous?",
    "What is your favorite subject in school?",
    "Do you prefer to stay at home or go out?",
    "What is your favorite ice cream flavor?",
    "Do you like to take photos or be in photos?",
    "What is your favorite animal sound?",
    "Do you prefer books or movies?",
    "What is your favorite time of year?",
    "Do you like to draw or paint?",
    "What is your favorite kind of pet?",
    "Do you prefer to work alone or in a team?",
    "What is your favorite type of plant?",
    "Do you like to write stories or read stories?",
    "What is your favorite musical instrument?",
    "Do you prefer hot drinks or cold drinks?",
    "What is your favorite time of day to exercise?",
    "Do you like to travel or stay close to home?",
    "What is your favorite childhood toy?",
    "Do you prefer to watch sports or play sports?",
    "What is your favorite kind of soup?",
    "Do you like to dance or watch others dance?",
    "What is your favorite way to spend a weekend?",
    "Do you prefer to work on a computer or on paper?",
    "What is your favorite thing about nature?",
    "Do you like to build things or take things apart?",
    "What is your favorite kind of bread?",
    "Do you prefer to listen to music or make music?",
    "What is your favorite type of weather for a walk?",
    "Do you like to read magazines or newspapers?",
    "What is your favorite way to stay active?",
    "Do you prefer to sing or play an instrument?",
    "What is your favorite holiday tradition?",
    "Do you like to swim in a pool or in the ocean?",
    "What is your favorite kind of pizza?",
    "Do you prefer to watch TV or listen to the radio?",
    "What is your favorite thing to do on a rainy day?",
    "Do you like to collect things or get rid of things?",
    "What is your favorite type of movie snack?",
    "Do you prefer to stay up late or wake up early?",
    "What is your favorite type of sandwich?",
    "Do you like to garden or visit gardens?",
    "What is your favorite kind of cake?",
    "Do you prefer to read ebooks or physical books?",
    "What is your favorite place to visit?",
    "Do you like to do puzzles or play games?",
    "What is your favorite type of bird?",
    "Do you prefer to watch a movie or a TV series?",
    "What is your favorite way to unwind?",
    "Do you like to explore new places or revisit favorites?",
    "What is your favorite type of breakfast food?",
    "Do you prefer to go to a concert or a play?",
    "What is your favorite kind of candy?",
    "Do you like to volunteer or donate to causes?",
    "What is your favorite way to spend time with family?",
    "Do you prefer to shop online or in stores?",
    "What is your favorite type of juice?",
    "Do you like to play sports or watch sports?",
    "What is your favorite thing to do on a holiday?",
    "Do you prefer to work from home or in an office?",
    "What is your favorite thing about your hometown?",
    "Do you like to cook new recipes or stick to favorites?",
    "What is your favorite outdoor activity?",
    "Do you prefer to write by hand or type?",
    "What is your favorite type of flower to grow?"
]

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    try:
        selected_questions = random.sample(questions, 3)
        app.logger.info("Selected questions: %s", selected_questions)
        return render_template('index.html', questions=selected_questions)
    except Exception as e:
        app.logger.error("Error in home route: %s", e)
        return f"An error occurred: {e}", 500

@app.route('/submit', methods=['POST'])
def submit():
    try:
        answers = request.form.getlist('answer')
        app.logger.info("User answers: %s", answers)
        
        prompt = "Create an abstract image based on these answers: " + ", ".join(answers)
        app.logger.info("Generated prompt: %s", prompt)
        
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"  # Reduce image size to mitigate timeout issues
        )
        image_url = response['data'][0]['url']
        app.logger.info("Generated image URL: %s", image_url)
        
        return render_template('result.html', image_url=image_url)
    except openai.error.Timeout as e:
        app.logger.error("OpenAI API request timed out: %s", e)
        return f"OpenAI API request timed out. Please try again.", 504
    except Exception as e:
        app.logger.error("Error in submit route: %s", e)
        return f"An error occurred: {e}", 500

# Route for favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

if __name__ == "__main__":
    app.run(debug=True)