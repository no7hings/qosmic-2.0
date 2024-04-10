# coding:utf-8


class ColorSpaceMtd(object):
    SRGB_TO_ACCESCG_MATRIX = [
        [0.613132422390542, 0.339538015799666, 0.047416696048269],
        [0.070124380833917, 0.916394011313573, 0.013451523958235],
        [0.020587657528185, 0.109574571610682, 0.869785404035327]
    ]
    ACCESCG_TO_SRGB_MATRIX = [
        [1.704858676289160, -0.621716021885330, -0.083299371729057],
        [-0.130076824208823, 1.140735774822504, -0.010559801677511],
        [-0.023964072927574, -0.128975508299318, 1.153014018916862]
    ]

    @classmethod
    def srgb_to_accescg(cls, rgb):
        matrix = cls.SRGB_TO_ACCESCG_MATRIX
        v_out = [
            matrix[0][0]*rgb[0]+matrix[0][1]*rgb[1]+matrix[0][2]*rgb[2],
            matrix[1][0]*rgb[0]+matrix[1][1]*rgb[1]+matrix[1][2]*rgb[2],
            matrix[2][0]*rgb[0]+matrix[2][1]*rgb[1]+matrix[2][2]*rgb[2]
        ]
        if len(rgb) > 3:
            v_out += rgb[3::]
        return v_out

    @classmethod
    def accescg_to_srgb(cls, rgb):
        matrix = cls.ACCESCG_TO_SRGB_MATRIX
        v_out = [
            matrix[0][0]*rgb[0]+matrix[0][1]*rgb[1]+matrix[0][2]*rgb[2],
            matrix[1][0]*rgb[0]+matrix[1][1]*rgb[1]+matrix[1][2]*rgb[2],
            matrix[2][0]*rgb[0]+matrix[2][1]*rgb[1]+matrix[2][2]*rgb[2]
        ]
        if len(rgb) > 3:
            v_out += rgb[3::]
        return v_out
