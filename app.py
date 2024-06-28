from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    url = "https://www.billybishopairport.com/flights/arrivals/"
    headers = {"User-Agent": "Edge"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find(id="flightsTable")
    raw_flights = results.find_all("td", class_=False)

    flights =[]
    for i in range(len(raw_flights)//4):    
        position = i * 4

        arrival_time = raw_flights[position].get_text()
        flight_num = raw_flights[position+1].get_text()
        origin = raw_flights[position+2].get_text()
        status = raw_flights[position+3].get_text()

        flights.append([arrival_time, flight_num, origin, status])

    last_arrived_index = next(i for i, flight in reversed(list(enumerate(flights))) if flight[3] == "Arrived")
    selected_flights = flights[max(0, last_arrived_index - 2) : last_arrived_index + 7]

    return render_template('home.html', flights=selected_flights)

if __name__ == '__main__':
    app.run(debug=True)
