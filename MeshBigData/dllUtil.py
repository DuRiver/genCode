import ctypes
import sys

'''*! \enum Direction
 * 旋转角ξ：以绝对正北方向为准线，顺时针为正，逆时针为负，取值范围为0<ξ<2π
 *
 * 方位定义如下：
 *
 * 0 -> DUENORTH	  正北	  0	   <= ξ <=   π/8 || 15π/8 < ξ < 2π
 *
 * 1 -> NORTHEAST	  东北	    π/8 < ξ <= 3 π/8
 *
 * 2 -> DUEEAST       正东	  3 π/8 < ξ <= 5 π/8
 *
 * 3 -> SOUTHEAST	  东南	  5 π/8 < ξ <= 7 π/8
 *
 * 4 -> DUESOUTH	  正南	  7 π/8 < ξ <= 9 π/8
 *
 * 5 -> SOUTHWEST	  西南	  9 π/8 < ξ <= 11π/8
 *
 * 6 -> DUEWEST       正西	  11π/8 < ξ <= 13π/8
 *
 * 7 -> NORTHWEST	  西北	  13π/8 < ξ <= 15π/8
 *
 * 100 -> DUPLICATION 重合
 *'''


class MyEnumDirection(ctypes.Structure):
    _fields_ = [('DUENORTH', ctypes.c_uint8), ('NORTHEAST', ctypes.c_uint8), ('DUEEAST', ctypes.c_uint8), ('SOUTHEAST', ctypes.c_uint8), ('DUESOUTH',
                                                                                                                                          ctypes.c_uint8), ('SOUTHWEST', ctypes.c_uint8), ('DUEWEST', ctypes.c_uint8), ('NORTHWEST', ctypes.c_uint8), ('DUPLICATION', ctypes.c_uint8)]


class GCode2D(ctypes.Structure):
    _fields_ = [('layer', ctypes.c_int), ('lonCode',
                                          ctypes.c_uint), ('latCode', ctypes.c_uint)]


class GCode1D(ctypes.Structure):
    _fields_ = [('layer', ctypes.c_int), ('code', ctypes.c_ulonglong)]


class GCodePoint(ctypes.Structure):
    _fields_ = [('layer', ctypes.c_int), ('longitude',
                                          ctypes.c_double), ('latitude', ctypes.c_double)]


class GeoRange(ctypes.Structure):
    _fields_ = [('minLon', ctypes.c_double), ('minLat', ctypes.c_double),
                ('maxLon', ctypes.c_double), ('maxLat', ctypes.c_double)]


class GeoPoint(ctypes.Structure):
    _fields_ = [('longitude', ctypes.c_double), ('latitude', ctypes.c_double)]


class GCodeColRow(ctypes.Structure):
    _fields_ = [('layer', ctypes.c_int),
                ('row', ctypes.c_int), ('col', ctypes.c_int)]


class GCode2DNode(ctypes.Structure):
    pass


GCode2DNode._fields_ = [
    ('code', GCode2D), ('next', ctypes.POINTER(GCode2DNode))]


class GCode2DList(ctypes.Structure):
    pass


GCode2DList._fields_ = [('count', ctypes.c_int), ('head', ctypes.POINTER(
    GCode2DNode)), ('last', ctypes.POINTER(GCode2DNode)), ('list', ctypes.POINTER(GCode2DNode))]


class GCode1DNode(ctypes.Structure):
    pass


GCode1DNode._fields_ = [
    ('code', GCode1D), ('next', ctypes.POINTER(GCode1DNode))]


class GCode1DList(ctypes.Structure):
    pass


GCode1DList._fields_ = [('count', ctypes.c_int), ('head', ctypes.POINTER(
    GCode1DNode)), ('last', ctypes.POINTER(GCode1DNode)), ('list', ctypes.POINTER(GCode1DNode))]


class GCodeNode(ctypes.Structure):
    pass


GCodeNode._fields_ = [('code', ctypes.c_ulonglong),
                      ('next', ctypes.POINTER(GCodeNode))]


class GCodeList(ctypes.Structure):
    pass


GCodeList._fields_ = [('count', ctypes.c_int), ('head', ctypes.POINTER(
    GCodeNode)), ('last', ctypes.POINTER(GCodeNode)), ('list', ctypes.POINTER(GCodeNode))]


class DoubleNode(ctypes.Structure):
    pass


DoubleNode._fields_ = [('value', ctypes.c_double),
                       ('next', ctypes.POINTER(DoubleNode))]


class DoubleList(ctypes.Structure):
    pass


DoubleList._fields_ = [('count', ctypes.c_int), ('head', ctypes.POINTER(
    DoubleNode)), ('last', ctypes.POINTER(DoubleNode)), ('list', ctypes.POINTER(DoubleNode))]


class IntNode(ctypes.Structure):
    pass


IntNode._fields_ = [('value', ctypes.c_double),
                    ('next', ctypes.POINTER(IntNode))]


class IntList(ctypes.Structure):
    pass


IntList._fields_ = [('count', ctypes.c_int), ('head', ctypes.POINTER(
    IntNode)), ('last', ctypes.POINTER(IntNode)), ('list', ctypes.POINTER(IntNode))]


class GCodeLineParam(ctypes.Structure):
    pass


GCodeLineParam._fields_ = [('k', ctypes.c_double),
                           ('b', ctypes.c_double), ('flag', ctypes.c_int)]


class PointCodeNode(ctypes.Structure):
    pass


PointCodeNode._fields_ = [('points', ctypes.POINTER(GeoPoint)), ('pointCount',
                                                                 ctypes.c_int), ('code', GCode2D), ('next', ctypes.POINTER(PointCodeNode))]


class PointCodeList(ctypes.Structure):
    pass


PointCodeList._fields_ = [('count', ctypes.c_int), ('head', ctypes.POINTER(
    PointCodeNode)), ('last', ctypes.POINTER(PointCodeNode)), ('list', ctypes.POINTER(PointCodeNode))]

if sys.platform == 'win32':
    libc = ctypes.cdll.LoadLibrary("GeoSOT.dll")
else:
    libc = ctypes.CDLL('GeoSOT.lib')

myEnumDirection = MyEnumDirection(0, 1, 2, 3, 4, 5, 6, 7, 100)


def toGCode2DFromGCodePoint(codePoint):
    '''**
    * @brief 带有编码层级的经纬度点转二维编码
    * @param codePoint 带有编码层级的经纬度点
    * @return 二维编码
    * @error input valid 返回层级为-1的编码
    *'''
    libc.toGCode2DFromGCodePoint.argtypes = (GCodePoint,)
    libc.toGCode2DFromGCodePoint.restype = GCode2D
    return libc.toGCode2DFromGCodePoint(codePoint)

# GEOSOT_2D_API GCode2D toGCode2DFromGCodePoint(GCodePoint codePoint);


def toGCodePointFromGCode2D(gcode2d):
    '''**
    * @brief 二维编码转带有编码层级的经纬度点
    * @param code 二维编码
    * @return 带有编码层级的经纬度点
    *'''
    libc.toGCodePointFromGCode2D.argtypes = (GCode2D,)
    libc.toGCodePointFromGCode2D.restype = GCodePoint
    return libc.toGCodePointFromGCode2D(gcode2d)

# GEOSOT_2D_API GCodePoint toGCodePointFromGCode2D(GCode2D code);


def toGCode1DFromGCode2D(gcode2d):
    '''**
    * @brief 二维编码转一维编码
    * @param code 二维编码
    * @return 一维编码
    *'''
    libc.toGCode1DFromGCode2D.argtypes = (GCode2D,)
    libc.toGCode1DFromGCode2D.restype = GCode1D
    return libc.toGCode1DFromGCode2D(gcode2d)

# GEOSOT_2D_API GCode1D toGCode1DFromGCode2D(GCode2D code);


def toGCode2DFromGCode1D(gcode1d):
    '''**
    * @brief 一维编码转二维编码
    * @param code 一维编码
    * @return 二维编码
    *'''
    libc.toGCode2DFromGCode1D.argtypes = (GCode1D,)
    libc.toGCode2DFromGCode1D.restype = GCode2D
    return libc.toGCode2DFromGCode1D(gcode1d)

# GEOSOT_2D_API GCode2D toGCode2DFromGCode1D(GCode1D code);


def isGCode2DExistent(gcode2d):
    '''**
    * @brief 二维编码对应区域是否真实存在
    * @param code 二维编码
    * @return true存在，false不存在
    *'''
    libc.isGCode2DExistent.argtypes = (GCode2D,)
    libc.isGCode2DExistent.restype = ctypes.c_bool
    return libc.isGCode2DExistent(gcode2d)

# GEOSOT_2D_API bool isGCode2DExistent(GCode2D code);


def toGeoRangeFromGCode2D(gcode2d):
    '''**
    * @brief 二维编码转地理范围
    * @param code 二维编码
    * @return 地理范围
    *'''
    libc.toGeoRangeFromGCode2D.argtypes = (GCode2D,)
    libc.toGeoRangeFromGCode2D.restype = GeoRange
    return libc.toGeoRangeFromGCode2D(gcode2d)

# GEOSOT_2D_API GeoRange toGeoRangeFromGCode2D(GCode2D code);


def toGCodeColRowFromGCode2D(gcode2d):
    '''**
    * @brief 二维编码转编码行列号
    * @param code 二维编码
    * @return 编码行列号
    *'''
    libc.toGCodeColRowFromGCode2D.argtypes = (GCode2D,)
    libc.toGCodeColRowFromGCode2D.restype = GCodeColRow
    return libc.toGCodeColRowFromGCode2D(gcode2d)

# GEOSOT_2D_API GCodeColRow toGCodeColRowFromGCode2D(GCode2D code);


