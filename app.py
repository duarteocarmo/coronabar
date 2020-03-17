import rumps
import requests
import datetime
import webbrowser

URL = "https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID19Portugal_UltimoRel/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outSR=102100&resultOffset=0&resultRecordCount=50"
ABOUT_PAGE = "https://github.com/duarteocarmo/coronapt"
SOURCE_PAGE = "https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/"

class CoronaApp(object):
    def __init__(self):
        self.app = rumps.App("Corona PT", "🦠")
        self.data = self.get_data(sender=None)

        self.suspected = rumps.MenuItem(
            title=f"Suspeitos: {self.data.get('casossuspeitos')}"
        )
        self.confirmed_cases = rumps.MenuItem(
            title=f"Confirmados: {self.data.get('casosconfirmados')}"
        )
        self.recovered = rumps.MenuItem(
            title=f"Recuperados: {self.data.get('recuperados')}"
        )
        self.deceased = rumps.MenuItem(
            title=f"Óbitos: {self.data.get('nrobitos')}"
        )
        self.last_refresh = rumps.MenuItem(
            title=f"Data: {self.get_date_from_timestamp(self.data.get('datarelatorio'))}"
        )
        self.source = rumps.MenuItem(title="Fonte: DGS", callback=self.source)
        self.refresh = rumps.MenuItem(title="Refresh", callback=self.get_data)
        self.about = rumps.MenuItem(title="About", callback=self.about)

        self.app.menu = [
            self.suspected,
            self.confirmed_cases,
            self.recovered,
            self.deceased,
            self.last_refresh,
            self.refresh,
            self.source,
            self.about,
        ]

    def get_data(self, sender):

        try:

            response = requests.request("GET", URL)

            data = response.json().get("features")[0].get("attributes")

            self.data = data

            if len(list(self.app.menu)) > 1:
                self.suspected.title = (
                    f"Suspeitos: {data.get('casossuspeitos')}"
                )
                self.confirmed_cases.title = (
                    f"Confirmados: {data.get('casosconfirmados')}"
                )
                self.recovered.title = (
                    f"Recuperados: {data.get('recuperados')}"
                )
                self.deceased.title = f"Óbitos: {data.get('nrobitos')}"
                self.last_refresh.title = f"Data: {self.get_date_from_timestamp(data.get('datarelatorio'))}"
                print("Updated.")

            return data

        except Exception as e:
            print(str(e))
            return False

    def about(self,  sender):
        try:
            webbrowser.open(ABOUT_PAGE)
        except Exception as e:
            print(str(e))
            return True
    def source(self,  sender):
        try:
            webbrowser.open(SOURCE_PAGE)
        except Exception as e:
            print(str(e))
            return True


    @staticmethod
    def get_date_from_timestamp(timestamp):
        timestamp = timestamp / 1000
        # return datetime.datetime.utcfromtimestamp(timestamp).strftime(
        #     "%d/%m %H:%M"
        # )
        return datetime.datetime.now().strftime("%d/%m %H:%M")

    def run(self):

        self.app.run()


if __name__ == "__main__":
    app = CoronaApp()
    app.run()
