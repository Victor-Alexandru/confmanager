from random import  shuffle
from confsite import models
'''
Class responsible for assigning papers to reviewers
'''
NO_REV_PER_PAPER = 2


class AssignPaper:

    def __init__(self, file, conference):
        '''

        :param file: the name of the config file
        :param conference: the conference object
        '''
        self._done = {}
        self._file = file
        self._conference = conference
        self.read_init()

    @staticmethod
    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")

    def read_init(self):
        '''
        Read from file if the conference has been already been assigned
        :return:
        '''
        with open('./bidreview/assign/' + self._file, 'r') as f:
            for line in f.readlines():
                line.strip('\n')
                line = line.split(':')
                conf_id = int(line[0])
                status = AssignPaper.str2bool(line[1])
                self._done[conf_id] = status

    def end(self):
        with open('./bidreview/assign/' + self._file, 'w') as f:
            for conf in self._done.keys():
                item = 0
                if self._done[conf]:
                    item = 1
                f.write(str(conf) + ":" + str(item) + '\n')


    def assign_review(self, paper, reviewer):

        review = models.Review(pcId=reviewer, paperId=paper, status="", comments="")
        review.save()

    def has_bid_paper(self, reviewer, paper):

        abstract = paper.paperId
        bids = list(models.Bid.objects.filter(pcId=reviewer, abstractId=abstract))
        return len(bids) > 0

    def has_review_paper(self, reviewer, paper):

        review = list(models.Review.objects.filter(pcId=reviewer, paperId=paper))
        return len(review) > 0

    def assign(self):
        '''
        Assign the reviers papers
        Does the following: Checks if the papers have already been assigned, if so exits
        else:
        1) go through all the papers as @paper:
                initialize variable counter with 0, the number of reviewers of @paper;
                2) go through all the bids of the @paper RANDOMLY as @bid:
                    if counter = NO_REV_PER_PAPER:
                        break loop 2)
                    if @bid.status = 'accept':
                        assign @review from @bid.reviewer to @paper empty
                        increment counter
                end 2)
                if counter < NO_REV_PER_PAPER: <cond1>
                    3) go through reviewers as @reviewer:
                        if @reviewer doesn't have bid for @paper and <cond1>:
                        assign @review from @reviewer to @paper empty
                        increment counter and  <cond1>
                    end 3)

                if <cond1>:
                    4) go through reviewers as @reviewer:
                        if @reviewer doesn't have review for @paper and <cond1>:
                            assign @review from @reviewer to @paper empty
                            increment counter
                    end 4)
        end 1)
        :return:
        '''
        if self._done[self._conference.id]:
            return

        reviewers = list(models.ProgramCommitteeMember.objects.filter(cId=self._conference))
        papers = list(models.Paper.objects.filter(paperId__authorId__cId=self._conference))

        for paper in papers:
            counter = 0
            bids = list(models.Bid.objects.filter(abstractId=paper.paperId))
            shuffle(bids)
            for bid in bids:
                if counter == NO_REV_PER_PAPER:
                    break
                if bid.status is True:
                    self.assign_review(paper, bid.pcId)
                    counter += 1
            if counter < NO_REV_PER_PAPER:
                for reviewer in reviewers:
                    if counter == NO_REV_PER_PAPER:
                        break
                    if not self.has_bid_paper(reviewer, paper):
                        self.assign_review(paper, reviewer)
                        counter += 1
            if counter < NO_REV_PER_PAPER:
                for reviewer in reviewers:
                    if counter == NO_REV_PER_PAPER:
                        break
                    if not self.has_review_paper(reviewer, paper):
                        self.assign_review(paper, reviewer)
                        counter += 1
        self._done[self._conference.id] = True
        self.end()