def toGCode2DFromGCodeColRow(gcodecolrow):
    '''**
    * @brief 编码行列号转二维编码
    * @param colRow 编码行列号
    * @return 二维编码
    *'''
    libc.toGCode2DFromGCodeColRow.argtypes = (GCodeColRow,)
    libc.toGCode2DFromGCodeColRow.restype = GCode2D
    return libc.toGCode2DFromGCodeColRow(gcodecolrow)

# GEOSOT_2D_API GCode2D toGCode2DFromGCodeColRow(GCodeColRow colRow);


def displaceGCode2D(gcode2d, dispOfLon, dispOfLat):
    '''**
    * @brief 二维编码位移运算
    * @param code 二维编码
    * @param dispOfLon 经度方向位移量>0：右移；=0：静止；<0：左移
    * @param dispOfLat 纬度方向位移量>0：上移；=0：静止；<0：下移
    * @return 二维编码
    *'''
    libc.displaceGCode2D.argtypes = (GCode2D, ctypes.c_int, ctypes.c_int)
    libc.displaceGCode2D.restype = GCode2D
    return libc.displaceGCode2D(gcode2d, dispOfLon, dispOfLat)
# GEOSOT_2D_API GCode2D displaceGCode2D(GCode2D code, int dispOfLon, int dispOfLat);


'''**
* @brief 按Z序对二维编码进行排序
* @param list 二维编码链表指针
* @return 二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * sortGCode2DByZOrder(GCode2DList *list);

'''**
* @brief 计算二维编码的四个子编码对应区域真实存在的数量
* @param code 二维编码
* @return 对应区域真实存在的子编码的数量
*'''
# GEOSOT_2D_API int getRealAreaCountOfSonCodeOfGCode2D(GCode2D code);

'''**
* @brief 二维编码去重
* @param list 二维编码链表指针
* @return 去重后的二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * getUniqueGCode2D(GCode2DList *list);

'''**
* @brief 同层级二维编码聚合
* @param list 二维编码链表指针
* @return 聚合后的二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * togetherGCode2DOfSameLayer(GCode2DList *list);


def getGeographicRange(geopointP, pointCount):
    '''**
    * @brief 计算点的地理范围
    * @param points 点的指针
    * @param pointCount 点的数量
    * @return 地理范围
    *'''
    libc.getGeographicRange.argtypes = (ctypes.POINTER(GeoPoint), ctypes.c_int)
    libc.getGeographicRange.restype = GeoRange
    return libc.getGeographicRange(geopointP, pointCount)

# GEOSOT_2D_API GeoRange getGeographicRange(GeoPoint *points, int pointCount);


def getOnlyOneGCode2D(minLon, maxLon, minLat, maxLat):
    '''**
    * @brief 只得到一个完全覆盖的二维编码
    * @param minLon 最小经度
    * @param maxLon 最大经度
    * @param minLat 最小纬度
    * @param maxLat 最大纬度
    * @return 二维编码
    *'''
    libc.getOnlyOneGCode2D.argtypes = (
        ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    libc.getOnlyOneGCode2D.restype = GCode2D
    return libc.getOnlyOneGCode2D(minLon, maxLon, minLat, maxLat)

# GEOSOT_2D_API GCode2D getOnlyOneGCode2D(double minLon, double maxLon, double minLat, double maxLat);


'''**
* @brief 只得到一个完全覆盖的二维编码
* @param points 点的指针
* @param pointCount 点的数量
* @return 二维编码
*'''
# GEOSOT_2D_API GCode2D getOnlyOneGCode2DV2(GeoPoint *points, int pointCount);


def getGeoCenterOfGCode2D(gcode2d):
    '''**
    * @brief 计算二维编码的地理中心点
    * @param code 二维编码
    * @return 地理点
    *'''
    libc.getGeoCenterOfGCode2D.argtypes = (GCode2D,)
    libc.getGeoCenterOfGCode2D.restype = GeoPoint
    return libc.getGeoCenterOfGCode2D(gcode2d)

# GEOSOT_2D_API GeoPoint getGeoCenterOfGCode2D(GCode2D code);


def getGCode2DOfPoint(longitude, latitude, layer):
    '''**
    * @brief 计算点的二维编码
    * @param longitude 点的经度，范围是[-180.0,180.0]
    * @param latitude 点的纬度，范围是[-90.0,90.0]
    * @param layer 层级，范围是[1,32]
    * @return 二维编码
    *'''
    libc.getGCode2DOfPoint.argtypes = (
        ctypes.c_double, ctypes.c_double, ctypes.c_int)
    libc.getGCode2DOfPoint.restype = GCode2D
    return libc.getGCode2DOfPoint(longitude, latitude, layer)

# GEOSOT_2D_API GCode2D getGCode2DOfPoint(double longitude, double latitude, int layer);


def getGCode2DOfLine(geopoint1, geopoint2, layer):
    '''**
    * @brief 计算线的二维编码
    * @param p1 起点
    * @param p2 终点
    * @param layer 层级，范围是[1,32]
    * @return 二维编码链表指针
    *'''
    libc.getGCode2DOfLine.argtypes = (GeoPoint, GeoPoint, ctypes.c_int)
    libc.getGCode2DOfLine.restype = ctypes.POINTER(GCode2DList)
    return libc.getGCode2DOfLine(geopoint1, geopoint2, layer)

# GEOSOT_2D_API GCode2DList * getGCode2DOfLine(GeoPoint p1, GeoPoint p2, int layer);


def getGCode2DOfPolyline(pointsP, pointCount, layer):
    '''**
    * @brief 计算多线的二维编码
    * @param points 点的指针
    * @param pointCount 点的数量
    * @param layer 层级，范围是[1,32]
    * @return 二维编码链表指针
    *'''
    libc.getGCode2DOfPolyline.argtypes = (ctypes.POINTER(GeoPoint), ctypes.c_int, ctypes.c_int)
    libc.getGCode2DOfPolyline.restype = ctypes.POINTER(GCode2DList)
    return libc.getGCode2DOfPolyline(pointsP, pointCount, layer)
# GEOSOT_2D_API GCode2DList * getGCode2DOfPolyline(GeoPoint *points, int pointCount, int layer);

def getGCode2DOfPolygon(pointsP, pointCount, layer):
    '''**
    * @brief 计算多边形的二维编码
    * @param points 点的指针
    * @param pointCount 点的数量
    * @param layer 层级，范围是[1,32]
    * @return 二维编码链表指针
    *'''
    libc.getGCode2DOfPolygon.argtypes = (ctypes.POINTER(GeoPoint), ctypes.c_int, ctypes.c_int)
    libc.getGCode2DOfPolygon.restype = ctypes.POINTER(GCode2DList)
    return libc.getGCode2DOfPolygon(pointsP, pointCount, layer)
# GEOSOT_2D_API GCode2DList * getGCode2DOfPolygon(GeoPoint *points, int pointCount, int layer);

'''**
* @brief 计算(复杂)多边形的二维编码
* @param points 点的指针
* @param pointCount 点的数量
* @param innerPoint 多边形内部一点
* @param layer 层级，范围是[1,32]
* @return 二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * getGCode2DOfComplexPolygon(GeoPoint *points, int pointCount, GeoPoint innerPoint, int layer);

'''**
* @brief 计算多边形的某一层级的1~4个二维编码
* @param points 点的指针
* @param pointCount 点的数量
* @return 二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * get1To4GCode2DOfPolygon(GeoPoint *points, int pointCount);

'''**
* @brief 计算平行四边形的二维编码
* @param points 点的指针
* @param layer 层级，范围是[1,32]
* @return 二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * getGCode2DOfParallelogram(GeoPoint *points, int layer);

'''**
* @brief 计算矩形的二维编码
* @param leftTopLon 左上角经度
* @param leftTopLat 左上角纬度
* @param rightBottomLon 右下角经度
* @param rightBottomLat 右下角纬度
* @param layer 层级，范围是[1,32]
* @return 二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * getGCode2DOfRectangle(double leftTopLon, double leftTopLat, double rightBottomLon, double rightBottomLat, int layer);

'''**
* @brief 计算二维编码的父编码
* @param code 二维编码
* @param generation 代数 >0；=1：父编码；=2：祖父编码...
* @return 二维编码
*'''
# GEOSOT_2D_API GCode2D getFatherOfGCode2D(GCode2D code, int generation);

'''**
* @brief 判断二维编码subject是不是二维编码attribute的父编码
* @param subject 主语，二维编码
* @param attribute 定语，二维编码
* @return true，是；false，不是
*'''
# GEOSOT_2D_API bool isFatherGCode2DOf(GCode2D subject, GCode2D attribute);

'''**
* @brief 计算二维编码的子编码
* @param code 二维编码
* @param generation 代数 >0；=1：子编码；=2：孙子编码...
* @return 二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * getSonOfGCode2D(GCode2D code, int generation);

'''**
* @brief 判断二维编码subject是不是二维编码attribute的子编码
* @param subject 主语，二维编码
* @param attribute 定语，二维编码
* @return true，是；false，不是
*'''
# GEOSOT_2D_API bool isSonGCode2DOf(GCode2D subject, GCode2D attribute);

'''**
* @brief 计算二维编码的四邻域
* @param code 二维编码
* @return 二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * get4NeighborOfGCode2D(GCode2D code);

'''**
* @brief 计算二维编码的八邻域
* @param code 二维编码
* @return 二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * get8NeighborOfGCode2D(GCode2D code);

'''**
* @brief 计算二维编码之间的包含关系
* @param code1 二维编码
* @param code2 二维编码
* @return -1:不包含；0：相等；1：code1包含code2；2：code2包含code1
*'''


# GEOSOT_2D_API int judgeContainRelationOfGCode2D(GCode2D code1, GCode2D code2);

