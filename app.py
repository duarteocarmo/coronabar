import rumps
import requests
import datetime
import webbrowser


class CoronaBar(object):
    base_api_url = "https://coronavirus-19-api.herokuapp.com/countries"
    default_country = "USA"
    update_interval = 5 # seconds

    def __init__(self):
        self.app = rumps.App("Corona Bar", "🦠")
        self.countries = rumps.MenuItem(title="Select Country")
        self.country = self.default_country

        self.app.menu = [
            self.countries,
        ]
        country_list = self.get_country_list()
        self.timer = rumps.Timer(self.on_update, self.update_interval)
        self.setup(country_list, self.country)

    def setup(self, country_list, default_country):
        for country in country_list:
            self.countries.add(
                rumps.MenuItem(
                    title=f"{country}", callback=self.update_country_listing
                )
            )

        self.update_country_listing(
            rumps.MenuItem(title=f"{self.default_country}")
        )
        self.timer.start()

    def update_country_listing(self, country):
        for k, v in self.app.menu.items():
            if k not in ["Select Country", "Quit"]:
                del self.app.menu[k]

        data = self.get_country_data(country.title)
        current_time = datetime.datetime.now().strftime("%H:%M")
        for k, v in data.items():
            self.app.menu.add(rumps.MenuItem(title=f"{k}: {v}"))
        self.app.menu.add(rumps.MenuItem(title=f"Updated at {current_time}"))
        self.country = country.title
        print("Updated.")

    def on_update(self, sender):
        print(self.country)

    def run(self):
        self.app.run()

    def get_country_list(self):
        response = requests.request("GET", self.base_api_url)
        data = response.json()
        country_list = [e["country"] for e in data]
        return sorted(country_list)

    def get_country_data(self, country):
        response = requests.request("GET", f"{self.base_api_url}/{country}")
        data = response.json()
        return data




if __name__ == "__main__":
    app = CoronaBar()
    app.run()
