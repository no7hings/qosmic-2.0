# coding:utf-8


class MtgRigNamespace:
    @classmethod
    def to_master_layer_namespace(cls, rig_namespace):
        return '{}:master'.format(rig_namespace)

    @classmethod
    def to_master_layer_name(cls, rig_namespace):
        return MtgLayerNamespace.to_master_later_name(
            cls.to_master_layer_namespace(rig_namespace)
        )
    
    @classmethod
    def to_layer_namespace(cls, rig_namespace, key):
        return '{}:{}'.format(rig_namespace, key)

    @classmethod
    def to_layer_name(cls, rig_namespace, key):
        return MtgLayerNamespace.to_layer_name(
            cls.to_layer_namespace(rig_namespace, key)
        )

    @classmethod
    def to_persp_camera_shape_name(cls, rig_namespace):
        return '{}:master:persp_camShape'.format(rig_namespace)


class MtgLayerNamespace:
    MASTER_LAYER_NAME = 'MASTER_LAYER'
    LAYER_NAME = 'LAYER'

    MASTER_LAYER_KEY = 'master:MASTER_LAYER'

    @classmethod
    def to_master_later_name(cls, layer_namespace):
        return '{}:{}'.format(layer_namespace, cls.MASTER_LAYER_NAME)

    @classmethod
    def to_layer_name(cls, layer_namespace):
        return '{}:{}'.format(layer_namespace, cls.LAYER_NAME)
