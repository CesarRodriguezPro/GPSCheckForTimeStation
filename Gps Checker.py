from geopy.distance import distance
import pandas as pd
import optparse
import os



#####################################################################################
#  API information , key and code to import information from TIMESTATION.COM
CODE = 34
key_api = os.environ.get('TimeStation_key')
dir_path = os.path.abspath(os.path.dirname(__file__))

# Information for the location with GPS Coordinates
with open(os.path.join(dir_path, 'location.txt'), 'r') as dest_file:
    real_gps_locations = dest_file.read()
####################################################################################


''' this setup the quick input of information from the terminal.'''
parser = optparse.OptionParser()
parser.add_option('-i', "--start", dest="date_start", help="the starting date of the search in this format 'yyyy-mm-dd'")
parser.add_option('-f', "--end", dest="date_end", help="the last date of the search in this format 'yyyy-mm-dd'")
parser.add_option('-d', "--distance", dest="distance_val", help="the distance from the center location")
parser.add_option('-p', "--print", dest='print_value', help='this will print the result in a csv file' )
(options, arguments) = parser.parse_args()

date1 = options.date_start
date2 = options.date_end
distance_ = options.distance_val
print_result = options.print_value
save_to_print = os.path.join(dir_path, 'result.txt')  # where items to print will be save


def importing_gps_data():

    ''' the data imported from the Locations.txt comes in the following format:

    location_name : (decimal degrees, decimal degrees)

    and normally take the coordinates for my Location.txt from a website like https://www.gps-coordinates.net/
    please note that this script uses the line divider('\n') as a way to check for independent blocks of Gps Coordinates.
    make sure that the names in location.txt are a exact match with the names that timestation has on their servers.'''

    pair_gps_values = {}
    for items in real_gps_locations.split('\n'):
        item = items.split(':')
        pair_gps_values[item[0]] = item[1]
    return pair_gps_values


def check_distance(original, destino):
    ''' using geopy i calculate the distance in Feets and return the answer.'''

    dist = distance(original, destino).feet
    return dist


def get_data():
    ''' this grap the data from the website and download as a csv file and upload it in to a pandas dataframe'''

    url = f"https://api.mytimestation.com/v0.1/reports/?api_key={key_api}&Report_StartDate={date1}&Report_EndDate={date2}&id={CODE}&exportformat=csv"
    raw_data = pd.read_csv(url)
    return raw_data
    

def from_str_to_gps(gps):

    ''' when converting the database to dict, the values was given to me in str, normally that is not a problems
    but the string has spaces and additional characters  that make geopy raise error, this funtions will clean the str
    and send it clean '''
    
    clean_gps = gps.strip().replace('(', '').replace(')', '').replace(',', ' ').split()
    return clean_gps[0], clean_gps[1]  # return Latitud and longitud


def main_func_gps():

    def print_values_to_csv(values_to_print):
        with open(save_to_print, 'w') as csvfile:
            csvfile.write( f"|{'#':4}|{'Date':^11}|{'Name':^30}|{'Department':^25}|{'Device':^30}|{'Time':^8}|{'Activity':^10}|{'Distance':^10}| \n")
            csvfile.write('-'*145 +'\n' )
            for values in values_to_print:
                csvfile.write(f"|{values[0]:<4}|{values[1]:11}|{values[2]:30}|{values[3]:25}|{values[4]:30}|{values[5]:8}|{values[6]:10}|{values[7]:10.2f}|\n")

    ######## index for display #########################################################################################
    print(" \n\n |{:4}|{:^11}|{:^30}|{:^25}|{:^30}|{:^8}|{:^10}|{:^10}|"
          .format('#', 'Date', 'Name', 'Department', 'Device', 'Time', 'Activity', 'Distance'))
    print('-'*145)
    ####################################################################################################################
    
    csv_data = get_data()
    locations = importing_gps_data()
    server_data = csv_data.to_dict('index') 
    
    values_to_print = []
    num = 1
    for server_items in server_data.values():
        try:
            if server_items['Department'] in locations.keys():
                source_latitude, source_longitude= from_str_to_gps(locations[server_items['Department']])
                total_distance = check_distance((source_latitude, source_longitude), (server_items['Latitude'], server_items['Longitude']))
                if total_distance >= int(distance_):
                    print(f" |{num:<4}|{server_items['Date']:11}|{server_items['Name']:30}|{server_items['Department']:25}|{server_items['Device']:30}|{server_items['Time']:8}|{server_items['Activity']:10}|{total_distance:10.2f}|")
                    values_to_print.append([num, server_items['Date'], server_items['Name'], server_items['Department'], server_items['Device'], server_items['Time'], server_items['Activity'], total_distance])
                    num += 1
        except:
            pass
        
        finally:
            if print_result and print_result.lower() == 'true':
                print_values_to_csv(values_to_print=values_to_print)


if __name__ == '__main__':

    main_func_gps()
    

