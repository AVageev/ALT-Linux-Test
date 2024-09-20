import argparse
import json
from altlinux import fetch_branch_packages, compare_packages

def main():
    parser = argparse.ArgumentParser(description="Compare ALT Linux branches package lists")
    parser.add_argument('--output', help='Output file to save JSON result', default='output.json')
    args = parser.parse_args()

    # Получаем данные из API
    packages_sisyphus = fetch_branch_packages('sisyphus')
    packages_p10 = fetch_branch_packages('p10')

    # Сравниваем списки пакетов
    comparison_result = compare_packages(packages_sisyphus, packages_p10)

    # Записываем результат в файл
    with open(args.output, 'w') as f:
        json.dump(comparison_result, f, indent=4)


if __name__ == '__main__':
    main()