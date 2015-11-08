import sys, os, os.path, glob, stat

class Options():
  __slots__ = ('args', 'project', 'cmake', 'root', 'source', 'binary')
  def __init__(self):
    import optparse
    parser = optparse.OptionParser()
    parser.add_option("-p", "--project",  dest="project", default=r"/vlab/source/pickle/putty/pickle/Putty.prj",  help="project file to convert from")
    parser.add_option("-c", "--cmake",    dest="cmake",   default="",  help="cmake file to convert to")
    parser.add_option("-r", "--root",     dest="root",    default="/putty",  help="root common to source and build")
    parser.add_option("-s", "--source",   dest="source",  default='${CMAKE_CURRENT_SOURCE_DIR}',  help="cmake source")
    parser.add_option("-b", "--binary",   dest="binary",  default='${CMAKE_CURRENT_BINARY_DIR}',  help="cmake binary")
    (options, args) = parser.parse_args()
    self.args       = args
    self.project    = options.project
    self.cmake      = options.cmake
    self.root       = options.root
    self.source     = options.source
    self.binary     = options.binary
    
class Class():
  pass

def fixup(filepath, root, cmake):
  to_lower=['.si','.sh','.pi','.so','.sql']
  dp, ne = os.path.split(filepath.replace('\\', '/'))
  d, p   = os.path.splitdrive(dp.lower())
  n, e   = os.path.splitext(ne)
  if e in to_lower:
    n = n.lower()
  i = p.find(root)
  if i == 0: 
    p = p[len(root):]  
  return '%s%s/%s%s' % (cmake, p, n, e)

def check_switch(switch, root):
  if len(switch) > 2: 
    if switch[1] == ':' or switch.lower().replace('\\', '/').find(root) == 0:
      return fixup(switch, root, '')
  return switch
    
def main():
  options = Options() 
  infile = open(options.project, 'rt')
  inlines = infile.readlines()
  infile.close()
  state = None; SWITCHES=1; SOURCE=2; TARGETS=3
  switch  = {}
  sources = []
  for inline in inlines:
    line = inline.strip()
    if len(line) == 0:
      continue
    if state == None:
      if line == '[Switches]':
        state = SWITCHES
    elif state == SWITCHES:
      if line == '[Source]':
        state = SOURCE
        continue 
      if line == '[Targets]':
        state = TARGETS
        continue
      arr = line.split('=') 
      if len(arr) == 2:
        switch[arr[0]] = check_switch(arr[1], options.root)
    elif state == SOURCE:  
      if line == '[Targets]':
        state = TARGETS
        continue
      arr = line.split()
      if len(arr) >= 1:
        source = Class()
        source.name = fixup(arr[0], options.root, options.source)
        source.targets = []
        sources.append(source)
    elif state == TARGETS:  
      if line == '[Source]':
        state = SOURCE
        continue
      arr = line.split()
      if len(arr) == 4:
        target = Class()
        target.name = fixup(arr[1], options.root, options.binary)
        source.targets.append(target)
  for source in sources:
    print source.name    
    for target in source.targets:
      print ' ', target.name
  for x in sorted(switch):
    print x, switch[x]    
      
if __name__ == '__main__':
  exit(main())    

