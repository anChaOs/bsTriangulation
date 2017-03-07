#!/usr/bin/env python3
# coding: utf8
# 20170307 anChaOs

import math


class Point(object):

    def __init__(self, x, y):
        self._x = float(x)
        self._y = float(y)

    def getx(self):
        return self._x

    def gety(self):
        return self._y

    def setx(self, x):
        self._x = float(x)

    def sety(self, y):
        self._y = float(y)

    def __repr__(self):
        return '<Point(%.2f, %.2f)>' % (self._x, self._y)



PI = 3.14159265359

class Triangulation(object):

    def __init__(self):
        self.coord = []     # 坐标集合
        self.rxlevel = []   # 信号强度集合，单位是dbm或ASU
        self.count = 0

    def add(self, point, rxlevel):
        if not isinstance(point, Point) or not isinstance(rxlevel, int):
            raise ValueError()

        self.coord.append(point)
        self.rxlevel.append(rxlevel)
        self.count += 1

    def location(self, freq=1000):
        """
            freq: 接收频率设为1000Mhz，如果你的设备能获取到实际的接收频率，可以修改这个参数
        """
        distance_weight = []    # 位置权重
        distance_sum    = 0
        lat             = []    # 纬度
        lon             = []    # 经度

        for i, coord in enumerate(self.coord):
            lat.append(coord.gety()/180*PI)
            lon.append(coord.getx()/180*PI)
            dweight = math.pow(10.0, (130.0 + self.rxlevel[i] - 20.0*math.log10(freq))/20.0)
            distance_weight.append(dweight)
            distance_sum += dweight

        x = 0
        y = 0
        z = 0

        for i in range(len(lat)):
            x += math.cos(lat[i]) * math.cos(lon[i]) * distance_weight[i]
            y += math.cos(lat[i]) * math.sin(lon[i]) * distance_weight[i]
            z += math.sin(lat[i]) * distance_weight[i]

        x_avg = x/distance_sum
        y_avg = y/distance_sum
        z_avg = z/distance_sum

        # 转换为经纬度坐标
        lat_avg = math.atan(z_avg / math.sqrt(x_avg*x_avg + y_avg*y_avg)) * 180.0 / PI
        lon_avg = math.atan(y_avg / x_avg) * 180.0 / PI

        if lon_avg < 0:
            lon_avg += 180.0

        return Point(lon_avg, lat_avg)


if __name__ == '__main__':
    # 初始化Triangulation对象
    t = Triangulation()

    # 依次增加基站，add参数有两个：
    # 1. point:     坐标对x,y，x为纬度，y为经度
    # 2. rxlevel:   信号强度
    t.add(Point(116.0, 40.0), 100)
    t.add(Point(115.0, 39.0), 60)
    t.add(Point(115.0, 40.0), 80)
    t.add(Point(116.0, 39.0), 75)

    # 计算结果，返回Point对象
    point = t.location()

    # 用point.getx()获取纬度
    # 用point.gety()获取经度
    print(point, point.getx(), point.gety())