# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

db = DAL('sqlite://EduDB.sqlite')

db.define_table('profile',
                Field('pid','id'),
                Field('name','string',notnull = True),
                Field('username','string',notnull = True,unique = True),
                Field('dob','date'),
                Field('is_stud','boolean',notnull = True),
                Field('email','string',notnull = True),
                Field('pwd','password',notnull = True),
                Field('profile_pic','blob'),
                redefine = True,
                fake_migrate=True,
                migrate = True,
                primarykey=['pid']
                )
db.define_table('category',
                Field('cid','id'),
                Field('cname','string',notnull = True),
                redefine = True,
                migrate = True,
                fake_migrate=True,
                primarykey=['cid']
                )

db.define_table('test',
                Field('tid','id'),
                Field('tname','string',notnull = True),
                Field('category',db.category.cid,notnull = True),
                Field('tlink','string',notnull = True),
                Field('teacher_id',db.profile.pid,notnull = True),
                Field('negative','double'),
                Field('last_date','date'),
                redefine = True,
                fake_migrate=True,
                migrate = True,
                primarykey=['tid']
                )
db.define_table('statistics',
                Field('stud_id',db.profile.pid,notnull = True),
                Field('test_id',db.test.tid,notnull = True),
                Field('score','double'),
                Field('taken_on','datetime'),
                migrate = True,
                fake_migrate=True,
                primarykey=['stud_id','test_id','taken_on']
               )

#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.janrain_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
