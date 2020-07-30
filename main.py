import requests
from trello import TrelloApi
import auth
import sys
import datetime
import inspect

from pprint import pprint

class TrelloObj(object):
    def __init__(self):
        self.user = auth.user
        self.trello = TrelloApi(auth.key, auth.token)
        self.kl = self.trello.members.get_board(self.user)
        self.board_id = ''
        for item in self.kl:
            if item['name'] == auth.board:
                self.board_id = item['id']

        self.all_lists = self.trello.boards.get_list(self.board_id)

    def ArchiveOldBoard(self):
        y = datetime.date.today() - datetime.timedelta(days=2)
        w = y - datetime.timedelta(days=6)
        week_str = w.isoformat() + ' to ' + y.isoformat()
        print(week_str)

        for item in self.all_lists:
            if item['name'] == 'Done - ' + week_str:
                list_id = item['id']
                pprint(item)

        resp = requests.put("https://trello.com/1/lists/%s/closed" % (list_id),
                params=dict(key=auth.key, token=auth.token), data={'value' : 'true'})
        pprint(resp.content)

    def CreateWeeklyBoard(self):
        for item in self.all_lists:
            if 'Waiting' in item['name']:
                position = item['pos']
        

        u = datetime.date.today()
        s = u + datetime.timedelta(days=1)
        d = datetime.timedelta(days=6)
        t = s + d

        week_str = s.isoformat() + ' to ' + t.isoformat()

        resp = requests.post("https://trello.com/1/boards/%s/lists" % (self.board_id),
                params=dict(key=auth.key, token=auth.token), data={'name': 'Done - ' + week_str, 'pos' : position+1})

if __name__ == "__main__":
    # execute only if run as a script
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    print('Argument Pos 1 ', str(sys.argv[1]))

    argument = sys.argv[1]

    list_of_methods = inspect.getmembers(TrelloObj(), predicate=inspect.ismethod)
    for (key, method) in list_of_methods:
        if key == argument:
            method()



