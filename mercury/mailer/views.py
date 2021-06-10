import csv
import io

import boto3
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EmailSerializer, GetUrlSerializer, TestEmailSerializer
from .utilities import render_templates, send_email


class GetUrlView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = GetUrlSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = serializer.validated_data["image"]
        file_name = serializer.validated_data["file_name"]

        c = 1
        response = {
            "data": [],
        }

        s3_resource = boto3.resource("s3")
        bucket_name = "mercury-mailer"

        s3_resource.Bucket(bucket_name).put_object(
            Key=f"{file_name}.png",
            Body=image,
            ACL="public-read",
            ContentType="image/png",
            ContentDisposition="inline",
        )

        response["data"].append(
            f"https://{bucket_name}.s3.ap-south-1.amazonaws.com/{file_name}.png"
        )
        c += 1

        return Response(response)


class SendEmailView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = {}
        c = 1
        serializer = EmailSerializer(data=request.data)

        if serializer.is_valid():

            file = serializer.validated_data["recipients"]

            recipient_data = csv.DictReader(io.StringIO(file.read().decode()))

            for data in recipient_data:

                body_html = render_templates(
                    serializer.validated_data["body_mjml"], data
                )

                response[c] = send_email(
                    sender_name=serializer.validated_data["sender_name"],
                    sender_email=serializer.validated_data["sender_email"],
                    recipient_email=data["email"],
                    subject=serializer.validated_data["subject"],
                    body_text=serializer.validated_data["body_text"],
                    body_html=body_html,
                    aws_region=serializer.validated_data["aws_region"],
                )
                c += 1

        else:
            response = serializer.errors

        return Response(response)


class SendTestEmailView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = {}
        c = 1
        serializer = TestEmailSerializer(data=request.data)

        if serializer.is_valid():

            file = serializer.validated_data["recipients"]

            recipient_data = csv.DictReader(io.StringIO(file.read().decode()))
            data = [i for i in recipient_data]

            test_recipient_emails = serializer.validated_data[
                "test_recipient_emails"
            ] + [serializer.validated_data["sender_email"]]

            for email in test_recipient_emails:

                body_html = render_templates(
                    serializer.validated_data["body_mjml"], data[0]
                )

                response[c] = send_email(
                    sender_name=serializer.validated_data["sender_name"],
                    sender_email=serializer.validated_data["sender_email"],
                    recipient_email=email,
                    subject=serializer.validated_data["subject"],
                    body_text=serializer.validated_data["body_text"],
                    body_html=body_html,
                    aws_region=serializer.validated_data["aws_region"],
                )
                c += 1

        else:
            response = serializer.errors

        return Response(response)