'''**
* @brief 计算二维编码链表的交集
* @param list1 二维编码链表指针
* @param list2 二维编码链表指针
* @return 二维编码链表交集的指针
*'''
# GEOSOT_2D_API GCode2DList * getIntersectionOfGCode2Ds(GCode2DList *list1, GCode2DList *list2);

'''**
* @brief 计算二维编码的交集
* @param code1 二维编码
* @param code2 二维编码
* @return 相交二维编码，若无相交区域，返回的二维编码层级为-1
*'''
# GEOSOT_2D_API GCode2D getIntersectionOfGCode2D(GCode2D code1, GCode2D code2);

'''**
* @brief 计算二维编码链表的并集
* @param list1 二维编码链表指针
* @param list2 二维编码链表指针
* @return 二维编码链表并集的指针
*'''
# GEOSOT_2D_API GCode2DList * getUnionOfGCode2Ds(GCode2DList *list1, GCode2DList *list2);

'''**
* @brief 计算二维编码的并集
* @param code1 二维编码
* @param code2 二维编码
* @return 二维编码链表并集的指针
*'''
# GEOSOT_2D_API GCode2DList * getUnionOfGCode2D(GCode2D code1, GCode2D code2);

'''**
* @brief 计算二维编码的格网缓冲区
* @param list 二维编码链表指针
* @param gridCount 缓冲网格的个数
* @param layer 层级，范围是[1,32]
* @return 缓冲区的二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * getBufferOfGCode2DsByGrid(GCode2DList *list, int gridCount, int layer);

'''**
* @brief 计算二维编码的距离缓冲区
* @param list 二维编码链表指针
* @param distance 距离，单位为米
* @param layer 层级，范围是[1,32]
* @return 缓冲区的二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * getBufferOfGCode2DsByDistance(GCode2DList *list, double distance, int layer);

'''**
* @brief 计算二维编码链表的重心
* @param list 二维编码链表指针
* @return 重心二维编码
*'''
# GEOSOT_2D_API GCode2D getBaryCenterOfGCode2Ds(GCode2DList *list);

'''**
* @brief 计算二维编码对应网格的经向和纬向的长度
* @param code 二维编码
* @param flag 纬向边长类型标识，0：靠近赤道的纬向边长；2：远离赤道的纬向边长；1：纬度为两者平均值的纬向边长。
* @return GeoPoint.longitude表示经向长度，GeoPoint.latitude表示纬向长度
* @note 输入标识取值不等于0,1,2时，不计算B_Length
*'''
# GEOSOT_2D_API GeoPoint getLengthsOfGCode2D(GCode2D code, int flag);


def toGCodeFromGCode1D(gcode1d):
    '''**
    * @brief 一维编码转整型编码
    * @param code 一维编码
    * @return 整型编码
    * @note 如果一维编码的层级等于32，将返回0。
    *'''
    libc.toGCodeFromGCode1D.argtypes = (GCode1D,)
    libc.toGCodeFromGCode1D.restype = ctypes.c_ulonglong
    return libc.toGCodeFromGCode1D(gcode1d)

# GEOSOT_2D_API unsigned long long toGCodeFromGCode1D(GCode1D code);


def toGCodeFromGCode2D(gcode2d):
    '''**
    * @brief 二维编码转整型编码
    * @param code 二维编码
    * @return 整型编码
    * @note 如果一维编码的层级等于32，将返回0。
    *'''
    libc.toGCodeFromGCode2D.argtypes = (GCode2D,)
    libc.toGCodeFromGCode2D.restype = ctypes.c_ulonglong
    return libc.toGCodeFromGCode2D(gcode2d)

# GEOSOT_2D_API unsigned long long toGCodeFromGCode2D(GCode2D code);


def toGCode1DFromGCode(ullcode):
    '''**
    * @brief 整型编码转一维编码
    * @param code 整型编码
    * @return 一维编码
    *'''
    libc.toGCode1DFromGCode.argtypes = (ctypes.c_ulonglong,)
    libc.toGCode1DFromGCode.restype = GCode1D
    return libc.toGCode1DFromGCode(ullcode)

# GEOSOT_2D_API GCode1D toGCode1DFromGCode(unsigned long long code);


def toGCode2DFromGCode(ullcode):
    '''**
    * @brief 整型编码转二维编码
    * @param code 整型编码
    * @return 二维编码
    *'''
    libc.toGCode2DFromGCode.argtypes = (ctypes.c_ulonglong,)
    libc.toGCode2DFromGCode.restype = GCode2D
    return libc.toGCode2DFromGCode(ullcode)

# GEOSOT_2D_API GCode2D toGCode2DFromGCode(unsigned long long code);


def getLayerOfGCode(ullcode):
    '''**
    * @brief 计算整型编码所在层级
    * @param code 整型编码
    * @return 层级，范围是[1,31]
    *'''
    libc.getLayerOfGCode.argtypes = (ctypes.c_ulonglong,)
    libc.getLayerOfGCode.restype = ctypes.c_int
    return libc.getLayerOfGCode(ullcode)

# GEOSOT_2D_API int getLayerOfGCode(unsigned long long code);


def getMinSonOfGCode(ullcode):
    '''**
    * @brief 计算整型编码的最小子编码
    * @param code 整型编码
    * @return 整型编码
    *'''
    libc.getMinSonOfGCode.argtypes = (ctypes.c_ulonglong,)
    libc.getMinSonOfGCode.restype = ctypes.c_ulonglong
    return libc.getMinSonOfGCode(ullcode)

# GEOSOT_2D_API unsigned long long getMinSonOfGCode(unsigned long long code);


def getMaxSonOfGCode(ullcode):
    '''**
    * @brief 计算整型编码的最大子编码
    * @param code 整型编码
    * @return 整型编码
    *'''
    libc.getMaxSonOfGCode.argtypes = (ctypes.c_ulonglong,)
    libc.getMaxSonOfGCode.restype = ctypes.c_ulonglong
    return libc.getMaxSonOfGCode(ullcode)

# GEOSOT_2D_API unsigned long long getMaxSonOfGCode(unsigned long long code);


def getFatherOfGCode(ullcode):
    '''**
    * @brief 计算整型编码的直系父编码
    * @param code 整型编码
    * @return 整型编码
    *'''
    libc.getFatherOfGCode.argtypes = (ctypes.c_ulonglong,)
    libc.getFatherOfGCode.restype = ctypes.c_ulonglong
    return libc.getFatherOfGCode(ullcode)

# GEOSOT_2D_API unsigned long long getFatherOfGCode(unsigned long long code);


'''**
* @brief 计算多边形的N层二维编码
* @param points 点的指针
* @param pointCount 点的数量
* @param maxLayer 最大层级，范围是[1,32]
* @return 二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * getNLayersGCode2DOfPolygon(GeoPoint *points, int pointCount, int maxLayer);

'''**
* @brief 计算正数方向的经(纬)度线
* @param minValue 最小经(纬)度
* @param maxValue 最小经(纬)度
* @param layer 层级
* @return double型链表的指针
*'''
# GEOSOT_2D_API DoubleList * getPositiveLines(double minValue, double maxValue, int layer);

'''**
* @brief 根据经度跨度或者纬度跨度计算自适应层级
* @param delta 经度跨度或者纬度跨度
* @return 层级，范围是[4,32]
*'''
# GEOSOT_2D_API int getAdaptiveLayerByDelta(double delta);

'''**
* @brief 计算所有的经(纬)度线
* @param minValue 最小经(纬)度
* @param maxValue 最大经(纬)度
* @param layer 层级，范围是[1,32]
* @return double型链表指针
*'''
# GEOSOT_2D_API DoubleList * getAllLines(double minValue, double maxValue, int layer);

'''**
* @brief 计算自适应的所有的经(纬)度线
* @param minValue 最小经(纬)度
* @param maxValue 最大经(纬)度
* @return double型链表指针
*'''
# GEOSOT_2D_API DoubleList * getAdaptivePositiveLines(double minValue, double maxValue);

'''**
* @brief 计算自适应的所有的经(纬)度线
* @param minValue 最小经(纬)度
* @param maxValue 最大经(纬)度
* @return double型链表指针
*'''
# GEOSOT_2D_API DoubleList * getAdaptiveAllLines(double minValue, double maxValue);

'''**
* @brief 一维编码链表转二维编码链表
* @param list 一维编码链表指针
* @return 二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * toGCode2DListFromGCode1DList(GCode1DList *list);

'''**
* @brief 整型编码链表转二维编码链表
* @param list 整型编码链表指针
* @return 二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * toGCode2DListFromGCodeList(GCodeList *list);

'''**
* @brief 整型编码链表转一维编码链表
* @param list 整型编码链表指针
* @return 一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * toGCode1DListFromGCodeList(GCodeList *list);

