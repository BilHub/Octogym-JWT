from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets
from .models import Client, Personnel, Coach, Maladie
from .serializers import ClientSerialiser, PersonnelSerializer, CoachSerializer, MaladieSerializer, ClientNameSerializer, ClientCreateSerialiser, ClientNameDropSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum
from rest_framework import pagination
from rest_framework import filters
from rest_framework import status

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class ClientAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ClientCreateSerialiser
    queryset = Client.objects.all()
    parser_classes = [MultiPartParser, FormParser]

   # lookup_field = 'slug'
   # permission_classes = (AllowAny, )

class ClientListAPIView(AutoPrefetchViewSetMixin, generics.ListAPIView):
    permission_classes = (AllowAny, )
    pagination_class = StandardResultsSetPagination

    queryset = Client.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = ClientSerialiser
    # lookup_field = 'slug'
    permission_classes = (AllowAny, )
    search_fields = ['=id','last_name',  'first_name', 'phone']


class ClientNamesDropListAPIView(generics.ListAPIView):
    queryset = Client.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = ClientNameDropSerializer
    permission_classes = (AllowAny, )


class ClientDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Client.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = ClientSerialiser
    def get_object(self):
        obj = get_object_or_404(Client.objects.filter(id=self.kwargs["pk"]))
        return obj
    def get(self , request, *args, **kwargs):
        # try:
        obj = get_object_or_404(Client.objects.filter(id=self.kwargs["pk"]))
        ax = self.serializer_class(obj)
        return Response(ax.data)
        # except:
        #     msg = 'le client nexiste pas'
            # return Response({'message': msg}, status=404)

class ClientDestroyAPIView(generics.DestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerialiser
    # lookup_field = 'slug'
    # permission_classes = (AllowAny, )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
################################################
#################  PERSONNEL  ##################
################################################

class PersonnelCreateAPIView(generics.CreateAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    permission_classes = (AllowAny, )

class PersonnelListAPIView(generics.ListAPIView):
    queryset = Personnel.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = PersonnelSerializer
    # lookup_field = 'slug'
    permission_classes = (AllowAny, )


class PersonnelDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Personnel.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = PersonnelSerializer
    # permission_classes = (AllowAny, )

    def get_object(self):
        obj = get_object_or_404(Personnel.objects.filter(id=self.kwargs["pk"]))
        return obj
    

class PersonnelDestroyAPIView(generics.DestroyAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    # lookup_field = 'slug'
    permission_classes = (AllowAny, )

###############################################
#################   COACHS   ##################
###############################################
class CoachCreateAPIView(generics.CreateAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    # permission_classes = (AllowAny, )

class CoachListAPIView(generics.ListAPIView):
    # permission_classes = (AllowAny, )
    queryset = Coach.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = CoachSerializer
    # lookup_field = 'slug'

class CoachDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Coach.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = CoachSerializer
    # permission_classes = (AllowAny, )

    def get_object(self):
        obj = get_object_or_404(Coach.objects.filter(id=self.kwargs["pk"]))
        return obj
    

class CoachDestroyAPIView(generics.DestroyAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    # lookup_field = 'slug'
    # permission_classes = (AllowAny, )

class MaladieCreateAPIView(generics.CreateAPIView):
    queryset = Maladie.objects.all()
    serializer_class = MaladieSerializer
    permission_classes = (AllowAny,)

class MaladieViewSet(viewsets.ViewSet):
    queryset = Maladie.objects.all()
    serializer_class = MaladieSerializer
    permission_classes = (AllowAny, )

    def list(self, request):
        queryset = Maladie.objects.all()
        serializer = MaladieSerializer(queryset, many=True)
        return Response(serializer.data)


class ClientNameViewAPI(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    # permission_classes = (IsAuthenticated,)

    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientNameSerializer
    search_fields = [ '=id','^last_name', '^first_name', '^phone']
    filter_backends = (filters.SearchFilter,)

# class ClientPaeiementsViewAPI(generics.ListAPIView):
#     queryset = Client.objects.all()
#     serializer_class = ClientTransactionsSerializer
class ClientPresenceViewAPI(generics.ListAPIView):
    # pagination_class = StandardResultsSetPagination

    queryset = Client.objects.all().order_by('id')
    serializer_class = ClientNameDropSerializer
    search_fields = ['^last_name', '=id', '^first_name']
    filter_backends = (filters.SearchFilter,)

@api_view(['GET'])
def total_dettes(request):
    dettes = Client.objects.all().aggregate(Sum('dette'))
    return Response(dettes)

@api_view(['GET'])
def total_abonnes(request):
    total_abonnees = Client.objects.all().count()
    return Response( { 'abonnees': total_abonnees})


# @api_view(['GET'])
# def abonnements(request):
#     total_abonnees = Client.objects.all().count()
#     return Response( { 'abonnees': total_abonnees})


