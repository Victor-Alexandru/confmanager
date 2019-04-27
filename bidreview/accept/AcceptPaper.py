from confsite import models

class AcceptPaper:

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
                status = AcceptPaper.str2bool(line[1])
                self._done[conf_id] = status

    def get_reviews_of_paper(self, paper):
        reviews = models.Review.objects.filter(paperId=paper)
        return reviews

    def accept_paper(self, paper):
        paper.accepted = True
        paper.save()

    def reject_paper(self, paper):
        paper.accepted = False
        paper.save()

    def end(self):
        with open('./bidreview/accept/' + self._file, 'w') as f:
            for conf in self._done.keys():
                item = 0
                if self._done[conf]:
                    item = 1
                f.write(str(conf) + ":" + str(item) + '\n')

    def accept(self):
        """
        Accepts papers at the conference by creating links between

        :return:
        """
        if self._done[self._conference.id]:
            return
        counter = 0
        papers = models.Paper.objects.filter(paperId__authorId__cId=self._conference)
        for paper in papers:
            reviews = self.get_reviews_of_paper(paper)
            allTrue = True
            allFalse = True
            for review in reviews:
                if review.status not in ('Strong Accept', 'Accept', 'Weak Accept', 'Borderline'):
                     allTrue = False
                if review.status not in ('Weak Reject', 'Strong Reject', 'Reject'):
                    allFalse = False
            if allTrue:
                counter += 1
                self.accept_paper(paper)
                continue
            if allFalse:
                counter += 1
                self.reject_paper(paper)
                continue
        if counter == len(papers):
            self._done[self._conference.id] = True
        self.end()


