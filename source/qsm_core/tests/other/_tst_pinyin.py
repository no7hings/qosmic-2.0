# coding:utf-8
import lxbasic.pinyin as bsc_pinyin

print(
    bsc_pinyin.Text.cleanup(
        'A001_002 测试'
    )
)

print(
    bsc_pinyin.Text.cleanup(
        'A001_002_测试'
    )
)

print(
    bsc_pinyin.Text.cleanup(
        'A001_002_测试A', stop_on_chs=True
    )
)

print(
    bsc_pinyin.Text.cleanup(
        'A001_002_测试_A', stop_on_chs=True
    )
)

print(
    bsc_pinyin.Text.to_pinyin_name(
        'A001_002_测试_A'
    )
)


