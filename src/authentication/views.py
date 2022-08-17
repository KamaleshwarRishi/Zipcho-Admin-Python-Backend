import json

from core.settings.base import SUPPORT_EMAIL_USER
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import connection
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.decorators import (api_view, parser_classes,
                                       permission_classes)
from rest_framework.exceptions import NotAuthenticated, UnsupportedMediaType
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from zipchoAdmin.zipchoReponse import countryResponse, genderReponse

from .authResponse import *
from .models import *
from .serializer import *
from .utils import SendVerificationOTP, dictFetchAll, getS3FileUrl


@extend_schema(methods=['post'], request=loginEmailPwdRequest,
                    responses={200: loginResponse, 400 : ErrorResponse})
#@extend_schema(methods=['post'], request=loginEmailPwdRequest,
#                    responses={200: loginResponse, 400 : ErrorResponse})
@api_view(['POST'])
@permission_classes([])
def login(request):
    try : 
        print("At loginWithEmail")
        data = request.data
        check = 0 

        if User.objects.filter(email = data['emailMobile']).exists() : 
            print("Logged in with email")
            user = User.objects.get(email = data['emailMobile'])
            check = 1
        
        if User.objects.filter(mobileNumber = data['emailMobile']).exists() : 
            print("Logged in with Mobile Number")
            user = User.objects.get(mobileNumber = data['emailMobile']) 
            check = 1 
        
        if check == 1 and user.check_password(data['password']):
            print("here")
            ismobileNumberVerified = user.mobileNumberVerified
            if ismobileNumberVerified == True:
                print("Password is correct and mobile number is verified !")
                token = RefreshToken.for_user(user)
                data = {}
                data['refresh'] = str(token)
                data['access'] = str(token.access_token)
                
                data['otp'] = 0
                data['email']  = 'NA'
                data['mobileNumber'] = 'NA'
                data['mobileNumberVerified'] = user.mobileNumberVerified

                return Response({"status": 200,"message": "Success",'data' : data})
            else : 
                print("Password is correct and mobile number is NOT verified !")
                data = {}
                data['refresh'] = 'NA'
                data['access'] = 'NA'
                data['otp'] = 1234
                data['email']  = user.email
                data['mobileNumber'] = user.mobileNumber
                data['mobileNumberVerified'] = user.mobileNumberVerified

                return Response({"status" : 403, "message" : "Mobile Number Not Verified", 
                                "data": data})

        else : 
            raise Exception('Email or Password Mismatch')
    
    except ObjectDoesNotExist as e : 
        print(e)
        message = "Not Account Found. Please Signup"
        return Response({"status": 409,"message": message, "data" : None})
    
    except Exception as e : 
        print(e)
        message = "Failed at Login"
        if e.args[0] == 'Mobile Number or Password Mismatch' :
            message = str(e.args[0])
        return Response({"status": 400,"message": message, "data": None})

@extend_schema(methods=['post'], request=sigupRequest,
                    responses={200: signupResponse, 400 : ErrorResponse})
@csrf_exempt
@api_view(['POST'])
@permission_classes([])
def signUp(request):
    try :
        print("At Signup ... ")

        data = request.data 

        if User.objects.filter(email=data['email']).exists():
            print(f"Email already exists")
            raise Exception ("Email already exists")

        if User.objects.filter(mobileNumber=data['mobileNumber']).exists():
            print(f"MobileNumber already exists ")
            raise Exception ("MobileNumber already exists")

        user = User.objects.create(
            email=data['email'],
            username = data['email'],
            first_name = data['firstName'],
            last_name = data['lastName'],
            mobileNumber = data['mobileNumber'],
            role = data['role'],
            termsAgreed = bool(data['termsAgreed']),
            password=make_password(data['password'])
        )

        #token = RefreshToken.for_user(user)
        data = {}
        data['email']= user.email
        data['mobileNumber'] = user.mobileNumber
        # OTP Generate 3rd Party
        data['otp'] = 1234
        #data['refresh'] = str(token)
        #data['access']  = str(token.access_token)

        return Response({"status": 200,
                        "message":"Success",
                        'data':data})

    except Exception as e: 
        print(e)
        message="Signup Failed"
        if e.args[0] == 'Email already exists':
            message = str(e.args[0])
            return Response({"status": 409,"message": message, "data": None})
        if e.args[0] == 'MobileNumber already exists':
            message = str(e.args[0])
            return Response({"status": 409,"message": message, "data": None})
        print(message)
        return Response({"status": 400,"message": message, "data": None})


