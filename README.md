# [covid19-tracker](http://www.sars-cov-2019.com/)
Covid 19 Dashboard to Track the Pandemic Pattern. Click [here](http://www.sars-cov-2019.com/) for live demo. It is a desktop site.

## Welcome to [Covid19 Dashboard](http://www.sars-cov-2019.com/)

The dashboad has been developed using python's visualization library [Dash](https://plotly.com/dash/) and the data source for this dashboard is [Novel COVID API](https://corona.lmao.ninja/)

### Features of this dashboard

1. Live Updates on Confirmed, Active, Recovered and Deaths in the World
2. World Map to check country wise live covid 19 details. Once you hover over the bubble representing country (country selected using provided dropdown) you would see below information. 
   - Confirmed: Total Number of Covid 19 Positive Patients
   - Active: Number of Active patients
   - Recovered: Number of Recovered patients
   - Deaths: Number of patients died due to covid 19
   - Critical: Number of patients in critical stage
   - Today's Case: Number of postives detected for current date
   - Today's Death: Number of deaths reported for current date
   - TestPerOneMillion: Number of Tests done per one million so far
   - DeathsPerOneMillion: Number of patients died per million so far
   - Test: Total Number of Tests done so far
   
   Below screenshot shows how the information is displayed in the dashboard ![screenshot](https://github.com/suraj-deshmukh/covid19-tracker/blob/master/screenshots/dash5.png)
   
   You can even search specific country like below and map would re-center itself to selected country ![screenshot](https://github.com/suraj-deshmukh/covid19-tracker/blob/master/screenshots/dash2.png)
   
 3. Stacked Bar Chart representing the Confirmed cases progress pattern with 3 sub categories as Active, Recovered and Deaths. For eg. If you want to see only Active cases pattern then just disable the other two i.e Recovered and Deaths by clicking on respective legents (once you click on them there could would turn into gray) as shown in the below screenshot ![screenshot](https://github.com/suraj-deshmukh/covid19-tracker/blob/master/screenshots/dash4.png) 
