# -*- coding: utf-8 -*-

'''
   Created on 07/09/2011
   @author: C&C - HardSoft
'''

from   gluon.html import XML, A, URL
from   gluon      import current
import re
import unicodedata
import os, sys
import string
import traceback
import base64
import uuid
import shutil
from fileutils import up, w2p_unpack, read_file, write_file
from HOFsGenericas import *
import zipfile
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

def web2py_uuid():
    return str(uuid.uuid4())

def change(dic, obj):
    if isinstance(obj, list):
        for n, i in enumerate(obj):
            for k, v in dic.items():
                obj[n] = i.replace(k, v)
                i = obj[n]
    else:
        if isinstance(obj, str):
            for k, v in dic.items():
                obj = obj.replace(k, v)
    return obj

dra = {'\xc3\x80':'À', '\xc3\x81':'Á', '\xc3\x82':'Â', '\xc3\x83':'Ã',
       '\xc3\x84':'Ä', '\xc3\x85':'Å', '\xc3\x86':'Æ', '\xc3\x87':'Ç',
       '\xc3\x88':'È', '\xc3\x89':'É', '\xc3\x8a':'Ê', '\xc3\x8b':'Ë',
       '\xc3\x8c':'Ì', '\xc3\x8d':'Í', '\xc3\x8e':'Î', '\xc3\x8f':'Ï',
       '\xc3\x90':'Ð', '\xc3\x91':'Ñ', '\xc3\x92':'Ò', '\xc3\x93':'Ó',
       '\xc3\x94':'Ô', '\xc3\x95':'Õ', '\xc3\x96':'Ö', '\xc3\x98':'Ø',
       '\xc3\x99':'Ù', '\xc3\x9a':'Ú', '\xc3\x9b':'Û', '\xc3\x9c':'Ü',
       '\xc3\x9d':'Ý', '\xc3\x9e':'Þ', '\xc3\x9f':'ß', '\xc3\xa0':'à',
       '\xc3\xa1':'á', '\xc3\xa2':'â', '\xc3\xa3':'ã', '\xc3\xa4':'ä',
       '\xc3\xa5':'å', '\xc3\xa6':'æ', '\xc3\xa7':'ç', '\xc3\xa8':'è',
       '\xc3\xa9':'é', '\xc3\xaa':'ê', '\xc3\xab':'ë', '\xc3\xac':'ì',
       '\xc3\xad':'í', '\xc3\xae':'î', '\xc3\xaf':'ï', '\xc3\xb0':'ð',
       '\xc3\xb1':'ñ', '\xc3\xb2':'ò', '\xc3\xb3':'ó', '\xc3\xb4':'ô',
       '\xc3\xb5':'õ', '\xc3\xb6':'ö', '\xc3\xb8':'ø', '\xc3\xb9':'ù',
       '\xc3\xba':'ú', '\xc3\xbb':'û', '\xc3\xbc':'ü', '\xc3\xbd':'ý',
       '\xc3\xbe':'þ', '\xc3\xbf':'ÿ'}

def nUni2Uni(txt):
    return change(dra, txt)

#def remover_acentos(txt, codif='latin-1'):
def remover_acentos(txt, codif='cp1252'):

    for k in dra.keys():
        if  k in txt:
            codif='utf-8'
            break

    return unicodedata.normalize('NFKD', txt.decode(codif)).encode('ASCII', 'ignore')

def safe_str(obj):
    try:
        obj = str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        try:
            obj = unicode(obj).encode('unicode_escape', 'ignore')
            for x in obj:
                if  ord(x) > 255:
                    obj.replace(x, ' ')
        except:
            return ''
    dic = {'\\xc7':'A', '\\xb5':'A', '\\xb7':'A',  '\\x84':'A',
           '\\x90':'E', '\\xd4':'E', '\\xd3':'E',
           '\\xd6':'I', '\\xde':'I', '\\xd8':'I',
           '\\xe5':'O', '\\xe0':'O', '\\x99':'O',
           '\\xe9':'U', '\\xeb':'U', '\\x9a':'U',
           '\\xc6':'a', '\\xa0':'a', '\\x85':'a',  '\\x84':'a',
           '\\xe3':'a', '\\xe1':'a',
           '\\x82':'e', '\\x8a':'e', '\\x89':'e',  '\\xea':'e',
           '\\xe4':'o', '\\xa2':'o', '\\x95':'o',  '\\x94':'o',
           '\\xf3':'o', '\\xf4':'o', '\\xf5':'o',
           '\\xa3':'u', '\\x97':'u', '\\x81':'u',  '\\xfa':'u',
           '\\x87':'c', '\\xe7':'c', '\\r'  :'\r', '\\n'  :'\n'}
    for k, v in dic.items():
        try:
            obj = obj.replace(k, v)
        except:
            break
    return obj

