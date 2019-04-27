from django.shortcuts import render
from django.http import HttpResponse
from confsite.models import *


def index(request):
    if request.POST:
        # adding hard-coded data
        try:
            # some fields would not be created if we knew the current user
            first_conference = Conference.objects.all()[0]
            log = Login(email="johnsmith@john.com", password="admin")
            log.save()
            participant = Participant(email=log, name="John Smith", website="a.com", affiliation="affiliation a")
            participant.save()

            # oif we have in the request information about the user and the conference we need to add only this field
            conf_auth = ConferenceAuthor(pEmail=participant, cId=first_conference, rank="listener")
            conf_auth.save()
            conf_session = ConferenceSession.objects.all()[0]

            conf_auth_session = ConferenceAuthorSession.save(conferenceAuthorId=conf_auth,
                                                             conferenceSessionId=conf_session)
            conf_auth_session.save()
        except ValueError as ve:
            print(ve)

    context = {
        'currentUser': request.user,
        'conferences': Conference.objects.all(),
        'conferenceAuthors': ConferenceAuthor.objects.all(),
        'conferenceSession': ConferenceSession.objects.all(),
        'conferenceAuthorSession': ConferenceAuthorSession.objects.all()
    }

    return render(request, 'conferences/index.html', context)


def user_profile(request):
    context = {
        'currentUser': request.user,
        'conferences': Conference.objects.all(),
        'conferenceAuthors': ConferenceAuthor.objects.all(),
        'conferenceSession': ConferenceSession.objects.all(),
        'conferenceAuthorSession': ConferenceAuthorSession.objects.all()
    }

    return render(request, 'conferences/edit-profile.html', context)
