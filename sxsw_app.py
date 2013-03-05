from flask import Flask, render_template, request
import time

APP = Flask(__name__)

from subtledata import SDobjects

SD = SDobjects(api_key='12345')

APP.debug = True

DEV_GARAGE = SD.location(500)

@APP.route('/', methods=['GET'])
def show_homepage():
    return render_template("menu.jinja2", location=DEV_GARAGE)

@APP.route('/order', methods=['POST'])
def take_order():
    new_ticket = DEV_GARAGE.open_ticket(delivery=True)

    for form_input in request.form:

        if 'qty' in form_input[0]:
            item_id = form_input[0].split('-')
            item_qty = int(form_input[1])
            new_ticket.add_item(item_id=item_id, quantity=item_qty)
        elif 'seat_number' in form_input[0]:
            seat_number = int(form_input[1])
            new_ticket.delivery_address = 'Seat #' + str(seat_number)

    success = new_ticket.submit()

    if success['status'] == 'success':
        time.sleep(2)
        new_ticket.close_and_pay()
        return render_template('receipt.jinja2', location=DEV_GARAGE, success=True)
    else:
        return render_template('receipt.jinja2', location=DEV_GARAGE, success=False)

@APP.route('/subscribe', methods=['POST'])
def subscribe_email():
    new_email = request.form.get('email', None)

    with open("emails.txt", "a") as myfile:
        myfile.write(new_email)

    return render_template('thank_you.jinja2', location=DEV_GARAGE)

if __name__ == '__main__':
    APP.run()