def safe_string(obj):

    try:
        obj = str(obj)
    except:
        # obj is unicode
        try:
            obj = '%s'.decode('cp1252', 'ignore').\
                                               encode('cp1252', 'ignore') % obj
            for x in obj:
                if  ord(x) > 128:
                    obj.replace(x, ' ')
        except:
            obj = ''

    return obj

def iterInv(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]

def txtAbrev(txt, lgt, removerAcentos=1):
    if  removerAcentos:
        txt=remover_acentos(txt)
    for w in words(txt):
        if len(txt) <= lgt:
            break
        if w+' '  in txt:
            txt=txt.replace(w+' ',w[0:3]+'.',1)
        else:
            txt=txt.replace(w,w[0:3]+'.',1)
    return txt[0:lgt]

def insAster72(txt):
    ts=''
    tl=txt.split('\n')
    for l in tl:
         if l[6:7] == '*':
             if len(l) < 72:
                 l+=(' '*(71-len(l))+'*')
         ts+=l+'\n'
    return ts

def Capitalize(string, N=2):

    if  not string:
        return ''

    words  = string.split()
    result = words[0].capitalize() if words else ''

    if  words: del(words[0])

    for word in words:
        if len(word) > N:
            if word[1] == "'":
                result += ' ' + word[:2].lower() + word[2:].capitalize()
            else:
                result += ' ' + word.capitalize()
        else:
            result += ' ' + word

    return result

def Select(db, name=None, table=None, fields=[], prefix=None, \
               todos='', lookups={}, masks=[], filtro='',     \
               distinct=False, orderby='', value=0, width='', \
               submit=True):

    if  not db or not name or not table or not fields: return ''

    if  not filtro:
        rows = db(db[table]).select(orderby=fields[1] \
                                    if not orderby else orderby)
    else:
        rows = db(filtro).select(orderby=fields[1] \
                                    if not orderby else orderby)

    options = [[0, '-- Selecione --']]

    if  todos:
        options.append([999999, todos])

    for row in rows:
        if  masks:
            if  not masks[0]:
                expr0 = row[fields[0]]
            else:
                expr0 = eval("'(%s) %s' % (row['" + masks[0][0] + \
                                         "'], row['" + masks[0][1] + "'])")
            if  not masks[1]:
                expr1 = row[fields[1]]
            else:
                expr1 = eval("'(%s) %s' % (row['" + masks[1][0] + \
                                         "'], row['" + masks[1][1] + "'])")
        else:
            expr0 = row[fields[0]]
            expr1 = row[fields[1]]
        if  lookups:
            if  lookups.has_key(fields[1]):
                expr1 = db(db[lookups[fields[1]][0]].id==expr1).\
                                         select()[0][lookups[fields[1]][1]]
        options.append([expr0, expr1])

    if  submit:
        ret = "<select name='%s' id='%s_%s' %s onChange=\"%s\">" % \
                      (name, (prefix if prefix else table), name,
              'style=\'width: %s\'' % width if width else '', \
                      XML("jQuery('#action').attr('value','submit');" + \
                          "jQuery(document.forms).each(function()"    + \
                          "{this.submit();});"))
    else:
        ret = "<select name='%s' id='%s_%s' %s>" % \
                    (name, (prefix if prefix else table), name, \
                            'style=\'width: %s\'' % width if width else '')

    antx  = ''

    for option in options:
        if  distinct:
            if  option[1] <> antx:
                antx = option[1]
                if  int(option[0]) == int(value):
                    ret += "<option value='%s' selected='selected'>%s" % \
                                                     (option[0], option[1])
                    ret += "</option>"
                else:
                    ret += "<option value='%s'>%s</option>" % \
                                                     (option[0], option[1])
        else:
            if  int(option[0]) == int(value):
                ret += "<option value='%s' selected='selected'>%s" % \
                                                     (option[0], option[1])
                ret += "</option>"
            else:
                ret += "<option value='%s'>%s</option>" % \
                                                     (option[0], option[1])

    ret += '</select>'

    return ret

