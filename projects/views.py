from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from documents.forms import DocumentForm
from documents.models import Documents
from kala.views import LoginRequiredMixin, AdminRequiredMixin
from people.models import People
from .models import Projects
from .forms import ProjectForm, permission_forms


class ProjectsView(LoginRequiredMixin, TemplateView):
    template_name = 'projects.html'

    def get_context_data(self, **kwargs):
        return {
            'companies': self.request.user.get_companies_list(),
            'form': self.form,
            }

    def dispatch(self, request, *args, **kwargs):
        self.form = ProjectForm(request.POST or None, company=request.user.company,
                                is_admin=self.request.user.is_admin)
        return super(ProjectsView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'You do not have permission to create a new project')
            return redirect(reverse('projects'))

        if self.form.is_valid():
            project = self.form.save()
            messages.success(request, 'The project has been created')
            return redirect(reverse('project', args=[project.pk]))
        return self.render_to_response(self.get_context_data())


class ProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'project.html'

    def get_context_data(self, **kwargs):
        return {
            'documents': Documents.active.filter(project=self.project),
            'form': self.form,
            'project': self.project,
            }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Projects.active, pk=pk)
        person = People.objects.get(pk=self.request.user.pk)
        self.form = DocumentForm(request.POST or None, request.FILES or None, person=person,
                                 project=self.project)
        return super(ProjectView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            if request.user.is_admin:
                self.project.set_active(False)
                messages.success(request, 'The project has been deleted')
                return redirect(reverse('projects'))
            else:
                messages.error(request, 'You do not have permission to delete this project')
                return redirect(reverse('project', args=[self.project.pk]))

        if self.form.is_valid():
            self.form.save()
            messages.success(request, 'The document has been created')
            return redirect(reverse('project', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())


class ProjectPermissions(AdminRequiredMixin, TemplateView):
    template_name = 'permissions.html'

    def get_context_data(self, **kwargs):
        return {
            'forms': self.forms,
            'project': self.project,
            }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Projects.active, pk=pk)
        self.forms = permission_forms(request, self.project)
        return super(ProjectPermissions, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        all_valid = True
        for form in self.forms:
            if form.is_valid():
                form.save()
            else:
                all_valid = False
        if all_valid:
            messages.success(request, 'The permissions have been updated.')
            return redirect(reverse('permissions', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())