'''**
* @brief 二维编码链表转一维编码链表
* @param list 二维编码链表指针
* @return 一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * toGCode1DListFromGCode2DList(GCode2DList *list);

'''**
* @brief 二维编码链表转整型编码链表
* @param list 二维编码链表指针
* @return 整型编码链表指针
* @note 注意二维编码链表的层级不能等于32
*'''
# GEOSOT_2D_API GCodeList * toGCodeListFromGCode2DList(GCode2DList *list);

'''**
* @brief 一维编码链表转整型编码链表
* @param list 一维编码链表指针
* @return 整型编码链表指针
* @note 注意一维编码链表的层级不能等于32
*'''
# GEOSOT_2D_API GCodeList * toGCodeListFromGCode1DList(GCode1DList *list);


def isGCode1DExistent(gcode1d):
    '''**
    * @brief 一维编码对应区域是否真实存在
    * @param code 一维编码
    * @return true存在，false不存在
    *'''
    libc.isGCode1DExistent.argtypes = (GCode1D,)
    libc.isGCode1DExistent.restype = ctypes.c_bool
    return libc.isGCode1DExistent(gcode1d)

# GEOSOT_2D_API bool isGCode1DExistent(GCode1D code);


def isGCodeExistent(ullcode):
    '''**
    * @brief 整型编码对应区域是否真实存在
    * @param code 整型编码
    * @return true存在，false不存在
    *'''
    libc.isGCodeExistent.argtypes = (ctypes.c_ulonglong,)
    libc.isGCodeExistent.restype = ctypes.c_bool
    return libc.isGCodeExistent(ullcode)

# GEOSOT_2D_API bool isGCodeExistent(unsigned long long code);


def toGeoRangeFromGCode1D(gcode1d):
    '''**
    * @brief 一维编码转地理范围
    * @param code 一维编码
    * @return 地理范围
    *'''
    libc.toGeoRangeFromGCode1D.argtypes = (GCode1D,)
    libc.toGeoRangeFromGCode1D.restype = GeoRange
    return libc.toGeoRangeFromGCode1D(gcode1d)

# GEOSOT_2D_API GeoRange toGeoRangeFromGCode1D(GCode1D code);


def toGeoRangeFromGCode(ullcode):
    '''**
    * @brief 整型编码转地理范围
    * @param code 整型编码
    * @return 地理范围
    *'''
    libc.toGeoRangeFromGCode.argtypes = (ctypes.c_ulonglong,)
    libc.toGeoRangeFromGCode.restype = GeoRange
    return libc.toGeoRangeFromGCode(ullcode)

# GEOSOT_2D_API GeoRange toGeoRangeFromGCode(unsigned long long code);


'''**
* @brief 一维编码转编码行列号
* @param code 一维编码
* @return 编码行列号
*'''
# GEOSOT_2D_API GCodeColRow toGCodeColRowFromGCode1D(GCode1D code);

'''**
* @brief 整型编码转编码行列号
* @param code 整型编码
* @return 编码行列号
*'''
# GEOSOT_2D_API GCodeColRow toGCodeColRowFromGCode(unsigned long long code);

'''**
* @brief 编码行列号转一维编码
* @param colRow 编码行列号
* @return 一维编码
*'''
# GEOSOT_2D_API GCode1D toGCode1DFromGCodeColRow(GCodeColRow colRow);

'''**
* @brief 编码行列号转整型编码
* @param colRow 编码行列号
* @return 整型编码
*'''
# GEOSOT_2D_API unsigned long long toGCodeFromGCodeColRow(GCodeColRow colRow);

'''**
* @brief 一维编码位移运算
* @param code 一维编码
* @param dispOfLon 经度方向位移量>0：右移；=0：静止；<0：左移
* @param dispOfLat 纬度方向位移量>0：上移；=0：静止；<0：下移
* @return 一维编码
*'''
# GEOSOT_2D_API GCode1D displaceGCode1D(GCode1D code, int dispOfLon, int dispOfLat);

'''**
* @brief 整型编码位移运算
* @param code 二维编码
* @param dispOfLon 经度方向位移量>0：右移；=0：静止；<0：左移
* @param dispOfLat 纬度方向位移量>0：上移；=0：静止；<0：下移
* @return 整型编码
*'''
# GEOSOT_2D_API unsigned long long displaceGCode(unsigned long long code, int dispOfLon, int dispOfLat);

'''**
* @brief 按Z序对一维编码进行排序
* @param list 一维编码链表指针
* @return 一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * sortGCode1DByZOrder(GCode1DList *list);

'''**
* @brief 按Z序对整型编码进行排序
* @param list 整型编码链表指针
* @return 整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * sortGCodeByZOrder(GCodeList *list);

'''**
* @brief 计算一维编码的四个子编码对应区域真实存在的数量
* @param code 一维编码
* @return 对应区域真实存在的子编码的数量
*'''
# GEOSOT_2D_API int getRealAreaCountOfSonCodeOfGCode1D(GCode1D code);

'''**
* @brief 计算整型编码的四个子编码对应区域真实存在的数量
* @param code 整型编码
* @return 对应区域真实存在的子编码的数量
*'''
# GEOSOT_2D_API int getRealAreaCountOfSonCodeOfGCode(unsigned long long code);

'''**
* @brief 一维编码去重
* @param list 一维编码链表指针
* @return 去重后的一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * getUniqueGCode1D(GCode1DList *list);

'''**
* @brief 整型编码去重
* @param list 整型编码链表指针
* @return 去重后的整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * getUniqueGCode(GCodeList *list);

'''**
* @brief 同层级一维编码聚合
* @param list 一维编码链表指针
* @return 聚合后的一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * togetherGCode1DOfSameLayer(GCode1DList *list);

'''**
* @brief 同层级整型编码聚合
* @param list 整型编码链表指针
* @return 聚合后的整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * togetherGCodeOfSameLayer(GCodeList *list);


def getOnlyOneGCode1D(minLon, maxLon, minLat, maxLat):
    '''**
    * @brief 只得到一个完全覆盖的一维编码
    * @param minLon 最小经度
    * @param maxLon 最大经度
    * @param minLat 最小纬度
    * @param maxLat 最大纬度
    * @return 一维编码
    *'''
    libc.getOnlyOneGCode1D.argtypes = (
        ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    libc.getOnlyOneGCode1D.restype = GCode1D
    return libc.getOnlyOneGCode1D(minLon, maxLon, minLat, maxLat)

# GEOSOT_2D_API GCode1D getOnlyOneGCode1D(double minLon, double maxLon, double minLat, double maxLat);


def getOnlyOneGCode(minLon, maxLon, minLat, maxLat):
    '''**
    * @brief 只得到一个完全覆盖的整型编码
    * @param minLon 最小经度
    * @param maxLon 最大经度
    * @param minLat 最小纬度
    * @param maxLat 最大纬度
    * @return 整型编码
    *'''
    libc.getOnlyOneGCode.argtypes = (
        ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    libc.getOnlyOneGCode.restype = ctypes.c_ulonglong
    return libc.getOnlyOneGCode(minLon, maxLon, minLat, maxLat)
# GEOSOT_2D_API unsigned long long getOnlyOneGCode(double minLon, double maxLon, double minLat, double maxLat);


def getOnlyOneGCode1DV2(geopointP, pointCount):
    '''**
    * @brief 只得到一个完全覆盖的一维编码
    * @param points 点的指针
    * @param pointCount 点的数量
    * @return 一维编码
    *'''
    libc.getOnlyOneGCode1DV2.argtypes = (
        ctypes.POINTER(GeoPoint), ctypes.c_int)
    libc.getOnlyOneGCode1DV2.restype = GCode1D
    return libc.getOnlyOneGCode1DV2(geopointP, pointCount)
# GEOSOT_2D_API GCode1D getOnlyOneGCode1DV2(GeoPoint *points, int pointCount);


def getOnlyOneGCodeV2(geopointP, pointCount):
    '''**
    * @brief 只得到一个完全覆盖的整型编码
    * @param points 点的指针
    * @param pointCount 点的数量
    * @return 整型编码
    *'''
    libc.getOnlyOneGCodeV2.argtypes = (ctypes.POINTER(GeoPoint), ctypes.c_int)
    libc.getOnlyOneGCodeV2.restype = ctypes.c_ulonglong
    return libc.getOnlyOneGCodeV2(geopointP, pointCount)

# GEOSOT_2D_API unsigned long long getOnlyOneGCodeV2(GeoPoint *points, int pointCount);


def getGeoCenterOfGCode1D(gcode1d):
    '''**
    * @brief 计算一维编码的地理中心点
    * @param code 一维编码
    * @return 地理点
    *'''
    libc.getGeoCenterOfGCode1D.argtypes = (GCode1D,)
    libc.getGeoCenterOfGCode1D.restype = GeoPoint
    return libc.getGeoCenterOfGCode1D(gcode1d)

# GEOSOT_2D_API GeoPoint getGeoCenterOfGCode1D(GCode1D code);


def getGeoCenterOfGCode(ullcode):
    '''**
    * @brief 计算整型编码的地理中心点
    * @param code 整型编码
    * @return 地理点
    *'''
    libc.getGeoCenterOfGCode.argtypes = (ctypes.c_ulonglong,)
    libc.getGeoCenterOfGCode.restype = GeoPoint
    return libc.getGeoCenterOfGCode(ullcode)

# GEOSOT_2D_API GeoPoint getGeoCenterOfGCode(unsigned long long code);


def getGCode1DOfPoint(longitude, latitude, layer):
    '''**
    * @brief 计算点的一维编码
    * @param longitude 点的经度
    * @param latitude 点的纬度
    * @param layer 层级
    * @return 一维编码
    *'''
    libc.getGCode1DOfPoint.argtypes = (
        ctypes.c_double, ctypes.c_double, ctypes.c_int)
    libc.getGCode1DOfPoint.restype = GCode1D
    return libc.getGCode1DOfPoint(longitude, latitude, layer)

# GEOSOT_2D_API GCode1D getGCode1DOfPoint(double longitude, double latitude, int layer);


def getGCodeOfPoint(longitude, latitude, layer):
    '''**
    * @brief 计算点的整型编码
    * @param longitude 点的经度
    * @param latitude 点的纬度
    * @param layer 层级，范围是[1,31]
    * @return 整型编码
    *'''
    libc.getGCodeOfPoint.argtypes = (
        ctypes.c_double, ctypes.c_double, ctypes.c_int)
    libc.getGCodeOfPoint.restype = ctypes.c_ulonglong
    return libc.getGCodeOfPoint(longitude, latitude, layer)

# GEOSOT_2D_API unsigned long long getGCodeOfPoint(double longitude, double latitude, int layer);


'''**
* @brief 计算线的一维编码
* @param p1 起点
* @param p2 终点
* @param layer 层级
* @return 一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * getGCode1DOfLine(GeoPoint p1, GeoPoint p2, int layer);

