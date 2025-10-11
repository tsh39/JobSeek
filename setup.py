from setuptools import setup, find_packages

setup(
    name="jobseek",
    version="0.1.0",
    description="Modular job scraper for multiple ATS platforms",
    author="JobSeek Contributors",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "urllib3>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "jobseek=jobseek.cli:main",
        ],
    },
)
