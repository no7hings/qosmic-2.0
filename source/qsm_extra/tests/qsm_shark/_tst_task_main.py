# coding:utf-8
import qsm_shark.resolve as c


stage = c.Stage()

print stage.root.get_location()

print stage.find_project('QSM_TST_NEW').get_location()

print stage.find_asset('QSM_TST_NEW', 'sam')

print stage.find_asset_task('QSM_TST_NEW', 'sam', 'modeling')
