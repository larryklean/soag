# coding: utf8

from gluon.contrib.pyfpdf import FPDF
import erwin as modelo
import datetime
import cPickle as pickle

@auth.requires_login()
def index():
    iderwin = request.args(0)
    erwin   = db(db.erwins.id == iderwin).select().first()
    parms   = db(db.parametros.id == 1).select().first()
    arqui   = os.path.join( '\\\\'
                          , '127.0.0.1'
                          , 'c$'
                          , parms.web2py
                          , 'applications'
                          , parms.soag
                          , 'private'
                          , 'erwin_%s.p' % iderwin)
    try:
        pickef = pickle.load(open(arqui, "rb"))
    except:
        pickef = None
    model = modelo.Erwin()
    le    = model.load(picke=pickef, all=False)
    if  not le['retorno']:
        session.flash = le['flash']
        session.labelErrors = le['labelErrors']
        session.msgsErrors = le['msgsErrors']
        buttons = []
        pickef  = None
    else:
        ents    = model.getEntityPhysical()
        db.erwins.nomeExterno1.requires = IS_IN_SET(ents, zero='-- Selecione --')
        db.erwins.default1.requires     = IS_NOT_EMPTY()
        db.erwins.nomeExterno2.requires = IS_NOT_EMPTY()
        db.erwins.nomeExterno3.requires = IS_IN_SET(ents, zero='-- Selecione --')
        db.erwins.default3.requires     = IS_IN_SET(['Sequencial 1 em 1'], zero='-- Selecione --')
        form = SQLFORM(db.erwins, iderwin, deletable=False)
        if  request.vars:
            form.vars.codigoAplicacao = request.vars.codigoAplicacao = erwin.codigoAplicacao
            form.vars.nome = request.vars.nome = erwin.nome
            form.vars.status = request.vars.status = erwin.status
        if  form.accepts(request.vars, session):
            db(db.erwins.id == iderwin).update(status=4,
                                               mensagem='Pendente Processamento',
                                               usuarioConfirmacao=auth.user.id,
                                               dataConfirmacao=datetime.datetime.today())
            session.status_id = 4
            session.flash = 'Padroes Alterados'
            redirect(URL('index', args=(iderwin)))
        erwin = db(db.erwins.id == iderwin).select().first()
        if  erwin.nomeExterno1 and erwin.default1 and erwin.nomeExterno2 and \
            erwin.nomeExterno3 and erwin.default3:
            buttons = [['Validar Padroes', 'validar', '90', '150','490', '1100']]
        else:
            buttons = []
    if  session.get('flash', None):
        response.flash = session.flash
        session.flash  = None
    if  session.get('labelErrors', None):
        form.labelErrors    = session.labelErrors
        session.labelErrors = None
    if  session.msgsErrors:
        form.errors        = session.msgsErrors
        session.msgsErrors = None
    query   = db.erwins.id==iderwin
    return dict(listdetail.index(['Formacao do Nome DCLGEN'],
                                  'erwins', erwins,
                                  query, form,
                                  width_label='35%',
                                  width_field='65%',
                                  noDetail=['codigoAplicacao',
                                            'nome',
                                            'arquivo',
                                            'status',
                                            'mensagem',
                                            'usuarioConfirmacao',
                                            'dataConfirmacao'],
                                  noList=True,
                                  optionDelete=False,
                                  buttonClear=False,
                                  buttons=buttons,
                                  buttonSubmit=True if pickef else False))

@auth.requires_login()
def orderby():
    listdetail.orderby('erwins', erwins)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('erwins', erwins)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = 'id==%d' % session.iderwin
    return listdetail.search('erwins', erwins, query=query)

@auth.requires_login()
def validar():
    iderwin = session.get('iderwin', 0)
    if  iderwin:
        parms = db(db.parametros.id == 1).select().first()
        arqui = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.web2py
                            , 'applications'
                            , parms.soag
                            , 'private'
                            , 'erwin_%s.p' % iderwin)
        try:
            pickef = pickle.load(open(arqui, "rb"))
        except:
            pickef = None
        if  pickef:
            erwin  = db(db.erwins.id == iderwin).select().first()
            model  = modelo.Erwin()
            le     = model.load(picke=pickef, all=False)
            if  not le['retorno']:
                session.flash = le['flash']
                session.labelErrors = le['labelErrors']
                session.msgsErrors = le['msgsErrors']
                redirect(URL('index', args=(iderwin)))
            ents   = model.getEntidades('')
            dicOk  = {}
            lisDup = []
            lisSn2 = []
            for ent in ents:
                entidade = ent['User_Formatted_Physical_Name'].upper()

                regto = db((db.erwinents.erwin == iderwin) &
                           (db.erwinents.entidade == entidade)).select().first()
                if  regto:
                    dicOk[regto.nomeExterno1] = entidade
                    continue

                ne1 = ent['Entity.Physical.%s' % erwin.nomeExterno1]
                if  ne1 != erwin.default1:
                    continue

                ne2 = erwin.nomeExterno2
                ne3 = ent['Entity.Physical.%s' % erwin.nomeExterno3]

                nomeExterno1 = ne1 + ne2 + ne3

                nomeExterno1 = nomeExterno1.upper()
                nomeExterno2 = ''
                obs = ''

                if  ne1:
                    if  ne3.strip():
                        nomeExterno2 = nomeExterno1
#                    else:

                if  nomeExterno2:
                    if  nomeExterno1 in dicOk.keys():
                        obs = '{} ja definido para a entidade {}'.format(nomeExterno1, dicOk[nomeExterno1])
                        nomeExterno2 = ''
                        lisDup.append(entidade)
                    else:
                        dicOk[nomeExterno1] = entidade
                else:
                    lisSn2.append(entidade)
                    obs = 'Default Assumido'

                db(db.erwinents.insert(erwin=iderwin
                                      ,entidade=entidade
                                      ,nomeExterno1=nomeExterno1
                                      ,nomeExterno2=nomeExterno2
                                      ,obs=obs))

            ne1 = erwin.default1
            ne2 = erwin.nomeExterno2
            ents = lisDup + lisSn2
            maxseq = model.getMaxSequencia(db, iderwin, ne1+ne2, 'nomeExterno1')
            for ent in ents:
                nomeExterno2 = ne1 + ne2 + maxseq
                maxseq = model.addSequencia(nomeExterno2)
                db(db.erwinents.entidade==ent).update(nomeExterno2=nomeExterno2)
        redirect('../validarpadraoerwin/index')
    else:
        redirect(URL('index'))

@auth.requires_login()
def report():
    id = request.args(0)
    if not id: redirect(URL('index'))
    title = "Nome Externo"
    heading = "First Paragraph"
    text = 'xpto ' * 100
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Times','B',15)
    pdf.cell(w=210,h=9,txt=title,border=0,ln=1,align='C',fill=0)
    pdf.set_font('Times','B',15)
    pdf.cell(w=0,h=6,txt=heading,border=0,ln=1,align='L',fill=0)
    pdf.set_font('Times','',12)
    pdf.multi_cell(w=0,h=5,txt=text)
    response.headers['Content-Type']='application/pdf'
    return pdf.output(name='report.pdf',dest='S')

@auth.requires_login()
def download():
    return response.download(request, db)

# vim: ft=python