@extend_schema(methods=["GET"],
               responses = {200: getProfileResponse, 400 : ErrorResponse, 401: UnauthorizedResponse})
#@extend_schema(methods=['get'],
#                    responses={200: getProfileResponse, 400 : ErrorResponse})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    try :
        print("AT getProfile")
        user = list(User.objects.filter(id = request.user.id).values())[0]
       
        temp = {}
        dataToSend=[]
        
        profileData = list(profile.objects.filter(user_id=user['id']).values())[0]
        temp['userId'] = str(user['id'])
        temp['profileImage'] = getS3FileUrl(str(profileData['profileImage']))
        
        temp['firstName'] = user['first_name']
        temp['lastName'] = user['last_name']
        temp['username'] = user['username']
        temp['bio'] = profileData['bio']

        temp['email'] = user['email']
        temp['mobileNumber'] = user['mobileNumber']
        
        if profileData['gender_id'] != None :
            temp['gender'] = list(gender.objects.filter(id = profileData['gender_id']).values())[0]
        else :
            temp['gender'] = None

        if profileData['country_id'] != None :
            temp['country'] = list(country.objects.filter(id = profileData['country_id']).values('id','country'))[0]
        else : 
            temp['country'] = None
        
        dataToSend.append(temp)
        
        return Response({"status": 200,
                        "message":"Success",
                        "data":dataToSend})

    except Exception as e: 
        print(e)
        return Response({"status": 400,"message":"Failed", "data": None})


@extend_schema(methods=['post'], request = updateProfileRequest,
                    responses={200: updateProfileResponse, 400: ErrorResponse})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def updateProfile(request):
    try :
        print("AT updateProfile")

        data = request.data 

        user = User.objects.get(id = request.user.id)
        profileData = profile.objects.get(user_id=user.id)
        
        if request.FILES.get('profileImage') != None : 
            imageType = request.FILES.get('profileImage').name.split('.')[-1]
            if imageType == "jpg" or imageType == "png" or imageType == 'jpeg':
                profileData.profileImage = request.FILES.get('profileImage')
            else: 
                raise Exception("Please upload JPG/JPEG/PNG image format")

        if data['firstName'] != 'NA':
            user.first_name = data['firstName']
        
        if data['lastName'] != 'NA' :
            user.last_name = data['lastName']
        
        if data['username'] != 'NA' :
            user.username = data['username']
        
        if data['bio'] != 'NA' :
            profileData.bio = data['bio']

        if data['gender'] != 0:
            profileData.gender_id = data['gender']
        if data['country'] != 0:
            profileData.country_id = data['country']
        
        user.save()
        profileData.save()
        
        return Response({"status": 200,
                        "message":"Success"})

    except Exception as e: 
        print(e)
        status = 400
        message = 'Failed while updating profile'
        if e.args[0] == 'Please upload JPG/JPEG/PNG image format':
            message = 'Please upload JPG/JPEG/PNG image format'
            status = 415
        
        return Response({"status": status,"message": message, "data": None})

'''
class updateProfile(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer'''

@extend_schema(methods=['post'], request = verifyOTPRequest,
                    responses={200: verifyOTPResponse, 400: ErrorResponse})
