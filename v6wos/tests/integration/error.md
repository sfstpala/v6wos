# Error

    >>> res = get("/api/404")
    >>> res.status_code
    404
    >>> dump(res.json())
    {
        "reason": "not found",
        "status": 404
    }
