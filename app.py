from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    coffee = ["☕️","☕️☕️","☕️☕️☕️","☕️☕️☕️☕️","☕️☕️☕️☕️☕️"]
    wifi_strength = ["❌", "📶", "📶📶", "📶📶📶", "📶📶📶📶", "📶📶📶📶📶"]
    power_outlet_rating = ["❌", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"]

    cafe = StringField('Cafe name', validators=[DataRequired()])
    address_url = StringField(label="Cafe Location on Gmaps (URL)", validators=[DataRequired(), URL()])
    open_time = StringField(label="Opening Time (e.g. 8AM)", validators=[DataRequired()])
    closing_time = StringField(label="Closing Time e.g. 8pm", validators=[DataRequired()])
    coffee_rating = SelectField(label="Coffee Rating", choices=coffee, validators=[DataRequired()])
    wifi_rating = SelectField(label="WiFi Strength Rating", choices=wifi_strength, validators=[DataRequired()])
    power_outlet = SelectField(label="Power Socket Availability", choices=power_outlet_rating, validators=[DataRequired()])

    submit = SubmitField('Submit')

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        responses = [form.cafe.data, form.address_url.data, form.open_time.data, form.closing_time.data, form.coffee_rating.data, form.wifi_rating.data, form.power_outlet.data]
        f = open("cafe-data.csv", "a")
        writer = csv.writer(f)
        writer.writerow(responses)
        f.close()
        return redirect(url_for('cafes'))

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
