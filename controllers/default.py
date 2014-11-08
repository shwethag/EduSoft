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

def process():
    name = request.vars['fname']
    uname = request.vars['uname']
    dob = request.vars['dob']
    category = request.vars['category']
    mailid = request.vars['mailid']
    pwd = request.vars['pwd']
    rpwd = request.vars['rpwd']
    if pwd != rpwd:
        response.flash = T('Password did not match!!')
        redirect(request.env.http_referrer)
    else:
        return dict(arg=request.args,var=request.vars)

def insertProfile():
    form=SQLFORM(db.profile).process()
    return dict(form=form)

def displayProfile():
    rows=db(db.profile).select()
    return dict(message=rows)

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
