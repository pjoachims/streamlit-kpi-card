import setuptools
from pathlib import Path

# Read the README file for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="streamlit-kpi-card",
    version="0.1.0",
    author="",
    author_email="",
    description="A beautiful, interactive KPI card component for Streamlit with time series visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pjoachims/streamlit-kpi-card",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Streamlit",
    ],
    keywords="streamlit kpi card metrics dashboard visualization",
    python_requires=">=3.7",
    install_requires=[
        "streamlit>=1.0.0",
        "pandas>=1.0.0",
    ],
)
