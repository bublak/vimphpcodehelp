python import sys

python import vim
python sys.path.append(vim.eval('expand("<sfile>:h")'))

"move to class file
"
" This function exptects the created 'tag' file, and loaded, because it use it to find class.
function! PavelCodeNavigate(sCls, lineNumber)

python <<EOF
import vim

from CodeNavigate import CodeNavigate

lines = vim.current.buffer

searchWord = vim.eval("a:sCls")
lineNumber = int(vim.eval("a:lineNumber"))

lineNumber = lineNumber - 1 #correction to right line, where is cursor
searchWord = searchWord.strip()

codeMove = CodeNavigate()
result = codeMove.startSearching(searchWord, lines, lineNumber)

if result != False:
    #print result
    vim.command('e ' + result)
else:
    print result

EOF
endfunction

function! PavelClassContextHint(sCls, lineNumber)
python << endOfPython

from ClassContextHint import ClassContextHint
from CodeNavigate import CodeNavigate

cch = ClassContextHint("bb") # TODO set path properly

filename = None
##################TODO  tohle je stejny jako v CodeNavigate
lines = vim.current.buffer

searchWord = vim.eval("a:sCls")
lineNumber = int(vim.eval("a:lineNumber"))

lineNumber = lineNumber - 1 #correction to right line, where is cursor
searchWord = searchWord.strip()

if searchWord == '':
    #print "using actual file:"
    filename = vim.eval("@%")
else:
    codeMove = CodeNavigate()
    result = codeMove.startSearching(searchWord, lines, lineNumber)

    if result != False:
        filename = result
    else:
        print result
##################TODO  tohle je stejny jako v CodeNavigate

if filename:
    cch.getContextHintsForFile(filename, True)


endOfPython
endfunction


function! PavelMethodContextHint(sCls, lineNumber, className)
python << endOfPython

from ClassContextHint import ClassContextHint
from CodeNavigate import CodeNavigate

cch = ClassContextHint("bb") # TODO set path properly

filename = None
##################TODO  tohle je stejny jako v CodeNavigate
lines = vim.current.buffer

searchWord = vim.eval("a:sCls")
className = vim.eval("a:className")
lineNumber = int(vim.eval("a:lineNumber"))
print '============= '
print className
print searchWord
print lineNumber

lineNumber = int(vim.eval("a:lineNumber"))


filename = None
##################TODO  tohle je stejny jako v CodeNavigate
lines = vim.current.buffer

searchWord = vim.eval("a:sCls")
lineNumber = int(vim.eval("a:lineNumber"))

lineNumber = lineNumber - 1 #correction to right line, where is cursor
searchWord = searchWord.strip()

if searchWord == '':
    #print "using actual file:"
    filename = vim.eval("@%")
else:
    codeMove = CodeNavigate()
    result = codeMove.startSearching(className, lines, lineNumber)

    if result != False:
        filename = result
    else:
        filename = vim.eval("@%")

if filename:
    cch.getMethodHintForFile(filename, searchWord, True)


endOfPython
endfunction
