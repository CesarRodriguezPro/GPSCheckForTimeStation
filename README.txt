Hello Everyone,
i use this program to check if my employees clock in around the area the need to be working by using the gps of timestation
we have around 600 employees in 6 different locations its really hard to check eveyone of those independantly 

this programs require that you have a API Key from timestation. 
normally you send a request to http://support.mytimestation.com/customer/portal/emails/new
they will send you a encryped key, just created a text file and save it as "Api_key.txt".
next you can go to a website like "https://www.gps-coordinates.net/" and type you address or the
address of your jobsite (or where you want to place the timestation.) and you will get a decimal GPS 
cordinates.

created a file name 'location.txt' and save them (look at the location_sample.txt for format)
please save the "location.txt" and "Api_key.txt" in the same place of the script.
please dont leave space on the gps location on the location file. 
example: 
264 kent avenue:(40.2225151, -71.258865) - the space in the GPS coordinates (before the -71) can created a problem try to avoid it by just dont leave spaces 
like this:
264 kent avenue:(40.2225151,-71.258865) please notice the space before the -71 now is gone.
the name of the location (264 kent avenue) must be exact as the csv file.


how to use:
open terminal and execute script:
C:\Users\User\Desktop\GpsChecker> python "Gps Checker.py" -i 'yyyy-mm-dd' -f 'yyyy-mm-dd' -d 'distance limit'

now let me explain:

this programs looks throught a peried of time and compare the distance of from the timestation server and 
the locations you have save on the "location.txt", so you need to give the programs the followings information

- "-i" inicial date in format yyyy-mm-dd
- "-f" final date in format yyyy-mm-dd
- "-d" Distance in miles from the jobsite (GPS is too accurate so i Around the result. 1 mile )
- "-n" search with a name , please type exactly as in the source data. 

the distance will give you result equal or greater than the distance you input.