def SelectString(name='', options=[], default='', width='', submit=False):

    if  not name or not options:
        return ''

    if  submit:
        ret = "<select name='%s' id='%s' %s onChange=\"%s\">" % \
                    (name, name, 'style=\'width: %s\'' % width  \
                        if width else '', \
                            XML("jQuery('#action').attr('value',"   + \
                                "'submit');jQuery(document.forms)." + \
                                "each(function(){this.submit();});"))
    else:
        ret = "<select name='%s' id='%s' %s>" % \
               (name, name, 'style=\'width: %s\'' % width if width else '')

    for option in options:

        if  isinstance(option, list):
            if  isinstance(option[0], int):
                if  int(option[0]) == int(default):
                    ret += "<option value='%s' selected='selected'>%s" % \
                                                     (option[0], option[1])
                    ret += "</option>"
                else:
                    ret += "<option value='%s'>%s</option>" % \
                                                     (option[0], option[1])
            else:
                if  option[0] == default:
                    ret += "<option value='%s' selected='selected'>%s" % \
                                                     (option[0], option[1])
                    ret += "</option>"
                else:
                    ret += "<option value='%s'>%s</option>" % \
                                                     (option[0], option[1])
        else:
            opt = [option, option]
            if  isinstance(opt[0], int):
                if  int(opt[0]) == int(default):
                    ret += "<option value='%s' selected='selected'>%s" % \
                                                           (opt[0], opt[1])
                    ret += "</option>"
                else:
                    ret += "<option value='%s'>%s</option>" % \
                                                           (opt[0], opt[1])
            else:
                if  opt[0] == default:
                    ret += "<option value='%s' selected='selected'>%s" % \
                                                           (opt[0], opt[1])
                    ret += "</option>"
                else:
                    ret += "<option value='%s'>%s</option>" % \
                                                           (opt[0], opt[1])

    ret += '</select>'

    return ret

def buttons(executes):

    ret = ''

    for execute in executes:

        if  len(execute) == 2:
            ret += ('&nbsp;' if ret else '') + \
                str(A(current.T(execute[0]),_class='button',_href=URL(execute[1])))

        if  len(execute) == 3:
            ret += ('&nbsp;' if ret else '') + \
                str(A(current.T(execute[0]),_class='button', \
                    _onclick=XML('popupw(\'' +URL(execute[1])+'\',\''+\
                        execute[2]+'\',\'290\',\'280\',\'650\');')))

        if  len(execute) == 4:
            ret += ('&nbsp;' if ret else '') + \
                str(A(current.T(execute[0]),_class='button', \
                    _onclick=XML('popupw(\'' +URL(execute[1])+'\',\''+\
                        execute[2]+ '\',\''+execute[3]+\
                            '\',\'280\',\'650\');')))

        if  len(execute) == 5:
            ret += ('&nbsp;' if ret else '') + \
                str(A(current.T(execute[0]),_class='button', \
                    _onclick=XML('popupw(\'' +URL(execute[1])+'\',\''+\
                        execute[2]+ '\',\''+execute[3]+'\',\''+execute[4]+\
                            '\',\'650\');')))
        if  len(execute) == 6:
            ret += ('&nbsp;' if ret else '') + \
                str(A(current.T(execute[0]),_class='button', \
                    _onclick=XML('popupw(\'' +URL(execute[1])+'\',\''+\
                        execute[2]+'\',\''+execute[3]+'\',\''+execute[4]+\
                            '\',\''+execute[5]+'\');')))

    return ret

def System(obj, parms):

    try:
        os.system('%s %s' % (obj, parms))
    except:
        return traceback.format_exc()

def repeat(char=' ', times=0):

    ret = ''

    for idx in xrange(0, times):
        ret += char

    return ret