@api_view(['POST'])
@permission_classes([])
def verifyOTP(request):
    try :
        print("At verifyOTP ... ")

        data = request.data 
        
        finalData = {}
        user = User.objects.get(email=data['email'], mobileNumber=data['mobileNumber'])
        if data['otp'] == 1234 : 
            
            if user.mobileNumberVerified == True :
                print("already Verified ")
                token = RefreshToken.for_user(user)
                finalData['refresh'] = str(token)
                finalData['access']  = str(token.access_token)
                return Response({"status": 200,"message":"Success" , "data" : finalData})

            if user.mobileNumberVerified == False :
                print("not Verified so verifying now .. ")
                print(f"OTP Verified for : {user}")
                user.mobileNumberVerified = True
                user.save()
                token = RefreshToken.for_user(user)
                finalData['refresh'] = str(token)
                finalData['access']  = str(token.access_token)
                return Response({"status": 200,"message":"Success" , "data" : finalData})
           
        
        return Response({"status": 400,"message":"OTP Verification Failed", "data": None})
    
    except ObjectDoesNotExist :
        message = "Not Active Accounts Found. Please Signup"
        return Response({"status": 404,"message": message, "data": None})

    except Exception as e: 
        print(e)
        message="OTP Verification Failed"
        return Response({"status": 400,"message": message, "data": None})    

@extend_schema(methods=['post'], request = resetPasswordRequest,
                    responses={200: resetPasswordResponse, 400: ErrorResponse})
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def resetPassword(request):
    try :
        print("At resetPassword ... ")

        data = request.data
        user = User.objects.get(id = request.user.id)
        
        if data['password'] == data['confirmPassword']:
            user.password=make_password(data['password'])
            user.save()
            return Response({"status": 200,"message":"Success"})
        else : 
            raise Exception("Password and Confirm Password did not match") 
    
    except ObjectDoesNotExist :
        message = "Not Active Accounts Found. Please Signup"
        return Response({"status": 404,"message": message, "data": None})

    except Exception as e: 
        print(e)
        status = 400
        message="Reset Password Failed"
        if e.args[0] == 'Password and Confirm Password did not match':
            status = 409
            message = e.args[0]
        return Response({"status": status,"message": message, "data": None})    

@extend_schema(methods=['post'], request = loginWithOTPRequest,
                    responses={200: loginWithOTPResponse,
                              400: ErrorResponse})
@api_view(['POST'])
@permission_classes([])
def loginWithOTP(request):
    try :
        print("At loginWithOTP ... ")

        data = request.data 

        if User.objects.filter(mobileNumber=data['mobileNumber']).exists():

            user = User.objects.get(mobileNumber=data['mobileNumber'])
            data = {}
            
            if user.mobileNumberVerified == True :
                print(f"{user} is verified ")

                #token = RefreshToken.for_user(user)
                #data['refresh'] = str(token)
                #data['access']  = str(token.access_token)
               
                data['mobileNumber'] = user.mobileNumber
                data['email'] = user.email
                data['otp'] = 1234
                data['mobileNumberVerified'] = user.mobileNumberVerified

                # Send Welcome Mail To User / OTP
                otpStatus = SendVerificationOTP.send_mail_otp(otp=1234, to_email_address=user.email)
                if otpStatus == 0:
                    print(f"Failed to Send Mail for : {user.email}")
                else : 
                    print(f"OTP has been send to mail : {user.email}")

                return Response({"status": 200,
                                "message":"Success",
                                'data':data})
            
            else : 
                print(f"{user} is NOT verified")
                data['mobileNumber'] = user.mobileNumber
                data['email'] = user.email
                data['otp'] = 1234
                data['mobileNumberVerified'] = user.mobileNumberVerified
                

                return Response({"status": 403,
                                "message":"Mobile Number Not Verified",
                                'data':data})
        
        else : 
            raise Exception("No active accounts found. Please signup")

    except Exception as e: 
        print(e)
        message="Login With OTP Failed"
        if e.args[0] == 'No active accounts found. Please signup':
            message = str(e.args[0])
            return Response({"status": 404,"message": message, "data": None})
        
        return Response({"status": 400,"message": message, "data": None})


@extend_schema(methods=['post'], request = validateUsernameRequest,
                    responses={200: validateUsernameResponse, 400: ErrorResponse})
