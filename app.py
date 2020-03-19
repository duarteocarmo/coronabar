import rumps
import requests
import datetime
import webbrowser


class CoronaBar(object):
    base_api_url = "https://coronavirus-19-api.herokuapp.com/countries"
    default_country = "USA"
    update_interval = 900  # seconds
    about_url = "https://github.com/duarteocarmo/coronabar"

    # APP
    def __init__(self):
        self.app = rumps.App("Corona Bar", "🦠")
        self.countries = rumps.MenuItem(title="Select Country")
        self.about = rumps.MenuItem(title="About", callback=self.about)

        self.country = self.default_country

        self.app.menu = [self.countries, self.about]

        country_list = self.get_country_list()
        self.setup(country_list, self.country)

    def setup(self, country_list, default_country):
        for country in country_list:
            self.countries.add(
                rumps.MenuItem(
                    title=f"{country}", callback=self.update_country_listing
                )
            )

        self.create_country_listing(
            rumps.MenuItem(title=f"{self.default_country}")
        )

    def about(self, sender):
        try:
            webbrowser.open(self.about_url)
        except Exception as e:
            print(str(e))
            return False

    def create_country_listing(self, country):
        # print("Creating")
        data = self.get_country_data(country.title)
        for k, v in data.items():
            self.app.menu.add(rumps.MenuItem(self.string_mapper(k, v)))
        current_time = datetime.datetime.now().strftime("%H:%M")
        self.app.menu.add(rumps.MenuItem(title=f"Updated at {current_time}"))
        # print("Created")
        self.timer = rumps.Timer(self.on_update, self.update_interval)
        self.timer.start()

    def update_country_listing(self, country):
        # print("Update")
        self.country = country.title
        for k, v in self.app.menu.items():
            if k not in ["Select Country", "Quit", "About"]:
                del self.app.menu[k]

        data = self.get_country_data(country.title)
        for k, v in data.items():
            self.app.menu.insert_before(
                "Quit", rumps.MenuItem(self.string_mapper(k, v))
            )

        current_time = datetime.datetime.now().strftime("%H:%M")
        self.app.menu.insert_before(
            "Quit", rumps.MenuItem(title=f"Updated at {current_time}")
        )
        # print(f"Updated,country is {self.country}")

    def on_update(self, sender):
        # print("Timer is running.")
        self.update_country_listing(rumps.MenuItem(title=self.country))

    def run(self):
        self.app.run()

    # DATA
    def get_country_list(self):
        response = requests.request("GET", self.base_api_url)
        data = response.json()
        country_list = [e["country"] for e in data]
        return sorted(country_list)

    def get_country_data(self, country):
        response = requests.request("GET", f"{self.base_api_url}/{country}")
        data = response.json()
        return data

    # STRING MAPPER
    def string_mapper(self, key, value):
        if not self.is_camel_case(key):

            return f"{key.title()}: {value}"
        elif key == "todayCases":
            return f"Cases Today: {value}"

        elif key == "todayDeaths":
            return f"Deaths Today: {value}"

        elif key == "casesPerOneMillion":
            return f"Per Million: {value}"

        else:
            return f"{key}: {value}"

    @staticmethod
    def is_camel_case(s):
        # https://stackoverflow.com/a/10182901 thanks :)
        return s != s.lower() and s != s.upper() and "_" not in s


if __name__ == "__main__":
    app = CoronaBar()
    app.run()
