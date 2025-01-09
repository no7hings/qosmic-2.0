# coding:utf-8

hsv_in = 0, 1.0, 1.0

hsv_offset = 0, 0.5, 0.5

print float(int((hsv_in[0]+(hsv_offset[0]-0.5))*100.0)%100.0)/100.0
