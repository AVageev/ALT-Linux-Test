import requests
import rpm
import json

def fetch_branch_packages(branch: str):
    url = f'https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data)) 
        return data
    else:
        raise Exception(f"Failed to fetch data for branch {branch}: {response.status_code}")


def rpm_vercmp(version1, version2):
    """
    Сравнивает версии RPM пакетов.
    :param version1: Версия пакета в формате 'version-release'
    :param version2: Версия пакета в формате 'version-release'
    :return: 1, если первая версия больше, -1 если меньше, 0 если равны
    """
    return rpm.labelCompare((None, version1, None), (None, version2, None))

def compare_packages(packages_sisyphus, packages_p10):
    arch_comparison = {}

    # Получаем архитектуры из данных
    sisyphus_packages = packages_sisyphus.get('packages', [])
    p10_packages = packages_p10.get('packages', [])

    # Группируем пакеты по архитектуре
    sisyphus_archs = {}
    for pkg in sisyphus_packages:
        arch = pkg['arch']
        if arch not in sisyphus_archs:
            sisyphus_archs[arch] = {}
        sisyphus_archs[arch][pkg['name']] = pkg

    p10_archs = {}
    for pkg in p10_packages:
        arch = pkg['arch']
        if arch not in p10_archs:
            p10_archs[arch] = {}
        p10_archs[arch][pkg['name']] = pkg

    # Сравниваем пакеты
    for arch in sisyphus_archs.keys() | p10_archs.keys():
        sisyphus_set = set(sisyphus_archs.get(arch, {}).keys())
        p10_set = set(p10_archs.get(arch, {}).keys())

        only_in_p10 = list(p10_set - sisyphus_set)
        only_in_sisyphus = list(sisyphus_set - p10_set)

        version_higher_in_sisyphus = []
        for pkg in sisyphus_set & p10_set:
            sisyphus_version = sisyphus_archs[arch][pkg]['version']
            p10_version = p10_archs[arch][pkg]['version']
            if rpm_vercmp(sisyphus_version, p10_version) > 0:
                version_higher_in_sisyphus.append(pkg)

        arch_comparison[arch] = {
            "only_in_p10": only_in_p10,
            "only_in_sisyphus": only_in_sisyphus,
            "version_higher_in_sisyphus": version_higher_in_sisyphus
        }

    return arch_comparison