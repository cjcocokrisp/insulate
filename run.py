# Insulate - Developed by Christopher Coco
# The purpose of this app is to motivate children with Type 1 Diabetes to have good blood sugars by rewarding them from being in range.
# This app was developed with the Dexcom API to allow users to get their blood sugars from their Dexcom device.
# If you are cloning the source code from the Github respository make sure you have all of the libraries that this application uses. They are listed below.
# Libraries used: pygame*, datetime, clipboard*, json, requests*, webbrowser, and http.client (All the libraries marked with a * need to be installed)
# https://github.com/cjcocokrisps/Insulate
# For how to use instructions please few the projects README.md file. 


from main import *

if __name__=='__main__':
    instance = App()
    while instance.running:
        instance.new() 
