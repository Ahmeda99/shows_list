from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Show
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests

# Add the following import
from django.http import HttpResponse

def searchbar(request):
  if request.method == 'GET':
    user_input = request.GET.get('search')
    response = requests.get(f'https://api.tvmaze.com/search/shows?q={user_input}')
    data = response.json()[0]
    print(data['show'])
    return render (request, 'search.html', {'data': data})

# Define the home view
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

# def shows_index(request):
#   return render(request, 'shows/index.html', { 'shows': shows })

def shows_index(request):
  shows = Show.objects.filter(user=request.user)
  return render(request, 'shows/index.html', { 'shows': shows })

def shows_detail(request, show_id):
  show = Show.objects.get(id=show_id)
  return render(request, 'shows/detail.html', { 'show': show })

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class ShowCreate(CreateView):
  model = Show
  fields = ['name', 'rating', 'description', 'cast']
  success_url = '/shows/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class ShowUpdate(UpdateView):
  model = Show
  fields = ['name', 'rating', 'description', 'cast']

class ShowDelete(DeleteView):
  model = Show
  success_url = '/shows/'