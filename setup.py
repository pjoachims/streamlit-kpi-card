import setuptools

setuptools.setup(
    name="streamlit-kpi-card",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A beautiful KPI card component for Streamlit",
    long_description="A custom Streamlit component for displaying KPI metrics with values, deltas, and time series charts.",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "streamlit>=1.0.0",
        "pandas>=1.0.0",
    ],
)
