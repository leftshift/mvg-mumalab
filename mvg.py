from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from operator import attrgetter
app = Flask(__name__)

import MVGLive

DEBUG = True
SECRET_KEY = 'dev key'

app.config.from_object(__name__)

mvg = MVGLive.MVGLive()

@app.route("/")
def main():
    data = mvg.getlivedata("Siemenswerke")
    for dept in data:
        dept["station"] = "Siemenswerke"

    data2 = mvg.getlivedata("Obersendling")
    for dept in data2:
        dept["station"] = "Obersendling"

    combined = data + data2
    combined = sorted(combined, key=lambda dept: dept['time'])
    print(combined)

    return render_template("table.html", data=combined, autorefresh=True)

@app.route("/raw")
def raw_json():
    data = mvg.getlivedata("Siemenswerke")
    data += mvg.getlivedata("Obersendling")
    data = sorted(data, key=lambda dept: dept['time'])
    return str(data)

if __name__ == "__main__":
    app.run()
