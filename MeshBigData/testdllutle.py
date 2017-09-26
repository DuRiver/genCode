import dllUtil
import ctypes


geopoint = dllUtil.GCodePoint(19, 106, 32)

code = dllUtil.getGCodeOfPoint(geopoint.longitude, geopoint.latitude, geopoint.layer)
code1d = dllUtil.getGCode1DOfPoint(geopoint.longitude, geopoint.latitude, geopoint.layer)
code2d = dllUtil.getGCode2DOfPoint(geopoint.longitude, geopoint.latitude, geopoint.layer)
code2 = dllUtil.toGCodeFromGCode2D(code2d)

gode2dt = dllUtil.toGCode2DFromGCode(code)
print(code)
print(code1d.code, code1d.code/2)
print(code2d)
code1 = ctypes.c_ulonglong(206461482982965248)

code21 = dllUtil.toGCodeFromGCode1D(code1d)
code11 = dllUtil.toGCodeFromGCode2D(code2d)
aa = dllUtil.toGeoRangeFromGCode(code1)
georange21 = dllUtil.toGeoRangeFromGCode(code21)
georange2d = dllUtil.toGeoRangeFromGCode2D(code2d)
print(georange2d.minLat)
print(georange2d['maxLat'])
georange1d = dllUtil.toGeoRangeFromGCode1D(code1d)
print(georange1d)
georange = dllUtil.toGeoRangeFromGCode(ctypes.c_ulonglong(206461482966188032))
print(georange)
center = dllUtil.getGeoCenterOfGCode(code)
print(dllUtil.myEnumDirection.DUENORTH)