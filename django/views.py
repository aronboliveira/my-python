# views.py
from django.http import JsonResponse
from django.views import View
from .models import User, Patient, Student, Professional, Appointment, AGData, EDData, OdData, Schedule
from django.core.management import call_command

class Controller(View):
    def check_user_validity(request, id):
        try:
            user = User.objects.get(id=id)
            if user:
                if user.authorized:
                    return Controller.res_user_validity(2)
                else:
                    return Controller.res_user_validity(1)
            else:
                return Controller.res_user_validity(0)
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return Controller.res_user_validity(-1)
    @staticmethod
    def res_user_validity(n):
        if n == -1:
            return JsonResponse({"message": "Failed to connect"}, status=500)
        elif n == 0:
            return JsonResponse({"message": "User not registered"}, status=404)
        elif n == 1:
            return JsonResponse({"message": "User not authorized"}, status=403)
        elif n == 2:
            return JsonResponse({"message": "User authorized"}, status=200)
        else:
            return JsonResponse({"message": "Unknown status"}, status=400)
    def studs_table(self):
        return JsonResponse(list(Student.objects.values('id', 'cpf', 'dre', 'graduation', 'semester', 'beginning_semester', 'beginning_day', 'activity_day')), 
        safe=False)
    def profs_table(self):
        return JsonResponse(list(Professional.objects.values(
            'id', 'cpf', 'graduation', 'beginning_semester', 'beginning_day'
        )), safe=False)
    def patients_table(self):
        return JsonResponse(list(Patient.objects.values(
            'id', 'cpf', 'name', 'email', 'telephone', 'next_appointed_day',
            'treatment_period', 'signature', 'current_status', 'historic__date',
            'historic__type', 'historic__professional__id', 'historic__student__id',
            'historic__notes'
        )), safe=False)
    def submit_ag_form(self, request):
        return self._handle_form_submission(request, AGData, 'ag_data', 'submit_ag_form')
    def submit_ed_form(self, request):
        return self._handle_form_submission(request, EDData, 'ed_data', 'submit_ed_form')
    def submit_od_form(self, request):
        return self._handle_form_submission(request, OdData, 'od_data', 'submit_od_form')
    def submit_cons_form(self, request):
        return self._handle_appointment_form_submission(request)
    def submit_stud_form(self, request):
        return self._handle_form_submission(request, Student, 'students', 'submit_stud_form')
    def submit_prof_form(self, request):
        return self._handle_form_submission(request, Professional, 'professionals', 'submit_prof_form')
    def schedule_form(self, request):
        return self._handle_form_submission(request, Schedule, 'schedules', 'schedule_form')
    def _handle_form_submission(self, request, model_cls, dynamic_table_name, method_name):
        if request.method == 'POST':
            try:
                form_data = request.POST  
                submitter_id = form_data.get('submitter_id')  
                submitter_privilege = form_data.get('submitter_privilege')
                if submitter_privilege == 'student':
                    submitter_model = Student
                else:
                    submitter_model = Professional
                submitter, _ = submitter_model.objects.get_or_create(id=submitter_id)
                dynamic_data = model_cls.objects.create(
                    submitter_id=submitter.id,
                    submitter_privilege=submitter_privilege,
                    submitter_name=submitter.name,
                )
                try:
                    call_command('makemigrations')
                    call_command('migrate')
                    return JsonResponse({'message': 'Form submitted successfully.'})
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=500)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
    def _handle_appointment_form_submission(self, request):
        if request.method == 'POST':
            try:
                form_data = request.POST
                patient_id = form_data.get('patient_id')
                professional_id = form_data.get('professional_id')
                student_id = form_data.get('student_id')
                patient, _ = Patient.objects.get_or_create(id=patient_id)
                professional, _ = Professional.objects.get_or_create(id=professional_id)
                student, _ = Student.objects.get_or_create(id=student_id)
                appointment = Appointment.objects.create(
                    patient=patient,
                    professional=professional,
                    student=student,
                )
                return JsonResponse({'message': 'Form submitted successfully.'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)