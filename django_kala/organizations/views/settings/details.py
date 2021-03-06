from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from organizations.models import Organization
from organizations.forms import DetailsForm


class DetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'organizations/settings/details.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'organization': self.organization,
            'can_invite': self.organization.has_change(self.request.user) or self.organization.has_create(
                self.request.user),
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.organization = get_object_or_404(Organization.objects.active(), pk=pk)
        if not self.organization.has_change(request.user):
            raise PermissionDenied('You do not have permission to change this organization.')
        self.form = DetailsForm(request.POST or None, instance=self.organization)
        return super(DetailsView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save()
            return redirect(reverse('organizations:details', args=[self.organization.pk]))
        return self.render_to_response(self.get_context_data())
