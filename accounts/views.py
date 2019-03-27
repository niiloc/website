# accounts/views.py

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView
from django.db import models
from accounts.models import Series
from django.shortcuts import render, HttpResponse
import requests
from django.forms import ModelForm
from django.db.models import Count, Q
import json
import secrets
from django.contrib import messages


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class ProfileView(TemplateView):
    template_name = "profile.html"

def request_page(request, series_in_order):
	if(request.GET.get('picker')):
		print("It did it!")
		picked_series = generateRandom(series_in_order)
		messages.success(request, "Your pick is " + picked_series)
	return render(request,'profile.html')

def printList(request):
	parsedData = []
	current_user = str(request.user)
	print(current_user)
	seriesCan = Series.objects.all()
	vote_data = []
	series_in_order = []
	name_vote = []
	series_id = []
	random_name = ""
	#print(seriesCan)
	# 	req = tmdb.Search('title')
	# 	jsonList = []
	# 	jsonList.append(json.loads(show.content))

	if request.method == 'POST':
		delete_this_id = request.POST.get('foo')
		print(delete_this_id)

		tb_deleted = Series.objects.filter(seriesid=delete_this_id).filter(user_profile=current_user).first()
		tb_deleted.delete()


	#else:
	for series in seriesCan:
		print(series.user_profile)
		print("---")
		print(current_user)
		print(series.user_profile == current_user)
		print("levelss" == current_user)
		print(series.user_profile == "levelss")
		if series.user_profile == current_user:

			seriesData = {}
			seriesData['user'] = series.user_profile
			seriesData['series_id'] = series.seriesid
			seriesData['series_name'] = series.seriesname
			seriesData['vote_average'] = series.vote_average
			vote_data.append(float(series.vote_average))
			series_in_order.append(series.seriesname)
			name_vote.append([str(series.seriesname), float(series.vote_average)])
			series_id.append(series.seriesid)
			parsedData.append(seriesData)
			print(parsedData)
			print(vote_data)
			print(type(series_in_order))
			print("here:")
			print(name_vote)

	dataset = Series.objects.all()
	categories = list()
	under_4 = list()
	average = list()
	more_6 = list()

	if request.method == "GET" and request.GET.get('picker') == "Pick random":
		random_name = generateRandom(series_in_order)
		print("random name is " + random_name)
	for entry in dataset:

		categories.append('This')
		under_4.append(4)
		average.append(5)
		more_6.append(9)
	print(categories)
	print(under_4)
	return render(request, 'profile.html', {
		'categories': json.dumps(categories),
		'under_4': json.dumps(under_4),
		'average': json.dumps(average),
		'more_6': json.dumps(more_6),
		'dataset': dataset,
		'series_list': parsedData,
		'vote_average_data': vote_data,
		'series_name_for_plot': json.dumps(series_in_order),
		'name_vote': json.dumps(name_vote),
		'random_series': random_name
		})

def generateRandom(series_in_order):
	list_of_names = series_in_order
	return secrets.choice(list_of_names)

