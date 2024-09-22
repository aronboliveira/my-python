from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Controller

urlpatterns = [
    path('admin/', admin.site.urls),
    path('studs_table/', Controller.as_view(actions={'get': 'studs_table'}), name='studs_table'),
    path('profs_table/', Controller.as_view(actions={'get': 'profs_table'}), name='profs_table'),
    path('patients_table/', Controller.as_view(actions={'get': 'patients_table'}), name='patients_table'),
    path('check_user_validity/', Controller.as_view(actions={'get': 'check_user_validity'}), name='user_validity'),
    path('submit_ag_form/', Controller.as_view(actions={'post': 'submit_ag_form'}), name='ag_form'),
    path('submit_ed_form/', Controller.as_view(actions={'post': 'submit_ed_form'}), name='ed_form'),
    path('submit_od_form/', Controller.as_view(actions={'post': 'submit_od_form'}), name='od_form'),
    path('submit_cons_form/', Controller.as_view(actions={'post': 'submit_cons_form'}), name='cons_form'),
    path('submit_stud_form/', Controller.as_view(actions={'post': 'submit_stud_form'}), name='stud_form'),
    path('submit_prof_form/', Controller.as_view(actions={'post': 'submit_prof_form'}), name='prof_form'),
    path('schedule_form/', Controller.as_view(actions={'post': 'schedule_form'}), name='schedule_form')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
