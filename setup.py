import setuptools


setuptools.setup(
    name="v6wos", version="24.0.0",
    packages=setuptools.find_packages(),
    author="Stefano Palazzo",
    author_email="stefano.palazzo@gmail.com",
    url="https://github.com/sfstpala/v6wos",
    license="ISC",
    test_suite="v6wos.tests",
    zip_safe=False,
    install_requires=[
        "docopt==0.6.2",
        "tornado==4.4.1",
        "pyyaml==3.12",
        "jsonschema==2.5.1",
        "requests==2.11.1",
        "tornado-couchdb==0.3.0",
        "dnspython==1.14.0",
    ],
    entry_points={
        "console_scripts": [
            "v6wos = v6wos.__main__:main",
        ]
    },
    package_data={
        "v6wos": [
            "tests/integration/index.md",
            "tests/integration/hosts.md",
            "tests/integration/error.md",
            "config/local.yaml",
            "config/debug.yaml",
            "templates/index.html",
            "templates/error.html",
            "static/css/index.css",
            "static/script/env.js",
            "resources/top100.txt",
        ],
    },
)
