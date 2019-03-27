# views.py

from django.shortcuts import render, HttpResponse
import requests
import json
from tmdbv3api import TMDb
from tmdbv3api import TV
from django.contrib import messages
from django.db import models
from accounts.models import Series


# Create your views here.

def index(request):
    return HttpResponse('Hello World!')

def home(request):
	return render(request, 'omdb/home.html')

# search title by given string
def search(request):
	tmdb = TMDb()
	tmdb.api_key = '9c4c89ef54bdd1c4303ca26d4852c6a4'
	tv = TV()


	parsedData = []
	if request.method == 'POST':
		title = request.POST.get('title')
		show = tv.search(title)
		print(show)
	# 	req = tmdb.Search('title')
	# 	jsonList = []
	# 	jsonList.append(json.loads(show.content))
		for result in show:
			searchData = {}
			searchData['name'] = result.name
			searchData['overview'] = result.overview
			searchData['id'] = result.id
	# 		searchData['type'] = data['type']
	# 		searchData['imdb_id'] = data['imdb_id']
			parsedData.append(searchData)

	elif request.method == 'GET' and request.GET.get('foo') is not None:
		series_id = request.GET.get('foo', '1')

		url = ("https://api.themoviedb.org/3/tv/" + series_id + "?" + "api_key=" + tmdb.api_key)
		print(url)
		#payload = {'api_key': 'tmdb.api_key', 's_id': 'series_id'}
		#tv_vote_avg = request.GET('https://api.themoviedb.org/3/tv/', params=payload)
		r = requests.get(url)
		print(r.url)
		print(r)
		print(r.content)
		r_content = r.json()
		print(r_content.keys())
		print(r_content['vote_average'])
		average_vote = r_content['vote_average']
		#print(tv_vote_avg)
		print(series_id)
		print(r_content['name'])
		series_name = r_content['name']
		user_id = request.user
		Series.objects.create(seriesid = series_id, 
			user_profile = user_id,
			seriesname = series_name,
			vote_average = average_vote
			)

		messages.success(request, "Serie added successfully!")

	#return render(request, 'omdb/main.html', {'result': show})
	return render(request, 'omdb/main.html', {'show': parsedData})

