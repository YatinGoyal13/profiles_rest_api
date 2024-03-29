from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from rest_framework import viewsets
from . import models
from . import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated




# Create your views here.
class HelloApiView(APIView):
    """Test API view."""
    
    serializer_class = serializers.HelloSerializer
    
    def get(self,request,format=None):
        """returns a list of APIView features."""
        an_apiview=['Uses HTTP methods as function (Get, Post, patch, etc)',
                    'It is similar to a traditional Django View',
                    'gives you the most control over your logic.',
                    'Is mapped manually  to urls']
        
        return Response({'message':'Hello!','an_apiview':an_apiview})
    
    def post(self, request):
        """Create a hello message with our name."""
        
        serializer= serializers.HelloSerializer(data=request.data)
        
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = f'hello {name}'
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request,pk=None):
        """Handles updating an object."""
        
        return Response ({'method': 'put'})
    
    def patch(self, request,pk=None):
        """Patch request, only updates fields provided in the request."""
        
        return Response ({'method': 'patch'})    
    
    def delete(self, request,pk=None):
        """Delete an object."""
        
        return Response ({'method': 'delete'})   
    
class HelloViewSet(viewsets.ViewSet):
    """Test API Viewsets."""
    serializer_class = serializers.HelloSerializer
    def list(self, request):
        """return a hello message"""
        a_viewset=[
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code.'
        ] 
        return Response ({'message': 'hello!', 'a_viewset': a_viewset})
    
    def create(self, request):
        """Create a hello message with our name."""
        
        serializer= serializers.HelloSerializer(data=request.data)
        
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = f'hello {name}'
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request,pk=None):
        """Handles getting an object by its id."""
        
        return Response ({'method': 'get'})
       
    def update(self, request,pk=None):
        """Handles updating an object."""
        
        return Response ({'method': 'put'})
    
    def partial_update(self, request,pk=None):
        """Patch request, only updates fields provided in the request."""
        
        return Response ({'method': 'patch'})    
    
    def destroy(self, request,pk=None):
        """Delete an object."""
        
        return Response ({'method': 'delete'})  
    
class UserProfileViewset(viewsets.ModelViewSet):
    """Handles creating, reading, and updating users profile."""
    serializer_class=serializers.UserProfileSerializer
    queryset= models.UserProfile.objects.all()
    authentication_classes=(TokenAuthentication,)
    permission_classes=(permissions.UpdateOwnProfile,)  
    filter_backends=(filters.SearchFilter,)
    search_fields=('name','email',) 
    
class LoginViewSet(viewsets.ViewSet):
    """checks email amd password and returns an auth token"""
    
    serializer_class=AuthTokenSerializer
    
    def create(self, request):
        """use the obtained auth token apiview to validate and create a token"""
        
        return ObtainAuthToken().as_view()(request=request._request)   
    
    
class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating , reading, and updating profile feed items"""
    
    authentication_classes = (TokenAuthentication,)
    serializer_class=serializers.ProfilefeedItemSerializer
    queryset=models.ProfileFeedItem.objects.all()
    permission_classes=(permissions.PostOwnStatus, IsAuthenticated)
    def perform_create(self, serializer):
        """set the user profile to the logged in user"""
        
        serializer.save(user_profile=self.request.user)
