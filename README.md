# RetroPark
# This is the main code project for Team 5 RetroPark

#spot-selector.py Readme
spot-selector.py is used to create the location data of each individual parking spot and place them into a formatted .csv.

To run spot-selector you need to give it two arguments, image and output. The image should be a sample image of the final device location, output should be a .csv to save the data to. Running this script will delete the contents of the given .csv or create it if it does not exists.

Sample Command

python spot-selecter.py -i '.\Test Images\Ximenes_Phone_IR_closecenter.jpg' -o .\IR_closecenter_location.csv

Once you run the script you may then begin selecting the spots.

1. Click on the top left corner of the spot
2. bottom left
3. bottom right
4. top right
5. Press spacebar to confirm selection
6. Repeat

If at any point you misclick or want to start over the current selection, press 'R'. Once you are done press 'Q' to save and quit.

#spot-map-viewer.py Readme
The spot-map-viewer.py script lets you view the set bounds of parking spots determined by spot-selector.py.

spot-map-viewer requires two arguments, -i for the same image and -d for the spot location data.

Sample Command

python .\spot-map-viewer.py -i '.\Test Images\Ximenes_Phone_IR_closecenter.jpg' -d .\IR_closecenter_location.csv

Once you run the command you will be able to view the spot locations.