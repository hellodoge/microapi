from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, reverse
from .models import API
from . import runner


def execute_view(request, uid):
    api = get_object_or_404(API, uid=uid)

    if not api.enabled:
        return HttpResponseNotFound

    return runner.handle_request(api, request.body)


@login_required
def disable_api_view(request, uid):
    api = get_object_or_404(API, uid=uid)
    if api.owner != request.user:
        return HttpResponseForbidden

    if api.enabled:
        api.enabled = False
        api.save(update_fields=['enabled'])
    messages.info(request, f'API {api.title} has been disabled')

    return redirect(request.GET.get('next', reverse('manager-home')))


@login_required
def enable_api_view(request, uid):
    api = get_object_or_404(API, uid=uid)
    if api.owner != request.user:
        return HttpResponseForbidden

    if not api.enabled:
        api.enabled = True
        api.save(update_fields=['enabled'])
    messages.info(request, f'API {api.title} has been enabled')

    return redirect(request.GET.get('next', reverse('manager-home')))
