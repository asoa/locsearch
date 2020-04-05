from django.shortcuts import render
from django.http import HttpResponse
from .models import Consultant
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from choices import state_choices
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConsultantSerializer
from rest_framework import viewsets


def search(request):
    consultants = Consultant.objects.all()

    # paginator = Paginator(consultants, 6)
    # page = request.GET.get('page')  # request to the search form is a get request
    # paged_listings = paginator.get_page(page)

    # filter by city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            consultants = consultants.filter(city__iexact=city)

    # filter by state
    if 'state' in request.GET and 'State' not in request.GET['state']:  # TODO second condition is a band-aid
        state = request.GET['state']
        if state:
            consultants = consultants.filter(state__iexact=state)

    # Filter by exact state
    if 'zipcode' in request.GET:
        zipcode = request.GET['zipcode']
        if zipcode:
            consultants = consultants.filter(zipcode__iexact=zipcode)

    if 'name' in request.GET:
        name = request.GET['name']
        if name:
            consultants = consultants.filter(name__icontains=name)

    if 'trainee' in request.GET:
        consultants = consultants.filter(trainee=True)
    else:
        consultants = consultants.filter(trainee=False)

    if 'approved' in request.GET:
        consultants = consultants.filter(approved=True)

    if 'certified' in request.GET:
        consultants = consultants.filter(r_certified=True)

    if 'ambassador' in request.GET:
        consultants = consultants.filter(ambassador=True)

    if 'distributor' in request.GET:
        consultants = consultants.filter(distributor=True)

    if 'trichology' in request.GET:
        consultants = consultants.filter(trichology=True)

    context = {
        'states': state_choices,
        'consultants': consultants.values(),
        'values': request.GET
    }
    return render(request, 'consultants/search.html', context=context)


def like(request):
    if request.method == 'GET':
        _consultant = request.GET['consultant_id']
        consultant = Consultant.objects.get(id=_consultant)
        consultant.likes += 1
        consultant.save()
        return HttpResponse('success')

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_consultant(request, pk):
    try:
        if request.method == 'GET':
            consultant = Consultant.objects.get(pk=pk)
            serializer = ConsultantSerializer(consultant)
            return Response(serializer.data)
    except Consultant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single consultant
    if request.method == 'GET':
        return Response({})
    # delete a single consultant
    elif request.method == 'DELETE':
        return Response({})
    # update details of a single consultant
    elif request.method == 'PUT':
        return Response({})


@api_view(['GET', 'POST'])
def get_post_consultant(request):
    # get all consultants
    if request.method == 'GET':
        consultants = Consultant.objects.all()
        serializer = ConsultantSerializer(consultants, many=True)
        return Response(serializer.data)
        # return Response({})
    # insert a new record for a consultant
    elif request.method == 'POST':
        return Response({})

# class ConsultantViewSet(viewsets.ModelViewSet):
#     queryset = Consultant.objects.all()
#     serializer_class = ConsultantSerializer
