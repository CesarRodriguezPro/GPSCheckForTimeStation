import pandas as pd
from geopy import distance
import warnings
import os
import optparse
warnings.simplefilter(action='ignore', category=UserWarning)

''' this program uses the api from timestation to get the imformation of the gps  and comparate to
a list a gps list of current location around the city
i created this to verify that our workers clock in around the jobsites that they are say they are

'''

#####################################################################################
#  API information , key and code to import information from TIMESTATION.COM
CODE = 34
key_api = os.environ.get('TimeStation_key')
dir_path = os.path.abspath(os.path.dirname(__file__))
####################################################################################


''' this setup the quick input of information from the terminal.'''
parser = optparse.OptionParser()
parser.add_option('-i', "--start", dest="date_start", help="the starting date of the search in this format 'yyyy-mm-dd'")
parser.add_option('-f', "--end", dest="date_end", help="the last date of the search in this format 'yyyy-mm-dd'")
parser.add_option('-d', "--distance", dest="distance_val", help="the distance from the center location")
parser.add_option('-n', "--name", dest="name_val", help="search for name")
parser.add_option('-p', "--print", dest='print_value', help='this will print the result in a csv file' )
(options, arguments) = parser.parse_args()

date1 = options.date_start
date2 = options.date_end
distance_ = float(options.distance_val) if options.distance_val else 0 
name_ = options.name_val if options.name_val else ""
print_answer = True if options.print_value and options.print_value =='true' else False

save_to_print = os.path.join(dir_path, 'result.csv') 
CSV_FILE_PATH =  f"https://api.mytimestation.com/v0.1/reports/?api_key={key_api}&Report_StartDate={date1}&Report_EndDate={date2}&id={CODE}&exportformat=csv"


class GPSTracker:
    '''this class take a csv file form timestation and take the information for the gps location and comparate to a list o locations that is save in a file call "location.txt"
    the main idea is to check if employees clock in in the close range of the location the presume clock in. '''
   
    def __init__(self, load_data, distance_apart=0, name=''):
        self.user_distance = distance_apart
        self.name = name
        self.load_data = load_data

        self.base_locations = {}
        with open(os.path.join(dir_path,'location.txt'), 'r') as self.file:
            self.base_data = self.file.read()
            self.location_list = (stuff for stuff in self.base_data.strip().split('\n'))
            for self.single_location in self.location_list:
                self.single_location = self.single_location.split(':')
                self.cord = self.single_location[1].lstrip().strip().replace('(', '').replace(")", '').split(',')
                self.base_locations[self.single_location[0]] = (self.cord[0], self.cord[1])

    def process_data(self):
        print('Start Processing Data From csv File\n')
        data = self.get_data()
        data['Latitude'].fillna(0)
        data['Longitude'].fillna(0)
        data['GPS_data'] = list(zip(data.Latitude, data.Longitude))
        data['baseGps'] = data['Department'].apply(self.find_deparment_gps)
        data['distance'] = data.apply(self.get_distance, axis=1)
        after_distance = data[data['distance'] > self.user_distance]
        after_name = after_distance[data['Name'].str.contains(self.name)]
        after_name.index = after_name.index + 1
        return after_name[['Date', 'Name', 'Department', 'Device', 'Time', 'Activity', 'distance']]

    def display_information(self):
        data_display = self.process_data()
        data_d = data_display.to_dict(orient='index')
        ready_display = (item for item in data_d.values())
        print(f"|{'#':^5}|{'Date':12}|{'Name':30}|{'Department':24}|{'Device':20}|{'Time':7}|{'Activity':10}|{'distance':8}|")
        print("-"*126)
        n = 1
        for i in ready_display:
            print(f"|{n:^5}|{i['Date']:12}|{i['Name']:30}|{i['Department']:24}|{i['Device']:20}|{i['Time']:7}|{i['Activity']:10}|{i['distance']:8.2f}|")
            n += 1
        print('\n finish sorting data')

    def export_to_csv(self,path):
        self.process_data().to_csv(path)
        os.startfile(path)
        print('finish exporting.')

    def get_data(self):
        raw_data = pd.read_csv(self.load_data)
        selected_data = raw_data[['Date', 'Name', 'Department', 'Device', 'Time', 'Activity', 'Latitude', 'Longitude']]
        return selected_data

    def find_deparment_gps(self, department):
        return self.base_locations.get(department, (0, 0))

    def get_distance(self, value):
        try:
            return distance.distance(value[8], value[9]).miles
        except:
            return 0

   
if __name__ == '__main__':
    os.system('cls')
    print(f'\n[+]---- >  stating date {date1}, end date {date2} ,  distance -> {distance_} Miles, search for {name_} \n')
    print('-'*127)
    active = GPSTracker(load_data=CSV_FILE_PATH, distance_apart=distance_, name=name_)
    active.export_to_csv(save_to_print) if print_answer == True else active.display_information()