'''**
* @brief 计算线的整型编码
* @param p1 起点
* @param p2 终点
* @param layer 层级，范围是[1,31]
* @return 整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * getGCodeOfLine(GeoPoint p1, GeoPoint p2, int layer);

'''**
* @brief 计算多线的一维编码
* @param points 点的指针
* @param pointCount 点的数量
* @param layer 层级
* @return 一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * getGCode1DOfPolyline(GeoPoint *points, int pointCount, int layer);

'''**
* @brief 计算多线的整型编码
* @param points 点的指针
* @param pointCount 点的数量
* @param layer 层级，范围是[1,31]
* @return 整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * getGCodeOfPolyline(GeoPoint *points, int pointCount, int layer);

'''**
* @brief 计算多边形的一维编码
* @param points 点的指针
* @param pointCount 点的数量
* @param layer 层级
* @return 一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * getGCode1DOfPolygon(GeoPoint *points, int pointCount, int layer);

'''**
* @brief 计算多边形的整型编码
* @param points 点的指针
* @param pointCount 点的数量
* @param layer 层级，范围是[1,31]
* @return 整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * getGCodeOfPolygon(GeoPoint *points, int pointCount, int layer);

'''**
* @brief 计算(复杂)多边形的一维编码
* @param points 点的指针
* @param pointCount 点的数量
* @param innerPoint 多边形内部一点
* @param layer 层级
* @return 一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * getGCode1DOfComplexPolygon(GeoPoint *points, int pointCount, GeoPoint innerPoint, int layer);

'''**
* @brief 计算(复杂)多边形的整型编码
* @param points 点的指针
* @param pointCount 点的数量
* @param innerPoint 多边形内部一点
* @param layer 层级，范围是[1,31]
* @return 整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * getGCodeOfComplexPolygon(GeoPoint *points, int pointCount, GeoPoint innerPoint, int layer);

'''**
* @brief 计算多边形的某一层级的1~4个一维编码
* @param points 点的指针
* @param pointCount 点的数量
* @return 一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * get1To4GCode1DOfPolygon(GeoPoint *points, int pointCount);

'''**
* @brief 计算多边形的某一层级的1~4个整型编码
* @param points 点的指针
* @param pointCount 点的数量
* @return 整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * get1To4GCodeOfPolygon(GeoPoint *points, int pointCount);

'''**
* @brief 计算平行四边形的一维编码
* @param points 点的指针
* @param layer 层级
* @return 一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * getGCode1DOfParallelogram(GeoPoint *points, int layer);

'''**
* @brief 计算平行四边形的整型编码
* @param points 点的指针
* @param layer 层级，范围是[1,31]
* @return 整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * getGCodeOfParallelogram(GeoPoint *points, int layer);

'''**
* @brief 计算矩形的一维编码
* @param leftTopLon 左上角经度
* @param leftTopLat 左上角纬度
* @param rightBottomLon 右下角经度
* @param rightBottomLat 右下角纬度
* @param layer 层级
* @return 一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * getGCode1DOfRectangle(double leftTopLon, double leftTopLat, double rightBottomLon, double rightBottomLat, int layer);

'''**
* @brief 计算矩形的整型编码
* @param leftTopLon 左上角经度
* @param leftTopLat 左上角纬度
* @param rightBottomLon 右下角经度
* @param rightBottomLat 右下角纬度
* @param layer 层级，范围是[1,31]
* @return 整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * getGCodeOfRectangle(double leftTopLon, double leftTopLat, double rightBottomLon, double rightBottomLat, int layer);

'''**
* @brief 计算一维编码的父编码
* @param code 一维编码
* @param generation 代数 >0；=1：父编码；=2：祖父编码...
* @return 一维编码
*'''
# GEOSOT_2D_API GCode1D getFatherOfGCode1D(GCode1D code, int generation);

'''**
* @brief 计算整型编码的父编码
* @param code 整型编码
* @param generation 代数 >0；=1：父编码；=2：祖父编码...
* @return 整型编码
* @note 不同于getFatherOfGCode，该方法原理上同getFatherOfGCode2D
*'''
# GEOSOT_2D_API unsigned long long getFatherOfGCodeV2(unsigned long long code, int generation);

'''**
* @brief 判断一维编码subject是不是一维编码attribute的父编码
* @param subject 主语，一维编码
* @param attribute 定语，一维编码
* @return true，是；false，不是
*'''
# GEOSOT_2D_API bool isFatherGCode1DOf(GCode1D subject, GCode1D attribute);

'''**
* @brief 判断整型编码subject是不是整型编码attribute的父编码
* @param subject 主语，整型编码
* @param attribute 定语，整型编码
* @return true，是；false，不是
*'''
# GEOSOT_2D_API bool isFatherGCodeOf(unsigned long long subject, unsigned long long attribute);

'''**
* @brief 计算一维编码的子编码
* @param code 一维编码
* @param generation 代数 >0；=1：子编码；=2：孙子编码...
* @return 一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * getSonOfGCode1D(GCode1D code, int generation);

'''**
* @brief 计算整型编码的子编码
* @param code 整型编码
* @param generation 代数 >0；=1：子编码；=2：孙子编码...
* @return 整型编码链表指针
* @note 不同于getSonOfGCode，该方法原理上同getSonOfGCode2D
*'''
# GEOSOT_2D_API GCodeList * getSonOfGCodeV2(unsigned long long code, int generation);

'''**
* @brief 判断一维编码subject是不是一维编码attribute的子编码
* @param subject 主语，一维编码
* @param attribute 定语，一维编码
* @return true，是；false，不是
*'''
# GEOSOT_2D_API bool isSonGCode1DOf(GCode1D subject, GCode1D attribute);

'''**
* @brief 判断整型编码subject是不是整型编码attribute的子编码
* @param subject 主语，整型编码
* @param attribute 定语，整型编码
* @return true，是；false，不是
*'''
# GEOSOT_2D_API bool isSonGCodeOf(unsigned long long subject, unsigned long long attribute);

'''**
* @brief 计算一维编码的四邻域
* @param code 一维编码
* @return 一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * get4NeighborOfGCode1D(GCode1D code);

'''**
* @brief 计算整型编码的四邻域
* @param code 整型编码
* @return 整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * get4NeighborOfGCode(unsigned long long code);

'''**
* @brief 计算一维编码的八邻域
* @param code 一维编码
* @return 一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * get8NeighborOfGCode1D(GCode1D code);

'''**
* @brief 计算整型编码的八邻域
* @param code 整型编码
* @return 整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * get8NeighborOfGCode(unsigned long long code);

'''**
* @brief 计算一维编码之间的包含关系
* @param code1 一维编码
* @param code2 一维编码
* @return -1:不包含；0：相等；1：code1包含code2；2：code2包含code1
*'''
# GEOSOT_2D_API int judgeContainRelationOfGCode1D(GCode1D code1, GCode1D code2);


def judgeContainRelationOfGCode(code1, code2):
    '''**
    * @brief 计算整型编码之间的包含关系
    * @param code1 整型编码
    * @param code2 整型编码
    * @return -1:不包含；0：相等；1：code1包含code2；2：code2包含code1
    *'''
    libc.judgeContainRelationOfGCode.argtypes = (
        ctypes.c_ulonglong, ctypes.c_ulonglong)
    libc.judgeContainRelationOfGCode.restype = ctypes.c_int
    return libc.judgeContainRelationOfGCode(code1, code2)
# GEOSOT_2D_API int judgeContainRelationOfGCode(unsigned long long code1, unsigned long long code2);


'''**
* @brief 计算一维编码链表的交集
* @param list1 一维编码链表指针
* @param list2 一维编码链表指针
* @return 一维编码链表交集的指针
*'''
# GEOSOT_2D_API GCode1DList * getIntersectionOfGCode1Ds(GCode1DList *list1, GCode1DList *list2);

'''**
* @brief 计算整型编码链表的交集
* @param list1 整型编码链表指针
* @param list2 整型编码链表指针
* @return 整型编码链表交集的指针
*'''
# GEOSOT_2D_API GCodeList * getIntersectionOfGCodes(GCodeList *list1, GCodeList *list2);

'''**
* @brief 计算一维编码的交集
* @param code1 一维编码
* @param code2 一维编码
* @return 相交一维编码，若无相交区域，返回的一维编码层级为-1
*'''
# GEOSOT_2D_API GCode1D getIntersectionOfGCode1D(GCode1D code1, GCode1D code2);

'''**
* @brief 计算整型编码的交集
* @param code1 整型编码
* @param code2 整型编码
* @return 相交整型编码，若无相交区域，返回的整型编码层级为-1
*'''
# GEOSOT_2D_API unsigned long long getIntersectionOfGCode(unsigned long long code1, unsigned long long code2);

'''**
* @brief 计算一维编码链表的并集
* @param list1 一维编码链表指针
* @param list2 一维编码链表指针
* @return 一维编码链表并集的指针
*'''
# GEOSOT_2D_API GCode1DList * getUnionOfGCode1Ds(GCode1DList *list1, GCode1DList *list2);

'''**
* @brief 计算整型编码链表的并集
* @param list1 整型编码链表指针
* @param list2 整型编码链表指针
* @return 整型编码链表并集的指针
*'''
# GEOSOT_2D_API GCodeList * getUnionOfGCodes(GCodeList *list1, GCodeList *list2);

'''**
* @brief 计算一编码的并集
* @param code1 一维编码
* @param code2 一维编码
* @return 一维编码链表并集的指针
*'''
# GEOSOT_2D_API GCode1DList * getUnionOfGCode1D(GCode1D code1, GCode1D code2);

'''**
* @brief 计算整型编码的并集
* @param code1 整型编码
* @param code2 整型编码
* @return 整型编码链表并集的指针
*'''
# GEOSOT_2D_API GCodeList * getUnionOfGCode(unsigned long long code1, unsigned long long code2);

