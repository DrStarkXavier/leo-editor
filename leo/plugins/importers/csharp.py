#@+leo-ver=5-thin
#@+node:ekr.20140723122936.18140: * @file importers/csharp.py
'''The @auto importer for C#.'''
import leo.core.leoImport as leoImport
BaseScanner = leoImport.BaseScanner
#@+others
#@+node:ekr.20140723122936.18035: ** class CSharpScanner
class CSharpScanner (BaseScanner):

    def __init__ (self,importCommands,atAuto):

        # Init the base class.
        BaseScanner.__init__(self,importCommands,atAuto=atAuto,language='c')

        # Set the parser delims.
        self.blockCommentDelim1 = '/*'
        self.blockCommentDelim2 = '*/'
        self.blockDelim1 = '{'
        self.blockDelim2 = '}'
        self.classTags = ['class','interface','namespace',]
        self.extraIdChars = ':'
        self.functionTags = []
        self.lineCommentDelim = '//'
        self.lineCommentDelim2 = None
        self.outerBlockDelim1 = '{'
        self.outerBlockDelim2 = '}'
        self.sigHeadExtraTokens = []
        self.sigFailTokens = [';','='] # Just like C.
#@-others
importer_dict = {
    'class': CSharpScanner,
    'extensions': ['.cs','.c#',],
    'name': 'C#',
}
#@-leo
