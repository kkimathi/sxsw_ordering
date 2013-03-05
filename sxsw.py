from flask import Flask, render_template, request
import subtledata

SD = subtledata.SubtleData('QVorMkxG', testing=True)
DEV_GARAGE = SD.Locations.get(448, include_menu=True)

APP = Flask(__name__)
APP.debug = True

@APP.route('/', methods=['GET'])
def show_homepage():

    items = DEV_GARAGE.menu.get_category(category_name='Bottle Beer').items

    return render_template("menu.jinja2", items=items[0:4])

@APP.route('/order', methods=['GET', 'POST'])
def take_order():

    if request.method == 'POST':
        seat_number = request.form['seat_number']
        ordered_item = request.form['ordered_item']

        new_ticket = DEV_GARAGE.tables[0].open_ticket(1657, 1977, custom_ticket_name='Seat ' + str(seat_number))

        new_ticket.add_item_to_order(ordered_item, 1)
        new_ticket.submit_order()

    else:
        ordered_item = None

    return render_template('email.jinja2', item_id=ordered_item)