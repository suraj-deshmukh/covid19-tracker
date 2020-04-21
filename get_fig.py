import plotly.graph_objects as go
import datetime
import requests

BASE_URL = "https://corona.lmao.ninja/v2/countries"

class Map:
    def __init__(self,):
        self.fig = go.Figure()
        self.lat, self.lon, self.hovertext, self.text = [], [], [], []
        self.data = None
    
    def _parse_data(self,):
        self.data = requests.get(BASE_URL)
        for i in self.data.json():
            self.lat.append(i.get('countryInfo').get('lat'))
            self.lon.append(i.get('countryInfo').get('long'))
            self.hovertext.append("Confirmed: %s<br>Deaths: %s<br>Critical: %s<br>Recovered: %s<br>Active: %s<br>Today's Cases: %s \
                             <br>Today's Death: %s<br>TestsPerOneMillion: %s<br>DeathsPerOneMillion: %s<br>Tests: %s<br>Last Updated: %s UTC"% \
                            (i['cases'],i['deaths'], i['critical'], i['recovered'], i['active'], i['todayCases'], i['todayDeaths'], \
                            i['testsPerOneMillion'], i['deathsPerOneMillion'], i['tests'], datetime.datetime.utcfromtimestamp(int(i['updated'])/1000)))
            self.text.append(i.get('country', ''))
    
    def get_fig(self,):
        self._parse_data()
        self.fig.add_trace(
            go.Scattermapbox(
                lat=self.lat,
                lon=self.lon,
                mode='markers+text',
                hovertemplate=self.hovertext,
                marker=go.scattermapbox.Marker(
                    size=30,
                    color='LightBlue',
                    opacity=0.5
                ),
                text=self.text,
                name='Stats'
            )
        )
        self.fig.update_layout(
            # title = 'World Map',
            # title_x=0.5,
            autosize=True,
            showlegend = False,
            hovermode='closest',
            # width=1769,
            # height=800,
            mapbox=dict(
                accesstoken="pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w",
                bearing=0,
                center=dict(
                    lat=23.173939,
                    lon=81.56512
                ),
                pitch=0,
                zoom=4
            ),
        )
        return self.fig
        
    def update_fig(self,):
        self.lat, self.lon, self.hovertext, self.text = [], [], [], []
        self._parse_data()
        self.fig.update_traces(hovertemplate=self.hovertext, lat=self.lat, lon=self.lon, text=self.text)
        return self.fig
        
        
def get_stack(country):
    covid_data = requests.get("https://corona.lmao.ninja/v2/historical/%s?lastdays=10000"%country)
    if covid_data.status_code == 200:
        data = covid_data.json()['timeline']
    else:
        covid_data = requests.get("https://corona.lmao.ninja/v2/historical/all?lastdays=10000")
        data = covid_data.json()
        country='World'
    ordered_cases = sorted(data['cases'].items(), key = lambda x:datetime.datetime.strptime(x[0], '%m/%d/%y'))
    ordered_deaths = sorted(data['deaths'].items(), key = lambda x:datetime.datetime.strptime(x[0], '%m/%d/%y'))
    ordered_recovered = sorted(data['recovered'].items(), key = lambda x:datetime.datetime.strptime(x[0], '%m/%d/%y'))
    x = [i[0] for i in ordered_cases]
    cases = [i[1] for i in ordered_cases]
    deaths = [i[1] for i in ordered_deaths]
    recovered = [i[1] for i in ordered_recovered]
    active = [cases[index] - deaths[index] - recovered[index] for index, i in enumerate(cases)]
    fig = go.Figure()
    yellow = ['yellow'] * len(x)
    red = ['red'] * len(x)
    green = ['green'] * len(x)    
    fig.add_traces(go.Bar(name='Active', x=x, y=active, marker_color=yellow))
    fig.add_traces(go.Bar(name='Deaths', x=x, y=deaths, marker_color=red))
    fig.add_traces(go.Bar(name='Recovered', x=x, y=recovered, marker_color=green))
    fig.update_layout(title='Covid 19 Pattern<br>Scope: %s'%country,barmode='stack',autosize=True)#,width=1769, height=800)
    return fig
        
        
        
        
        