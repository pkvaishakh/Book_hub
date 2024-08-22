from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .forms import *
from django.contrib import messages
import requests
from django.core.paginator import Paginator, EmptyPage,InvalidPage





class DestinationCreateView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializers
    permission_classes = [AllowAny]


class DestinationDetail(generics.RetrieveAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializers


class UpdateDestinationView(generics.RetrieveUpdateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializers


class DeleteDestination(generics.DestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializers


class SearchDestination(generics.ListAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializers

    def get_queryset(self):
        name = self.kwargs.get("place_name")
        return Destination.objects.filter(place_name__icontains=name)


def create_destination(request):
    if request.method == 'POST':
        form =DestinationForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                form.save()
                api_url="http://127.0.0.1:8000/create/"
                data = form.cleaned_data
                print(data)

                response = requests.post(api_url,data=data,files={'image':request.FILES['image']})
                if response.status_code == 400:
                    messages.success(request,'Destination created successfully')
                    return redirect('/')
                else:
                    messages.error(request,f'error{response.status_code}')
            except requests.RequestException as e:
                messages.error(request,f'error{response.status_code}')
        else:
            messages.error(request,'form is not valid')
            print(f'errors',form.errors)
    else:
        form = DestinationForm()
    return render(request,'create_destination.html',{'form':form})


def view_details(request,id):
    api_url = f"http://127.0.0.1:8000/detail/{id}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return render(request, 'view_details.html', {'data': data})
    else:
        messages.error(request, 'Failed to retrieve details')
        return redirect('/')  # Replace 'some_other_view' with your actual view




def update_destination(request, id):
    api_url = f"http://127.0.0.1:8000/detail/{id}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

    if request.method == 'POST':
        place_name = request.POST.get('place_name')
        weather = request.POST.get('weather')
        location = request.POST.get('location')
        google_map_link = request.POST.get('google_map_link')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        api_url = f"http://127.0.0.1:8000/update/{id}/"
        data = {
            "place_name": place_name,
            "weather": weather,
            "location": location,
            "google_map_link": google_map_link,
            "description": description,
        }
        
        files = {'image': image} if image else None  # Include image file only if it exists

        if files:
            response = requests.put(api_url, data=data, files=files)
        else:
            response = requests.put(api_url, data=data)

        if response.status_code == 200:
            messages.success(request, 'Destination updated successfully')
            return redirect('/')
        else:
            messages.error(request, f'Error while submitting to the REST API: {response.status_code}')


    return render(request, 'update_destination.html', {'data': data})



def delete_destination(request,id):
    api_url = f"http://127.0.0.1:8000/delete/{id}"
    response = requests.delete(api_url)

    if response.status_code == 204:
        messages.success(request,'destination deleted successfully')
    else:
        messages.error(request,'failed to delete destination')
    
    return redirect(r'/')


def index(request):
    if request.method == 'POST':
        search= request.POST['search']
        api_url = f"http://127.0.0.1:8000/search/{search}/"

        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
            else:
                data = None
        except requests.RequestException as e:
            data = None
        return render(request,'index.html',{"data":data})
    
    else:
        api_url = "http://127.0.0.1:8000/create/"

        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
                original_data = data

                paginator = Paginator(original_data,6)
                page_number =request.GET.get('page')
                try:
                    page = paginator.get_page(page_number)
                except EmptyPage:
                    page = paginator.page(page_number.num_pages)

                context = {
                    "destinations" : page,
                }
                return render(request,'index.html',context)
            else:
                return render(request,"index.html",{"error_message":f"Error:{response.status_code}"})
        except requests.RequestException as e:
            return render(request, "index.html", {"error_message": f"Error:{str(e)}"})

    
