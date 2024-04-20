# coding:utf-8
import lxbasic.database as bsc_database


if __name__ == '__main__':
    for _i_key in [
        'surface',
        'atlas',
        'displacement',
        'asset',
        'plant',
        'imperfection',
        'texture',
        'test',
        'hdri',
    ]:
        dtb_opt_ = bsc_database.DtbOptForResource.generate(_i_key)
        #
        dtb_opt_.setup_entity_categories()
        dtb_opt_.setup_entities()
        dtb_opt_.accept()
    # dtb_opt_.create_category_group('atlas')
    # dtb_opt_.create_category('fern', '/atlas')
    # dtb_opt_.create_type('other', '/atlas/fern')
    # dtb_opt_.create_category_root()
    # print dtb_opt_.get_type_force('/atlas/fern/other')
    # print dtb_opt_.create_resource('/atlas/sword_fern_pjvef2')
    # print dtb_opt_.create_resource_property('/atlas/sword_fern_pjvef2.version', '/atlas/sword_fern_pjvef2/v0001')
    # print dtb_opt_.create_version('/atlas/sword_fern_pjvef2/v0001')
