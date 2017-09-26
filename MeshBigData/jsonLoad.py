import tileUtil
import random
import insertFuc
import re
import requests
import dllUtil
import ctypes 


class JsonLoad(object):
    def __init__(self, jsonUrl="https://{s}.data.osmbuildings.org/0.2/anonymous/tile/15"):
        # jsonUrl='https://{s}.data.osmbuildings.org/0.2/anonymous/tile/15/'
        self.jsonUrl = jsonUrl

    def genUrlPoToBd(self, po1, level):
        url = "http://47.92.3.2:800/geoSOT-API/Point2Code/{0}/{1}/{2}".format(
            po1[0], po1[1], level)
        return url

    def genUrlBdToRange(self, bd):
        url = "http://47.92.3.2:800/geoSOT-API/Code2Range/{0}".format(bd)
        return url

    def getBound(self, coordinates):
        minX = coordinates[0][0]
        minY = coordinates[0][1]
        maxX = coordinates[0][0]
        maxY = coordinates[0][1]
        for i in range(len(coordinates)):
            if (minX > coordinates[i][0]):
                minX = coordinates[i][0]

            if (minY > coordinates[i][1]):
                minY = coordinates[i][1]

            if (maxX < coordinates[i][0]):
                maxX = coordinates[i][0]

            if (maxY < coordinates[i][1]):
                maxY = coordinates[i][1]

        # rect = [minX, minY, maxX, maxY]
        return [
            [minX, minY],
            [minX, maxY],
            [maxX, maxY],
            [maxX, minY]
        ]

    def getBdOfPoint(self, po, level):
        # urlStr = self.genUrlPoToBd(po, level)
        # jsonBd = requests.get(urlStr).json()
        # return jsonBd['bdCode']

        gcode2d = dllUtil.getGCode2DOfPoint(ctypes.c_double(
            po[0]), ctypes.c_double(po[1]), ctypes.c_int(level))
        return dllUtil.toGCodeFromGCode2D(gcode2d)

    def getCbdOfPolygon(self, polygon):
        center = tileUtil.getCentroid(polygon)
        # urlStr = self.genUrlPoToBd(center, 31)
        # jsonBd = requests.get(urlStr).json()
        gcode2d = dllUtil.getGCode2DOfPoint(ctypes.c_double(
            center[0]), ctypes.c_double(center[1]), ctypes.c_int(31))
        gcode = dllUtil.toGCodeFromGCode2D(gcode2d)
        # return [jsonBd['bdCode'], [center]]
        return [gcode, [center]]

    def getBoundBd(self, coordinates):
        polyBound = self.getBound(coordinates)
        ra = list(range(1, 25))
        ra.reverse()
        for i in ra:
            bdcodett = None
            flag = True
            for j in range(len(polyBound)):
                # urlStr = self.genUrlPoToBd(polyBound[j], i)
                # jsonBd = requests.get(urlStr).json()
                gcode2d = dllUtil.getGCode2DOfPoint(ctypes.c_double(
                    polyBound[j][0]), ctypes.c_double(polyBound[j][1]), ctypes.c_int(i))
                gcode = dllUtil.toGCodeFromGCode2D(gcode2d)
                if bdcodett is None:
                    # bdcodett = jsonBd['bdCode']
                    bdcodett = gcode
                else:
                    # codee = jsonBd['bdCode']
                    codee = gcode
                    if bdcodett == codee:
                        flag = True
                    else:
                        flag = False
                if flag:
                    continue
                else:
                    break
            if flag:
                tmp = polyBound[0]
                polyBound.append(tmp)
                return [bdcodett, i, [polyBound]]

    def getIntrestBd(self, coordinates):
        polyBound = self.getBound(coordinates)
        ra = list(range(8, 28))

        for i in ra:

            center = tileUtil.getCentroid([coordinates])

            # urlStr = self.genUrlPoToBd(center, i)
            # jsonBd = requests.get(urlStr).json()
            gcode2d = dllUtil.getGCode2DOfPoint(ctypes.c_double(
                center[0]), ctypes.c_double(center[1]), ctypes.c_int(31))
            gcode = dllUtil.toGCodeFromGCode2D(gcode2d)

            bdcodett = gcode
            # bdcodett = jsonBd['bdCode']
            # recUrlStr = self.genUrlBdToRange(bdcodett)
            # recRange = requests.get(recUrlStr).json()
            # recRange = recRange['range']
            recRange = dllUtil.toGeoRangeFromGCode2D(gcode2d)

            # if recRange['minLon'] > polyBound[0][0] and recRange['minLat'] > polyBound[0][1] and recRange['maxLon'] < polyBound[2][0] and recRange['maxLat'] < polyBound[2][1]:
            #     rect = [[[recRange['minLon'], recRange['minLat']], [recRange['minLon'], recRange['maxLat']], [
            #         recRange['maxLon'], recRange['maxLat']], [recRange['maxLon'], recRange['minLat']], [recRange['minLon'], recRange['minLat']]]]
            if recRange.minLon > polyBound[0][0] and recRange.minLat > polyBound[0][1] and recRange.maxLon < polyBound[2][0] and recRange.maxLat < polyBound[2][1]:
                rect = [[[recRange.minLon, recRange.minLat], [recRange.minLon, recRange.maxLat], [
                    recRange.maxLon, recRange.maxLat], [recRange.maxLon, recRange.minLat], [recRange.minLon, recRange.minLat]]]

                return [bdcodett, i, rect]

    def _polyFormat(self, coordinates):
        polyloop = coordinates
        if len(polyloop) < 2:
            return 'SRID=4326;POINT(' + str(polyloop[0][0]) + ' ' + str(polyloop[0][1]) + ')'
        points = []
        for po in polyloop:
            point = ' '.join(map(str, po))
            points.append(point)

        lineStringFormat = 'SRID=4326;POLYGON((' + ','.join(points) + '))'

        return lineStringFormat

    # Rect=[[min,min],[max,max]]
    def pushJsonData(self, Rect=[[116.38156,39.914714], [116.537074,40.0284]]):
        sqlHelper = insertFuc.pgsqlHelper()
        insertRule = '''CREATE OR REPLACE RULE insert_ignore_on_nodes AS
                ON INSERT TO bjmap.nodes
                WHERE EXISTS (SELECT 1 FROM bjmap.nodes WHERE bdc = NEW.bdc)
                DO INSTEAD NOTHING'''
        insertRule2 = '''CREATE OR REPLACE RULE insert_ignore_on_attributes AS
                ON INSERT TO bjmap.attributes
                WHERE EXISTS (SELECT 1 FROM bjmap.attributes WHERE bdc = NEW.bdc)
                DO INSTEAD NOTHING'''
        sqlHelper.executeNonQurery(insertRule)
        sqlHelper.executeNonQurery(insertRule2)

        if re.match(r'^https?:/{2}.+$', self.jsonUrl):

            minLat = Rect[0][1]
            minLon = Rect[0][0]
            maxLat = Rect[1][1]
            maxLon = Rect[1][0]
            try:
                while minLat <= maxLat:
                    minLon = Rect[0][0]
                    high = 0
                    wigth = 0
                    while minLon <= maxLon:
                        tileNum = tileUtil.deg2num(minLat, minLon, 15)
                        tileEdge = tileUtil.tileEdges(
                            tileNum[0], tileNum[1], 15)
                        high = tileEdge[2] - tileEdge[0]
                        wigth = tileEdge[3] - tileEdge[1]

                        s = random.choice(['a', 'b', 'c'])
                        jsonU = self.jsonUrl.replace('{s}', s)
                        urlStr = jsonU + '/' + \
                            str(tileNum[0]) + '/' + str(tileNum[1]) + '.json'
                        r = requests.get(urlStr)
                        if r.text == '':
                            print('continue!')
                            r.close()
                            continue
                        jsonData = r.json()
                        features = jsonData['features']
                        insertNodes = ""
                        insertAttri = ""
                        for feature in features:
                            ide = feature['id']
                            proer = feature['properties']
                            geome = feature['geometry']
                            typee = geome['type']
                            name = 'building'
                            coordinates = geome['coordinates']
                            bdc = self.getCbdOfPolygon(coordinates)
                            bdb = self.getBoundBd(coordinates[0])
                            # bdi = self.getIntrestBd(coordinates[0])

                            insertNodes += "({0},{1},'{2}','{3}','{4}',ST_GeomFromEWKT('{5}'),ST_GeomFromEWKT('{6}'),ST_GeomFromEWKT('{7}'),{8})".format(bdc[0], bdb[0], ide, typee, name, self._polyFormat(bdc[1]), self._polyFormat(coordinates[0]), self._polyFormat(bdb[2][0]), bdb[1])
                            insertNodes += ', '

                            insertAttri += "({0},{1},'{2}','{3}',{4},{5})".format(bdc[0], bdb[0], ide, 'red', 3, 1)
                            insertAttri += ', '


                            # insertStr = "INSERT INTO bjmap.nodes (bdc, bdb, id, type, name, center, bounder, bdbounder, levelb) VALUES(%s,%s,%s,%s,%s,ST_GeomFromEWKT(%s),ST_GeomFromEWKT(%s),ST_GeomFromEWKT(%s),%s)"
                            # sqlHelper.executeNonQurery(insertStr, (bdc[0], bdb[0], ide, typee, name, self._polyFormat(bdc[1]), self._polyFormat(coordinates[0]), self._polyFormat(bdb[2][0]), bdb[1]))
                            # insertStr2 = "INSERT INTO bjmap.attributes (bdc, bdb, id, color, height, minheight) VALUES(%s, %s, %s, %s, %s, %s)"
                            # sqlHelper.executeNonQurery(insertStr2, (bdc[0], bdb[0], ide, 'red', 3, 1))

                        insertNodes = insertNodes.rstrip(', ')
                        insertAttri = insertAttri.rstrip(', ')
                        insertNodes = "INSERT INTO bjmap.nodes (bdc, bdb, id, type, name, center, bounder, bdbounder, levelb) VALUES " + insertNodes
                        insertAttri = "INSERT INTO bjmap.attributes (bdc, bdb, id, color, height, minheight) VALUES " + insertAttri
                        sqlHelper.executeNonQurery(insertNodes)
                        sqlHelper.executeNonQurery(insertAttri)
                        r.close()
                        minLon += wigth

                    minLat += high
            finally:
                sqlHelper.closeConnection()
        rulStr = 'DROP RULE insert_ignore_on_nodes ON bjmap.nodes'
        rulStr2 = 'DROP RULE insert_ignore_on_attributes ON bjmap.attributes'
        sqlHelper.executeNonQurery(rulStr)
        sqlHelper.executeNonQurery(rulStr2)
        sqlHelper.closeConnection()


jstest = JsonLoad()
jstest.pushJsonData()
