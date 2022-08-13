import os

from core.settings.base import (AWS_STORAGE_BUCKET_NAME, EMAIL_HOST_PASSWORD,
                                EMAIL_HOST_USER)
from django.core.mail import send_mail
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorge(S3Boto3Storage):
    bucket_name = AWS_STORAGE_BUCKET_NAME
    
def getS3FileUrl(filename):
    try: 
        file_dir_name_within_bucket = filename
        file_path_within_bucket = os.path.join(file_dir_name_within_bucket)

        media_storage = MediaStorge()

        file_url = media_storage.url(file_dir_name_within_bucket)
        return file_url

    except Exception as e : 
        print("Error at get s3 url")
        print
        
def dictFetchAll(cursor):
    columns = [col[0] for col in cursor.description]
    
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class SendVerificationOTP(object):
    @staticmethod
    def send_mail_otp(otp, to_email_address):
        try: 
            print(f"{EMAIL_HOST_USER} : {EMAIL_HOST_PASSWORD}")
            return send_mail(subject="Signup OTP for Zipcho",
                            message=f"Your verification otp is {otp}.",
                            from_email=EMAIL_HOST_USER, 
                            recipient_list=[to_email_address],
                            fail_silently=False)

        except Exception as e:
            print(e)
            print("Failed at  sending otp in mail")
            return 0

