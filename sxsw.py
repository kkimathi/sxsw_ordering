"""
Subtledata SXSW Demo Application
To Use:

Set the following variables to valid Subtledata IDs:

--API_KEY
--LOCATION_ID
--USER_ID
--DEVICE_ID

LICENSE (The MIT License)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

from flask import Flask, render_template, request
import subtledata

#Initialize Flask
APP = Flask(__name__)

#Turn on debugging to make life easier
APP.debug = True

#Set our API key to our Subtledata Web API
API_KEY = '@@@@@@@'

#Set our location ID
LOCATION_ID = 12345

#We will need a valid user ID and device ID to submit orders
USER_ID = 12345
DEVICE_ID = 12345

#Initialize the Subtledata Library with our API Key
SD = subtledata.SubtleData(API_KEY)

#Fetch our location since we will need it for all calls
DEV_GARAGE = SD.Locations.get(LOCATION_ID, include_menu=True)

#Main Route to show the menu
@APP.route('/', methods=['GET'])
def show_homepage():
    """
    Show homepage will present the menu to our user

    :return: Template(Menu.jinja2)
    """

    #Get the items we want to display
    items = DEV_GARAGE.menu.get_category(category_name='Bottle Beer').items

    #Display our menu and associated items
    return render_template("menu.jinja2", items=items[0:4])

#POST route to accept and create the order
@APP.route('/order', methods=['POST'])
def take_order():
    """
    Receive our order and process it

    :return: Template(confirmation.jinja2)
    """

    #Set our seat number from the form
    seat_number = request.form['seat_number']

    #Set our ordered item from the form
    ordered_item = request.form['ordered_item']

    #Open a new ticket using our user and device ID
    #Set its ticket name to a custom value so that we know which seat to go to
    new_ticket = DEV_GARAGE.tables[0].open_ticket(USER_ID,
                        DEVICE_ID,
                        custom_ticket_name='Seat ' + str(seat_number))

    #Add (stage) one of our items to our order
    new_ticket.add_item_to_order(ordered_item, 1)

    #Submit our order for processing
    new_ticket.submit_order()

    #Return the confirmation
    return render_template('confirmation.jinja2', item_id=ordered_item)

#Start Flask
if __name__ == '__main__':
    APP.run('0.0.0.0')