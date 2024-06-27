# {
#     "email":"xyz@123.com",
#     "name":"xyz",
    # "password":"123456",
    # "password2":"123456",
#     "tc":"True"
# }
# views.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.
#generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes =[UserRenderer]
    def post(self, request, format=None):
        serializer= UserRegistrationSerializer(data=request.data)#send the request data to serializer
        serializer.is_valid(raise_exception =True)
        user=serializer.save()
        token = get_tokens_for_user(user) #calling the function after user save
        return Response({'token':token, 'msg': 'Registration Success'},
        status=status.HTTP_201_CREATED)
            
        
    

class UserLoginView(APIView):
    renderer_classes =[UserRenderer] #useful for frontend
    def post(self,request,format =None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) #to handle the errors we create rnderer.py file 
        email=serializer.data.get('email')
        password=serializer.data.get('password')
        user=authenticate(email=email,password=password)
        if user is not None:
            token = get_tokens_for_user(user) #calling the function after user save
            return Response({'token' : token,'msg': 'Login Success'},
            status=status.HTTP_200_OK)
        else :
            return Response({'errors': {'non_field_errors':['Email or password is not valid']}},
                                status=status.HTTP_404_NOT_FOUND)
     
    
class UserProfileView(APIView):
    renderer_classes =[UserRenderer] #useful for frontend
    permission_classes =[IsAuthenticated]
    def get(self,request,format=None):
        serializer =UserProfileSerializer(request.user)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
    renderer_classes =[UserRenderer] #useful for frontend
    permission_classes =[IsAuthenticated]
    def post(self,request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})

        if serializer.is_valid(raise_exception=True):
            return Response ({'msg': 'Password change Successfully'},
                status=status.HTTP_200_OK)
       
class SendPasswordResetEmailView(APIView):
    renderer_classes =[UserRenderer]
    def post(self,request,format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response ({'msg': 'Password reset link is send.Please check your Password'},
                status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView (APIView):
    renderer_classes =[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer = UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response ({'msg': 'Password reset Successfully'},
                status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

            


