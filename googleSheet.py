import pygsheets
import numpy as np


gc = pygsheets.authorize(service_file='/home/cfarancho/DepartureTimeSensor/cfa-departure-time-cf700c401d86.json')
#gc = pygsheets.authorize(client_secret='/home/cfarancho/DepartureTimeSensor/client_secret_45261759359-tqclvslpu4pkvoe96nfc2462i2aro3gb.apps.googleusercontent.com.json')
# Authorize pygsheets with your .json file
#gc = pygsheets.authorize(client_secret='/home/cfarancho/DepartureTimeSensor/client_secret_45261759359-tqclvslpu4pkvoe96nfc2462i2aro3gb.apps.googleusercontent.com.json')
#gc = pygsheets.authorize(client_secret='Documents/Python/DepartureTimeSensor/client_secret_45261759359-tqclvslpu4pkvoe96nfc2462i2aro3gb.apps.googleusercontent.com.json')

# Open spreadsheet and then worksheet
sh = gc.open('departure_time')
wks = sh.sheet1

# Update a cell with value (just to let him know values is updated ;) )
#wks.update_value('A1', "Hey yank this numpy array")
#my_nparray = np.random.randint(10, size=(3, 4))

# update the sheet with array
#wks.update_values('A2', my_nparray.tolist())

# share the sheet with your friend
#sh.share("christopher.diaz@ranchocfa.com, role='writer', notify=True)")

# Function to write to Google Sheets
def writeToGoogleSheet(carNumVar, timeVar, dateVar):
    # Open spreadsheet and then worksheet
    sh = gc.open('departure_time')
    wks = sh.sheet1
    # Update the sheet with the values
    wks.append_table(values=[carNumVar, timeVar, dateVar])
    return
