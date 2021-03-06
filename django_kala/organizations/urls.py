from django.conf.urls import url
from .views import OrganizationsView, NewOrganizationView, DetailsView, ManageAccessView

app_name='organizations'

urlpatterns = [
    url(
        regex=r'^$',
        view=OrganizationsView.as_view(),
        name='organizations',
    ),

    url(
        regex=r'^(?P<pk>\d+)/$',
        view=OrganizationsView.as_view(),
        name='organization',
    ),

    url(
        regex=r'^new$',
        view=NewOrganizationView.as_view(),
        name='new_organization',
    ),

    url(
        regex=r'^(?P<pk>\d+)/settings/details$',
        view=DetailsView.as_view(),
        name='details'
    ),

    url(
        regex=r'^(?P<pk>\d+)/settings/manage_access',
        view=ManageAccessView.as_view(),
        name='manage_access'
    ),

]
