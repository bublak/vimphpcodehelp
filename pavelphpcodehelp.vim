python import sys

python import vim
python sys.path.append(vim.eval('expand("<sfile>:h")'))

"move to class file
"
function! PavelNavigateToClass(sCls, lineNumber)

python <<EOF
import vim

from CodeNavigate import CodeNavigate

codeNav = CodeNavigate()

lines      = vim.current.buffer
searchWord = vim.eval("a:sCls")
searchWord = searchWord.strip()
lineNumber = int(vim.eval("a:lineNumber"))
lineNumber = lineNumber - 1 #correction to right line, where is cursor

filename = codeNav.navigateToClass(searchWord, lines, lineNumber)

if filename != False:
    vim.command('e ' + filename)
else:
    print filename

EOF
endfunction

function! PavelGetClassContextData(sCls, lineNumber)
python << endOfPython

from CodeNavigate import CodeNavigate

lines      = vim.current.buffer
searchWord = vim.eval("a:sCls")
searchWord = searchWord.strip()
lineNumber = int(vim.eval("a:lineNumber"))
lineNumber = lineNumber - 1 #correction to right line, where is cursor
filename   = vim.eval("@%")

codeNav = CodeNavigate()

codeNav.getClassContextData(searchWord, lines, lineNumber, filename)

endOfPython
endfunction


function! PavelGetFunctionAnotation(sCls, lineNumber, className)
python << endOfPython

from CodeNavigate import CodeNavigate

codeNav = CodeNavigate()

classNameOfFunction = vim.eval("a:className")
searchWord          = vim.eval("a:sCls")
lineNumber          = int(vim.eval("a:lineNumber"))
lineNumber          = lineNumber - 1 #correction to right line, where is cursor
lines               = vim.current.buffer
filename            = vim.eval("@%")

print '============= '
print 'class name: ' + classNameOfFunction
print 'function name: ' + searchWord

codeNav.getFunctionAnotation(searchWord, classNameOfFunction, lineNumber, lines, filename)

endOfPython
endfunction
