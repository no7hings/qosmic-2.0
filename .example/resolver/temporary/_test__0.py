# coding:utf-8

b = '1'


def test(boolean):
    print boolean


a = ((0, test(True)) if b else ('', test(1)))[0]

print a

# a = ((getParent().getParent().render_settings.camera, self.getNode().setBypassed(0)) if getParent().getParent().render_settings.camera else ('', self.getNode().setBypassed(1)))[0]
#
#
# 1 if getParent().getParent().render_settings.camera else 0

