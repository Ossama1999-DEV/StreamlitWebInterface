from setuptools import setup, find_packages 

setup(
    name="aocs_interface",
    version="0.1.0",
    description="AOCS Equipment Web Interface",
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
