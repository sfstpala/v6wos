import setuptools


setuptools.setup(
    name="xcvb", version="24.0.0",
    packages=setuptools.find_packages(),
    author="Stefano Palazzo",
    author_email="stefano.palazzo@gmail.com",
    url="https://github.com/sfstpala/xcvb",
    license="ISC",
    test_suite="xcvb.tests",
    zip_safe=False,
    install_requires=[
        "docopt==0.6.2",
        "tornado==4.4.1",
        "pyyaml==3.11",
        "jsonschema==2.5.1",
        "requests==2.11.1",
        "tornado-couchdb==0.3.0",
    ],
    entry_points={
        "console_scripts": [
            "xcvb = xcvb.__main__:main",
        ]
    },
    package_data={
        "xcvb": [
            "tests/integration/index.md",
            "tests/integration/error.md",
            "config/local.yaml",
            "config/debug.yaml",
            "templates/index.html",
            "templates/error.html",
            "static/css/index.css",
            "static/script/env.js",
        ],
    },
)
