import json
import multiprocessing
from django.http import (
    HttpResponse,
    HttpResponseServerError,
    HttpResponseBadRequest,
    JsonResponse
)
from RestrictedPython import compile_restricted, safe_globals
from microapi import config
from .models import API
from manager.models import APILog


def handle_request(api: API, request_body):
    queue = multiprocessing.Queue()

    proc = multiprocessing.Process(
        target=lambda: queue.put(run(api, request_body)),
    )
    proc.start()
    proc.join(config.RUNNER_TIMEOUT / 1000)

    if proc.is_alive():
        proc.terminate()
        return HttpResponseServerError(TimeoutError)
    else:
        return queue.get()


def run(api: API, request_body):

    loc = {}
    try:
        byte_code = compile_restricted(api.python_code, '<inline>', 'exec')
        exec(byte_code, safe_globals, loc)

        api.compiles = True
        api.save(update_fields=['compiles'])

    except Exception as e:
        api.compiles = False
        api.save(update_fields=['compiles'])
        return HttpResponseServerError(e)

    try:
        request = parse_request_body(request_body, api.request_body_type)
    except Exception as e:
        return HttpResponseBadRequest(e)

    try:

        if api.storage is None and config.INIT_FUNCTION_NAME in loc:
            api.storage = loc[config.INIT_FUNCTION_NAME]()
            api.save(update_fields=['storage'])

        if config.LOG_FUNCTION_NAME in loc:
            message = loc[config.LOG_FUNCTION_NAME](request, api.storage)
            if message is not None:
                APILog(message=str(message)[:100], api=api).save()

        if config.RESPONSE_FUNCTION_NAME not in loc:
            raise NameError(f'{config.RESPONSE_FUNCTION_NAME} is not defined')
        response = loc[config.RESPONSE_FUNCTION_NAME](request, api.storage)

        if config.UPDATE_FUNCTION_NAME in loc:
            api.storage = loc[config.UPDATE_FUNCTION_NAME](request, api.storage)
            api.save(update_fields=['storage'])

    except Exception as e:
        return HttpResponseServerError(e)

    if type(response) == dict:
        return JsonResponse(response)
    else:
        return HttpResponse(response)


def parse_request_body(body, body_type):
    if body_type == API.RequestBodyType.RAW_TEXT:
        return body.decode()
    elif body_type == API.RequestBodyType.JSON:
        return json.loads(body.decode())
    elif body_type == API.RequestBodyType.RAW_BIN:
        return bytes(body)
    raise NotImplementedError