'''**
* @brief 计算一维编码的格网缓冲区
* @param list 一维编码链表指针
* @param gridCount 缓冲网格的个数
* @param layer 层级
* @return 缓冲区的一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * getBufferOfGCode1DsByGrid(GCode1DList *list, int gridCount, int layer);

'''**
* @brief 计算整型编码的格网缓冲区
* @param list 整型编码链表指针
* @param gridCount 缓冲网格的个数
* @param layer 层级
* @return 缓冲区的整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * getBufferOfGCodesByGrid(GCodeList *list, int gridCount, int layer);

'''**
* @brief 计算一维编码的距离缓冲区
* @param list 一维编码链表指针
* @param distance 距离，单位为米
* @param layer 层级
* @return 缓冲区的一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * getBufferOfGCode1DsByDistance(GCode1DList *list, double distance, int layer);

'''**
* @brief 计算整型编码的距离缓冲区
* @param list 整型编码链表指针
* @param distance 距离，单位为米
* @param layer 层级
* @return 缓冲区的整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * getBufferOfGCodesByDistance(GCodeList *list, double distance, int layer);

'''**
* @brief 计算一维编码链表的重心
* @param list 一维编码链表指针
* @return 重心一维编码
*'''
# GEOSOT_2D_API GCode1D getBaryCenterOfGCode1Ds(GCode1DList *list);

'''**
* @brief 计算整型编码链表的重心
* @param list 整型编码链表指针
* @return 重心整型编码
*'''
# GEOSOT_2D_API unsigned long long getBaryCenterOfGCodes(GCodeList *list);

'''**
* @brief 计算一维编码对应网格的经向和纬向的长度
* @param code 一维编码
* @param flag
* @return GeoPoint.longitude表示经向长度，GeoPoint.latitude表示纬向长度
*'''
# GEOSOT_2D_API GeoPoint getLengthsOfGCode1D(GCode1D code, int flag);

'''**
* @brief 计算整型编码对应网格的经向和纬向的长度
* @param code 整型编码
* @param flag
* @return GeoPoint.longitude表示经向长度，GeoPoint.latitude表示纬向长度
*'''
# GEOSOT_2D_API GeoPoint getLengthsOfGCode(unsigned long long code, int flag);

'''**
* @brief 计算多边形的N层一维编码
* @param points 点的指针
* @param pointCount 点的数量
* @param maxLayer 最大层级
* @return 一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * getNLayersGCode1DOfPolygon(GeoPoint *points, int pointCount, int maxLayer);

'''**
* @brief 计算多边形的N层整型编码
* @param points 点的指针
* @param pointCount 点的数量
* @param maxLayer 最大层级
* @return 整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * getNLayersGCodeOfPolygon(GeoPoint *points, int pointCount, int maxLayer);


def getGirthOfGCode2D(gcode2d):
    '''**
    * @brief 计算二维编码对应网格在CGCS2000坐标系下的周长
    * @param code 二维编码
    * @return 周长，以米为单位
    *'''
    libc.getGirthOfGCode2D.argtypes = (GCode2D,)
    libc.getGirthOfGCode2D.restype = ctypes.c_double
    return libc.getGirthOfGCode2D(gcode2d)

# GEOSOT_2D_API double getGirthOfGCode2D(GCode2D code);


def getGirthOfGCode1D(gcode1d):
    '''**
    * @brief 计算一维编码对应网格在CGCS2000坐标系下的周长
    * @param code 一维编码
    * @return 周长，以米为单位
    *'''
    libc.getGirthOfGCode1D.argtypes = (GCode1D,)
    libc.getGirthOfGCode1D.restype = ctypes.c_double
    return libc.getGirthOfGCode1D(gcode1d)
# GEOSOT_2D_API double getGirthOfGCode1D(GCode1D code);


def getGirthOfGCode(ullcode):
    '''**
    * @brief 计算整型编码对应网格在CGCS2000坐标系下的周长
    * @param code 整型编码
    * @return 周长，以米为单位
    *'''
    libc.getGirthOfGCode.argtypes = (ctypes.c_ulonglong,)
    libc.getGirthOfGCode.restype = ctypes.c_double
    return libc.getGirthOfGCode(ullcode)
# GEOSOT_2D_API double getGirthOfGCode(unsigned long long code);


def getAreaOfGCode2D(gcode2d):
    '''**
    * @brief 计算二维编码对应网格在CGCS2000坐标系下的面积
    * @param code 二维编码
    * @return 面积，以平方米为单位
    *'''
    libc.getAreaOfGCode2D.argtypes = (GCode2D,)
    libc.getAreaOfGCode2D.restype = ctypes.c_double
    return libc.getAreaOfGCode2D(gcode2d)

# GEOSOT_2D_API double getAreaOfGCode2D(GCode2D code);


def getAreaOfGCode1D(gcode1d):
    '''**
    * @brief 计算一维编码对应网格在CGCS2000坐标系下的面积
    * @param code 一维编码
    * @return 面积，以平方米为单位
    *'''
    libc.getAreaOfGCode1D.argtypes = (GCode1D,)
    libc.getAreaOfGCode1D.restype = ctypes.c_double
    return libc.getAreaOfGCode1D(gcode1d)

# GEOSOT_2D_API double getAreaOfGCode1D(GCode1D code);


def getAreaOfGCode(ullcode):
    '''**
    * @brief 计算整型编码对应网格在CGCS2000坐标系下的面积
    * @param code 整型编码
    * @return 面积，以平方米为单位
    *'''
    libc.getAreaOfGCode.argtypes = (ctypes.c_ulonglong,)
    libc.getAreaOfGCode.restype = (ctypes.c_double)
    return libc.getAreaOfGCode(ullcode)
# GEOSOT_2D_API double getAreaOfGCode(unsigned long long code);


'''**
* @brief 计算二维编码对应网格在CGCS2000坐标系下的曲率
* @param code 二维编码
* @return 曲率
*'''
# GEOSOT_2D_API double getCurvatureOfGCode2D(GCode2D code);

'''**
* @brief 计算一维编码对应网格在CGCS2000坐标系下的曲率
* @param code 一维编码
* @return 曲率
*'''
# GEOSOT_2D_API double getCurvatureOfGCode1D(GCode1D code);

'''**
* @brief 计算整型编码对应网格在CGCS2000坐标系下的曲率
* @param code 整型编码
* @return 曲率
*'''
# GEOSOT_2D_API double getCurvatureOfGCode(unsigned long long code);

'''
**
* @brief 精确判断两个二维编码对应网格之间的方位关系
* @param code1 基准网格二维编码
* @param code2 被测网格二维编码
* @return 方位角，方位角用以正北方向为基准、逆时针旋转角的弧度值表示
* @note 位于同一经线圈上时，如果基准网格、被测网格的中心点距离北极点的纬度差绝对值之和小于或等于180°，视为被测网格在基准网格0°（0）方位角方向上，否则在180°（π）方位角方向上；
*
* 解释1）等于180°的情况可能很难理解，比如会出现南半球的点在北半球的点的正北方向。其实，认为前者在后者的正南方向也是对的，不过在这种情况下，会出现北半球的点在南半球的点的
*
* 正南方向，一样会出现奇怪的逻辑。但是，考虑到方位角以北极点为基准，因此，认为指定这种情况均属于被测网格在基准网格的正北方向更符合逻辑。这是一种极为特殊的情况，需要加以注意。
*
* 解释2）距离北极点的纬度差绝对值的含义如下例所示：网格中心点的纬度为60°，则距离北极点的纬度差绝对值为30°；网格中心点的纬度为-60°，则距离北极点的纬度差绝对值为150°。
*
* @note 位于同一纬线圈上时：
*
* 1）如果被测网格中心点和基准网格中心点的经度差大于180°，视为被测网格在基准网格270°（3π/2）方位角方向上；
*
* 2）如果被测网格中心点和基准网格中心点的经度差大于0°但小于或等于180°，视为被测网格在基准网格90°（π/2）方位角方向上；
*
* 3）如果被测网格中心点和基准网格中心点的经度差大于或等于-180°但小于0°，视为被测网格在基准网格270°（3π/2）方位角方向上；
*
* 4）如果被测网格中心点和基准网格中心点的经度差小于-180°，视为被测网格在基准网格90°（π/2）方位角方向上。
*
* @note 当两个网格重合时，输出无效值（即100）。
**
'''
# GEOSOT_2D_API double getAngleDirectionOfGCode2D(GCode2D code1, GCode2D code2);

'''**
* @brief 精确判断两个一维编码对应网格之间的方位关系
* @param code1 基准网格一维编码
* @param code2 被测网格一维编码
* @return 方位角，方位角用以正北方向为基准、逆时针旋转角的弧度值表示
**'''
# GEOSOT_2D_API double getAngleDirectionOfGCode1D(GCode1D code1, GCode1D code2);

'''**
* @brief 精确判断两个一维编码对应网格之间的方位关系
* @param code1 基准网格一维编码
* @param code2 被测网格一维编码
* @return 方位角，方位角用以正北方向为基准、逆时针旋转角的弧度值表示
**'''
# GEOSOT_2D_API double getAngleDirectionOfGCode(unsigned long long code1, unsigned long long code2);

'''**
* @brief 粗略判断两个二维编码对应网格之间的方位关系
* @param code1 基准网格二维编码
* @param code2 被测网格二维编码
* @return 方向
**'''
# GEOSOT_2D_API Direction getSimpleDirectionOfGCode2D(GCode2D code1, GCode2D code2);

'''**
* @brief 粗略判断两个一维编码对应网格之间的方位关系
* @param code1 基准网格一维编码
* @param code2 被测网格一维编码
* @return 方向
**'''
# GEOSOT_2D_API Direction getSimpleDirectionOfGCode1D(GCode1D code1, GCode1D code2);

