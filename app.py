import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify)

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

# The database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/top_zipcodes.sqlite"
db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)

plotly = Base.classes.top_zipcodes
# # Create our database model
# class top10(db.Model):
#     __tablename__ = 'top_zipcodes'

#     zipcode = db.Column(db.Integer, primary_key=True)
#     duplex = db.Column(db.String)
#     mobile = db.Column(db.String)
#     singlefamily = db.Column(db.String)
#     townhome = db.Column(db.Integer)

#     def __repr__(self):
#         return '<top10 %r>' % (self.name)


# # Create database tables
# #@app.before_first_request
# #def setup():
#     # Recreate database each time for demo
#     # db.drop_all()
#     #db.create_all()


@app.route("/")
def home():
    """Render Home Page."""
    return render_template("index.html")

@app.route("/Tableau.html")
def tableau_page():
    return render_template("Tableau.html")

@app.route("/rent_affordability.html")
def rent_page():
    return render_template("rent_affordability.html")

@app.route("/Plotly.html")
def Plotly_page():

    results = db.session.query(plotly.zipcode).all()
    z = [row[0] for row in results]
    
    return render_template("Plotly.html", zipcodes=z)

@app.route("/zipcode/<z>")
def zipcode_data(z):
    
    results = db.session.query(plotly.zipcode,plotly.duplex,plotly.mobile,plotly.singlefamily,plotly.townhouse).all()

    # Create lists from the query results
    hometype = ['Duplex','Mobile','SingleFamily','Townhome']
    #scores = [result[0] for result in results]
    scores = []
    for rows in results:
        ZIPP = rows[0]
        A = float(rows[1])
        B = float(rows[2])
        C = float(rows[3])
        D = float(rows[4])
        if ZIPP == int(z):
            scores.append(A)
            scores.append(B)
            scores.append(C)
            scores.append(D)
        else:
            continue
    
    
    # Generate the plot trace
    trace = {
        "x": hometype,
        "y": scores,
        "type": "bar"
    }
    return jsonify(trace)

    # Format the data for Plotly
 #   plot_trace = {
 #       "x": trace["x"].values.tolist(),
 #       "y": trace["y"].values.tolist(),
 #       "type": "bar"
 #   }
 #   return jsonify(plot_trace)


if __name__ == '__main__':
    app.run(debug=True)