def copyFile(argv1, argv2):

    try:

        with open(argv2, 'w') as f1:

            with open(argv1)  as f2:

                for line in f2:
                    f1.write(line)

        return [True, []]

    except:
        return [False, traceback.format_exc()]

def stringList(string, fatia, header):

    ret = ''

    while string:

        if (string[fatia:fatia+1] == ',' or string[fatia-1:fatia]) and \
           (string[fatia:fatia+1] <> ' '):
            idx = fatia
            tmp = ''
            while idx > 0 and string[idx-1:idx] <> ' ' and \
                  string[idx-1:idx] <> ',':
                  tmp  = string[idx-1:idx] + tmp
                  idx -= 1
            linha    = (header if ret else '') + string[0:idx]
            string   = string[idx:]
        else:
            linha  = (header if ret else '') + string[0:fatia]
            string   = string[fatia:]

        ret += ('\n' if ret else '') + linha

    return ret

def buttonsAjax(buttons):

    ret = ''

    if  buttons:
        for button in buttons:
            ret += ('&nbsp;&nbsp;&nbsp;' if not ret else '&nbsp;') + \
                        str(A(current.T(button[0]),_class='button',_onClick=\
                            XML("ajaxCall('%s','%s','%s');" % \
                                (button[1], button[2], button[3]))))

    return ret

def buttonsDownload(buttons):

    ret = ''

    if  buttons:
        for button in buttons:
            ret += (('&nbsp;&nbsp;&nbsp;' if not ret else '&nbsp;') +
                        str(A(button[0],_class='button',_href=URL(button[1]))))

    return ret

def CryptFileName(tabela, campo, arquivo):

    filename         = os.path.basename(arquivo.replace('/', os.sep).\
                                                         replace('\\', os.sep))
    m                = re.compile('\.(?P<e>\w{1,5})$').search(filename)
    extension        = m and m.group('e') or 'txt'
    uuid_key         = web2py_uuid().replace('-', '')[-16:]
    encoded_filename = base64.b16encode(filename).lower()
    newfilename      = '%s.%s.%s.%s' % \
                                    (tabela, campo, uuid_key, encoded_filename)
    newfilename      = newfilename[:(511 - len(extension))] + '.' + extension
    return newfilename

def compact(fileIn, fileOut, arcname=None):
    zip = zipfile.ZipFile(fileOut, mode='w')
    zip.write(fileIn, arcname=arcname, compress_type=compression)
    zip.close()

def desCompact(fileIn, path=None):
    zip = zipfile.ZipFile(fileIn)
    member = zip.namelist()[0]
    zip.extract(member, path)
    zip.close()
    return member

