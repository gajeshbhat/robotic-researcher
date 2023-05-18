from flask import Flask, render_template, request
from lib.robotics import Robot

app = Flask(__name__)

def get_scientist_info(scientist, summary_prediction=False, model="en_core_web_sm"):
    """
    Returns information about the scientist.
    """
    robot = Robot("Quandrinaut", [scientist], summary_prediction=summary_prediction, summary_prediction_model=model, headless=True)
    data = robot.get_scientists_summary()
    robot.close_browser()
    return data[0] if data else None

@app.route('/', methods=['GET', 'POST'])
def home():
    scientist_info = None
    if request.method == 'POST':
        scientist = request.form.get('scientist')
        summary_prediction = bool(request.form.get('summary_prediction'))  # Assuming this is a checkbox
        model = request.form.get('model')  # Assuming this is a dropdown or similar

        try:
            scientist_info = get_scientist_info(scientist, summary_prediction, model)
        except Exception as e:
            # Log the error message to console or to a file
            print(f"An error occurred: {e}")
            scientist_info = {"error": "An error occurred while processing your request. Please try again."}

    return render_template('index.html', scientist_info=scientist_info)

if __name__ == "__main__":
    app.run(debug=True)
