from flask import Flask, render_template
import scraper
import datetime
import data

app = Flask(__name__)
strava_id = 874803
datadict = dict()
totaaldict = dict()



_, week_num_now, _ = datetime.date.today().isocalendar()
_, week_num_begin, _ = datetime.date(2021,3,31).isocalendar()
for i in range(week_num_now - week_num_begin + 1):
    temp = scraper.get_data(strava_id, i)
    for runner in temp:
        datadict[runner[0]] = datadict.get(runner[0], 0) + runner[1]

for key in datadict:
    if key in data.gangdict:
        gng = data.gangdict[key]
        totaaldict[gng] = totaaldict.get(gng, 0) + datadict[key]

for key in data.deletedict:
    totaaldict[key] = totaaldict.get(key, 0) - data.deletedict[key] 

lst = []
for k, v in sorted(totaaldict.items(), key= lambda x : x[1], reverse= True):
    lst.append((k,round(v, 3)))

lstgem = sorted([ (x, round(y/data.gangtotaaldict[x], 3)) for x,y in lst] , key= lambda x : x[1], reverse= True)
@app.route("/")
def index():
    return render_template("index.html", totaalrest = lst ,gemiddeldrest = lstgem)

if __name__ == '__main__':
    app.run(debug=True)