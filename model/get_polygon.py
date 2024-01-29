def get_polygon(lons, lats, color='blue'):
    if len(lons) != len(lats):
        raise ValueError('the legth of longitude list  must coincide with that of latitude')
    geojd = {"type": "FeatureCollection"}
    geojd['features'] = []
    coords = []
    for lon, lat in zip(lons, lats): 
        coords.append((lon, lat))   
    coords.append((lons[0], lats[0]))  #close the polygon  
    geojd['features'].append({ "type": "Feature",
                               "geometry": {"type": "Polygon",
                                            "coordinates": [coords] }})
    layer=dict(sourcetype = 'geojson',
             source =geojd,
             below='',  
             type = 'fill',   
             color = color,
             opacity = 0.8)
    return layer