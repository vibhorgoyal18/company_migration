from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from migration import views

# API endpoints
urlpatterns = format_suffix_patterns([
    path('env-variables', views.MigrateEnvVariables.as_view()),
    path('company-settings', views.MigrateCompanySettings.as_view()),
    path('cities-branches', views.MigrateCitiesAndBranches.as_view()),
    path('update-post-url', views.UpdatePostUrl.as_view()),
    path('publish-processes', views.PublishProcesses.as_view()),
    path('assign-default-hub', views.AddDefaultHub.as_view()),
    path('datastore', views.MigrateDataStore.as_view()),
])
