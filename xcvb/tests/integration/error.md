# Error

    >>> res = requests.get("http://{}/api/404".format(host))
    >>> res.status_code
    404
    >>> dump(res.json())
    {
        "reason": "not found",
        "status": 404
    }
