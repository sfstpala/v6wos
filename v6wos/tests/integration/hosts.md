# Hosts

The `/api/hosts` route returns the list of hosts and whether
they have an AAAA record:

    >>> res = get("/api/hosts")
    >>> res.status_code
    200
    >>> dump(res.json())
    {
        "hosts": [
            "google.com",
            ...
        ]
    }

    >>> res = get("/api/hosts/google.com")
    >>> res.status_code
    200
    >>> dump(res.json())
    {
        "aaaa": [
            ...
        ],
        "host": "google.com"
    }
