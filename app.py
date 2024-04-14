from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
#from openai import OpenAI
import time
import os

#0.28.7

#instance of flask
app = Flask(__name__)

CORS(app)  #cross platform connection

#OpenAI API key
#client = OpenAI(api_key = "")

openai.api_key = ""


#route for the home pag
@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/engage')
def engage():
     return render_template('stakeholder.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    user_input = data['text']

    response = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-1106:personal:persona-v4:95AHfAM4",
            messages=[{"role": "user", "content": user_input}]
        )

    return jsonify({"response": response.choices[0].message})

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    persona = data['persona']
    question = data['question']
    
    # Logic to return different responses based on persona
    responses = {
        "student": f"As a student, you might find this explanation helpful: [details on {question}]",
        "professional": f"To be concise: [short answer about {question}]",
        "curious novice": f"Here’s a simple explanation: [simple details about {question}]",
        "expert": f"Considering your expertise, here's a deep dive into {question}.",
        "casual learner": f"Hey! Here’s a fun fact about {question}."
    }

    # Default response if persona not recognized
    response = responses.get(persona.lower(), "Sorry, I didn't recognize that persona. Please try again.")
    
    return jsonify({"response": response})

#log error   
@app.errorhandler(Exception)
def handle_error(e):
    return str(e), 500

# Check if the executed script is the main program and run the Flask application.
# By default, the Flask server runs on localhost:5000.
if __name__ == '__main__':
    app.run(debug=True)





###############ChatAssistant##########################
    

    
# @app.route('/assistant', methods=['POST'])
# def create_thread():
#     data = request.get_json()
#     user_message = data['text']
#     messages = ''
#     response = ''
    # try:

    #     run = client.beta.threads.runs.create(
    #     thread_id="thread_WCQwmtN0L5hEEVFlPB3RidyX",
    #     assistant_id="asst_kOLNquu2BqbGew1CYPc4PSjT",
    #     instructions=user_input
    #     )
                
    #     while run.status in ['queued', 'in_progress', 'cancelling']:
    #         time.sleep(1) # Wait for 1 second
    #         run = client.beta.threads.runs.retrieve(
    #             thread_id="thread_WCQwmtN0L5hEEVFlPB3RidyX",
    #             run_id=run.id
    #         )
    #     if run.status == 'completed': 
    #         messages = client.beta.threads.messages.list(
    #             thread_id="thread_WCQwmtN0L5hEEVFlPB3RidyX"
    #         )
    #     else:
    #         print(run.status)
    #     # Assuming the response contains the text output in a specific format
    #     for message in messages.data:
    #         for content in message.content:
    #             if content.type == 'text' and content.text and content.text.value:
    #                 text_output = content.text.value
    #     print(text_output)
    #     return jsonify({"response": text_output})
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     return e


    #thread = client.beta.threads.create()

#     try:
#         # # Add user message to the thread
#         # message = client.beta.threads.messages.create(
#         #     thread_id=thread.id,
#         #     role="user",
#         #     content=user_message
#         # )
#         # print("### message inside send_message is:", message)
#         return create_run("thread_WCQwmtN0L5hEEVFlPB3RidyX", user_message)

#     except Exception as e:
#         print(f"An error occurred while sending the message: {e}")
#         return None
    
# def create_run(thread_ID, user_message):
#     try:
#         # Run assistant
#         run = client.beta.threads.runs.create(
#             thread_id="thread_WCQwmtN0L5hEEVFlPB3RidyX",
#             assistant_id="asst_kOLNquu2BqbGew1CYPc4PSjT"
#         )
#         print("### run from create_run is:", run)
#         return display_assistant_response(thread_ID,run.id,user_message)
        
#     except Exception as e:
#         print(f"An error occurred while sending the message: {e}")
#         return None
    
# def display_assistant_response(thread_ID, run_id,user_message):
#     try:
#         # Display assistant response
#         run = client.beta.threads.runs.retrieve(
#         thread_id=thread_ID,
#         run_id=run_id
#         )
#         count = 0
#         while(run.status == "queued" or run.status == "in_progress" and count < 5):
#             time.sleep(5)
#             run = client.beta.threads.runs.retrieve(
#                 thread_id=thread_ID,
#                 run_id=run_id
#             )
#             count = count + 1        

#         # Retrieve messages from thread after run complete
#         messages = client.beta.threads.messages.list(
#             thread_id=thread_ID
#         )

#         print(f"---------------------------------------------")
#         for message in messages.data:
#             for content in message.content:
#                 if content.type == 'text' and content.text and content.text.value:
#                     value = content.text.value
#                     print("### Extracted value:", value)

#                     # Add the extracted value to the conversation history
#                     if value:  # Additional check to ensure value is not null
#                         system_message = {"role": "system", "content": value}
#                     else:
#                         print("Warning: Null value encountered in message content.")
#         return display_gpt_response(value, user_message)

#     except Exception as e:
#         print(f"An error occurred while sending the message: {e}")
#     return None

# def display_gpt_response(value, user_message):
#     try:
#         response = client.chat.completions.create(
#         model="gpt-4",
#         messages=[
#         {"role": "system", "content": value}
#         ]
#         )
#         return jsonify({"response": response.choices[0].message})
#     except Exception as e:
#         print(f"An error occurred while sending the message: {e}")
#         return None