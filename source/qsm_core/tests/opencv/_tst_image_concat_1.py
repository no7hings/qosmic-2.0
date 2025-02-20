# coding:utf-8
import lxbasic.cv.core as c

c.ImageConcat(
    [
        'Z:/temporaries/image_concat_test/max.png',
        'Z:/temporaries/image_concat_test/snook.png',
        'Z:/temporaries/image_concat_test/max.png',
        'Z:/temporaries/image_concat_test/snook.png',
        'Z:/temporaries/image_concat_test/snook.png',
        'Z:/temporaries/image_concat_test/max.png',
        'Z:/temporaries/image_concat_test/snook.png',
        'Z:/temporaries/image_concat_test/snook.png',
        'Z:/temporaries/image_concat_test/max.png',
        'Z:/temporaries/image_concat_test/snook.png',
        'Z:/temporaries/image_concat_test/snook.png',
    ],
    'Z:/temporaries/image_concat_test/output.png'
).show_result()