def lreclCopy(copy):

    if  isinstance(copy, list):
        book = copy
    else:
        if  isinstance(copy, str):
            book = copy.split('\n')
        else:
            book = []

    regc = {}

    linhas = filter(both(isNotRem, isNotBlank), book)

    while True:

        copy = False

        for li in linhas:

            if  li.find('COPY') > -1:

                copy = True

                break

        if  not copy: break

        idx = -1

        for li in linhas:

            idx += 1

            if  li.find('COPY') > -1:

                cols = li.split()

                book = cols[1].replace("'", '').replace('.', '')

                msg = 'COPY {} deve ser expandido.'.format(book)

                return {'retorno': False, 'msg': msg, 'lrecl': 0}

    linhaf = ''
    redefines = ''
    posdic = {}
    idxFiller = 1
    idx = 0
    posicao = 1
    itemGrupo = []
    nivel = 0
    occurs = 0
    niveloccurs = 0
    idl = 0

    for li in linhas:

        if  li.find('.') < 0:

            linhaf += li.upper()

            continue

        linhaf += li.upper()

        linha = linhaf.split()

        idl += 1

        nivel = int(linha[0])

        campo = linha[1].replace('.', '')

        if  campo == 'FILLER':

            cpo = '%s_%s' % (campo, '{:>02}'.format(idxFiller))

            idxFiller += 1

        else:

            cpo = campo

        itemGrupo.append([nivel, cpo])

        cpox = ''

        for idx in xrange(idl - 1, 0, -1):

            if  itemGrupo[idx][0] < nivel:

                cpox = itemGrupo[idx][1]

                break

        if  linhaf.find('REDEFINES ') > -1 and linhaf.find('PIC ') < 0:

            redefines = linha[3].replace('.', '')

            posdic[cpo] = posicao = posdic[redefines]

            regc[cpo] = {}

            regc[cpo]['nivel': nivel]
            regc[cpo]['natureza': '']
            regc[cpo]['posicao': posdic[cpo]]
            regc[cpo]['picture': '']
            regc[cpo]['tamanho': 0]
            regc[cpo]['inteiro': 0]
            regc[cpo]['decimais': 0]
            regc[cpo]['tipo': '']
            regc[cpo]['bytes': 0]
            regc[cpo]['redefines': redefines]
            regc[cpo]['itemGrupo': cpox]
            regc[cpo]['occurs': occurs]

            linhaf = ''

            continue

        if  linhaf.find('REDEFINES ') > -1 and \
            linhaf.find('PIC ') > -1:

            picture = linha[5]
            picts = picture.replace('.', '')

            if  len(linha) > 6:

                if  len(linha) == 7:

                    picture += (' ' + linha[6])

                else:

                    for idx in xrange(6, len(linha) - 1):

                        if  linha[idx].upper() != 'VALUE':

                            picture += (' ' + linha[idx])

            picture = picture.replace('S', '')

            pict = ''
            inteiro = 0
            decimais = 0
            tam = ''
            dec = ''
            idx = 0

            while picture[idx:idx + 1] != '(' and \
                  picture[idx:idx + 1] != ' ' and \
                  picture[idx:idx + 1] != '.':

                pict += picture[idx:idx + 1]
                idx += 1

            idx += 1

            while picture[idx:idx + 1] == ' ':

                idx += 1

            while picture[idx:idx + 1] != ')' and \
                  picture[idx:idx + 1] != ' ' and \
                  picture[idx:idx + 1] != '.':
                tam += picture[idx:idx + 1]
                idx += 1

            idx += 1

            while picture[idx:idx + 1] == ' ':

                idx += 1

            if  picture[idx:idx + 1] == 'V':

                dec = 'V'
                idx += 1

                while picture[idx:idx + 1] == '9' or \
                      picture[idx:idx + 1] == '(' or \
                      picture[idx:idx + 1] == ' ' or \
                      picture[idx:idx + 1] == '.':

                    idx += 1

                if  picture[idx:idx + 1] != 'U' and \
                    picture[idx:idx + 1] != '.':

                    while picture[idx:idx + 1] != ')' and \
                          picture[idx:idx + 1] != ' ' and \
                          picture[idx:idx + 1] != '.':

                        dec += picture[idx:idx + 1]
                        idx += 1

            if  dec == 'V':

                dec = ''

            if  dec != '' and (dec[1:] >= '0' and dec[1:] <= '9'):

                inteiro = int(tam)
                decimais = int(dec[1:])
                tam = str(int(tam) + int(dec[1:]))

            else:

                inteiro = int(tam)
                decimais = 0

            tam += dec
            tipo = ''
            idxtipo = picture.find(' COMP')

            if  idxtipo > -1:

                idxtipo += 1

                while picture[idxtipo:idxtipo + 1] != ' ' and \
                      picture[idxtipo:idxtipo + 1] != '.':

                    tipo += picture[idxtipo:idxtipo + 1]

                    idxtipo += 1

            redefines = linha[3].replace('.', '')

            posdic[cpo] = posicao = posdic[redefines] + 1

            regc[cpo] = {}

            regc[cpo]['nivel'] = nivel
            regc[cpo]['natureza'] = pict
            regc[cpo]['posicao'] = posdic[cpo]
            regc[cpo]['picture'] = picts
            regc[cpo]['tamanho'] = tam
            regc[cpo]['inteiro'] = inteiro
            regc[cpo]['decimais'] = decimais if decimais else 0
            regc[cpo]['tipo'] = tipo
            regc[cpo]['bytes'] = 0
            regc[cpo]['redefines'] = redefines
            regc[cpo]['itemGrupo'] = cpox
            regc[cpo]['occurs'] = occurs

            linhaf = ''

            continue

        if  linhaf.find('OCCURS ') > -1:

            if  len(linha) == 4:

                occurs = int(linha[3].replace('.', ''))

            elif len(linha) == 5:

                occurs = int(linha[3].replace('.', ''))

            else:

                occurs = int(linha[5].replace('.', ''))

            niveloccurs = nivel

            posdic[cpo] = posicao

            regc[cpo] = {}

            regc[cpo]['nivel'] = nivel
            regc[cpo]['natureza'] = ''
            regc[cpo]['posicao'] = posdic[cpo]
            regc[cpo]['picture'] = ''
            regc[cpo]['tamanho'] = 0
            regc[cpo]['inteiro'] = 0
            regc[cpo]['decimais'] = 0
            regc[cpo]['tipo'] = ''
            regc[cpo]['bytes'] = 0
            regc[cpo]['redefines'] = ''
            regc[cpo]['itemGrupo'] = cpox
            regc[cpo]['occurs'] = occurs

            linhaf = ''

            continue

        if  linhaf.find('PIC ') < 0:

            posdic[cpo] = posicao


            regc[cpo] = {}

            regc[cpo]['nivel'] = nivel
            regc[cpo]['natureza'] = ''
            regc[cpo]['posicao'] = posdic[cpo]
            regc[cpo]['picture'] = ''
            regc[cpo]['tamanho'] = 0
            regc[cpo]['inteiro'] = 0
            regc[cpo]['decimais'] = 0
            regc[cpo]['tipo'] = ''
            regc[cpo]['bytes'] = 0
            regc[cpo]['redefines'] = ''
            regc[cpo]['itemGrupo'] = cpox
            regc[cpo]['occurs'] = occurs

            linhaf = ''

            continue

        if  occurs:

            if  nivel <= niveloccurs:

                occurs = 0

                niveloccurs = 0

        redefines = ''

        linhaf = ''

        picture = linha[3]

        picts = picture.replace('.', '')

        if  len(linha) > 4:

            if  len(linha) == 5:

                picture += (' ' + linha[4])

            else:

                for idx in xrange(4, len(linha) - 1):

                    if  linha[idx].upper() != 'VALUE':

                        picture += (' ' + linha[idx])

        picture = picture.replace('S', '')

        pict = ''
        inteiro = 0
        decimais = 0
        tam = ''
        dec = ''
        idx = 0

        while picture[idx:idx + 1] != '(' and \
              picture[idx:idx + 1] != ' ' and \
              picture[idx:idx + 1] != '.':

            pict += picture[idx:idx + 1]
            idx += 1

        idx += 1

        while picture[idx:idx + 1] == ' ':

            idx += 1

        while picture[idx:idx + 1] != ')' and \
              picture[idx:idx + 1] != ' ' and \
              picture[idx:idx + 1] != '.':

            tam += picture[idx:idx + 1]
            idx += 1

        idx += 1

        while picture[idx:idx + 1] == ' ':

            idx += 1

        qt9 = 0

        if  picture[idx:idx + 1] == 'V':

            dec = 'V'
            idx += 1
            qt9 = 0

            while picture[idx:idx + 1] == '9' or \
                  picture[idx:idx + 1] == '(' or \
                  picture[idx:idx + 1] == ' ' or \
                  picture[idx:idx + 1] == '.':

                if  picture[idx:idx + 1] == '9':

                    qt9 += 1

                idx += 1

            if  picture[idx:idx + 1] != 'U' and \
                picture[idx:idx + 1] != '.':

                while picture[idx:idx + 1] != ')' and \
                      picture[idx:idx + 1] != ' ' and \
                      picture[idx:idx + 1] != '' and \
                      picture[idx:idx + 1] != '.':

                    dec += picture[idx:idx + 1]
                    idx += 1

        if  dec == 'V':

            dec = ''

        if  dec != '' and (dec[1:] >= '0' and dec[1:] <= '9'):

            inteiro = int(tam)
            decimais = int(dec[1:])

            tam = str(int(tam) + int(dec[1:]))

        else:

            inteiro = int(tam)
            decimais = qt9

        tam += dec
        tipo = ''
        idxtipo = picture.find(' COMP')

        if  idxtipo > -1:

            idxtipo += 1

            while picture[idxtipo:idxtipo + 1] != ' ' and \
                  picture[idxtipo:idxtipo + 1] != '.':

                tipo += picture[idxtipo:idxtipo + 1]
                idxtipo += 1

        if  redefines:

            posdic[cpo] = posicao = posdic[redefines] + 1

        else:

            posdic[cpo] = posicao

        nbytes = 0

        if  not redefines:

            if  pict == '9':

                if  tipo.find('COMP-3') > -1:

                    nbytes = (((inteiro + decimais) / 2) + 1)

                    posicao += nbytes

                elif tipo.find('COMP') > -1:

                    if  inteiro < 5:

                        posicao += 2
                        nbytes = 2

                    elif inteiro < 10:

                        posicao += 4
                        nbytes = 4

                    else:

                        posicao += 8
                        nbytes = 8

                else:

                    nbytes = inteiro + decimais
                    posicao += nbytes

            else:

                nbytes = inteiro
                posicao += nbytes

        regc[cpo] = {}

        regc[cpo]['nivel'] = nivel
        regc[cpo]['natureza'] = pict
        regc[cpo]['posicao'] = posdic[cpo]
        regc[cpo]['picture'] = picts
        regc[cpo]['tamanho'] = tam
        regc[cpo]['inteiro'] = inteiro
        regc[cpo]['decimais'] = decimais if decimais else 0
        regc[cpo]['tipo'] = tipo
        regc[cpo]['bytes'] = nbytes
        regc[cpo]['redefines'] = redefines
        regc[cpo]['itemGrupo'] = cpox
        regc[cpo]['occurs'] = occurs

    length = 0

    nivel = 0

    for k in regc:

        if  regc[k]['redefines']:
            nivel = regc[k]['nivel']
            continue

        if  nivel and regc[k]['nivel'] > nivel:
            continue

        nivel = 0

        try:
            bytes = int(regc[k]['bytes'])

        except:
            bytes = 0

        try:
            occurs = int(regc[k]['occurs'])

        except:
            occurs = 1

        length += (bytes * (occurs if occurs else 1))

    msg = 'calculo ok.'

    return {'retorno': True, 'msg': msg, 'lrecl': length}