'''**
* @brief 粗略判断两个整型编码对应网格之间的方位关系
* @param code1 基准网格整型编码
* @param code2 被测网格整型编码
* @return 方向
**'''
# GEOSOT_2D_API Direction getSimpleDirectionOfGCode(unsigned long long code1, unsigned long long code2);

'''**
* @brief 精确判断两个二维编码网格集之间的方位关系
* @param list1 基准网格二维编码链表指针
* @param list2 被测网格二维编码链表指针
* @return 方位角，方位角用以正北方向为基准、逆时针旋转角的弧度值表示
* @notes 位于同一经线圈上时，如果基准网格、被测网格的中心点距离北极点的纬度差绝对值之和小于或等于180°，视为被测网格在基准网格0°（0）方位角方向上，否则在180°（π）方位角方向上；
*
* 解释1）等于180°的情况可能很难理解，比如会出现南半球的点在北半球的点的正北方向。其实，认为前者在后者的正南方向也是对的，不过在这种情况下，会出现北半球的点在南半球的点的
*
* 正南方向，一样会出现奇怪的逻辑。但是，考虑到方位角以北极点为基准，因此，认为指定这种情况均属于被测网格在基准网格的正北方向更符合逻辑。这是一种极为特殊的情况，需要加以注意。
*
* 解释2）距离北极点的纬度差绝对值的含义如下例所示：网格中心点的纬度为60°，则距离北极点的纬度差绝对值为30°；网格中心点的纬度为 - 60°，则距离北极点的纬度差绝对值为150°。
*
* @notes 位于同一纬线圈上时：
*
* 1）如果被测网格中心点和基准网格中心点的经度差大于180°，视为被测网格在基准网格270°（3π / 2）方位角方向上；
*
* 2）如果被测网格中心点和基准网格中心点的经度差大于0°但小于或等于180°，视为被测网格在基准网格90°（π / 2）方位角方向上；
*
* 3）如果被测网格中心点和基准网格中心点的经度差大于或等于 - 180°但小于0°，视为被测网格在基准网格270°（3π / 2）方位角方向上；
*
* 4）如果被测网格中心点和基准网格中心点的经度差小于 - 180°，视为被测网格在基准网格90°（π / 2）方位角方向上。
*
* @notes 当两个网格重合时，输出无效值（即100）。
**'''
# GEOSOT_2D_API double getAngleDirectionOfGCode2Ds(GCode2DList *list1, GCode2DList *list2);

'''**
* @brief 精确判断两个一维编码网格集之间的方位关系
* @param list1 基准网格一维编码链表指针
* @param list2 被测网格一维编码链表指针
* @return 方位角，方位角用以正北方向为基准、逆时针旋转角的弧度值表示
**'''
# GEOSOT_2D_API double getAngleDirectionOfGCode1Ds(GCode1DList *list1, GCode1DList *list2);

'''**
* @brief 精确判断两个整型编码网格集之间的方位关系
* @param list1 基准网格整型编码链表指针
* @param list2 被测网格整型编码链表指针
* @return 方位角，方位角用以正北方向为基准、逆时针旋转角的弧度值表示
**'''
# GEOSOT_2D_API double getAngleDirectionOfGCodes(GCodeList *list1, GCodeList *list2);

'''**
* @brief 粗略判断两个二维编码网格集之间的方位关系
* @param list1 基准网格二维编码链表指针
* @param list2 被测网格二维编码链表指针
* @return 方向
**'''
# GEOSOT_2D_API Direction getSimpleDirectionOfGCode2Ds(GCode2DList *list1, GCode2DList *list2);

'''**
* @brief 粗略判断两个一维编码网格集之间的方位关系
* @param list1 基准网格一维编码链表指针
* @param list2 被测网格一维编码链表指针
* @return 方向
**'''
# GEOSOT_2D_API Direction getSimpleDirectionOfGCode1Ds(GCode1DList *list1, GCode1DList *list2);

'''**
* @brief 粗略判断两个整型编码网格集之间的方位关系
* @param list1 基准网格整型编码链表指针
* @param list2 被测网格整型编码链表指针
* @return 方向
**'''
# GEOSOT_2D_API Direction getSimpleDirectionOfGCodes(GCodeList *list1, GCodeList *list2);

'''**
* @brief 销毁整型编码链表，同时会擦除其中的数据
* @param list 整型编码链表指针的指针
* @note 销毁后，list指针将为空
*'''
# GEOSOT_2D_API void destroyGCodeList(GCodeList **list);

'''**
* @brief 销毁一维编码链表，同时会擦除其中的数据
* @param list 一维编码链表指针的指针
* @note 销毁后，list指针将为空
*'''
# GEOSOT_2D_API void destroyGCode1DList(GCode1DList **list);
'''**
* @brief 销毁二维编码链表，同时会擦除其中的数据
* @param list 二维编码链表指针的指针
* @note 销毁后，list指针将为空
*'''
# GEOSOT_2D_API void destroyGCode2DList(GCode2DList **list);
'''**
* @brief 销毁double型链表，同时会擦除其中的数据
* @param list double型链表指针的指针
* @note 销毁后，list指针将为空
*'''
# GEOSOT_2D_API void destroyDoubleList(DoubleList **list);

'''**
* @brief 创建点和编码链表
* @return 点和编码链表指针
*'''
# GEOSOT_2D_API PointCodeList * createPointCodeList();

'''**
* @brief 追加点和编码
* @param list 点和编码链表指针
* @param ps 点的指针
* @param pointCount 点的数量
* @param code 二维编码
*'''
# GEOSOT_2D_API void append2PointCodeList(PointCodeList *list, GeoPoint *ps, int pointCount, GCode2D code);

'''**
* @brief 得到点和编码链表的大小，等于结构体中的count
* @param list 点和编码链表指针
* @return 点和编码链表的大小
*'''
# GEOSOT_2D_API int getPointCodeListSize(PointCodeList *list);

'''**
* @brief 擦除点和编码链表中的数据，不销毁链表
* @param list 点和编码链表指针
*'''
# GEOSOT_2D_API void erasePointCodeList(PointCodeList *list);

'''**
* @brief 销毁点和编码链表，同时会擦除其中的数据
* @param list 点和编码链表指针
*'''
# GEOSOT_2D_API void destroyPointCodeList(PointCodeList **list);

'''**
* @brief 得到点和编码链表中的某一个节点
* @param list 点和编码链表指针
* @param index index 索引，从0开始。0表示头，- 1表示尾。
* @return index处的点和编码链表节点指针
*'''
# GEOSOT_2D_API PointCodeNode * getPointCodeNodeAt(PointCodeList *list, int index);

'''**
* @brief 往点和编码链表节点追加点
* @param node 点和编码链表节点
* @param longitude 经度
* @param latitude 纬度
*'''
# GEOSOT_2D_API void appendPoint2PointCodeNode(PointCodeNode *node, double longitude, double latitude);

'''**
* @brief 克隆点和编码链表节点的点
* @param node 点和编码链表节点
* @return 克隆后的点的指针
*'''
# GEOSOT_2D_API GeoPoint * clonePointsOfPointCodeNode(PointCodeNode *node);

'''**
* @brief 克隆点
* @param points 点的指针
* @param pointCount 点的数量
* @return 克隆后的点的指针
*'''
# GEOSOT_2D_API GeoPoint * clonePoints(GeoPoint *points, int pointCount);

'''**
* @brief 供计算编码使用
* @param area 点和编码链表节点指针
* @param lat 纬度
* @param lon 经度
* @return 点和编码链表指针
*'''
# GEOSOT_2D_API PointCodeList * breakArea(PointCodeNode *area, double lat, double lon);

'''**
* @brief 创建二维编码链表
* @return 二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * createGCode2DList();

'''**
* @brief 追加二维编码
* @param list 二维编码链表指针
* @param code 二维编码
*'''
# GEOSOT_2D_API void append2GCode2DList(GCode2DList *list, GCode2D code);

'''**
* @brief 得到二维编码链表的大小，等于结构体中的count
* @param list 二维编码链表指针
* @return 二维编码链表的大小
*'''
# GEOSOT_2D_API int getGCode2DListSize(GCode2DList *list);

'''**
* @brief 擦除二维编码链表中的数据，不销毁链表
* @param list 二维编码链表指针
*'''
# GEOSOT_2D_API void eraseGCode2DList(GCode2DList *list);

'''**
* @brief 得到二维编码链表中的某一个节点
* @param list 二维编码链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
* @return index处的二维编码链表节点指针
*'''
# GEOSOT_2D_API GCode2DNode * getGCode2DNodeAt(GCode2DList *list, int index);

'''**
* @brief 得到二维编码链表中的某一个编码
* @param list 二维编码链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
* @return index处的二维编码，当层级为 - 1时，表示不存在。
*'''
# GEOSOT_2D_API GCode2D getGCode2DAt(GCode2DList *list, int index);

'''**
* @brief 移除二维编码链表中的某一个节点
* @param list 二维编码链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
*'''
# GEOSOT_2D_API void removeGCode2DNodeAt(GCode2DList *list, int index);

'''**
* @brief 移除二维编码链表中的所有节点，等价于eraseGCode2DList()
* @param list 二维编码链表指针
*'''
# GEOSOT_2D_API void removeGCode2DNodeAll(GCode2DList *list);

'''**
* @brief 连接两个二维编码链表
* @param result 在前的链表，亦是结果链表。
* @param list 后面的链表。
* @note 执行完毕，list将会被置空(null)。
*'''
# GEOSOT_2D_API void connectGCode2DList(GCode2DList *result, GCode2DList *list);

'''**
* @brief 克隆二维编码链表
* @param list 二维编码链表指针
* @return 克隆后的二维编码链表指针
*'''
# GEOSOT_2D_API GCode2DList * cloneGCode2DList(GCode2DList *list);

'''**
* @brief 创建一维编码链表
* @return 一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * createGCode1DList();

