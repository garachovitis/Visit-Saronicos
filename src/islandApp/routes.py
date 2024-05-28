from flask import render_template, redirect, url_for, request, flash, abort
from islandApp import app
from datetime import datetime as dt
from islandApp.dbconnect import *

current_year = dt.now().year

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(415)
def unsupported_media_type(e):
    return render_template('errors/415.html'), 415

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

@app.route("/home/")
@app.route("/")
def islands():
    islands = getIslands()
    return render_template("index.html", islands=islands)

@app.route('/activities/<island>')
def activities(island):
    activities = get_activities_for_island(island)
    return render_template('activities.html', activities=activities, location=island.capitalize())

def get_activities_for_island(island):
    return [
        {'name': 'Activity 1', 'description': 'Description 1'},
        {'name': 'Activity 2', 'description': 'Description 2'},
        {'name': 'Activity 3', 'description': 'Description 3'},
    ]

@app.route('/beaches/<island>')
def beaches(island):
    beaches = []
    if island == 'spetses':
        beaches = getBeaches(1)
    elif island == 'hydra':
        beaches = getBeaches(2)
    elif island == 'poros':
        beaches = getBeaches(3)
    return render_template('beaches.html', island=island, beaches=beaches)

@app.route('/stay/<island>')
def stay(island):
    stay = []
    if island == 'spetses':
        stay = getStay(1)
    elif island == 'hydra':
        stay = getStay(2)
    elif island == 'poros':
        stay = getStay(3)
    return render_template('stay.html', island=island, stay=stay, location=island.capitalize())

@app.route('/food/<island>')
def food(island):
    food = []
    if island == 'spetses':
        food = getFood(1)
    elif island == 'hydra':
        food = getFood(2)
    elif island == 'poros':
        food = getFood(3)
    return render_template('food.html', island=island, food=food)

@app.route('/event/<island>')
def event(island):
    event = []
    if island == 'spetses':
        event = getEvent(1)
    elif island == 'hydra':
        event = getEvent(2)
    elif island == 'poros':
        event = getEvent(3)
    return render_template('event.html', island=island, event=event)

@app.route('/museum/<island>')
def museum(island):
    museum = []
    if island == 'spetses':
        museum = getMuseum(1)
    elif island == 'hydra':
        museum = getMuseum(2)
    elif island == 'poros':
        museum = getMuseum(3)
    return render_template('museum.html', island=island, museum=museum)

@app.route('/route/<island>')
def route(island):
    route = []
    museum = []
    beaches = []
    stay = []
    if island == 'spetses':
        route = getRoute(1)
        museum = getMuseum(1)
        beaches = getBeaches(1)
        stay = getStay(1)
    elif island == 'hydra':
        route = getRoute(2)
        museum = getMuseum(2)
        beaches = getBeaches(2)
        stay = getStay(2)
    elif island == 'poros':
        route = getRoute(3)
        museum = getMuseum(3)
        beaches = getBeaches(3)
        stay = getStay(3)
    return render_template('route.html', island=island, route=route, museum=museum, beaches=beaches, stay=stay)

@app.route('/buses/<int:startPlace>/<int:destinationPlace>/<island>')
def buses(startPlace, destinationPlace, island):
    connect = []
    route = []
    if island == 'spetses':
        connect, route = handle_bus_route(startPlace, destinationPlace, 1)
    elif island == 'poros':
        connect, route = handle_bus_route(startPlace, destinationPlace, 3)
    return render_template('buses.html', island=island, startPlace=startPlace, destinationPlace=destinationPlace, route=route, connect=connect)

def handle_bus_route(startPlace, destinationPlace, island_id):
    if startPlace < destinationPlace:
        connect = getConnect(startPlace, destinationPlace, island_id)
        route = getRoute(island_id)
        if not connect:
            route = getRoute(island_id)
    else:
        startPlace, destinationPlace = destinationPlace, startPlace
        connect = getConnect(startPlace, destinationPlace, island_id)
        route = getRoute(island_id)
    return connect, route
