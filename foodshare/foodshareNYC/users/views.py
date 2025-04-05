from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
import folium 


from django.shortcuts import render, get_object_or_404
from blog.models import Measurement, Post
from blog.forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from blog.utils import get_geo, get_center_coordinates, get_zoom
from geopy.distance import geodesic
#from django.contrib.auth import get_user_model
#User = get_user_model()




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    distance = None
    destination = None
    


    obj = get_object_or_404(Measurement, id=5)
    form =MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='measurements')

    
    ip = '184.170.253.68'
    country, city, lat, lon = get_geo(ip)
    location = geolocator.geocode(city)
    
    # location coordinates
    l_lat = lat
    #l_lat = 40.7008715
    l_lon = lon
    #l_lon = -73.9395218

    pointA = (l_lat, l_lon)

    # initial folium map
    m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon),zoom_start=10)
    # location marker
    folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
            icon=folium.Icon(color='purple')).add_to(m)


    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)
        # destination coordinates
        d_lat = destination.latitude
        d_lon = destination.longitude
        
        pointB = (d_lat, d_lon)
        # distance calculation
        distance =round(geodesic(pointA, pointB).miles, 2)

        # folium map modification  
        m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon), zoom_start=get_zoom(distance))       # location marker
        folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
                icon=folium.Icon(color='purple')).add_to(m)
        # destination marker
        folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=destination,
                icon=folium.Icon(color='red', icon='cloud')).add_to(m)

        #draw the line between location and destination
        line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
        m.add_child(line)


        instance.location = location
        instance.distance = distance
        instance.save()


    m = m._repr_html_()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'map': m,
        'distance': obj,
    'destination': destination,
    }

    return render(request, 'users/profile.html', context)
