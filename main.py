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
    if request.method == 'POST' and form.validate():
        result = MainSolver(form.route_len,
                            form.number_of_vehicles,
                            form.passenger_capacity,
                            form.route_time,
                            form.first_guard,
                            form.guard_duration,
                            form.number_of_guards,
                            form.area_population,
                            form.area_square).optimization_task()
        print(result)
    return render_template('calc.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)

