# Create your views here.
from rest_framework import generics
from .models import UserLocation
from .serializers import LocationSerializer
from .utils import lat_long_distance 
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Max
from django.db.models import OuterRef, Subquery


class UserLocationCRUDView(generics.RetrieveUpdateDestroyAPIView):
    
    lookup_field = 'pk'
    serializer_class = LocationSerializer
       
    def get_queryset(self): 
        return UserLocation.objects.all()
    
    def get_object(self):
        pk = self.kwargs.get("pk")
        user = self.request.user
        if not user.is_staff:
            return UserLocation.objects.filter(user=user).get(pk=pk)
               
        return UserLocation.objects.get(pk=pk)
    
  
class UserLocationListCreateView(generics.ListCreateAPIView):    
    serializer_class = LocationSerializer

    def create(self, request, *args, **kwargs):      
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():          
            serializer.save(user=request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self): 
        user = self.request.user
        if not user.is_staff:
            return UserLocation.objects.filter(user=user)
        return UserLocation.objects.all()

    
class UserLocationListView(generics.ListAPIView):
 
    serializer_class = LocationSerializer         

    def get_queryset(self):        
        user = self.request.user   
        if not user.is_staff:
            return UserLocation.objects.filter(user=user)   
        return UserLocation.objects.filter(user=self.kwargs['user'])

    
@permission_classes((IsAuthenticated, IsAdminUser)) 
class UserRouteListView(generics.ListAPIView):
      
    serializer = LocationSerializer
    
    def get_queryset(self): 
        user = self.kwargs['user']
        start = self.request.query_params.get('start_date', None)
        end = self.request.query_params.get('end_date', None)
        start_date = None
        end_date = None
        if start is not None:
            start_date = datetime.strptime(start, "%Y/%m/%d").date()
        if end is not None:
            end_date = datetime.strptime(end, "%Y/%m/%d").date()
        if start_date is not None and end_date is not None:
            return UserLocation.objects.filter(user=user, loctime__range=(
            datetime.combine(start_date, datetime.min.time()),
            datetime.combine(end_date, datetime.max.time()))).order_by("loctime")
        elif start_date is not None:
            return UserLocation.objects.filter(user=user, loctime__gte=
              datetime.combine(start_date, datetime.min.time())).order_by("loctime")
        elif end_date is not None:
            return UserLocation.objects.filter(user=user, loctime__lte=
              datetime.combine(end_date, datetime.min.time())).order_by("loctime")
        else:
            return   UserLocation.objects.filter(
            loctime=Subquery(
            (UserLocation.objects
            .filter(user=user))
            .annotate(last_time=Max('loctime'))
            .values('last_time')[:1]
            ), user=user)
        
    def list(self, request, *args, **kwargs):
        userLocations = self.get_queryset()
        locations = [] 
        dates = []
        distance = 0.00 
        i = 0 
        if userLocations is not None:   
            for i in range(len(userLocations) - 1):
                locations.append(userLocations[i].location)
                dates.append(userLocations[i].loctime)           
                distance += lat_long_distance(userLocations[i].latitude,
                                        userLocations[i + 1].latitude,
                                        userLocations[i].longitude,
                                        userLocations[i + 1].longitude)
        if(i > 0):       
            locations.append(userLocations[i + 1].location) 
            dates.append(userLocations[i + 1].loctime)  
      
        return Response({"locations":locations, "distance":distance, "dates":dates})
        
