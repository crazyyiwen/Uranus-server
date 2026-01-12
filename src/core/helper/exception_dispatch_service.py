from functools import singledispatch
from fastapi import HTTPException
import traceback

from core.models.return_model import ReturnModel

# Define generic exception handler to cover as many kinds of exception as possible
# exception structure:
# 1 status_code: depends on if it's api call
# 2 location: should be hidden for clients
# 3 exception str: should be exposed to clients
@singledispatch
def catch_exception(ex):
    return ex

# modify exception classification and details
# Define specific exception handler
@catch_exception.register
def _exception(ex: HTTPException):
    # specific http error 
    status = ex.status_code
    has_exception = True
    exception = ex.detail
    return ReturnModel(None, status, exception, has_exception)

@catch_exception.register
def _exception(ex: AttributeError):
    has_exception = True
    return ReturnModel(None, 500, traceback.format_exc(), has_exception)

@catch_exception.register
def _exception(ex: KeyError):
    has_exception = True
    return ReturnModel(None, 500, traceback.format_exc(), has_exception)

@catch_exception.register
def _exception(ex: TypeError):
    has_exception = True
    return ReturnModel(None, 500, traceback.format_exc(), has_exception)