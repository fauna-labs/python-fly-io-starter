from fauna.errors import FaunaException, FaunaError, AuthenticationError, AuthorizationError, QueryRuntimeError, AbortError


def generate_response(inputObject):
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type, Origin, X-Requested-With, Accept, Authorization, Access-Control-Allow-Methods, Access-Control-Allow-Headers, Access-Control-Allow-Origin",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT"
        },
        "body": inputObject
    }

def generate_error_response(err):    
    errorType = type(err)
    if errorType == AbortError:
        code = 400
        responseBody = err.abort
    elif errorType in (FaunaException, FaunaError, AuthenticationError, AuthorizationError):
        code = err.args[0]
        responseBody = err.args[1]
    elif errorType == QueryRuntimeError:
        code = err.args[0]
        responseBody = err.query_info.summary
    else:
        code = 400
        responseBody = err.args[0]

    response = {
        "statusCode": code,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type, Origin, X-Requested-With, Accept, Authorization, Access-Control-Allow-Methods, Access-Control-Allow-Headers, Access-Control-Allow-Origin",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT"
        },
        "body": responseBody
    }

    return response 