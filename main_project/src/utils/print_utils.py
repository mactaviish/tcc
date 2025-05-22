from gurobipy import Model
from tabulate import tabulate
from typing import List, Dict
from adjustText import adjust_text
from src.models.model_vars import ModelVars
from src.models.route import Route
from src.models.airport import Airport
import numpy as np
import gurobipy as gp
import src.consts as consts
import csv
import matplotlib.pyplot as plt
import networkx as nx
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

def print_solution(model: Model, variables: ModelVars):
  if model.status == gp.GRB.OPTIMAL:
    print("\nSolução ótima encontrada.")
    print(f"\nValor objetivo: {model.ObjVal}\n")

    print_table(model, variables)
  else:
      print("Nenhuma solução ótima foi encontrada.")

def print_table(model: Model, variables: ModelVars):
    table_data = []
    headers = ["Destination", "Airplane", "Flow", "Passengers", "Active Route", "Active Airplane"]
    for key, var in variables.F.items():
        if var.X > 0:
          destination, airplane = key
          active_route = "Yes" if variables.BIN[key].X >= 0.5 else "No"
          active_airplane = "Yes" if variables.BIN2[airplane].X >= 0.5 else "No"
          row = [
            destination,
            airplane,
            variables.F[key].X,
            variables.P[key].X,
            active_route,
            active_airplane
          ]
          table_data.append(row)
    table_data.append([
      "Valor objetivo",
      model.ObjVal
    ])
    print(tabulate(table_data, headers, tablefmt="fancy_grid"))
    with open(f"./output/{consts.ROUTES_YEAR}/{consts.AIRCRAFT_TYPE_LIMIT}.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(table_data)

def print_map(routes: List[Route], airports: Dict[str, Airport]):
  uffs_green = '#006633'
  water_color = '#B3DDF2'
  land_color = '#F5F5F5'
  states_line_color = '#999999'
  texts_back_color = '#FFFFFF'

  graph = nx.DiGraph()

  for route in routes:
    origin = airports.get(route.origin)
    destination = airports.get(route.destination)
    graph.add_node(route.origin, coord=(origin.lon_geo_point, origin.lat_geo_point))
    graph.add_node(route.destination, coord=(destination.lon_geo_point, destination.lat_geo_point))
    graph.add_edge(route.origin, route.destination)

  coords = nx.get_node_attributes(graph, 'coord')
  all_lons = [lon for lon, lat in coords.values()]
  all_lats = [lat for lon, lat in coords.values()]
  margin = 4

  plt.figure(figsize=(12, 10))
  ax = plt.axes(projection=ccrs.PlateCarree())
  ax.set_extent([
    min(all_lons) - margin, max(all_lons) + margin,
    min(all_lats) - margin, max(all_lats) + margin
  ])

  ax.add_feature(cfeature.LAND, facecolor=land_color)
  ax.add_feature(cfeature.OCEAN, facecolor=water_color)
  ax.add_feature(cfeature.LAKES, facecolor=water_color)
  ax.add_feature(cfeature.RIVERS, edgecolor=water_color)

  estados = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none',
    edgecolor=states_line_color,
    linestyle=':',
    linewidth=1
  )
  ax.add_feature(estados)

  shapename = 'admin_0_countries'
  countries_shp = shpreader.natural_earth(resolution='50m', category='cultural', name=shapename)
  for country in shpreader.Reader(countries_shp).records():
    if country.attributes['NAME_LONG'] == 'Brazil':
      geom = country.geometry
      ax.add_geometries(
        [geom],
        ccrs.PlateCarree(),
        facecolor='none',
        edgecolor=uffs_green,
        linewidth=1.0,
        linestyle='solid'
      )

  texts = []
  for node, (lon, lat) in coords.items():
    hub_node = max(graph.nodes, key=lambda n: graph.degree(n))
    fontweight = 'bold' if node == hub_node else 'normal'

    ax.plot(lon, lat, 'o', color=uffs_green, markersize=5, transform=ccrs.PlateCarree())
    text = ax.text(
      lon, lat, node,
      transform=ccrs.PlateCarree(),
      fontsize=8,
      fontweight=fontweight,
      color=uffs_green,
      bbox=dict(facecolor=texts_back_color, edgecolor='none', alpha=0.75, boxstyle='round,pad=0.2')
    )
    texts.append(text)
  adjust_text(texts, only_move={'points': 'y', 'texts': 'xy'}, autoalign='y', expand_text=(1.1, 1.2))

  for u, v in graph.edges():
    lon1, lat1 = coords[u]
    lon2, lat2 = coords[v]

    curved_lons, curved_lats = curved_line(lon1, lat1, lon2, lat2)
    ax.plot(curved_lons, curved_lats, color=uffs_green, linewidth=1, alpha=0.8, transform=ccrs.PlateCarree())

  plt.savefig(f"./output/{consts.ROUTES_YEAR}/air_network_map.png", dpi=300, bbox_inches="tight")

def curved_line(lon1, lat1, lon2, lat2, n_points=100, curvature_factor=0.3):
  mid_lon = (lon1 + lon2) / 2
  mid_lat = (lat1 + lat2) / 2

  dx = lon2 - lon1
  dy = lat2 - lat1
  dist = np.hypot(dx, dy)

  if dist == 0:
    return [lon1] * n_points, [lat1] * n_points

  curvature = curvature_factor * dist

  mid_lat += curvature

  curve = []
  for i in range(n_points):
    t = i / (n_points - 1)
    lon = (1 - t)**2 * lon1 + 2 * (1 - t) * t * mid_lon + t**2 * lon2
    lat = (1 - t)**2 * lat1 + 2 * (1 - t) * t * mid_lat + t**2 * lat2
    curve.append((lon, lat))

  return zip(*curve)

def output_filename(extension: str) -> str:
  return f"./output/{consts.ROUTES_YEAR}/{consts.AIRCRAFT_TYPE_LIMIT}.{extension}"