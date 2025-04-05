from django.shortcuts import render, get_object_or_404
from .models import Measurement, Post
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from .utils import get_geo, get_center_coordinates, get_zoom
from geopy.distance import geodesic
import folium 
import socket
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
#User = get_user_model()

from users.models import CustomUser


def home(request):

	context = { 
	'posts': Post.objects.all()
	}
	return render(request, 'blog/home.html', context)


class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5 

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	paginate_by = 5 

	def get_queryset(self):
		user = get_object_or_404(CustomUser, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')




class PostDetailView(DetailView):
	model = Post
	fields = ['title', 'image', 'content']

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'image', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def about(request):
	return render(request, 'blog/about.html', {'title': "About"})



def calculate_distance_view(request):
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
		m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon), zoom_start=get_zoom(distance))		# location marker
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
	'distance': obj,
	'destination': destination,
	'form': form,
	'map': m,
	}

	return render(request, "blog/main.html", context)

