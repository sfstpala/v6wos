# Index

The `/api` route returns basic information about the service:

    >>> res = get("/api")
    >>> res.status_code
    200
    >>> dump(res.json())
    {
        "service": "xcvb",
        "version": "... (...)"
    }