'''
[Switches]
Autoclose=0
BinDir=\putty\sql\so
BinExt=.so
BlankPadded=0
CharZ=0
ConnReqd=1
ControlDB=npud00
CppHeader=0
CSNet7Dir=\putty\cs\Header
CSNet7Ext=cs
EightByte=0
ExitReqd=0
ExtendedC=1
ExtendedFlags=0
ExtendedPAS=0
ExtendedVB=0
HeaderDir=\putty\c\inclsql
HeaderExt=.sh
IDLDir=\putty\sql\idl
IDLExt=.ii
IDLMod=putty
IDLModExt=.im
IDLUbi=0
Internal=1
LittleTCSIDL2=0
LittleTrue=1
LogDir=\putty\sql\logs
LogExt=.log
OneSQLScript=1
PARMSApp=Pgfeupm
PARMSDescr=Simon Version 3
PARMSDir=\putty\sql\Params
PARMSExt=.pi
PARMSFileName=C:\Putty\bin\Pgfeupm.parms
PARMSPassword=tiger
PARMSRegistry=\SOFTWARE\Nedcor\Putty\Parameter Control
PARMSServer=dn29
PARMSUser=npu
PARMSVersion=3
PASDir=\putty\sql\pas
PASExt=.pas
PickleExec=C:\Putty\bin\pickle.bat
PrefixVBClasses=0
ProjBinDir=\putty\bin\
ProjBinExt=.bin
ProjDir=\putty\bin\
ProjExt=.prj
ProjFileNode=putty
PythonDir=\putty\sql\py
PythonExt=.py
SqlAuditExt=.aud
SqlConExt=.con
SqlDir=\putty\sql\sqldefs
SqlExt=.sql
SqlGrantExt=.gra
SqlIdxExt=.idx
SqlProcExt=.pro
SqlSnapExt=.sna
SqlTableExt=.tab
SqlViewsExt=.vie
TargetC=1
TargetCSAdoNet=0
TargetCSIDL2=0
TargetCSNet7=1
TargetCSRW=0
TargetIDL=0
TargetPAS=0
TargetPython=1
TargetSO=1
TargetSQL=1
TargetVB=0
TargetVB5=1
TargetVBCode3=0
TargetVBforADOR=0
TargetVBforIDL=0
TargetVBNet7=0
UConnect=npu/tiger@dn29
UnderScore=0
UnlockedProject=0
UseUsedBy=0
VB5Dir=\putty\vb\inclbas
VB5Ext=.cls
VBCode3Dir=\putty\vb\inclbas
VBDir=\putty\vb\inclbas
VBExt=.bas
VBforIDLDir=\putty\vb\inclbas
Verbose=0
Version2Bin=0
VersionSaved=611.0.0
WhichDB=0

[Source]
c:\Putty\sql\Si\BlobData.si # 9

[Targets]
3 \putty\c\inclsql\BlobData.sh # 0
4 \putty\sql\logs\BlobData.log # 0
2 \putty\sql\so\BlobData.so # 0
1 \putty\sql\sqldefs\BlobData.sql # 0

[Source]
c:\Putty\sql\Si\Group.si # 1

[Targets]
3 \putty\cs\Header\Group.cs # 0
3 \putty\cs\Header\i3_group.cs # 0
3 \putty\c\inclsql\Group.sh # 0
4 \putty\sql\logs\Group.log # 0
6 \putty\sql\Params\Group.pi # 0
8 \putty\sql\py\db_group.py # 0
8 \putty\sql\py\i3_group.py # 0
2 \putty\sql\so\Group.so # 0
1 \putty\sql\sqldefs\Group.sql # 0

[Source]
c:\Putty\sql\Si\persistent.si # 4

[Targets]
3 c:\Putty\sql\Si\i3_persistent # 0
3 \putty\c\inclsql\persistent.sh # 0
4 \putty\sql\logs\persistent.log # 0
8 \putty\sql\py\db_persistent.py # 0
8 \putty\sql\py\i3_persistent.py # 0
2 \putty\sql\so\persistent.so # 0
1 \putty\sql\sqldefs\persistent.sql # 0

[Source]
c:\Putty\sql\Si\ScriptsGroup.si # 1

[Targets]
3 \putty\cs\Header\i3_scriptsgroup.cs # 0
3 \putty\cs\Header\ScriptsGroup.cs # 0
3 \putty\c\inclsql\ScriptsGroup.sh # 0
4 \putty\sql\logs\ScriptsGroup.log # 0
6 \putty\sql\Params\ScriptsGroup.pi # 0
8 \putty\sql\py\db_scriptsgroup.py # 0
8 \putty\sql\py\i3_scriptsgroup.py # 0
2 \putty\sql\so\ScriptsGroup.so # 0
1 \putty\sql\sqldefs\ScriptsGroup.sql # 0

[Source]
c:\Putty\sql\Si\simon.si # 545

[Targets]
3 \putty\c\inclsql\simon.sh # 0
4 \putty\sql\logs\simon.log # 0
2 \putty\sql\so\simon.so # 0
1 \putty\sql\sqldefs\simon.sql # 0

[Source]
c:\Putty\sql\Si\StaffGroup.si # 4

[Targets]
3 \putty\cs\Header\i3_staffgroup.cs # 0
3 \putty\cs\Header\StaffGroup.cs # 0
3 \putty\c\inclsql\StaffGroup.sh # 0
4 \putty\sql\logs\StaffGroup.log # 0
6 \putty\sql\Params\StaffGroup.pi # 0
8 \putty\sql\py\db_staffgroup.py # 0
8 \putty\sql\py\i3_staffgroup.py # 0
2 \putty\sql\so\StaffGroup.so # 0
1 \putty\sql\sqldefs\StaffGroup.sql # 0

[Source]
\putty\SQL\Si\Accounttype.si # 1

[Targets]
3 \putty\cs\Header\Accounttype.cs # 0
3 \putty\cs\Header\i3_accounttype.cs # 0
3 \putty\c\inclsql\Accounttype.sh # 0
4 \putty\sql\logs\Accounttype.log # 0
6 \putty\sql\Params\Accounttype.pi # 0
8 \putty\sql\py\db_accounttype.py # 0
8 \putty\sql\py\i3_accounttype.py # 0
2 \putty\sql\so\Accounttype.so # 0
1 \putty\sql\sqldefs\Accounttype.sql # 0
3 \putty\vb\inclbas\AccountType.cls # 0
3 \putty\vb\inclbas\AccountTypeDeleteOne.cls # 0

[Source]
\Putty\SQL\Si\AlmanacBank.si # 131

[Targets]
3 \putty\c\inclsql\AlmanacBank.sh # 0
4 \putty\sql\logs\AlmanacBank.log # 0
6 \putty\sql\Params\AlmanacBank.pi # 0
8 \putty\sql\py\db_almanacbank.py # 0
8 \putty\sql\py\i3_almanacbank.py # 0
3 \Putty\SQL\Si\i3_almanacbank # 0
2 \putty\sql\so\AlmanacBank.so # 0
1 \putty\sql\sqldefs\AlmanacBank.sql # 0

[Source]
\Putty\SQL\Si\AlmanacCorrespondent.si # 4

[Targets]
3 \putty\c\inclsql\AlmanacCorrespondent.sh # 0
4 \putty\sql\logs\AlmanacCorrespondent.log # 0
6 \putty\sql\Params\AlmanacCorrespondent.pi # 0
8 \putty\sql\py\db_almanaccorrespondent.py # 0
8 \putty\sql\py\i3_almanaccorrespondent.py # 0
3 \Putty\SQL\Si\i3_almanaccorrespondent # 0
2 \putty\sql\so\AlmanacCorrespondent.so # 0
1 \putty\sql\sqldefs\AlmanacCorrespondent.sql # 0

[Source]
\putty\SQL\Si\Audittrail.si # 1

[Targets]
3 \putty\c\inclsql\Audittrail.sh # 0
4 \putty\sql\logs\Audittrail.log # 0
2 \putty\sql\so\Audittrail.so # 0
1 \putty\sql\sqldefs\Audittrail.sql # 0

[Source]
\putty\SQL\Si\Bankaccount.si # 1

[Targets]
3 \putty\c\inclsql\Bankaccount.sh # 0
4 \putty\sql\logs\Bankaccount.log # 0
6 \putty\sql\Params\Bankaccount.pi # 0
2 \putty\sql\so\Bankaccount.so # 0
1 \putty\sql\sqldefs\Bankaccount.sql # 0

[Source]
\putty\sql\si\bankaccproc.si # 1

[Targets]
3 \putty\c\inclsql\bankaccproc.sh # 0
4 \putty\sql\logs\bankaccproc.log # 0
8 \putty\sql\py\db_bankaccproc.py # 0
8 \putty\sql\py\i3_bankaccproc.py # 0
3 \putty\sql\si\i3_bankaccproc # 0
2 \putty\sql\so\bankaccproc.so # 0
1 \putty\sql\sqldefs\bankaccproc.sql # 0

[Source]
\Putty\SQL\Si\BankCorrespondents.si # 1

[Targets]
3 \putty\c\inclsql\BankCorrespondents.sh # 0
4 \putty\sql\logs\BankCorrespondents.log # 0
6 \putty\sql\Params\BankCorrespondents.pi # 0
8 \putty\sql\py\db_bankcorrespondents.py # 0
8 \putty\sql\py\i3_bankcorrespondents.py # 0
3 \Putty\SQL\Si\i3_bankcorrespondents # 0
2 \putty\sql\so\BankCorrespondents.so # 0
1 \putty\sql\sqldefs\BankCorrespondents.sql # 0

[Source]
\putty\SQL\Si\Bankfile.si # 47

[Targets]
3 \putty\c\inclsql\Bankfile.sh # 0
4 \putty\sql\logs\Bankfile.log # 0
6 \putty\sql\Params\Bankfile.pi # 0
8 \putty\sql\py\db_bankfile.py # 0
8 \putty\sql\py\i3_bankfile.py # 0
3 \putty\SQL\Si\i3_bankfile # 0
2 \putty\sql\so\Bankfile.so # 0
1 \putty\sql\sqldefs\Bankfile.sql # 0

[Source]
\putty\sql\si\bankfileproc.si # 11

[Targets]
3 \putty\c\inclsql\bankfileproc.sh # 0
4 \putty\sql\logs\bankfileproc.log # 0
2 \putty\sql\so\bankfileproc.so # 0
1 \putty\sql\sqldefs\bankfileproc.sql # 0

[Source]
\putty\SQL\Si\Comments.si # 1

[Targets]
3 \putty\c\inclsql\Comments.sh # 0
4 \putty\sql\logs\Comments.log # 0
8 \putty\sql\py\db_comments.py # 0
8 \putty\sql\py\i3_comments.py # 0
3 \putty\SQL\Si\i3_comments # 0
2 \putty\sql\so\Comments.so # 0
1 \putty\sql\sqldefs\Comments.sql # 0

[Source]
\putty\SQL\Si\Country.si # 132

[Targets]
3 \putty\c\inclsql\Country.sh # 0
4 \putty\sql\logs\Country.log # 0
6 \putty\sql\Params\Country.pi # 0
8 \putty\sql\py\db_country.py # 0
8 \putty\sql\py\i3_country.py # 0
3 \putty\SQL\Si\i3_country # 0
2 \putty\sql\so\Country.so # 0
1 \putty\sql\sqldefs\Country.sql # 0

[Source]
\Putty\SQL\Si\CountryCurrency.si # 1

[Targets]
3 \putty\c\inclsql\CountryCurrency.sh # 0
4 \putty\sql\logs\CountryCurrency.log # 0
6 \putty\sql\Params\CountryCurrency.pi # 0
2 \putty\sql\so\CountryCurrency.so # 0
1 \putty\sql\sqldefs\CountryCurrency.sql # 0

[Source]
\putty\SQL\Si\Currency.si # 7

[Targets]
3 \putty\c\inclsql\Currency.sh # 0
4 \putty\sql\logs\Currency.log # 0
6 \putty\sql\Params\Currency.pi # 0
2 \putty\sql\so\Currency.so # 0
1 \putty\sql\sqldefs\Currency.sql # 0

[Source]
\Putty\SQL\Si\Dates.si # 1

[Targets]
3 \putty\c\inclsql\Dates.sh # 0
4 \putty\sql\logs\Dates.log # 0
6 \putty\sql\Params\Dates.pi # 0
8 \putty\sql\py\db_dates.py # 0
8 \putty\sql\py\i3_dates.py # 0
3 \Putty\SQL\Si\i3_dates # 0
2 \putty\sql\so\Dates.so # 0
1 \putty\sql\sqldefs\Dates.sql # 0

[Source]
\Putty\SQL\si\Domain.si # 1

[Targets]
3 \putty\c\inclsql\Domain.sh # 0
4 \putty\sql\logs\Domain.log # 0
2 \putty\sql\so\Domain.so # 0
1 \putty\sql\sqldefs\Domain.sql # 0

[Source]
\Putty\SQL\Si\Drivers.si # 1

[Targets]
3 \putty\c\inclsql\Drivers.sh # 0
4 \putty\sql\logs\Drivers.log # 0
6 \putty\sql\Params\Drivers.pi # 0
2 \putty\sql\so\Drivers.so # 0
1 \putty\sql\sqldefs\Drivers.sql # 0

[Source]
\putty\SQL\Si\Fields.si # 24

[Targets]
3 \putty\c\inclsql\Fields.sh # 0
4 \putty\sql\logs\Fields.log # 0
8 \putty\sql\py\db_fields.py # 0
8 \putty\sql\py\i3_fields.py # 0
3 \putty\SQL\Si\i3_fields # 0
2 \putty\sql\so\Fields.so # 0
1 \putty\sql\sqldefs\Fields.sql # 0

[Source]
\putty\SQL\Si\FieldSearchDef.si # 1

[Targets]
3 \putty\c\inclsql\FieldSearchDef.sh # 0
4 \putty\sql\logs\FieldSearchDef.log # 0
6 \putty\sql\Params\FieldSearchDef.pi # 0
2 \putty\sql\so\FieldSearchDef.so # 0
1 \putty\sql\sqldefs\FieldSearchDef.sql # 0

[Source]
\Putty\SQL\Si\FigCorrBankProc.si # 1

[Targets]
3 \putty\c\inclsql\FigCorrBankProc.sh # 0
4 \putty\sql\logs\FigCorrBankProc.log # 0
8 \putty\sql\py\db_figcorrbankproc.py # 0
8 \putty\sql\py\i3_figcorrbankproc.py # 0
3 \Putty\SQL\Si\i3_figcorrbankproc # 0
2 \putty\sql\so\FigCorrBankProc.so # 0
1 \putty\sql\sqldefs\FigCorrBankProc.sql # 0

[Source]
\putty\sql\si\figcorrespondentbank.si # 21

[Targets]
3 \putty\c\inclsql\figcorrespondentbank.sh # 0
4 \putty\sql\logs\figcorrespondentbank.log # 0
6 \putty\sql\Params\figcorrespondentbank.pi # 0
2 \putty\sql\so\figcorrespondentbank.so # 0
1 \putty\sql\sqldefs\figcorrespondentbank.sql # 0

[Source]
\putty\sql\si\fileinput.si # 7

[Targets]
3 \putty\c\inclsql\fileinput.sh # 0
4 \putty\sql\logs\fileinput.log # 0
2 \putty\sql\so\fileinput.so # 0
1 \putty\sql\sqldefs\fileinput.sql # 0

[Source]
\putty\sql\si\fileoutput.si # 1

[Targets]
3 \putty\c\inclsql\fileoutput.sh # 0
4 \putty\sql\logs\fileoutput.log # 0
2 \putty\sql\so\fileoutput.so # 0
1 \putty\sql\sqldefs\fileoutput.sql # 0

[Source]
\putty\sql\si\finidcorrespondentrouting.si # 1

[Targets]
3 \putty\c\inclsql\finidcorrespondentrouting.sh # 0
4 \putty\sql\logs\finidcorrespondentrouting.log # 0
6 \putty\sql\Params\finidcorrespondentrouting.pi # 0
8 \putty\sql\py\db_finidcorrespondentrouting.py # 0
8 \putty\sql\py\i3_finidcorrespondentrouting.py # 0
3 \putty\sql\si\i3_finidcorrespondentrouting # 0
2 \putty\sql\so\finidcorrespondentrouting.so # 0
1 \putty\sql\sqldefs\finidcorrespondentrouting.sql # 0

[Source]
\putty\SQL\Si\Lookup.si # 28

[Targets]
3 \putty\c\inclsql\Lookup.sh # 0
4 \putty\sql\logs\Lookup.log # 0
6 \putty\sql\Params\Lookup.pi # 0
8 \putty\sql\py\db_lookup.py # 0
8 \putty\sql\py\i3_lookup.py # 0
3 \putty\SQL\Si\i3_lookup # 0
2 \putty\sql\so\Lookup.so # 0
1 \putty\sql\sqldefs\Lookup.sql # 0

[Source]
\putty\SQL\Si\LookupProc.si # 1

[Targets]
3 \putty\c\inclsql\LookupProc.sh # 0
4 \putty\sql\logs\LookupProc.log # 0
2 \putty\sql\so\LookupProc.so # 0
1 \putty\sql\sqldefs\LookupProc.sql # 0

[Source]
\putty\SQL\Si\Message.si # 1

[Targets]
3 \putty\c\inclsql\Message.sh # 0
4 \putty\sql\logs\Message.log # 0
8 \putty\sql\py\db_message.py # 0
8 \putty\sql\py\i3_message.py # 0
3 \putty\SQL\Si\i3_message # 0
2 \putty\sql\so\Message.so # 0
1 \putty\sql\sqldefs\Message.sql # 0

[Source]
\putty\SQL\Si\Queue.si # 1

[Targets]
3 \putty\c\inclsql\Queue.sh # 0
4 \putty\sql\logs\Queue.log # 0
6 \putty\sql\Params\Queue.pi # 0
2 \putty\sql\so\Queue.so # 0
1 \putty\sql\sqldefs\Queue.sql # 0

[Source]
\putty\SQL\Si\Queuerecovery.si # 4

[Targets]
3 \putty\c\inclsql\Queuerecovery.sh # 0
4 \putty\sql\logs\Queuerecovery.log # 0
2 \putty\sql\so\Queuerecovery.so # 0
1 \putty\sql\sqldefs\Queuerecovery.sql # 0

[Source]
\Putty\SQL\Si\QueueType.si # 1

[Targets]
3 \putty\c\inclsql\QueueType.sh # 0
4 \putty\sql\logs\QueueType.log # 0
6 \putty\sql\Params\QueueType.pi # 0
2 \putty\sql\so\QueueType.so # 0
1 \putty\sql\sqldefs\QueueType.sql # 0

[Source]
\putty\SQL\Si\Reply.si # 1

[Targets]
3 \putty\c\inclsql\Reply.sh # 0
4 \putty\sql\logs\Reply.log # 0
8 \putty\sql\py\db_reply.py # 0
8 \putty\sql\py\i3_reply.py # 0
3 \putty\SQL\Si\i3_reply # 0
2 \putty\sql\so\Reply.so # 0
1 \putty\sql\sqldefs\Reply.sql # 0

[Source]
\putty\SQL\Si\Response.si # 24

[Targets]
3 \putty\c\inclsql\Response.sh # 0
4 \putty\sql\logs\Response.log # 0
8 \putty\sql\py\db_response.py # 0
8 \putty\sql\py\i3_response.py # 0
3 \putty\SQL\Si\i3_response # 0
2 \putty\sql\so\Response.so # 0
1 \putty\sql\sqldefs\Response.sql # 0

[Source]
\putty\SQL\Si\Routing.si # 1

[Targets]
3 \putty\c\inclsql\Routing.sh # 0
4 \putty\sql\logs\Routing.log # 0
8 \putty\sql\py\db_routing.py # 0
8 \putty\sql\py\i3_routing.py # 0
3 \putty\SQL\Si\i3_routing # 0
2 \putty\sql\so\Routing.so # 0
1 \putty\sql\sqldefs\Routing.sql # 0

[Source]
\putty\SQL\Si\ScriptProcs.si # 1

[Targets]
3 \putty\cs\Header\i3_scriptprocs.cs # 0
3 \putty\cs\Header\ScriptProcs.cs # 0
3 \putty\c\inclsql\ScriptProcs.sh # 0
4 \putty\sql\logs\ScriptProcs.log # 0
8 \putty\sql\py\db_scriptprocs.py # 0
8 \putty\sql\py\i3_scriptprocs.py # 0
2 \putty\sql\so\ScriptProcs.so # 0
1 \putty\sql\sqldefs\ScriptProcs.sql # 0

[Source]
\putty\SQL\Si\Scripts.si # 1

[Targets]
3 \putty\cs\Header\Scripts.cs # 0
3 \putty\c\inclsql\Scripts.sh # 0
4 \putty\sql\logs\Scripts.log # 0
2 \putty\sql\so\Scripts.so # 0
1 \putty\sql\sqldefs\Scripts.sql # 0

[Source]
\putty\SQL\Si\ScriptVersion.si # 1

[Targets]
3 \putty\c\inclsql\ScriptVersion.sh # 0
4 \putty\sql\logs\ScriptVersion.log # 0
2 \putty\sql\so\ScriptVersion.so # 0
1 \putty\sql\sqldefs\ScriptVersion.sql # 0

[Source]
\putty\SQL\Si\Sourcesystem.si # 8

[Targets]
3 \putty\c\inclsql\Sourcesystem.sh # 0
4 \putty\sql\logs\Sourcesystem.log # 0
6 \putty\sql\Params\Sourcesystem.pi # 0
2 \putty\sql\so\Sourcesystem.so # 0
1 \putty\sql\sqldefs\Sourcesystem.sql # 0

[Source]
\putty\SQL\Si\Staff.si # 1

[Targets]
3 \putty\cs\Header\i3_staff.cs # 0
3 \putty\cs\Header\Staff.cs # 0
3 \putty\c\inclsql\Staff.sh # 0
4 \putty\sql\logs\Staff.log # 0
6 \putty\sql\Params\Staff.pi # 0
8 \putty\sql\py\db_staff.py # 0
8 \putty\sql\py\i3_staff.py # 0
2 \putty\sql\so\Staff.so # 0
1 \putty\sql\sqldefs\Staff.sql # 0

[Source]
\putty\SQL\Si\Staffprofile.si # 7

[Targets]
3 \putty\c\inclsql\Staffprofile.sh # 0
4 \putty\sql\logs\Staffprofile.log # 0
2 \putty\sql\so\Staffprofile.so # 0
1 \putty\sql\sqldefs\Staffprofile.sql # 0

[Source]
\putty\SQL\Si\Staffqueueconfig.si # 1

[Targets]
3 \putty\c\inclsql\Staffqueueconfig.sh # 0
4 \putty\sql\logs\Staffqueueconfig.log # 0
2 \putty\sql\so\Staffqueueconfig.so # 0
1 \putty\sql\sqldefs\Staffqueueconfig.sql # 0

[Source]
\putty\SQL\Si\Staffqueueperm.si # 1

[Targets]
3 \putty\c\inclsql\Staffqueueperm.sh # 0
4 \putty\sql\logs\Staffqueueperm.log # 0
6 \putty\sql\Params\Staffqueueperm.pi # 0
2 \putty\sql\so\Staffqueueperm.so # 0
1 \putty\sql\sqldefs\Staffqueueperm.sql # 0

[Source]
\Putty\SQL\Si\Staffqueuepermproc.si # 1

[Targets]
3 \putty\c\inclsql\Staffqueuepermproc.sh # 0
4 \putty\sql\logs\Staffqueuepermproc.log # 0
2 \putty\sql\so\Staffqueuepermproc.so # 0
1 \putty\sql\sqldefs\Staffqueuepermproc.sql # 0

[Source]
\putty\SQL\Si\StreamFieldMsgRel.si # 0

[Targets]
3 \putty\c\inclsql\StreamFieldMsgRel.sh # 0
4 \putty\sql\logs\StreamFieldMsgRel.log # 0
6 \putty\sql\Params\StreamFieldMsgRel.pi # 0
2 \putty\sql\so\StreamFieldMsgRel.so # 0
1 \putty\sql\sqldefs\StreamFieldMsgRel.sql # 0

[Source]
\putty\SQL\Si\StreamFieldsdef.si # 0

[Targets]
3 \putty\c\inclsql\StreamFieldsdef.sh # 0
4 \putty\sql\logs\StreamFieldsdef.log # 0
6 \putty\sql\Params\StreamFieldsdef.pi # 0
2 \putty\sql\so\StreamFieldsdef.so # 0
1 \putty\sql\sqldefs\StreamFieldsdef.sql # 0

[Source]
\putty\SQL\Si\Streammessageformat.si # 0

[Targets]
3 \putty\c\inclsql\Streammessageformat.sh # 0
4 \putty\sql\logs\Streammessageformat.log # 0
6 \putty\sql\Params\Streammessageformat.pi # 0
2 \putty\sql\so\Streammessageformat.so # 0
1 \putty\sql\sqldefs\Streammessageformat.sql # 0

[Source]
\Putty\SQL\Si\Streams.si # 1

[Targets]
3 \putty\c\inclsql\Streams.sh # 0
4 \putty\sql\logs\Streams.log # 0
8 \putty\sql\py\db_streams.py # 0
8 \putty\sql\py\i3_streams.py # 0
3 \Putty\SQL\Si\i3_streams # 0
2 \putty\sql\so\Streams.so # 0
1 \putty\sql\sqldefs\Streams.sql # 0

[Source]
\Putty\SQL\Si\Streamtype.si # 2

[Targets]
3 \putty\c\inclsql\Streamtype.sh # 0
4 \putty\sql\logs\Streamtype.log # 0
6 \putty\sql\Params\Streamtype.pi # 0
2 \putty\sql\so\Streamtype.so # 0
1 \putty\sql\sqldefs\Streamtype.sql # 0

[Source]
\Putty\SQL\Si\Summary.si # 1

[Targets]
3 \putty\c\inclsql\Summary.sh # 0
4 \putty\sql\logs\Summary.log # 0
8 \putty\sql\py\db_summary.py # 0
8 \putty\sql\py\i3_summary.py # 0
3 \Putty\SQL\Si\i3_summary # 0
2 \putty\sql\so\Summary.so # 0
1 \putty\sql\sqldefs\Summary.sql # 0

[Source]
\putty\SQL\Si\TestMessage.si # 1

[Targets]
3 \putty\c\inclsql\TestMessage.sh # 0
4 \putty\sql\logs\TestMessage.log # 0
2 \putty\sql\so\TestMessage.so # 0
1 \putty\sql\sqldefs\TestMessage.sql # 0

[Source]
\putty\SQL\Si\TestPack.si # 72

[Targets]
3 \putty\c\inclsql\TestPack.sh # 0
4 \putty\sql\logs\TestPack.log # 0
6 \putty\sql\Params\TestPack.pi # 0
2 \putty\sql\so\TestPack.so # 0
1 \putty\sql\sqldefs\TestPack.sql # 0

[Source]
\putty\SQL\Si\TestPackMessage.si # 1

[Targets]
3 \putty\c\inclsql\TestPackMessage.sh # 0
4 \putty\sql\logs\TestPackMessage.log # 0
2 \putty\sql\so\TestPackMessage.so # 0
1 \putty\sql\sqldefs\TestPackMessage.sql # 0

[Source]
\putty\sql\si\testpackpayment.si # 1

[Targets]
3 \putty\c\inclsql\testpackpayment.sh # 0
4 \putty\sql\logs\testpackpayment.log # 0
2 \putty\sql\so\testpackpayment.so # 0
1 \putty\sql\sqldefs\testpackpayment.sql # 0

'''