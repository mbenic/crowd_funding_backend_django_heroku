from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics


from .models import Project, Pledge
from .serializers import RegisterSerializer, UserSerializer, ProjectSerializer, PledgeSerializer


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username
            #'email': token.user.email,
        })
    
    # maybe Return user + token shaped like this is better for frontend to use instead of making another request to get user info after login
        # return Response({
        #     "user": {
        #         "id": user.id,
        #         "username": user.username
        #     },
        #     "token": token.key
        # })
 

 

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return User.objects.all()

    # Equivalent to /user endpoint
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer

#     def get_permissions(self):
#         if self.action in ['list', 'retrieve']:
#             return [permissions.AllowAny()]
#         return [permissions.IsAuthenticated()]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'pledges']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get', 'post'])
    def pledges(self, request, pk=None):
        project = self.get_object()

        if request.method == 'GET':
            pledges = project.pledges.all()
            serializer = PledgeSerializer(pledges, many=True)
            return Response(serializer.data)

        if request.method == 'POST':
            serializer = PledgeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(supporter=request.user, project=project)
            return Response(serializer.data)
        
    
class PledgeViewSet(viewsets.ModelViewSet):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'index_for_project']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    # # POST /projects/{project}/pledges
    # @action(detail=False, methods=['post'], url_path='projects/(?P<project_id>[^/.]+)/pledges')
    # def store_for_project(self, request, project_id=None):
    #     data = request.data.copy()
    #     data['project'] = project_id

    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user=request.user)

    #     return Response(serializer.data)

    # # GET /projects/{project}/pledges
    # @action(detail=False, methods=['get'], url_path='projects/(?P<project_id>[^/.]+)/pledges')
    # def index_for_project(self, request, project_id=None):
    #     pledges = Pledge.objects.filter(project_id=project_id)
    #     serializer = self.get_serializer(pledges, many=True)
    #     return Response(serializer.data)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        # Create user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create token for that user
        token, created = Token.objects.get_or_create(user=user)

        # Return user + token
        return Response({
            'user_id': token.user_id,
            'username': token.user.username,
            "token": token.key
        })