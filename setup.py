from setuptools import setup, find_packages


def get_requirements() -> str:

    file_path = "C:\\Users\\hp\\Desktop\\Sensor-Fault-Detection\\requirements.txt"

    HypenEDot = '-e .'

    file = open(file_path, 'r')

    install_requirements = []

    for req in file.readlines():
        install_requirements.append(str(req.replace('\n', ' ')))

    return install_requirements.remove(HypenEDot)


setup(

    name="Sensor_Fault_Detection",
    version="0.0.1",
    author="Komal",
    author_email="saianurag234@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()


)
