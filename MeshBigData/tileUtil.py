import math


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) +
                                (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)


def numTiles(z):
    return(math.pow(2, z))


def latEdges(y, z):
    n = numTiles(z)
    unit = 1 / n
    relY1 = y * unit
    relY2 = relY1 + unit
    lat1 = mercatorToLat(math.pi * (1 - 2 * relY1))
    lat2 = mercatorToLat(math.pi * (1 - 2 * relY2))
    return(lat1, lat2)


def Radians(angle):
    return angle * math.pi / 180


def lonEdges(x, z):
    n = numTiles(z)
    unit = 360 / n
    lon1 = -180 + x * unit
    lon2 = lon1 + unit
    return(lon1, lon2)


def tileEdges(x, y, z):
    lat1, lat2 = latEdges(y, z)
    lon1, lon2 = lonEdges(x, z)
    return((lat2, lon1, lat1, lon2))  # S,W,N,E


def mercatorToLat(mercatorY):
    return(math.degrees(math.atan(math.sinh(mercatorY))))


def tileSizePixels():
    return(256)


def tileLayerExt(layer):
    if(layer in ('oam')):
        return('jpg')
    return('png')


def getCentroid(polygon):
    totalArea = 0
    totalX = 0
    totalY = 0
    points = polygon[0]

    for i in range(len(points)):
        if i == len(points)-1:
            a = points[0]
        else:
            a = points[i + 1]
            
        b = points[i]

        area = 0.5 * (a[0] * b[1] - b[0] * a[1])
        x = (a[0] + b[0]) / 3
        y = (a[1] + b[1]) / 3

        totalArea += area
        totalX += area * x
        totalY += area * y

    return [totalX / totalArea, totalY / totalArea]


# a = deg2num(45.55, 118.171715, 15)
# b = tileEdges(a[0], a[1], 15)
# print(a, b)
# print(b[2] - b[0], b[3] - b[1], (b[3] - b[1])
    #   * math.cos(Radians((b[0] + b[2]) / 2)))
