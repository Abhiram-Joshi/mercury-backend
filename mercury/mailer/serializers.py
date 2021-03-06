from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    sender_name = serializers.CharField(max_length=50)
    sender_email = serializers.EmailField()
    recipients = serializers.FileField(max_length=100, allow_empty_file=False)
    subject = serializers.CharField(max_length=1000)
    body_text = serializers.CharField()
    body_mjml = serializers.CharField()
    aws_region = serializers.CharField(max_length=20, default="ap-south-1")


class TestEmailSerializer(serializers.Serializer):
    sender_name = serializers.CharField(max_length=50)
    sender_email = serializers.EmailField()
    test_recipient_emails = serializers.ListField()
    recipients = serializers.FileField(max_length=100, allow_empty_file=False)
    subject = serializers.CharField(max_length=1000)
    body_text = serializers.CharField()
    body_mjml = serializers.CharField()
    aws_region = serializers.CharField(max_length=20, default="ap-south-1")


class GetUrlSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    image = serializers.ImageField(allow_empty_file=False)
