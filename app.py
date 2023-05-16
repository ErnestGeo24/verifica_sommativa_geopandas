import io
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import contextily as ctx
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, Response
app = Flask(__name__)

quartieriMI = gpd.read_file('https://github.com/ErnestGeo24/Esercizio_Geopandas_-_3_ripasso_verifica/raw/main/ds964_nil_wm.zip')
colonnine = pd.read_csv('https://github.com/ErnestGeo24/Esercizio_Geopandas_-_3_ripasso_verifica/raw/main/colonnine_ricarica_geo.csv')

def convertikm(km):
  return km / 2.59

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/input', methods=['GET'])
def input():
    input = request.args.get('input')
    return render_template('input.html')

@app.route('/input2', methods=['GET'])
def input2():
    return render_template('input2.html')

@app.route('/input3', methods=['GET'])
def input3():
    return render_template('input3.html')
    
@app.route('/input4', methods=['GET'])
def input4():
    return render_template('input4.html')
    
@app.route('/input5', methods=['GET'])
def input5():
    return render_template('input5.html')

@app.route('/input6', methods=['GET'])
def input6():
    return render_template('input6.html')

@app.route('/risultato1', methods=['GET'])
def risultato1():
    colonnine =colonnine.drop(colonnine[colonnine['LAT_Y_4326']== '-'].index)
    gdf = gpd.GeoDataFrame(colonnine, geometry = gpd.points_from_xy(colonnine['LONG_X_4326'], colonnine['LAT_Y_4326']), crs = 'EPSG:4326')
    return render_template('risultato1.html', table = gdf.to_html())

@app.route('/risultato2', methods=['GET'])
def risultato2():
    gdf3857 = gdf.to_crs(3857)
    quartieriMI3857 = quartieriMI.to_crs(3857)
    gdf3857 = gdf.to_crs(3857)
    ax = gdf3857.plot(color='k')
    ctx.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/risultato3', methods=['GET'])
def risultato3():
    ax = gdf3857.plot(edgecolor =  "k", facecolor = "None",figsize=(12,6),markersize = 5)
    quartieriMI3857.plot(ax=ax,edgecolor =  "red", facecolor = "None",figsize=(12,6),markersize = 5)
    ctx.add_basemap(ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/risultato4', methods=['GET'])
def risultato4():
    join = gpd.sjoin(gdf,quartieriMI,predicate ='intersects',how = 'left')
    qu = str(input('inserisci il quartiere: ')).upper()
    join3857 = join.to_crs(3857)
    ax = join3857[join3857['NIL'].str.contains(qu)].plot()
    ctx.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/risultato5', methods=['GET'])
def risultato5():
    quartconf = quartieriMI[quartieriMI.touches(quartieriMI[quartieriMI['NIL'] == qu].geometry.item())]
    quartconf3857 = quartconf.to_crs(3857)
    ax = join3857.plot(edgecolor =  "k", facecolor = "None",figsize=(12,6),markersize = 5)
    quartconf3857.plot(ax=ax,edgecolor =  "red", facecolor = "None",figsize=(12,6),markersize = 5)
    ctx.add_basemap(ax = ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/risultato6', methods=['GET'])
def risultato6():
    latitudine = float(input())
    longitudine = float(input())
    punto= gpd.GeoSeries([Point(longitudine,latitudine)], crs = 3857)
    ax = join3857[join3857.distance(punto.to_crs(3857).unary_union)<500].plot()
    ctx.add_basemap(ax = ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/risultato7', methods=['GET'])
def risultato7():
    ax = join.to_crs(3857).plot(figsize=(16,10), legend = True,column="numero_col",cmap="YlOrBr", alpha = 0.7,edgecolor="k" )
    ctx.add_basemap(ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=32245, debug=True)