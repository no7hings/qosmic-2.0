# coding:utf-8
'{}/look_checker'.format(
    '/'.join(
        self.getNode().getParent().getParameter(
            'cameras.{}.location'.format(self.getNode().getOutputPort("out").getConnectedPorts()[0].getName())
        ).getValue(0).split('/')[:-1]
    )
)