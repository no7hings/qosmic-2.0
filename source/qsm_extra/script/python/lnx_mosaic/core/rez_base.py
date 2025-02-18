# coding:utf-8
import rez.packages as rez_packages


class RezPackageFamily(object):
    PACKAGE_PATHS = [
        'Y:/deploy/rez-packages/internally/release',
        'Y:/deploy/rez-packages/internally/pre-release',
        'Y:/deploy/rez-packages/external',
        'Y:/deploy/rez-packages/application',
        'Y:/deploy/rez-packages/plugin'
    ]

    @classmethod
    def get_all(cls):
        list_ = []
        for i_package in rez_packages.iter_package_families(cls.PACKAGE_PATHS):
            list_.append(i_package)
        return list_
