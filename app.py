from flask import Flask, render_template, request, redirect, url_for
import sql_app

url = 'https://www.istu.edu/schedule/'
app = Flask(__name__)


@app.route('/')
def itu():
    sql_app.create()
    print("itu")
    week = sql_app.get_filtered_data()
    maxi = sql_app.maxi(week)
    return render_template('itu.html', week=week, maxi=maxi)

@app.route('/update', methods=['POST', 'Ge'])
def update():
    sql_app.create()
    print("update")
    sql_app.updata('https://www.istu.edu/schedule/')
    week = sql_app.get_filtered_data()
    maxi = sql_app.maxi(week)
    return render_template('itu.html', week=week, maxi=maxi)
@app.route('/filt', methods=['POST'])
def filter():
    print('filter')
    grop = request.form['group'].split(", ")
    if grop[0] != '':
        week = sql_app.get_filtered_data(group=grop)
        print(grop)
    else:
        year = request.form.getlist('year')
        learn = request.form.getlist('learn')
        institute = request.form.getlist('institute')
        week = sql_app.get_filtered_data(institute=institute,education_level=learn, year=year)
    maxi = sql_app.maxi(week)
    if not maxi:
        maxi = 1
    return render_template("itu.html", week=week, maxi=maxi)
if __name__ == '__main__':
    app.run(debug=True)