@api_view(['POST'])
@permission_classes([])
def validateUsername(request):
    try :
        print("at validateUsername")
        data = request.data 
        if User.objects.filter(username=data['username']).exists():
            return Response({"status": 409,"message":"Username Already Taken", "data": None})
        else : 
            return Response({"status": 200,"message":"Success"})

    except Exception as e: 
        print(e)
        return Response({"status": 400,"message":"Failed while validating username", "data": None})

@extend_schema(methods=['post'], request = validateEmailRequest,
                    responses={200: validateEmailResponse, 400: ErrorResponse})
@api_view(['POST'])
@permission_classes([])
def validateEmail(request):
    try :
        print("at validateEmail")
        data = request.data 
        if User.objects.filter(email=data['email']).exists():
            return Response({"status": 409,"message":"Email Already Taken", "data": None})
        else : 
            return Response({"status": 200,"message":"Success"})

    except Exception as e: 
        print(e)
        return Response({"status": 400,"message":"Failed while validating email", "data": None})

'''
@extend_schema(methods=['post'],
                request=profilePicRequest,
                responses={200: profilePicResponse, 
                                    400: ErrorResponse})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes((MultiPartParser,))
def profilePicUpdate(request):
    print("At profile Pic update ")
    try :
        print("Profile Pic Update ")
        data = request.data
        user = User.objects.get(id = request.user.id)
        print(f"User : {user}")
        profileData = profile.objects.get(user = user)
        if  request.FILES.get('profileImage') != None :
            imageType = request.FILES.get('profileImage').name.split('.')[-1]
            if imageType == "jpg" or imageType == "png" or imageType == 'jpeg':
                profileData.profileImage = request.FILES.get('profileImage')
                profileData.save()
            else: 
                raise Exception("Please upload JPG/JPEG/PNG image format")
        serializer = profilePicSerializer(profileData, many=False)
        return Response({"status": 200,"message":"Success",
                        "data": serializer.data})

    except Exception as e: 
        print(e)
        status = 400
        message = 'Failed while updating Profile Picture'
        if e.args[0] == 'Please upload JPG/JPEG/PNG image format':
            message = 'Please upload JPG/JPEG/PNG image format'
            status = 415
        return Response({"status": status,"message": message, "data": None}) 
'''

class profilePicUpdate(generics.RetrieveUpdateAPIView):
 
    serializer_class = profilePicSerializer
    queryset = User.objects.all()   
    parser_classes = [MultiPartParser]
    http_method_names=['put']
    permission_classes = [IsAuthenticated]
    
    @extend_schema(responses={200: profilePicResponse, 
                                    400: ErrorResponse})
                
    def put(self, request, id=None):
        print("At profile Pic update class")
        try :
            print("Profile Pic Update ")
            data = request.data
            user = User.objects.get(id = request.user.id)
            print(f"User : {user}")
            profileData = profile.objects.get(user = user)

            if  request.FILES.get('profileImage') != None :
                imageType = request.FILES.get('profileImage').name.split('.')[-1]
                if imageType == "jpg" or imageType == "png" or imageType == 'jpeg':
                    profileData.profileImage = request.FILES.get('profileImage')
                    profileData.save()
                else: 
                    raise Exception("Please upload JPG/JPEG/PNG image format")


            serializer = profilePicSerializer(profileData, many=False)
            return Response({"status": 200,"message":"Success",
                            "data": serializer.data})

        except Exception as e: 
            print(e)
            status = 400
            message = 'Failed while updating Profile Picture'
            if e.args[0] == 'Please upload JPG/JPEG/PNG image format':
                message = 'Please upload JPG/JPEG/PNG image format'
                status = 415
            return Response({"status": status,"message": message, "data": None}) 


