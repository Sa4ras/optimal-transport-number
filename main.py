from flask import Flask, request, render_template, flash
from forms.forms import UserInputForm
from helper_class import MainSolver

import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

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

        depart_hours = result[0]
        optimal_transport_number = result[1]
        departured_quantity = result[3]

        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.set_xlabel("Година відправлення")
        axis.set_ylabel("Кількість т-з")
        axis.bar(depart_hours, departured_quantity)
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

        if result[2]== 0 and result[4] == True:
            flash(f"""Для Вас має сенс покращити обслуговування маршруту!\
                      Мінімальна потрібна кількість т-з: {optimal_transport_number}\
                      Рекомендовані початки рейсів та кількість відбутих т-з у цей час:""", 'success')
            return render_template('plot.html', image=pngImageB64String)
        else:
            flash(f"""Для Вас є сенс збільшити автопарк!\
                      Мінімальна потрібна кількість т-з: {optimal_transport_number}\
                      Рекомендовані початки рейсів та кількість відбутих т-з у цей час:""", 'danger')
            return render_template('plot.html', image=pngImageB64String)
    return render_template('calc.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)

