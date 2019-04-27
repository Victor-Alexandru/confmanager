from django.db import models

'''
Aici aveti toate modelele, daca aveti nevoie de modificari sa anuntati si pe ceilalti
Puneti ce va trebuie fiecare in aplicatiile voastre
'''


class Login(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=32, null=False)

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email


class SteeringCommittee(models.Model):
    email = models.OneToOneField(Login, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=32, null=False)
    website = models.CharField(max_length=32, null=False)
    affiliation = models.CharField(max_length=32, null=False)

    def __str__(self):
        return str(self.email)

    def __unicode(self):
        return str(self.email)

    @property
    def memberEmails(self):
        l=[]
        print('call')
        d=SteeringCommittee.objects.all().values()
        for x in d:
            l.append(x['email_id'])
        return l


class Participant(models.Model):
    email = models.OneToOneField(Login, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=32, null=False)
    website = models.CharField(max_length=32, null=False)
    affiliation = models.CharField(max_length=32, null=False)

    def __str__(self):
        return str(self.name)

    def __unicode(self):
        return str(self.name)


class Conference(models.Model):
    name = models.CharField(max_length=32, null=False)
    submissionDeadline = models.DateField(null=False)
    reviewDeadline = models.DateField(null=False)
    conferenceDate = models.DateField(null=False)

    def __str__(self):
        return self.name

    def _unicode(self):
        return self.name


class ConferenceAuthor(models.Model):
    pEmail = models.ForeignKey(Participant, on_delete=models.CASCADE)
    cId = models.ForeignKey(Conference, on_delete=models.CASCADE)
    rank = models.CharField(max_length=32, default='listener')

    def __str__(self):
        return str(self.pEmail) + ' ' + str(self.cId) + ' ' + self.rank

    def __unicode(self):
        return str(self.pEmail) + ' ' + str(self.cId) + ' ' + self.rank


class ProgramCommitteeMember(models.Model):
    pEmail = models.ForeignKey(Participant, on_delete=models.CASCADE)
    cId = models.ForeignKey(Conference, on_delete=models.CASCADE)
    rank = models.CharField(max_length=32, default='listener')

    def __str__(self):
        return str(self.pEmail) + ' ' + str(self.cId) + ' ' + self.rank

    def __unicode(self):
        return str(self.pEmail) + ' ' + str(self.cId) + ' ' + self.rank


class ConferenceSession(models.Model):
    pcId = models.ForeignKey(ProgramCommitteeMember, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    startHour = models.TimeField(null=False)
    endHour = models.TimeField(null=False)
    roomNumber = models.IntegerField(null=False)

    def __str__(self):
        return str(self.pcId) + ' ' + str(self.date) + ' ' + str(self.startHour) + ' ' + str(self.endHour) + ' ' + str(
            self.roomNumber)

    def __unicode__(self):
        return str(self.pcId) + ' ' + str(self.date) + ' ' + str(self.startHour) + ' ' + str(self.endHour) + ' ' + str(
            self.roomNumber)


class ConferenceAuthorSession(models.Model):
    conferenceAuthorId = models.ForeignKey(ConferenceAuthor, on_delete=models.CASCADE)
    conferenceSessionId = models.ForeignKey(ConferenceSession, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.conferenceAuthorId) + ' ' + str(self.conferenceSessionId)

    def __unicode__(self):
        return str(self.conferenceAuthorId) + ' ' + str(self.conferenceSessionId)


class Abstract(models.Model):
    authorId = models.OneToOneField(ConferenceAuthor, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=False, default='')
    title = models.CharField(max_length=32, null=False)

    def __str__(self):
        return str(self.authorId) + ' ' + self.title

    def __unicode__(self):
        return str(self.authorId) + ' ' + self.title


class Paper(models.Model):
    paperId = models.OneToOneField(Abstract, on_delete=models.CASCADE)
    content = models.FileField(upload_to='uploads/', null=True)
    accepted = models.BooleanField(null=True)

    def __str__(self):
        return str(self.paperId)

    def __unicode__(self):
        return str(self.paperId)


class Review(models.Model):
    paperId = models.ForeignKey(Paper, on_delete=models.CASCADE)
    pcId = models.ForeignKey(ProgramCommitteeMember, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, null=False, default='borderline')
    comments = models.CharField(max_length=300, null=True, default='')

    def __str__(self):
        return str(self.paperId) + ' ' + str(self.pcId) + ' ' + self.status

    def __unicode__(self):
        return str(self.paperId) + ' ' + str(self.pcId) + ' ' + self.status


class Bid(models.Model):
    abstractId = models.ForeignKey(Abstract, on_delete=models.CASCADE)
    pcId = models.ForeignKey(ProgramCommitteeMember, on_delete=models.CASCADE)
    status = models.BooleanField()

    def __str__(self):
        return str(self.abstractId) + ' ' + str(self.pcId) + ' ' + str(self.status)

    def __unicode__(self):
        return str(self.abstractId) + ' ' + str(self.pcId) + ' ' + str(self.status)
