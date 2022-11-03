from sqlalchemy import create_engine
from models import Stacks, Users
from flask_sqlalchemy import SQLAlchemy
from notification import Notificator
from cve_parser import parser

engine = create_engine('mysql://aker:reka@localhost/cve')

def get_keywords() -> list:
    keywords = []
    query = "select *from stacks;"
    stacks = engine.connect().execute(query)
    for stack in stacks:
        keywords.append(stack[1])
    return keywords


def start_scheduling():
    keywords = get_keywords()
    cves = parser(keywords)
    stacks = engine.connect().execute("select * from stacks;")
    lister = []
    for i in stacks:
        temp = []
        for j in i:
            temp.append(j)
        lister.append(temp)
    notificator = Notificator()
    for i in range(len(keywords)):
        if lister[i][2] != lister[i][1] and lister[i][2] != cves[i][0]:
            stmt = f"select * from users as u inner join bridge as b on b.user_id=u.id where b.stack_id={lister[i][0]}"

            res = engine.connect().execute(stmt)
            for user in res:
                notificator.notificator(cves[i][0], cves[i][1], user[2])
            
            lister[i][2] = cves[i][0]
        elif lister[i][2] == lister[i][1]:
            #users = db.session.query(Users).filter(stacks[i].stack_name.in_(Users.following))
            stmt = f"select * from users as u inner join bridge as b on b.user_id=u.id where b.stack_id={lister[i][0]}"
            res = engine.connect().execute(stmt)
            userlst = []
            for k in res:
                t = []
                for j in k:
                    t.append(j)
                userlst.append(t)
            for user in userlst:
                notificator.notificator(cves[i][0], cves[i][1], user[2])
            lister[i][2] = cves[i][0]
