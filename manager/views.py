from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from api.models import API
from .models import APILog


class APIListView(LoginRequiredMixin, ListView):
    model = API

    template_name = 'manager/home.html'

    def get_queryset(self):
        return API.objects.filter(
            owner=self.request.user
        ).order_by('-enabled', '-modify_date')


class APIDetailView(LoginRequiredMixin, DetailView):
    model = API

    template_name = 'manager/api_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # https://stackoverflow.com/questions/26989078/how-to-get-full-url-from-django-request
        context['ABSOLUTE_ROOT'] = self.request.build_absolute_uri('/')[:-1].strip("/")

        logs = APILog.objects.filter(api=context.get('object')).order_by('time_logged')
        per_page: int = self.request.GET.get('per_page', 5)
        page_number: int = self.request.GET.get('page', 1)
        context['logs_page'] = Paginator(logs, per_page).get_page(page_number)

        return context


class APICreateView(LoginRequiredMixin, CreateView):
    model = API
    fields = ['title', 'python_code', 'request_body_type']

    success_url = reverse_lazy('manager-home')
    template_name = 'manager/api_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class APIUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = API
    fields = ['title', 'python_code', 'request_body_type', 'enabled']

    success_url = reverse_lazy('manager-home')
    template_name = 'manager/api_update.html'

    def form_valid(self, form):
        form.instance.compiles = None
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().owner == self.request.user


class DeleteAPIView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = API

    success_url = reverse_lazy('manager-home')
    template_name = 'manager/api_delete.html'

    def test_func(self):
        return self.get_object().owner == self.request.user


@login_required
def reset_api_view(request, uid):
    api = get_object_or_404(API, uid=uid)
    if api.owner != request.user:
        return HttpResponseForbidden

    if request.method == 'POST':
        APILog.objects.filter(api=api).delete()

        if api.storage is not None:
            api.storage = None
            api.save(update_fields=['storage'])
        messages.info(request, f'API {api.title} has been reset')
        return redirect(request.GET.get('next', reverse('manager-api', args=[api.uid])))

    return render(request, 'manager/api_reset.html', context={'api': api})
