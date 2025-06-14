import pygsheets
import numpy as np

#gc = pygsheets.authorize(service_file='/Users/jedSheeran/Downloads/cfa-departure-time-cf700c401d86.json')
gc = pygsheets.authorize(service_file='/home/cfarancho/DepartureTimeSensor/cfa-departure-time-cf700c401d86.json')

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

def readAllRows():
    # Read all rows from the Google Sheet
    return wks.get_all_values(returnas='matrix')[1:]  # Skip the header row

# Function to write to Google Sheets
def writeToGoogleSheet(carNumVar, timeVar, dateVar):
    # Open spreadsheet and then worksheet
    sh = gc.open('departure_time')
    wks = sh.sheet1
    # Update the sheet with the values
    wks.append_table(values=[carNumVar, timeVar, dateVar])
    return
