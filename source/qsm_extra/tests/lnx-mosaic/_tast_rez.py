# coding:utf-8

from rez import packages


def get_all_packages():
    # 获取 Rez 的包路径
    package_paths = [
        'Y:/deploy/rez-packages/internally/release',
        'Y:/deploy/rez-packages/internally/pre-release',
        'Y:/deploy/rez-packages/external',
        'Y:/deploy/rez-packages/application',
        'Y:/deploy/rez-packages/plugin'
    ]

    print package_paths

    # 存储所有包信息
    all_packages = set()

    # 遍历包路径并获取包信息
    for i_package_family in packages.iter_package_families(package_paths):
        # print i_package_family
        print i_package_family.resource
        # for j_version in i_package_family.iter_packages():
        #     print j_version

    return sorted(all_packages)


if __name__ == "__main__":
    get_all_packages()
