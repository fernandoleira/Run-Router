from flask import Flask, render_template, request, redirect

import weather_data

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root_page():

    return redirect("https://run-router.herokuapp.com/335315")

@app.route('/<location_key>', methods=['GET', 'POST'])
def show(location_key):
    # Search in query
    if request.method == 'POST':
        req = request.form.to_dict()
        search_city = weather_data.search_location(weather_data.API_KEY, req["name"])
        return redirect("https://run-router.herokuapp.com/" + search_city["Key"])

    loc_city = weather_data.search_location_from_key(weather_data.API_KEY, location_key)
    curr_con = weather_data.current_conditions(weather_data.API_KEY, location_key)
    map_url = "https://maps.googleapis.com/maps/api/js?key=AIzaSyC0Qef47L7GLU039tQdkODrkd0WsQg6OPs&libraries=places&callback=initMap"
    weather_img = "sunny"
    if curr_con["IsDay"] == False:
        weather_img = "night"
    elif curr_con["WeatherText"] == "Rain":
        weather_img = "rain"
    elif curr_con["WeatherText"] == "Snow":
        weather_img = "snow"

    data = [
        loc_city,
        curr_con,
        weather_data.hourly_forecast(weather_data.API_KEY, location_key),
        {"MapURL": map_url, "WeatherImg": weather_img}
    ]
    return render_template('index.html', data=data)

if __name__=="__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
