from setuptools import setup, find_packages

setup(
    name="tbget",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "tbget = tbget.tool:main"
        ]
    },
    package_data={
        # Include the test case files
        'tbget.testcases': ['*.txt'],
    },

    description="Tool for extracting Python tracebacks from anything.",
    author="John Sullivan",
    author_email="johnsullivan.pem+tbget@gmail.com",
    url="http://johncs.com",
)
