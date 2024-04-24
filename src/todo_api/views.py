from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import status
from .models import Todo, Movie
from .serializers import TodoSerializers, MovieSerializer
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from rest_framework import mixins


class TodoLisApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        todos = Todo.objects.filter(user=request.user)
        serializer = TodoSerializers(todos, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TodoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, user_id, todo_id):
        try:
            todo_instance = Todo.objects.filter(user= user_id).get(id=todo_id)
        except Todo.DoesNotExist:
            todo_instance = None

        return todo_instance

    def get(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(request.user, todo_id)
        if not todo_instance:
            return Response({"error": "todo id does not find"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TodoSerializers(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(request.user, todo_id)
        if not todo_instance:
            return Response({"error": "todo id does not find"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TodoSerializers(instance=todo_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(request.user, todo_id)
        if not todo_instance:
            return Response({"error": "todo id does not find"}, status=status.HTTP_400_BAD_REQUEST)
        todo_instance.delete()
        return Response({"message": "Todo succesfully deleted!"})


class TodoViewSet(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Todo.objects.all()

    def list(self, request, *args,**kwargs):
        serializer = TodoSerializers(self.queryset,many = True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset,pk = pk)
        serializer=TodoSerializers(item)
        return Response(serializer.data)

    def create(self, request):
        serializer = TodoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = TodoSerializers(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        item.delete()
        return Response({"message": "Todo succesfully deleted!"})


class RetrieveDeleteItem(GenericAPIView):
    serializer_class = TodoSerializers
    queryset = Todo.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateListItems(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    serializer_class = TodoSerializers
    queryset = Todo.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateDeleteItem(mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               GenericAPIView):
    serializer_class = TodoSerializers
    queryset = Todo.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MultipleFieldLookupMixin:

    def retrieve(self, request, *args, **kwargs):
        instance = Todo.objects.filter(user=request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ListAPIItem(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = TodoSerializers
    queryset = Todo.objects.all()


class MovieCreateItem(CreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
