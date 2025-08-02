from setuptools import setup, find_packages 

setup(
    name="WebInterface",
    version="0.1.0",
    description="Web Interface",
    author="Ton Nom",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "click",
        "openpyxl",
    ],
    python_requires=">=3.7",
)
