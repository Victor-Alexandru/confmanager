from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from confsite import models
from bidreview.assign.AssignPaper import AssignPaper
from bidreview.accept.AcceptPaper import AcceptPaper

def get_unclaimed_papers(conf_id, r_id):
    '''
    Gets the papers for an r_id which have no bid attached at conf conf_id
    :param r_id: the researcher id, int ; conf_id the id of the conference, int
    :return: the abstract list
    '''
    #conference = models.Conference.objects.filter(id=conf_id)[0]
    abstracts = models.Abstract.objects.filter(authorId__cId__id=conf_id).exclude(bid__pcId=r_id)
    return [a for a in abstracts]


def getAbstractAuthor(abstract):
    '''

    :param abstract: an abstract item
    :return: the author name of the abstract
    '''

    return models.ConferenceAuthor.objects.get(id = abstract.authorId)

def add_bid(request, rev_id, a_id):
    """
    Default handler for POST method to bid a paper
    :param request: the request, sent from JQuery
    :param rev_id: the id of the reviewer, string
    :param a_id: the id of the abstract, string
    :return: empty http
    """
    abstr = models.Abstract.objects.filter(id=int(a_id))[0]
    reviewer = models.ProgramCommitteeMember.objects.filter(id=int(rev_id))[0]
    bid = models.Bid(abstractId= abstr, pcId=reviewer, status=True)
    bid.save()
    return HttpResponse('')


def reject_bid(request, rev_id, a_id):
    """
    Default handler for the POST method to refuse a paper
    :param request: the request, sent from Jquery
    :param rev_id: the id of the reviewer, member of the Program Committee, string
    :param a_id: abstract id, string
    :return: empty http
    """
    abstr = models.Abstract.objects.filter(id=int(a_id))[0]
    reviewer = models.ProgramCommitteeMember.objects.filter(id=int(rev_id))[0]
    bid = models.Bid(abstractId=abstr, pcId=reviewer, status=False)
    bid.save()
    return HttpResponse('')

def abstracts_view(request, conf_id, rev_id):

    reviewer = list(models.ProgramCommitteeMember.objects.filter(id = rev_id))
    if len(reviewer) == 0:
        return HttpResponse('The searched reviewer does not exist')

    abstracts = get_unclaimed_papers(conf_id, rev_id)
    csrf = RequestContext(request)
    context_list = []
    for a in abstracts:
        context_list.append(get_abstract_context(a.id))

    context = {
        'abstracts' : context_list,
        'id' : rev_id,
        'csrf' : csrf
    }

    return render(request, 'bidreview/bidreview.html', context)

def paper_table_view(request, rev_id):
    '''
    See all the reviews of all papers for a reviewer
    :param request:
    :param r_id: the pc commitee ID
    :return:
    '''

    papers = models.Paper.objects.filter(review__pcId= rev_id)
    context_list = []
    for paper in papers:
        abstract_context = get_abstract_context(paper.paperId.id)
        rev = models.Review.objects.filter(pcId__id=rev_id, paperId=paper)[0]
        status = rev.status
        comment = rev.comments
        abstract_context['status'] = status
        abstract_context['comment'] = comment
        context_list.append(abstract_context)
    context = {
        'papers' : context_list,
        'id' : rev_id,
        'csrf' : RequestContext(request)
    }
    return render(request, 'bidreview/choosepaper.html', context)

def get_file_url_for_paper(abstract):
    """
    Returns the file url for an abstract id
    :param abstract_id: the id of the abstract
    :return: the URL of the paper of the abstract, or NULL if not found
    """

    paper = get_paper(abstract)
    if not (paper is None):
        file_url = paper.content.url
        return '/' + file_url
    return ''

def get_paper(abstract):
    paper = models.Paper.objects.filter(paperId=abstract)
    if not len(paper) == 0:
        return paper[0]
    return None


def get_participant(author):
    return author.pEmail

def get_author(abstract):
    return abstract.authorId


def get_abstract_context(abstract_id):
    a = models.Abstract.objects.filter(id = abstract_id)[0]
    a_dict = {
        'id': a.id,
        'author': a.authorId.pEmail.name,
        'title': a.title,
        'text': a.text
    }
    return a_dict

def paper_view(request, a_id):
    context = get_abstract_context(a_id)
    abstract = models.Abstract.objects.filter(id=a_id)[0]
    url = get_file_url_for_paper(abstract)
    context['url'] = url
    return render(request, 'bidreview/paper.html', context)

def assign_reviews(request, conf_id):
    conference = models.Conference.objects.filter(id = int(conf_id))[0]
    assigner = AssignPaper('data.in', conference)
    assigner.assign()
    return HttpResponse('ok! papers assigned for conference ' + str(conf_id))


def change_review_status(request, rev_id, a_id):
    new_status = request.POST['new_status']
    paper = models.Paper.objects.filter(paperId_id=a_id)[0]
    review = models.Review.objects.filter(paperId = paper, pcId_id=rev_id)[0]
    review.status = new_status
    review.save()

    return HttpResponse("ok")


def change_review_comment(request, rev_id, a_id):

    new_comment = request.POST['new_comment']
    paper = models.Paper.objects.filter(paperId_id=a_id)[0]
    review = models.Review.objects.filter(paperId = paper, pcId_id=rev_id)[0]
    review.comments = new_comment
    review.save()

    return HttpResponse("ok")


def change_review(request, rev_id, a_id):
    """
    Changes the status of a review with the new value
    :param request:
    :param rev_id: the reviewer id
    :param a_id: a_id
    :return:
    """

    req_type = request.POST['update_type']
    if req_type == 'status':
        return change_review_status(request, rev_id, a_id)
    elif req_type == 'comment':
        return change_review_comment(request, rev_id, a_id)
    return HttpResponse('Cannot find request type')


def get_other_reviews(reviewer, a_id):
    paper = models.Paper.objects.filter(paperId_id=a_id)[0]
    reviews = models.Review.objects.filter(paperId=paper).exclude(pcId=reviewer)
    return reviews

def create_review_context(review):
    review_id = review.id
    abstract = review.paperId.paperId
    abstract_title = abstract.title
    author_name = abstract.authorId.pEmail.name
    reviewer_name = review.pcId.pEmail.name
    status = review.status
    comment = review.comments
    return {
        'review_id': review_id,
        'title': abstract_title,
        'author': author_name,
        'reviewer': reviewer_name,
        'status': status,
        'comment': comment
    }


def see_review(request, rev_id, a_id):
    """
    See the reviews of the paper with abstract a_id, of other reviewers
    :param request:
    :param rev_id:
    :param a_id: the abstract id
    :return:
    """
    reviewer = models.ProgramCommitteeMember.objects.filter(id = rev_id)[0]
    reviews = get_other_reviews(reviewer, a_id)
    review_contexts = []
    for review in reviews:
        review_contexts.append(create_review_context(review))

    context = {
        'rev_id': rev_id,
        'a_id': a_id,
        'reviews' : review_contexts
    }

    return render(request, 'bidreview/otherreview.html', context)

def accept_conference(request, conf_id):
    conference = models.Conference.objects.filter(id = conf_id)[0]
    accepter = AcceptPaper("data.in", conference)
    accepter.accept()
    return HttpResponse("Ok! Accepted papers for conference " + str(conf_id))