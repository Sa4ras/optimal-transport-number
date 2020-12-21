from flask import Flask, redirect, url_for, request, session, render_template, flash
from forms.forms import UserInputForm
from helper_class import MainSolver

app = Flask(__name__)
app.secret_key = 'development-key'

@app.route("/", methods = ['GET'])
def welcome():
    return render_template('welcome.html')

@app.route('/calculus', methods=["GET", "POST"])
def calc():
    form = UserInputForm()
    if request.method == 'POST' and form.validate() and form.validate_on_submit():
        user_input = request.form.to_dict()
        result = MainSolver(float(user_input['route_len']),
                            int(user_input['number_of_vehicles']),
                            int(user_input['passenger_capacity']),
                            str(user_input['route_time']),
                            str(user_input['first_guard']),
                            int(user_input['guard_duration']),
                            int(user_input['number_of_guards']),
                            int(user_input['area_population']),
                            float(user_input['area_square'])).optimization_task()
        print('result:', result)

    return render_template('calc.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)

