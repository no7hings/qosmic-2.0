# coding:utf-8
import numpy as np


# Formula from: http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
def rgb_to_xyz(r, g, b, w):
    xyz_r = np.array([r[0]/r[1], 1, (1-r[0]-r[1])/r[1]])
    xyz_g = np.array([g[0]/g[1], 1, (1-g[0]-g[1])/g[1]])
    xyz_b = np.array([b[0]/b[1], 1, (1-b[0]-b[1])/b[1]])
    xyz_w = np.array([w[0]/w[1], 1, (1-w[0]-w[1])/w[1]])

    s = xyz_w*np.linalg.inv(np.matrix([xyz_r, xyz_g, xyz_b]))

    m = np.matrix(
        [[s.item(0)*xyz_r[0], s.item(1)*xyz_g[0], s.item(2)*xyz_b[0]],
         [s.item(0)*xyz_r[1], s.item(1)*xyz_g[1], s.item(2)*xyz_b[1]],
         [s.item(0)*xyz_r[2], s.item(1)*xyz_g[2], s.item(2)*xyz_b[2]]]
        )

    return m


# https://en.wikipedia.org/wiki/Academy_Color_Encoding_System#Converting_CIE_XYZ_values_to_ACES2065-1_values
ap1_r = [0.713, 0.293]
ap1_g = [0.165, 0.830]
ap1_b = [0.128, 0.044]
aces_w = [0.32168, 0.33767]

ap1_to_xyz = rgb_to_xyz(ap1_r, ap1_g, ap1_b, aces_w)
xyz_to_ap1 = np.linalg.inv(ap1_to_xyz)

# print(ap1_to_xyz)
print("XYZ to AP1")
print(xyz_to_ap1)

# http://terathon.com/blog/rgb-xyz-conversion-matrix-accuracy/
srgb_r = [0.64, 0.33]
srgb_g = [0.3, 0.6]
srgb_b = [0.15, 0.06]
d65 = [0.3127, 0.3290]

srgb_to_xyz = rgb_to_xyz(srgb_r, srgb_g, srgb_b, d65)
xyz_to_srgb = np.linalg.inv(srgb_to_xyz)

print("sRGB to XYZ to AP1")
print(xyz_to_ap1*srgb_to_xyz)

d60_to_d65 = np.matrix(
    [[0.987224, -0.00611327, 0.0159533],
     [-0.00759836, 1.00186, 0.00533002],
     [0.00307257, -0.00509595, 1.08168]]
    )

d65_to_d60 = np.linalg.inv(d60_to_d65)

print("sRGB to XYZ to d65 to d60 to AP1")
print((xyz_to_ap1*d65_to_d60*srgb_to_xyz).tolist())


# print(srgb_to_xyz)
# print(np.linalg.inv(srgb_to_xyz))

# http://www.brucelindbloom.com/index.html?Eqn_ChromAdapt.html
# https://github.com/ampas/aces-dev/blob/master/transforms/ctl/lib/ACESlib.Utilities_Color.ctl

def bradford(ws, wd):
    b = np.matrix(
        [[0.8951000, -0.7502000, 0.0389000],
         [0.2664000, 1.7135000, -0.0685000],
         [-0.1614000, 0.0367000, 1.0296000]]
        )

    xyz_ws = np.array([ws[0]/ws[1], 1, (1-ws[0]-ws[1])/ws[1]])
    xyz_wd = np.array([wd[0]/wd[1], 1, (1-wd[0]-wd[1])/wd[1]])

    pyb_s = xyz_ws*b
    pyb_d = xyz_wd*b

    mid = np.matrix(
        [[pyb_d.item(0)/pyb_s.item(0), 0, 0],
         [0, pyb_d.item(1)/pyb_s.item(1), 0],
         [0, 0, pyb_d.item(2)/pyb_s.item(2)]]
        )

    return b*mid*np.linalg.inv(b)


print(bradford(aces_w, d65).tolist())
print(d60_to_d65.tolist())
