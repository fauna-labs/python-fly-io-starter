# Copyright Fauna, Inc.
# SPDX-License-Identifier: MIT-0

from fauna.errors import (
    FaunaError,
    AbortError,
)
from fauna.encoding import QuerySuccess, QueryStats
from fauna import Page
import os


def generate_response(res: QuerySuccess):
    stats: QueryStats = res.stats
    data = res.data
    if type(res.data) == Page:
        data = data.data

    headers = {
        "Access-Control-Allow-Headers": "Content-Type, Origin, X-Requested-With, Accept, Authorization, Access-Control-Allow-Methods, Access-Control-Allow-Headers, Access-Control-Allow-Origin",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT",
    }
    response = {
        "flyStats": {"usingFlyRegion": os.getenv("FLY_REGION", "unknown")},
        "faunaStats": {
            "query_time_ms": stats.query_time_ms,
            "compute_ops": stats.compute_ops,
            "read_ops": stats.read_ops,
            "write_ops": stats.write_ops,
        },
        "data": data,
    }
    return response, 200, headers


def generate_error_response(error: FaunaError):
    code = error.status_code
    responseBody = error.message

    errorType = type(error)    
    if errorType == AbortError:
        responseBody = error.abort

    headers = {
        "Access-Control-Allow-Headers": "Content-Type, Origin, X-Requested-With, Accept, Authorization, Access-Control-Allow-Methods, Access-Control-Allow-Headers, Access-Control-Allow-Origin",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT",
    }
    response = {"error": responseBody}

    return response, code, headers