def apath(path='', r=None):
    """
    Builds a path inside an application folder

    Parameters
    ----------
    path:
        path within the application folder
    r:
        the global request object

    """

    opath = up(r.folder)
    while path[:3] == '../':
        (opath, path) = (up(opath), path[3:])
    return os.path.join(opath, path).replace('\\', '/')

def app_create(db, app, request, force=False, key=None, info=False):
    """
    Create a copy of welcome.w2p (scaffolding) app

    Parameters
    ----------
    app:
        application name
    request:
        the global request object

    """
    path = apath(app, request)
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            if info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False
    elif not force:
        if info:
            return False, "Application exists"
        else:
            return False
    try:
        w2p_unpack('welcome.w2p', path)
        for subfolder in [
            'models', 'views', 'controllers', 'databases',
            'modules', 'cron', 'errors', 'sessions', 'cache',
            'languages', 'static', 'private', 'uploads']:
            subpath = os.path.join(path, subfolder)
            if not os.path.exists(subpath):
                os.mkdir(subpath)
        dbt = os.path.join(path, 'models', 'db.py')
        if os.path.exists(dbt):
            data = read_file(dbt)
            data = data.replace('<your secret key>',
                                'sha512:' + (key or web2py_uuid()))
            write_file(dbt, data)

        parms = db(db.parametros.id==1).select()[0]

        template = os.path.join('\\\\'
                              , '127.0.0.1'
                              , 'c$'
                              , parms.web2py
                              , 'applications'
                              , parms.soag
                              , 'Template'
                              , 'web2py') + os.sep

        models = os.path.join('\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.web2py
                            , 'applications'
                            , app
                            , 'models') + os.sep

        shutil.copyfile(template + 'addgets.py', models + 'addgets.py')

        shutil.copyfile(template + 'forms.py', models + 'forms.py')

        shutil.copyfile(template + 'listdetail.py', models + 'listdetail.py')

        shutil.copyfile(template + 'menu1.py', models + 'menu.py')

        shutil.copyfile(template + 'menu2.py', models + 'menu2.py')

        if info:
            return True, None
        else:
            return True
    except:
        shutil.rmtree(path)
        if info:
            return False, traceback.format_exc(sys.exc_info)
        else:
            return False
