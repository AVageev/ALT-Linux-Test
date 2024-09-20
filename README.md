ALT Linux Package Comparison Tool
This Python module and CLI utility allows you to retrieve and compare the package lists from two branches of the ALT Linux distribution: sisyphus and p10. The output is a JSON structure containing:

Packages that exist in p10 but not in sisyphus
Packages that exist in sisyphus but not in p10
Packages where the version-release in sisyphus is greater than in p10, for each supported architecture.
Prerequisites
Python 3.10 or higher
RPM package manager
ALT Linux API access
Installation:

git clone https://github.com/AVageev/ALT-Linux-Test.git
cd altlinux-test
pip install -r requirements.txt
sudo apt-get update
sudo apt-get install rpm python3-rpm
python3 src/cli/compare_packages.py --output result.json

This will create a result.json file containing the comparison results.

Command-Line Options
--output <file>: Specify the output file for the comparison results (default is output.json).