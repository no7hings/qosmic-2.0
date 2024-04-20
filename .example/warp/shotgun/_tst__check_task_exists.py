# coding:utf-8
import lxresolver.core as rsv_core

import lxbasic.shotgun as bsc_shotgun

f = '/production/shows/nsa_dev/assets/chr/td_test/user/work.dongchangbao/katana/scenes/surface/td_test.srf.surface.v000_002.katana'

resolver = rsv_core.RsvBase.generate_root()

rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(
    f
)

stg_connector = bsc_shotgun.StgConnector()
print stg_connector.get_stg_task(**rsv_scene_properties.value)

t = stg_connector.find_stg_task(
    project='nsa_dev', resource='td_test', task='surface'
)

print stg_connector._stg_instance.find(
    entity_type='Step',
    filters=[
        ['short_name', 'is', 'SRF'],
    ],
    fields=['short_name']
)

print bsc_shotgun.StgEntityQuery(
    stg_connector, {'type': 'Step', 'id': 173}
).get_all()

s = bsc_shotgun.StgEntityQuery(
    stg_connector, t
).get('step')
print s
print bsc_shotgun.StgEntityQuery(
    stg_connector, s
).get_all()

"""
{'sg_notice_to_people': [], 'code': 'Surfacing', 'list_order': 13, 'color': '127,127,127', 'sg_notice_to_description': None, 'updated_at': datetime.datetime(2023, 2, 20, 17, 49, 3, tzinfo=<shotgun_api3.lib.sgtimezone.LocalTimezone object at 0x7f3cff5da950>), 'sg_studio_site': 'Animation', 'cached_display_name': 'Surfacing', 'id': 321, 'custom_entity09_sg_steps_custom_entity09s': [], 'description': None, 'entity_type': 'Asset', 'created_by': {'type': 'HumanUser', 'id': 808, 'name': 'slash'}, 'department': None, 'type': 'Step', 'updated_by': {'type': 'HumanUser', 'id': 808, 'name': 'slash'}, 'short_name': 'SRF', 'sg_studio': None, 'step_sg_down_steps_steps': [], 'sg_using_in_cg': True, 'created_at': datetime.datetime(2022, 12, 8, 20, 22, 49, tzinfo=<shotgun_api3.lib.sgtimezone.LocalTimezone object at 0x7f3cff5da950>), 'sg_down_steps': [], 'sg_notice_to_group': []}
"""


