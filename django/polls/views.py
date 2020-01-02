from __future__  import print_function  # Python 2/3 compatibility
from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

from django.shortcuts import render


def index(request):
    context = {'action': 'show'}
    return render(request, 'polls/index.html', context)


def movies(request):
    graph = Graph()
    remoteConn = DriverRemoteConnection('ws://<path to neptune>:8182/gremlin','g')
    g = graph.traversal().withRemote(remoteConn)
    #print(g.V().limit(2).toList())
    myList = g.V().has('name', request.POST['actor_name']).out().limit(40).values().toList()
    remoteConn.close()
    context = {'actor': request.POST['actor_name'], 'movies': myList}
    return render(request, 'polls/movie-results.html', context)


def joint_movies(request):
    statics.load_statics(globals())
    inputs = [x.strip() for x in request.POST['actor_names'].split(',')]
    graph = Graph()
    remoteConn = DriverRemoteConnection('ws://<path to neptune>:8182/gremlin','g')
    g = graph.traversal().withRemote(remoteConn)
    #print(g.V().limit(2).toList())
    if (len(inputs) == 2) :
        myList = g.V().has('name',inputs[0]).repeat(out().where(__.in_().has('name',inputs[1]))).emit().values().toList()
    else :
        myList = g.V().has('name',inputs[0]).repeat(out().where(__.in_().has('name',inputs[1])).where(__.in_().has('name',inputs[2]))).emit().values().toList()

    remoteConn.close()
    #print(myList)
    context = {'actor': request.POST['actor_names'], 'movies': myList}
    return render(request, 'polls/movie-results.html', context)


def actors(request):
    graph = Graph()
    remoteConn = DriverRemoteConnection('ws://<path to neptune>:8182/gremlin','g')
    g = graph.traversal().withRemote(remoteConn)
    myList = g.V().has('title', request.POST['movie_name']).in_().limit(40).values().toList()
    remoteConn.close()
    context = {'movie': request.POST['movie_name'], 'actors': myList}
    return render(request, 'polls/movie-results.html', context)

def separation(request):
    statics.load_statics(globals())
    inputs = [x.strip() for x in request.POST['actor_names'].split(',')]
    graph = Graph()
    remoteConn = DriverRemoteConnection('ws://<path to neptune>:8182/gremlin','g')
    g = graph.traversal().withRemote(remoteConn)
    myList = g.V().has('name',inputs[0]).repeat(out().in_().simplePath()).until(has('name',inputs[1])).path().by('name').by('title').limit(40).toList()
    remoteConn.close()
    context = {'actors': request.POST['actor_names'], 'separation': myList}
    return render(request, 'polls/movie-results.html', context)


def graphexp(request):
    context = {'action': 'show'}
    return render(request, 'polls/graphexp.html', context)
