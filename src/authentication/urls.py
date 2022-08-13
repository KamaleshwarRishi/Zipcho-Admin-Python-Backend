from .views import*
from django.urls import path, include

urlpatterns = [
    path('fcmRegister', fcmRegisterDevice, name='fcmRegisterDevice'),
    path('login', login, name = 'login'),
    #path('requestOTP', requestOTP, name='requestOTP'),
    path('loginWithOTP', loginWithOTP, name="loginWithOTP"),
    path('signup', signUp, name="signupUser"),
    path('verifyOTP', verifyOTP, name='verifyOTP'),
    path('resetPassword', resetPassword, name='resetPassword'),

    path('validateUsername', validateUsername, name="validateUsername"),
    path('validateEmail', validateEmail, name="validateEmail"),

    #Profile 
    path('profilePicUpdate', profilePicUpdate.as_view()),
    #path('profilePicUpdate', profilePicUpdate, name ="profilePicUpdate"),
    path('getProfile', getProfile, name = 'getProfile'),
    path('updateProfile', updateProfile, name='updateProfile'),

    # gender 
    path("getUserGender", getUserGender, name= "getUserGender"),
    
    # Country
    path("getUserCountry", getAllCountry, name= "getUserCountry"),

    # Languages
    path('getUserlanguages', getUserlanguages, name="getUserlanguages"),
    path('languagePreferences', languagePreferences, name="languagePreferences"),
    
    # Interest 
    path('userInterests', userInterests, name="userInterests"),
    path('getUserInterests', getUserInterests, name="getUserInterests"),

    # Category 
    path('userCategory', userCategories, name="userCategory" ),
    path('getUserCategory', getUserCategory , name="getUserCategory"),

    # Talent 
    path('getUserTalent', getUserTalent, name='getUserTalent'),
    path('userTalent', userTalents, name='userTalent'),

    #Settings
    path('contactUs', contactUs, name='contactUs'),
    path('help', help, name='help'),

]