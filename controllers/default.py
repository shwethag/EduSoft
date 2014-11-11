# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    """
    Redirecting to normal login page 
    """
   # response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))

def login():
    return dict()
    

def enterin():
    uname = request.vars['username']
    passwd = request.vars['pwd'] 
    dbUname=db(db.profile.username==uname).select(db.profile.username)
    if not dbUname:
        session.flash = T('Username does not exists')
        redirect(URL('login.html'))

    dbUname=db(db.profile.username==uname and db.profile.pwd == passwd).select(db.profile.username)
    if not dbUname:
        session.flash = T('Wrong password')
        redirect(URL('login.html'))

    redirect(URL('showUserProfile',vars=dict(username=dbUname[0]['username'])))

def process():
    fname = request.vars['fname']
    uname = request.vars['uname']
    bday = request.vars['dob']
    cat = request.vars['category']
    mailid = request.vars['mailid']
    passwd = request.vars['pwd']
    rasspwd = request.vars['rpwd']

    dbUname=db(db.profile.username==uname).select(db.profile.username)
    #print '----------------'
    #print dbUname[0]['username']
    #print '----------------'
    if dbUname and dbUname[0]['username'] == uname:
        session.flash = T('Username already exists!!')
        redirect(URL('login.html'))

    if passwd != rasspwd:
        session.flash = T('Password did not match!!')
        redirect(URL('login.html'))

    is_student = True;
    
    if cat == 'Teacher':
        is_student = False    
    
    #data=[{'name':name,'username':uname,'dob':dob,'is_stud':is_stud,'email':mailid,'pwd':pwd}]   

    db.profile.insert(name=fname,username=uname,dob=bday,is_stud=is_student,email=mailid,pwd=passwd)
    redirect(URL('showUserProfile',vars=dict(username=uname)))

def insertProfile():
    form=SQLFORM(db.profile).process()
    return dict(form=form)

def insertPic():
    rows = db(db.profile.username=='shwe').select('pid')
    for row in rows:
        record = row.pid
    print record
    record = db.profile[record]
    print "record",record
    form=SQLFORM(db.profile,record,fields=['profile_pic'],upload=URL('download'))
    if form.process().accepted:
        session.flash=T('Pic updated')
        
    else:
        session.flash=T('Error in upload')
        print form.errors
    return dict(form=form)

def deleteProfile():
    db.profile.truncate()
    db.commit()
    return 'All Records From Profile Table deleted'

def displayProfile():
    rows=db(db.profile).select()
    return dict(message=rows)

def showUserProfile():
    uname = request.vars['username']
    rows=db(db.profile.username==uname).select()
    vals = {}
    for row in rows:
        vals['name'] = row.name
        vals['username'] = row.username
        vals['dob'] = row.dob
        vals['type'] = row.is_stud
        vals['email'] = row.email
        vals['image'] = row.profile_pic
    return dict(vals)

def uploadImage():
    print request.vars
    print request.args
    uname = request.args[0]
    print "here", uname
   # db.profile.insert(profile_pic=)
    redirect(URL('showUserProfile',vars=dict(username=uname)))

def insertTest():
    form=SQLFORM(db.test).process()
    return dict(form=form)

def displayTest():
    rows=db(db.test).select()
    return dict(message=rows)

def insertCategory():
    form=SQLFORM(db.category).process()
    return dict(form=form)
    
def displayCategory():    
    rows=db(db.category).select()
    return dict(message=rows)

def insertStatistics():
    form=SQLFORM(db.statistics).process()
    return dict(form=form)
    
    
def displayStatistics():    
    rows=db(db.statistics).select()
    return dict(message=rows)
    
    
    
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
