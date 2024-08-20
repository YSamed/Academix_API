from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsStudent  

from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta
import secrets
import qrcode
from io import BytesIO
import base64

from attendance.models import QRCode, Attendance
from academics.models import Subject
from teachers.models import Teacher
from students.models import Student
from .permissions import IsTeacher, IsManager

class CleanupAttendanceAPIView(APIView):
    def post(self, request, *args, **kwargs):
        now = timezone.now()
        one_minute_ago = now - timedelta(minutes=1)
        count, _ = Attendance.objects.filter(timestamp__lt=one_minute_ago).delete()
        return Response({'status': f'Successfully deleted {count} records.'}, status=status.HTTP_200_OK)

class StartAttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher | IsManager]

    def post(self, request, *args, **kwargs):
        form_data = request.data
        selected_subject_ids = form_data.get('subject_ids', [])
        teacher_id = form_data.get('teacher_id')

        if not teacher_id:
            return Response({'error': 'Öğretmen ID\'si gerekli.'}, status=status.HTTP_400_BAD_REQUEST)

        teacher = get_object_or_404(Teacher, id=teacher_id)

        if not selected_subject_ids:
            return Response({'error': 'En az bir ders seçilmelidir.'}, status=status.HTTP_400_BAD_REQUEST)

        # Öğretmen için geçerli dersleri al
        if request.user.groups.filter(name='Teacher').exists():
            teacher_subject_ids = teacher.subjects.values_list('id', flat=True)
            valid_subject_ids = [sid for sid in selected_subject_ids if sid in teacher_subject_ids]
            subjects = Subject.objects.filter(id__in=valid_subject_ids)
        else:
            subjects = Subject.objects.filter(id__in=selected_subject_ids)

        if subjects.count() != len(selected_subject_ids):
            return Response({'error': 'Geçersiz ders ID\'leri.'}, status=status.HTTP_400_BAD_REQUEST)

        QRCode.objects.filter(subject__in=subjects, teacher=teacher, is_active=True).update(is_active=False)

        qr_codes = []
        for subject in subjects:
            qr_code, qr_code_base64 = self.generate_qr_code_and_password(subject.id, teacher)
            qr_codes.append({
                'subject': subject.name,
                'qr_code': qr_code_base64,
                'password': qr_code.password
            })

        response_data = {
            'qr_codes': qr_codes,
            'teacher': {
                'first_name': teacher.first_name,
                'last_name': teacher.last_name,
            },
            'subjects': list(subjects.values('name'))
        }

        return Response(response_data)

    def generate_qr_code_and_password(self, subject_id, teacher):
        code = secrets.token_urlsafe(16)
        password = secrets.token_hex(3)
        expires_at = timezone.now() + timedelta(seconds=10)  # 10 saniye geçerlilik süresi

        subject = get_object_or_404(Subject, id=subject_id)

        qr_code = QRCode.objects.create(
            code=code,
            password=password,
            expires_at=expires_at,
            subject=subject,
            teacher=teacher,
            is_active=True
        )

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(code)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        buffered = BytesIO()
        img.save(buffered, 'PNG')
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return qr_code, img_str



class ScanQRCodeAPIView(APIView):
    permission_classes = [IsAuthenticated, IsStudent] 

    def post(self, request, *args, **kwargs):
        qr_code_data = request.data.get('qr_code')
        password = request.data.get('password')
        student_id = request.data.get('student_id')

        # Öğrenci ID'si kontrolü
        if not student_id:
            return Response({'status': 'student_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        student = get_object_or_404(Student, id=student_id)

        # QR kodu veya şifre gerekli
        if not qr_code_data and not password:
            return Response({'status': 'qr_code or password is required'}, status=status.HTTP_400_BAD_REQUEST)

        # QR kodunu bulma
        qr_code = None
        if qr_code_data:
            qr_code = QRCode.objects.filter(code=qr_code_data, is_active=True).first()
        elif password:
            qr_code = QRCode.objects.filter(password=password, is_active=True).first()

        # QR kodu geçerli mi kontrolü
        if qr_code:
            if qr_code.is_valid() and (password == qr_code.password or not password):
                # Katılım kaydını oluştur
                Attendance.objects.create(student=student, qr_code=qr_code)
                # QR kodunu geçersiz kıl
                qr_code.is_active = False
                qr_code.save()
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'Invalid or expired QR code or incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'status': 'QR code or password is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        return Response({'student_id': student.id}, status=status.HTTP_200_OK)