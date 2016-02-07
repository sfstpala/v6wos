import setuptools


setuptools.setup(
    name="c24", version="24.0.0",
    packages=setuptools.find_packages(),
    author="Stefano Palazzo",
    author_email="stefano.palazzo@gmail.com",
    url="https://github.com/sfstpala/c24",
    license="ISC",
    test_suite="c24.tests",
    zip_safe=False,
    install_requires=[
        "docopt==0.6.2",
        "tornado==4.3",
        "pyyaml==3.11",
        "jsonschema==2.5.1",
    ],
    entry_points={
        "console_scripts": [
            "c24 = c24.__main__:main",
        ]
    },
    package_data={
        "c24": [
            "config/local.yaml",
            "config/debug.yaml",
            "templates/index.html",
            "templates/error.html",
            "static/css/index.css",
        ],
    },
)