'''**
* @brief 追加一维编码
* @param list 一维编码链表指针
* @param code 一维编码
*'''
# GEOSOT_2D_API void append2GCode1DList(GCode1DList *list, GCode1D code);

'''**
* @brief 得到一维编码链表的大小，等于结构体中的count
* @param list 一维编码链表指针
* @return 一维编码链表的大小
*'''
# GEOSOT_2D_API int getGCode1DListSize(GCode1DList *list);

'''**
* @brief 擦除一维编码链表中的数据，不销毁链表
* @param list 一维编码链表指针
*'''
# GEOSOT_2D_API void eraseGCode1DList(GCode1DList *list);

'''**
* @brief 得到一维编码链表中的某一个节点
* @param list 一维编码链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
* @return index处的一维编码链表节点指针
*'''
# GEOSOT_2D_API GCode1DNode * getGCode1DNodeAt(GCode1DList *list, int index);

'''**
* @brief 得到一维编码链表中的某一个编码
* @param list 一维编码链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
* @return index处的一维编码，当层级为 - 1时，表示不存在。
*'''
# GEOSOT_2D_API GCode1D getGCode1DAt(GCode1DList *list, int index);

'''**
* @brief 移除一维编码链表中的某一个节点
* @param list 一维编码链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
*'''
# GEOSOT_2D_API void removeGCode1DNodeAt(GCode1DList *list, int index);

'''**
* @brief 移除一维编码链表中的所有节点，等价于eraseGCode1DList()
* @param list 一维编码链表指针
*'''
# GEOSOT_2D_API void removeGCode1DNodeAll(GCode1DList *list);

'''**
* @brief 连接两个一维编码链表
* @param result 在前的链表，亦是结果链表。
* @param list 后面的链表。
* @note 执行完毕，list将会被置空(null)。
*'''
# GEOSOT_2D_API void connectGCode1DList(GCode1DList *result, GCode1DList *list);

'''**
* @brief 克隆一维编码链表
* @param list 一维编码链表指针
* @return 克隆后的一维编码链表指针
*'''
# GEOSOT_2D_API GCode1DList * cloneGCode1DList(GCode1DList *list);

'''**
* @brief 创建整型编码链表
* @return 整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * createGCodeList();

'''**
* @brief 追加整型编码
* @param list 整型编码链表指针
* @param code 整型编码
*'''
# GEOSOT_2D_API void append2GCodeList(GCodeList *list, unsigned long long code);

'''**
* @brief 得到整型编码链表的大小，等于结构体中的count
* @param list 整型编码链表指针
* @return 整型编码链表的大小
*'''
# GEOSOT_2D_API int getGCodeListSize(GCodeList *list);

'''**
* @brief 擦除整型编码链表中的数据，不销毁链表
* @param list 整型编码链表指针
*'''
# GEOSOT_2D_API void eraseGCodeList(GCodeList *list);

'''**
* @brief 得到整型编码链表中的某一个节点
* @param list 整型编码链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
* @return index处的整型编码链表节点指针
*'''
# GEOSOT_2D_API GCodeNode * getGCodeNodeAt(GCodeList *list, int index);

'''**
* @brief 得到整型编码链表中的某一个编码
* @param list 整型编码链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
* @return index处的整型编码，当层级为 - 1时，表示不存在。
*'''
# GEOSOT_2D_API unsigned long long getGCodeAt(GCodeList *list, int index);

'''**
* @brief 移除整型编码链表中的某一个节点
* @param list 整型编码链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
*'''
# GEOSOT_2D_API void removeGCodeNodeAt(GCodeList *list, int index);

'''**
* @brief 移除整型编码链表中的所有节点，等价于eraseGCodeList()
* @param list 整型编码链表指针
*'''
# GEOSOT_2D_API void removeGCodeNodeAll(GCodeList *list);

'''**
* @brief 连接两个整型编码链表
* @param result 在前的链表，亦是结果链表。
* @param list 后面的链表。
* @note 执行完毕，list将会被置空(null)。
*'''
# GEOSOT_2D_API void connectGCodeList(GCodeList *result, GCodeList *list);

'''**
* @brief 克隆整型编码链表
* @param list 整型编码链表指针
* @return 克隆后的整型编码链表指针
*'''
# GEOSOT_2D_API GCodeList * cloneGCodeList(GCodeList *list);

'''**
* @brief 创建int型链表
* @return int型链表指针
*'''
# GEOSOT_2D_API IntList * createIntList();

'''**
* @brief 追加int值
* @param list int型链表指针
* @param value 值
*'''
# GEOSOT_2D_API void append2IntList(IntList *list, int value);

'''**
* @brief 得到int型链表的大小，等于结构体中的count
* @param list int型链表指针
* @return int型链表的大小
*'''
# GEOSOT_2D_API int getIntListSize(IntList *list);

'''**
* @brief 擦除int型链表中的数据，不销毁链表
* @param list int型链表指针
*'''
# GEOSOT_2D_API void eraseIntList(IntList *list);

'''**
* @brief 销毁int型链表，同时会擦除其中的数据
* @param list int型链表指针
*'''
# GEOSOT_2D_API void destroyIntList(IntList **list);

'''**
* @brief 得到int型链表中的某一个节点
* @param list int型链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
* @return index处的int型链表节点指针
*'''
# GEOSOT_2D_API IntNode * getIntNodeAt(IntList *list, int index);

'''**
* @brief 得到int型链表中的某一个值
* @param list int型链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
* @return index处的值
*'''
# GEOSOT_2D_API int getIntAt(IntList *list, int index);

'''**
* @brief 设置int型链表中的某一个值
* @param list int型链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
* @param value 新值
*'''
# GEOSOT_2D_API void setIntAt(IntList *list, int index, int value);

'''**
* @brief 移除int型链表中的某一个节点
* @param list int型链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
*'''
# GEOSOT_2D_API void removeIntNodeAt(IntList *list, int index);

'''**
* @brief 移除int型链表中的所有节点，等价于eraseIntList()
* @param list int型链表指针
*'''
# GEOSOT_2D_API void removeIntNodeAll(IntList *list);

'''**
* @brief 连接两个int型链表
* @param result 在前的链表，亦是结果链表。
* @param list 后面的链表。
* @note 执行完毕，list将会被置空(null)。
*'''
# GEOSOT_2D_API void connectIntList(IntList *result, IntList *list);

'''**
* @brief 克隆int型链表
* @param list int型链表指针
* @return 克隆后的int型链表指针
*'''
# GEOSOT_2D_API IntList * cloneIntList(IntList *list);

'''**
* @brief 创建double型链表
* @return double型链表指针
*'''
# GEOSOT_2D_API DoubleList * createDoubleList();

'''**
* @brief 追加double值
* @param list double型链表指针
* @param value 值
*'''
# GEOSOT_2D_API void append2DoubleList(DoubleList *list, double value);

'''**
* @brief 得到double型链表的大小，等于结构体中的count
* @param list double型链表指针
* @return double型链表的大小
*'''
# GEOSOT_2D_API int getDoubleListSize(DoubleList *list);

'''**
* @brief 擦除double型链表中的数据，不销毁链表
* @param list double型链表指针
*'''
# GEOSOT_2D_API void eraseDoubleList(DoubleList *list);

'''**
* @brief 得到double型链表中的某一个节点
* @param list double型链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
* @return index处的double型链表节点指针
*'''
# GEOSOT_2D_API DoubleNode * getDoubleNodeAt(DoubleList *list, int index);

'''**
* @brief 得到double型链表中的某一个值
* @param list double型链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
* @return index处的值
*'''
# GEOSOT_2D_API double getDoubleAt(DoubleList *list, int index);

'''**
* @brief 移除double型链表中的某一个节点
* @param list double型链表指针
* @param index 索引，从0开始。0表示头，- 1表示尾。
*'''
# GEOSOT_2D_API void removeDoubleNodeAt(DoubleList *list, int index);

'''**
* @brief 移除double型链表中的所有节点，等价于eraseDoubleList()
* @param list double型链表指针
*'''
# GEOSOT_2D_API void removeDoubleNodeAll(DoubleList *list);

'''**
* @brief 连接两个double型链表
* @param result 在前的链表，亦是结果链表。
* @param list 后面的链表。
* @note 执行完毕，list将会被置空(null)。
*'''
# GEOSOT_2D_API void connectDoubleList(DoubleList *result, DoubleList *list);

'''**
* @brief 克隆double型链表
* @param list double型链表指针
* @return 克隆后的double型链表指针
*'''
# GEOSOT_2D_API DoubleList * cloneDoubleList(DoubleList *list);

'''**
* @brief 计算两地理点的编码线参数
* @param p1 起点
* @param p2 终点
* @return 编码线参数
*'''
# GEOSOT_2D_API GCodeLineParam getLineParam(GeoPoint p1, GeoPoint p2);


def getIntersectPointWithLonLat(p1, p2, inputs, flag):
    '''**
    * @brief 计算两地理点与经线或者纬线相交的点的纬度或者经度
    * @param p1 起点
    * @param p2 终点
    * @param input 经线经度或者纬线纬度
    * @param flag 0表示计算经度，1表示计算纬度
    * @return 相交点经度或者纬度
    * @note
    *'''
    libc.getIntersectPointWithLonLat.argtypes = (
        GeoPoint, GeoPoint, ctypes.c_double, ctypes.c_int)
    libc.getIntersectPointWithLonLat.restype = ctypes.c_double
    return libc.getIntersectPointWithLonLat(p1, p2, inputs, flag)

# GEOSOT_2D_API double getIntersectPointWithLonLat(GeoPoint p1, GeoPoint p2, double input, int flag);