@extend_schema(methods=['get'],
                    responses={200: getUserlanguageResponse, 400: ErrorResponse})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserlanguages(request):
    try :
        print("at selecting getUserlanguageResponse ")
        
        user = User.objects.get(id = request.user.id)
        
        with connection.cursor() as cursor : 
            languageQuery = f"SELECT \
                                zl.id, zl.language,\
                                IF(al.language_id IS NULL,0, 1) as isSelected\
                              FROM\
                                  zipchoAdmin_language zl\
                                      LEFT JOIN\
                                 authentication_languagepreference al ON zl.id = al.language_id\
                                    AND al.user_id = %s; "

            cursor.execute(languageQuery, [user.id])
            languageQuery = dictFetchAll(cursor)
            data = languageQuery

        return Response({"status": 200,"message":"Success", 
                        "data" : data})

    except Exception as e: 
        print(e)
        return Response({"status": 400,"message":"Failed", "data": None})


@extend_schema(methods=['post'], request = langPrefRequest,
                    responses={200: langPrefResponse, 400: ErrorResponse})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def languagePreferences(request):
    try :
        print("at selecting language Preferences")
        data = request.data 
        ids = data['ids']
        user = User.objects.get(id = request.user.id)

        languagePreferenceDelete = languagePreference.objects.filter(user=user)
        languagePreferenceDelete.delete()
        print("Deleted all language preference of user ")        

        for i in range(len(ids)):
            print(ids[i]) 
            langData, created = languagePreference.objects.get_or_create(user = user, 
                                            language = language.objects.get(id=ids[i]))

            '''if not created : 
                print("Already existing language so deleting ... ")
                langData.delete()'''
    
        return Response({"status": 200,"message":"Success"})

    except Exception as e: 
        print(e)
        return Response({"status": 400,"message":"Failed", "data": None})

@extend_schema(methods=['get'],
                    responses={200: getUserInterestResponse, 400: ErrorResponse})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserInterests(request):
    try :
        print("at selecting getUserInterests ")
        
        user = User.objects.get(id = request.user.id)

        with connection.cursor() as cursor : 
            interestQuery = f"SELECT  \
                                  i.id, i.interest,  \
                                  IF(ui.interest_id IS NULL, 0, 1) as isSelected \
                              FROM \
                                  zipchoAdmin_interest i \
                                      LEFT JOIN \
                                  authentication_userinterest ui ON i.id = ui.interest_id \
                                      AND ui.user_id = %s; "

            cursor.execute(interestQuery, [user.id])
            interestData = dictFetchAll(cursor)
            data = interestData

        return Response({"status": 200,"message":"Success", 
                        "data" : data})

    except Exception as e: 
        print(e)
        return Response({"status": 400,"message":"Failed", "data": None})


@extend_schema(methods=['post'], request = userInterestRequest,
                    responses={200: userInterestResponse, 400: ErrorResponse})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userInterests(request):
    try :
        print("at Entering userInterests ")
        data = request.data 
        ids = data['ids']
        
        user = User.objects.get(id = request.user.id)
        existingInterest = userInterest.objects.filter(user = user).values_list('interest_id', flat=True)
        
        # Clear all interest 
        userInterestDelete = userInterest.objects.filter(user = user)
        userInterestDelete.delete()
        print(f"Deleting all Previous User Interests")
        
        
        for i in range(len(ids)):
            try : 
                intData, created = userInterest.objects.get_or_create(user = user, 
                                            interest = interest.objects.get(id=ids[i]))

                '''if not created : 
                    print("Already Existing Interest so deleting ")
                    intData.delete()'''
                
            except Exception as e : 
                print(f"Invalid interest : {ids[i]}")
        

        return Response({"status": 200,"message":"Success"})

    except Exception as e: 
        print(e)
        return Response({"status": 400,"message":"Failed", "data": None})

@extend_schema(methods=['get'],
                    responses={200: getUserCategoryResponse, 400: ErrorResponse})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserCategory(request):
    try :
        print("at selecting getUserCategory ")
        
        user = User.objects.get(id = request.user.id)
        
        with connection.cursor() as cursor : 
            categoryQuery = f"SELECT \
                                  zc.id,\
                                  zc.category,\
                                  IF(COALESCE(ui.interest_id AND c.category_id) IS NULL,\
                                      0,\
                                      1) AS isSelected\
                              FROM\
                                  zipchoAdmin_category zc\
                                      JOIN\
                                  authentication_userinterest ui ON ui.interest_id = zc.interest_id\
                                      AND ui.user_id = %s\
                                      LEFT JOIN\
                                  authentication_usercategory c ON zc.id = c.category_id AND c.user_id = %s; "

            cursor.execute(categoryQuery, [user.id, user.id])
            interestData = dictFetchAll(cursor)
            data = interestData

        return Response({"status": 200,"message":"Success", 
                        "data" : data})

    except Exception as e: 
        print(e)
        return Response({"status": 400,"message":"Failed", "data": None})


