from setuptools import find_packages, setup

version = "0.1.0"


with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="cohort_utils",
    version=version,
    description="Helper tools for cohorts",
    author="Anne Marie Noronha",
    install_requires=required,
    packages=find_packages(where="."),
    package_dir={"": "."},
    package_data={"": ["**/*.json"]}
)



