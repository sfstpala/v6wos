# Index

    >>> res = requests.get("http://{}/api".format(host))
    >>> res.status_code
    200
    >>> dump(res.json())
    {
        "service": "xcvb",
        "version": "..."
    }
