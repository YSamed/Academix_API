from rest_framework import serializers
from attendance.models import QRCode
from teachers.models import Teacher
from academics.models import Subject

class AttendanceSerializer(serializers.Serializer):
    subject_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )

    def validate(self, data):
        teacher = self.context['teacher']
        subject_ids = data['subject_ids']
        valid_subjects = teacher.subjects.filter(id__in=subject_ids)

        if valid_subjects.count() != len(subject_ids):
            raise serializers.ValidationError("Geçersiz ders seçimi.")
        
        return data
