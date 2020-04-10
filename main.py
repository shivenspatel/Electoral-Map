import folium
import pandas

election_data=pandas.read_csv('Data/us-2016-presidential-election-by-states.csv')
s_name=list(election_data["State"])
s_win=list(election_data["Winner"])
s_gop=list(election_data["Republican"])
s_dem=list(election_data["Democratic"])

s = {}
for state in s_name:
    for winner in s_win:
        s[state] = winner
        s_win.remove(winner)
        break

def CheckState(state):
    return s.get(state)

state_data=pandas.read_csv('Data/states.csv')
# election_data=pandas.read_csv('Data/us-2016-presidential-election-by-states.csv')
sd_name=list(state_data['state'])
sd_capital=list(state_data['capital_city'])
sd_nickname=list(state_data['nickname'])
sd_flag=list(state_data['state_flag_url'])
sd_population=list(state_data['population'])
governor=list(state_data['name'])
governor_party=list(state_data['party'])

location=pandas.read_csv('Data/us-state-capitals.csv')
sd_lt = list(location["latitude"])
sd_ln = list(location["longitude"])

county_data=pandas.read_csv('Data/2016_US_County_Level_Presidential_Results.csv')
c_fips=list(county_data["combined_fips"])
c_winner=list(county_data["winner"])

c = {}
for county in c_fips:
    for cwinner in c_winner:
        c[county] = cwinner
        c_winner.remove(cwinner)
        break

def CheckCounty(county):
    return c.get(county)


html = """
<font face="verdana">
<h2 style="text-align: center;"><span style="text-decoration: underline;"><strong> %s </strong></span></h2>
<blockquote>
<p style="text-align: center;"><strong> %s </strong></p>
</blockquote>
<p>&nbsp;</p>
<table style="width: 350px; border-color: white;" border="0">
<tbody>
<tr>
<td style="width: 175px;">
<p>Governor: %s %s </p>
<p>State Capital: %s </p>
<p>Population: %s </p>
</td>
<td style="width: 175px;">
<img src="%s" alt="" width="175" height="105" />
</td>
</tr>
</tbody>
</table>
<table style="width: 375px; border-color: white;">
<tbody>
<tr>
<td style="width: 75px;"><img style="display: block; margin-left: auto; margin-right: auto;" src="https://bit.ly/33XNxDG" alt="" width="75" /></td>
<td style="width: 100px; text-align: center;">
<p>&nbsp;Donald Trump</p>
<p>(R-FL)</p>
<p><font color="#ff0000;"><b> %s </b></font></p>
</td>
<td style="width: 75px;">&nbsp;<img style="display: block; margin-left: auto; margin-right: auto;" src="https://bit.ly/2WXRsPj" alt="" width="75" height="75" /></td>
<td style="width: 100px;">
<p style="text-align: center;">&nbsp;Hillary Clinton</p>
<p style="text-align: center;">(D-NY)</p>
<p style="text-align: center;"><font color="#3333ff;"><b> %s </b></font></p>
</td>
</tr>
</tbody>
</table>
</font>
"""

m = folium.Map(location=[39.8283, -98.5795], zoom_start=5)
# tiles = "Stamen Terrain"

states = folium.FeatureGroup(name='States')
states.add_child(folium.GeoJson(data=open('GeoJson Files/us-state-boundaries.geojson', 'r', encoding='utf-8-sig').read(), 
style_function=lambda x :{'fillColor':'red' if CheckState(str(x["properties"]["basename"]))
 == "Republican" else 'blue', 'weight':0.5, 'fillOpacity':0.75, 'color':'white', 'bubbling_mouse_events':True}))

for nm, cp, lt, ln, nn, sf, sp, gv, gvp, sg, sd in zip(sd_name, sd_capital, sd_lt, sd_ln, sd_nickname, sd_flag, sd_population, governor, governor_party, s_gop, s_dem):
    iframe = folium.IFrame(html=html % (nm, nn, gv, gvp, cp, sp, sf, sg, sd), width=400, height=410)
    states.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe), 
        tooltip=nm, color='white', fill=True, fill_color='white'))

counties = folium.FeatureGroup(name='Counties')
counties.add_child(folium.GeoJson(data=open('GeoJson Files/us-counties.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x :{'fillColor':'red' if 
CheckCounty(int(x["id"])) == "TRUMP" else 'blue', 'weight':0.5, 'fillOpacity':0.75, 'color':'white'}))

cd = folium.FeatureGroup(name='Congressional Districts')
cd.add_child(folium.GeoJson(data=open('GeoJson Files/cong_dist.geojson', 'r', encoding='utf-8-sig').read()))

m.add_child(states)
m.add_child(counties)
m.add_child(cd)
m.add_child(folium.LayerControl())

# folium.vector_layers.path_options(line=True,radius=False,stroke=True,weight=0.25,opacity=0.5,fill=True,fill_opacity=0.75)
m.save("map.html")