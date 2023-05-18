from flask import Flask, render_template, request
from robotics import Robot

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    scientist_info = None
    if request.method == 'POST':
        scientist = request.form.get('scientist')
        scientist_robo = Robot("Quandrinaut", [scientist], summary_prediction=False, summary_prediction_model="en_core_web_sm",headless=True)
        scientist_data = scientist_robo.get_scientists_summary()
        scientist_robo.close_browser()
        if scientist_data:
            scientist_info = scientist_data[0]
    return render_template('index.html', scientist_info=scientist_info)

if __name__ == "__main__":
    app.run(debug=True)
