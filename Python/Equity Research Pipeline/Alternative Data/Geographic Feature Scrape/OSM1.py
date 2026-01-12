import osmnx as ox
import numpy as np
import pandas as pd
import pyvista as pv
from shapely.geometry import Polygon, MultiPolygon
from pathlib import Path
import random
import matplotlib.pyplot as plt

def osm_road_network(place):

    outlook = ox.graph_from_place(place, network_type='drive') #fetch
    projected_outlook = ox.project_graph(outlook) #transform for analysis
    road_basic_stats = ox.basic_stats(projected_outlook)

    ox.plot_graph(projected_outlook,
                  bgcolor='white', edge_color='black')

    return road_basic_stats


def osm_features(place,classification,feature_name,radius=1000):

    tags = {classification:feature_name}
    gdf = ox.features.features_from_address(place,tags,radius)

    return gdf


def osm_features_plot(place,classification,feature_name,radius=1000):

    gdf_points = osm_features(place, classification, feature_name, radius)
    outlook = ox.graph_from_address(place,dist=radius)

    fig, ax = ox.plot_graph(outlook,show=False,close=False,
                            bgcolor='white',
                            edge_color='black',node_size=0, edge_linewidth=0.5)
    gdf_points[gdf_points.geom_type == 'Point'].plot(ax=ax, color='red', markersize=20, zorder=5)

    plt.show()


def features_count_comparison(places_list,classification,feature_name,radius):
    df = pd.Series()
    for place in places_list:
        gdf = osm_features(place,classification,feature_name,radius)
        df.loc[place] = len(gdf.iloc[:,0])
    return df


def osm_features_plot_enhanced(place, classification, feature_name, radius=1000):


    tags = {classification: feature_name}
    gdf_features = ox.features.features_from_address(place, tags, radius)
    
    if gdf_features.empty:
        print(f"No features found for {classification}={feature_name} in {place}")
        return

    G = ox.graph_from_address(place, dist=radius, network_type='walk')


    fig, ax = ox.plot_graph(G, show=False, close=False,
                            bgcolor='white',
                            edge_color="#000000",  
                            edge_linewidth=0.5,    
                            node_size=0)

   
    gdf_plot = gdf_features.copy()
    gdf_plot['geometry'] = gdf_plot.geometry.centroid


    gdf_plot.plot(ax=ax, color='red', markersize=40, alpha=0.8, zorder=10)

    ax.set_title(f"{feature_name} in {place} (n={len(gdf_features)})", fontsize=10)

    plt.show()