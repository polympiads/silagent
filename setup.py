import setuptools

install_requires = open("requirements.txt", "r").readlines()

setuptools.setup(
    name="silagent",
    version="0.0.0",
    author="Polympiads",
    description="Software In the Loop Agent",
    install_requires=install_requires,
    url="https://github.com/polympiads/silagent",
    packages=["silagent", "silagent.tests", "silagent.runner", "silagent.build", "silagent.core", "silagent.container"]
)