@extend_schema(methods=['get'],
                    responses={200: getUserTalentResponse, 400: ErrorResponse})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserTalent(request):
    try :
        print("at selecting getUserTalent ")
        user = User.objects.get(id = request.user.id)
        
        with connection.cursor() as cursor : 
            talentQuery = f"SELECT  \
                                allTalent.id, \
                                allTalent.talents, \
                                allTalent.tag, \
                                IF(COALESCE(aut.typeOfTalent, \
                                            aut.talent_id, \
                                            aut.user_id, \
                                            aut.id) IS NULL, \
                                    0, \
                                    1) AS isSelected \
                            FROM \
                                (SELECT  \
                                    id, interest AS 'talents', 'interest' AS 'tag' \
                                FROM \
                                    zipchoAdmin_interest zi UNION ALL SELECT  \
                                    id, category AS 'talents', 'category' AS 'tag' \
                                FROM \
                                    zipchoAdmin_category zc) allTalent \
                                    LEFT OUTER JOIN \
                                authentication_usertalent aut ON allTalent.tag = aut.typeOfTalent \
                                    AND allTalent.id = aut.talent_id \
                                    AND aut.user_id = %s;  "

            cursor.execute(talentQuery,[user.id])
            talentData = dictFetchAll(cursor)
            data = talentData

        return Response({"status": 200,"message":"Success", 
                        "data" : data})

    except Exception as e: 
        print(e)
        return Response({"status": 400,"message":"Failed", "data": None})


@extend_schema(methods=['post'], request = userTalentRequest,
                    responses={200: userTalentResponse, 400: ErrorResponse})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userTalents(request):
    try :
        print("at Entering userTalent")
        data = request.data 
        user = User.objects.get(id=request.user.id)
        
        #{'interest': [4, 5], 'category': [5, 8]}
        interest = data['interest']
        category = data['category']
        print(interest)
        print(category)
        
        if len(interest) != 0 :
            print("Intersts present ")
            for i in range(len(interest)):
                newTalent,created = userTalent.objects.get_or_create(
                    typeOfTalent = "interest",
                    talent_id = interest[i],
                    user = user
                )

                '''if not created : 
                    print("Already existing interest talent so deleting ... ")
                    newTalent.delete()'''

        if len(category) != 0 :
            print("category present ")
            for i in range(len(category)):
                newTalent,created = userTalent.objects.get_or_create(
                    typeOfTalent = "category",
                    talent_id = category[i],
                    user = user
                )
                '''if not created : 
                    print("Already existing category talent so deleting ... ")
                    newTalent.delete()'''

        return Response({"status": 200,"message":"Success"})

    except Exception as e: 
        print(e)
        return Response({"status": 400,"message":"Failed", "data": None})

@extend_schema(methods=['post'], request = userCategoryRequest,
                    responses={200: userCategoryResponse, 400: ErrorResponse})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userCategories(request):
    try :
        print("at Entering userCategories ")
        data = request.data 
        ids = data['ids']
        print(f"ids : {ids}")
        
        user = User.objects.get(id = request.user.id)
        da = userCategory.objects.filter(user = user).values()

        # Clear all Category 
        userCategoryDelete = userCategory.objects.filter(user = user)
        userCategoryDelete.delete()
        print(f"Deleting all Previous User Category")

        print(f"da : {da}")
        existingCategories = userCategory.objects.filter(user = user).values_list('category_id', flat=True)
        print("existingCategories")
        print(existingCategories)
        for i in range(len(ids)):
            print(ids[i]) 
            try : 
                catData, created = userCategory.objects.get_or_create(user = user, 
                                            category = category.objects.get(id=ids[i]))
                '''if not created : 
                    print("Already Existing Category so deleting ")
                    catData.delete()'''
            except Exception as e:
                print(f"Invalid category : {ids[i]}")


        return Response({"status": 200,"message":"Success"})

    except Exception as e: 
        print(e)
        return Response({"status": 400,"message":"Failed", "data": None})

