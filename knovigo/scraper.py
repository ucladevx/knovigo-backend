import populartimes
import requests
import json #need?


WESTWOOD_LOCATIONS = [
	"ChIJM2_CO4G8woARCvO-wn-MObo", #Westwood Target
	"ChIJDepxE4G8woAR4BETlQXlSt8", #Westwood Trader Joe's
	"ChIJU9RXX4G8woARM6tDKbo-o40", #Westwood CVS
	"ChIJf5fVvoO8woARChfRh6MOi8o", #Westwood Whole Foods
	"ChIJz3nnNoG8woARM2mO30LUT-Q", #Westwood Ralph's
	"ChIJ9bElwYO8woARyFBerBC6aRs", #Westwood Barney's Beanery
	"EidKYW5zcyBTdGVwcywgTG9zIEFuZ2VsZXMsIENBIDkwMDk1LCBVU0EiLiosChQKEgmP7FgEibzCgBGSTtcJJ1JtZhIUChIJE9on3F3HwoAR9AhGJW_fL-I", #Tonga steps
	"ChIJD28uC4S8woARUk1Z5qNqmjk", #Westwood Diddy Riese
	"ChIJSXU3ioO8woARK-IVICYTrVI", #BJ's Restaurant and Brewery
]

api_key = ""
# remove hard coding for now
# don't push API keys !

def getPlaceData(place_id):
	# modify the fields we retrieve
	# do we rely more on the populartimes call to reduce redundant
	fields = "website,opening_hours,photos,price_level"
	response = requests.get("https://maps.googleapis.com/maps/api/place/details/json?place_id=" + place_id + "&fields=" + fields + "&key=" + api_key)
	print(response.json())

def getPopularTimeData(place_id):
	fields = "name,formatted_address,geometry.location,formatted_phone_number,rating, etc all retrieved here"
	response = populartimes.get_id(api_key, place_id)
	print(response)


getPlaceData(WESTWOOD_LOCATIONS[0])
getPopularTimeData(WESTWOOD_LOCATIONS[0])