@extend_schema(methods=['get'],
                    responses={200: genderReponse, 400: ErrorResponse})
@api_view(['GET'])
@permission_classes([AllowAny,])                    
def getUserGender(request):
    try : 
        print("At getUserGender")
        genData = list(gender.objects.all().values('id','gender'))
        print(genData)
        return Response({"status": 200,"message":"Success","data":genData})
       
    except Exception as e : 
        print(e)
        message = "Failed while fetching Gender for users "
        return Response({"status": 400,"message": message, "data": None})

@extend_schema(methods=['get'],
                    responses={200: countryResponse, 400: ErrorResponse})
@api_view(['GET'])
@permission_classes([AllowAny,])                    
def getAllCountry(request):
    try : 
        print("At getAllCountry")
        counData = list(country.objects.all().values('id','country'))
        print(counData)
        return Response({"status": 200,"message":"Success","data":counData})
       
    except Exception as e : 
        print(e)
        message = "Failed while fetching Country for user"
        return Response({"status": 400,"message": message, "data": None})

@extend_schema(methods=['post'], request = contactUsRequest,
                    responses={200: contactUsResponse, 400: ErrorResponse})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def contactUs(request):
    try :
        print("at contactUs ")
        data = request.data 
        
        message = f"Email : {data['email']} \n {data['message']}"
        m = send_mail(subject= f"Enquiry from {data['username']}",
                        message = message,from_email=data['email'],
                        recipient_list=[SUPPORT_EMAIL_USER],
                        fail_silently=False)
              
        print(m)

        return Response({"status": 200,"message":"Success", "data": [] })

    except Exception as e: 
        print("Failed while sending contact us mail : ",e)
        return Response({"status": 400,"message":"Failed", "data": None})


@extend_schema(methods=['get'],
                    responses={200: helpResponse, 400: ErrorResponse})
@api_view(['GET'])
@permission_classes([AllowAny,])                    
def help(request):
    try : 
        print("At help")

        dataToSend = []
      
        temp = {}  
        temp['question'] = 'How can we help you ?'
        temp['answer'] = "Do your pages have clear, easy-to-use navigation?  An accessible, easy-to-use navigation bar (or menu bar) is a key part of providing a good user experience. When building your navigation bar."
        
        dataToSend.append(temp)    
        temp = {}
        temp['question'] = 'Hello what can we do ?'
        temp['answer'] ="Open the Zipcho mobile app.Tap user-profile or your profile picture in the bottom right to go to your profile. "
        dataToSend.append(temp)    
         
        return Response({"status": 200,"message":"Success","data":dataToSend})
       
    except Exception as e : 
        print(e)
        message = "Failed while fetching help"
        return Response({"status": 400,"message": message, "data": None})

@extend_schema(methods=['post'], request = fcmRegisterDeviceRequest,
                    responses={200: fcmRegisterDeviceResponse, 400: ErrorResponse})
@api_view(['POST'])
@permission_classes([])
def fcmRegisterDevice(request):
    try :
        print("At fcmRegisterDevice ")
        data = request.data
        user_id = request.user.id 
        user = User.objects.get(id = user_id)
    
        newDevice , created = GCMDevice.objects.get_or_create(user = user,
                                                            cloud_message_type = 'FCM',
                                                            active = 1)
        newDevice.name = user.username
        newDevice.registration_id=data['registration_id']
        newDevice.save()                                        
        print(f"Created : {created}")
        
        return Response({"status": 200,"message":"Success"})

    except Exception as e: 
        print("failed while fcm Register : ",e)
        return Response({"status": 400,"message":"Failed to Register Device "})
