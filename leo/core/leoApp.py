# -*- coding: utf-8 -*-
#@+leo-ver=4-thin
#@+node:ekr.20031218072017.2608:@thin leoApp.py
#@@first

#@@language python
#@@tabwidth -4
#@@pagewidth 80

import leo.core.leoGlobals as g
import leo.core.leoPlugins as leoPlugins
import leo.core.leoVersion as leoVersion
import locale
import os
import sys
import leo.external.pickleshare

class LeoApp:

    """A class representing the Leo application itself.

    Ivars of this class are Leo's global variables."""

    #@    @+others
    #@+node:ekr.20031218072017.1416:app.__init__
    def __init__(self):

        # These ivars are the global vars of this program.
        self.afterHandler = None
        self.batchMode = False # True: run in batch mode.
        self.commandName = None # The name of the command being executed.
        self.config = None # The leoConfig instance.
        self.count = 0 # General purpose debugging count.
        self.debug = False # True: enable extra debugging tests (not used at present).
            # WARNING: this could greatly slow things down.
        self.debugSwitch = 0
            # 0: default behavior
            # 1: full traces in g.es_exception.
            # 2: call pdb.set_trace in g.es_exception, etc.
        self.defaultEncoding = 'utf-8' # set later during starup.
        ### self.tkEncoding = self.defaultEncoding ### Compatibility.
        self.disableSave = False
        self.enableUnitTest = True
        self.extensionsDir = None
        self.globalConfigDir = None # The directory that is assumed to contain the global configuration files.
        self.globalOpenDir = None # The directory last used to open a file.
        self.gui = None # The gui class.
        self.hasOpenWithMenu = False # True: open with plugin has been loaded.
        self.hookError = False # True: suppress further calls to hooks.
        self.hookFunction = None # Application wide hook function.
        self.homeDir = None # The user's home directory.
        self.homeLeoDir = None # The '.leo' subdirectory of the user's home directory. New in Leo 4.5b4.
        self.homeSettingsPrefix = '.' # prepend to "myLeoSettings.leo" and <machineName>LeoSettings.leo
        self.idle_imported = False # True: we have done an import idle
        self.idleTimeDelay = 100 # Delay in msec between calls to "idle time" hook.
        self.idleTimeHook = False # True: the global idleTimeHookHandler will reshedule itself.
        self.inBridge = False # True: running from leoBridge module.
        self.initing = True # True: we are initiing the app.
        self.killed = False # True: we are about to destroy the root window.
        self.leoID = None # The id part of gnx's.
        self.loadDir = None # The directory from which Leo was loaded.
        self.loadedPlugins = [] # List of loaded plugins that have signed on.
        self.log = None # The LeoFrame containing the present log.
        self.logInited = False # False: all log message go to logWaiting list.
        self.logIsLocked = False # True: no changes to log are allowed.
        self.logWaiting = [] # List of messages waiting to go to a log.
        self.menuWarningsGiven = False # True: supress warnings in menu code.
        self.nodeIndices = None # Singleton node indices instance.
        self.numberOfWindows = 0 # Number of opened windows.
        self.oneConfigFilename = '' # If non-empty, the name of a single configuration file.
        self.openWithFiles = [] # List of data used by Open With command.
        self.openWithFileNum = 0 # Used to generate temp file names for Open With command.
        self.openWithTable = None # The table passed to createOpenWithMenuFromTable.
        self.positions = 0 # Count of the number of positions generated.
        self.printWaiting = [] # Queue of messages to be sent to the printer.
        self.qt_use_tabs = False # True: allow tabbed main window.
        self.quitting = False # True if quitting.  Locks out some events.
        self.realMenuNameDict = {} # Contains translations of menu names and menu item names.
        self.root = None # The hidden main window. Set later.
        self.searchDict = {} # For communication between find/change scripts.
        self.scanErrors = 0 # The number of errors seen by g.scanError.
        self.scriptDict = {} # For communication between Execute Script command and scripts.
        self.silentMode = False # True if signon is more silent.
        self.statsDict = {} # Statistics dict used by g.stat, g.clear_stats, g.print_stats.
        self.trace = False # True: enable debugging traces.
        self.trace_gc = False # defined in run()
        self.trace_gc_calls = False # defined in run()
        self.trace_gc_verbose = False # defined in run()
        self.trace_gc_inited = False
        self.tracePositions = False
        self.trace_list = [] # "Sherlock" argument list for tracing().
        self.translateToUpperCase = False
        self.defaultEncoding = "utf-8"
        self.unicodeErrorGiven = True # True: suppres unicode tracebacks.
        self.unitTestDict = {} # For communication between unit tests and code.
        self.unitTesting = False # True if unit testing.
        self.useIpython = False
        self.use_psyco = False # Can't be a config param because it is used before config module can be inited.
        self.user_xresources_path = None # Resource file for Tk/tcl.
        self.windowList = [] # Global list of all frames.  Does not include hidden root window.

        # Global panels.  Destroyed when Leo ends.
        self.pythonFrame = None

        #@    << Define global constants >>
        #@+node:ekr.20031218072017.1417:<< define global constants >>
        # self.prolog_string = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"

        self.prolog_prefix_string = "<?xml version=\"1.0\" encoding="
        self.prolog_postfix_string = "?>"
        self.prolog_namespace_string = 'xmlns:leo="http://edreamleo.org/namespaces/leo-python-editor/1.1"'
        #@nonl
        #@-node:ekr.20031218072017.1417:<< define global constants >>
        #@nl
        #@    << Define global data structures >>
        #@+node:ekr.20031218072017.368:<< define global data structures >> (leoApp.py)
        # Internally, lower case is used for all language names.
        self.language_delims_dict = {
            # Keys are languages, values are 1,2 or 3-tuples of delims.
            "ada"           : "--",
            "batch"         : "REM_", # Use the REM hack.
            "actionscript"  : "// /* */", #jason 2003-07-03
            "autohotkey"    : "; /* */", #TL - AutoHotkey language
            "c"             : "// /* */", # C, C++ or objective C.
            "config"        : "#", # Leo 4.5.1
            "csharp"        : "// /* */", # C#
            "cpp"           : "// /* */",# C++.
            "css"           : "/* */", # 4/1/04
            "cweb"          : "@q@ @>", # Use the "cweb hack"
            "elisp"         : ";",
            "forth"         : "\\_ _(_ _)", # Use the "REM hack"
            "fortran"       : "C",
            "fortran90"     : "!",
            "haskell"       : "--_ {-_ _-}",
            "haxe"          : "//",
            "html"          : "<!-- -->",
            "ini"           : ";",
            "java"          : "// /* */",
            "kshell"        : "#", # Leo 4.5.1.
            "latex"         : "%",
            "lua"           : "--",  # ddm 13/02/06
            "noweb"         : "%", # EKR: 2009-01-30. Use Latex for doc chunks.
            "pascal"        : "// { }",
            "perl"          : "#",
            "perlpod"       : "# __=pod__ __=cut__", # 9/25/02: The perlpod hack.
            "php"           : "// /* */", # 6/23/07: was "//",
            "plain"         : "#", # We must pick something.
            "plsql"         : "-- /* */", # SQL scripts qt02537 2005-05-27
            "python"        : "#",
            "rapidq"        : "'", # fil 2004-march-11
            "rebol"         : ";",  # jason 2003-07-03
            "rest"          : ".._",
            "rst"           : ".._",
            "ruby"          : "#",  # thyrsus 2008-11-05
            "shell"         : "#",  # shell scripts
            "tcltk"         : "#",
            "tex"           : "%", # Bug fix: 2008-1-30: Fixed Mark Edginton's bug.
            "unknown"       : "#", # Set when @comment is seen.
            "unknown_language" : '#--unknown-language--', # For unknown extensions in @shadow files.
            "vim"           : "\"",
            "vimoutline"    : "#",  #TL 8/25/08 Vim's outline plugin
            "xml"           : "<!-- -->",
            "xslt"          : "<!-- -->",
        }

        self.language_extension_dict = {
            # Keys are languages, values are extensions.
            "ada"           : "ada",
            "actionscript"  : "as", #jason 2003-07-03
            "autohotkey"    : "ahk", #TL - AutoHotkey language
            "batch"         : "bat", # Leo 4.5.1.
            "c"             : "c",
            "config"        : "cfg",
            "cpp"           : "cpp",
            "css"           : "css", # 4/1/04
            "cweb"          : "w",
            "elisp"         : "el",
            "forth"         : "forth",
            "fortran"       : "f",
            "fortran90"     : "f90",
            "haskell"       : "hs",
            "haxe"          : "hx",
            "html"          : "html",
            "ini"           : "ini",
            "java"          : "java",
            "kshell"        : "ksh", # Leo 4.5.1.
            "latex"         : "tex", # 1/8/04
            "lua"           : "lua",  # ddm 13/02/06
            "noweb"         : "nw",
            "pascal"        : "p",
            "perl"          : "pl",      # 11/7/05
            "perlpod"       : "pod",  # 11/7/05
            "php"           : "php",
            "plain"         : "txt",
            "python"        : "py",
            "plsql"         : "sql", # qt02537 2005-05-27
            "rapidq"        : "bas", # fil 2004-march-11
            "rebol"         : "r",    # jason 2003-07-03
            # "rst"           : "rst", # caught by pylint.
            "rst"           : "rest",
            "ruby"          : "rb",   # thyrsus 2008-11-05
            "shell"         : "sh",   # DS 4/1/04
            "tex"           : "tex",
            "tcltk"         : "tcl",
            "unknown"       : "txt", # Set when @comment is seen.
            "vim"           : "vim",
            "vimoutline"    : "otl",  #TL 8/25/08 Vim's outline plugin
            "xml"           : "xml",
            "xslt"          : "xsl",
        }

        self.extension_dict = {
            # Keys are extensions, values are languages.
            "ada"   : "ada",
            "adb"   : "ada",
            "ahk"   : "autohotkey",  # EKR: 2009-01-30.
            "as"    : "actionscript",
            "bas"   : "rapidq",
            "bat"   : "batch",
            "c"     : "c",
            "cfg"   : "config",
            "cpp"   : "cpp",
            "css"   : "css",
            "el"    : "elisp",
            "forth" : "forth",
            "f"     : "fortran",
            "f90"   : "fortran90",
            "h"     : "c",
            "html"  : "html",
            "hs"    : "haskell",
            "ini"   : "ini",
            "java"  : "java",
            "ksh"   : "kshell", # Leo 4.5.1.
            "lua"   : "lua",  # ddm 13/02/06
            "nw"    : "noweb",
            "otl"   : "vimoutline",  #TL 8/25/08 Vim's outline plugin
            "p"     : "pascal",
            "pl"    : "perl",   # 11/7/05
            "pod"   : "perlpod", # 11/7/05
            "php"   : "php",
            "py"    : "python",
            "sql"   : "plsql", # qt02537 2005-05-27
            "r"     : "rebol",
            "rb"    : "ruby", # thyrsus 2008-11-05
            "rest"  : "rst",
            "rst"   : "rst",
            "sh"    : "shell",
            "tex"   : "tex",
            "txt"   : "plain",
            "tcl"   : "tcltk",
            "vim"   : "vim",
            "w"     : "cweb",
            "xml"   : "xml",
            "xsl"   : "xslt",
            "hx"    : "haxe",
        }

        # Extra language extensions, used to associate extensions with mode files.
        # Used by importCommands.languageForExtension.
        # Keys are extensions, values are corresponding mode file (without .py)
        # A value of 'none' is a signal to unit tests that no extension file exists.
        self.extra_extension_dict = {
            'actionscript': 'actionscript',
            'ada'   : 'ada95',
            'adb'   : 'none', # ada??
            'awk'   : 'awk',
            'bas'   : 'none', # rapidq
            'bat'   : 'none', # batch
            'cfg'   : 'none', # Leo 4.5.1
            'cpp'   : 'c',
            'el'    : 'lisp',
            'f'     : 'fortran90',
            'hx'    : 'none',
            'ksh'   : 'none', # Leo 4.5.1
            'nw'    : 'none', # noweb.
            'otl'   : 'none', # vimoutline.
            'pod'   : 'perl',
            'tcl'   : 'tcl',
            'unknown_language': 'none',
            'w'     : 'none', # cweb
        }

        self.global_commands_dict = {}
        #@-node:ekr.20031218072017.368:<< define global data structures >> (leoApp.py)
        #@nl
    #@-node:ekr.20031218072017.1416:app.__init__
    #@+node:ekr.20031218072017.2609:app.closeLeoWindow
    def closeLeoWindow (self,frame):

        """Attempt to close a Leo window.

        Return False if the user veto's the close."""

        c = frame.c

        # g.trace('frame',frame,g.callers(4))

        c.endEditing() # Commit any open edits.

        if c.promptingForClose:
            # There is already a dialog open asking what to do.
            return False

        g.app.config.writeRecentFilesFile(c) # Make sure .leoRecentFiles.txt is written.

        if c.changed:
            c.promptingForClose = True
            veto = frame.promptForSave()
            c.promptingForClose = False
            if veto: return False

        g.app.setLog(None) # no log until we reactive a window.

        g.doHook("close-frame",c=c) # This may remove frame from the window list.

        if frame in g.app.windowList:
            g.app.destroyWindow(frame)

        if g.app.windowList:
            # Pick a window to activate so we can set the log.
            frame = g.app.windowList[0]
            frame.deiconify()
            frame.lift()
            frame.c.setLog()
            frame.c.bodyWantsFocus()
            frame.c.outerUpdate()
        elif not g.app.unitTesting:
            g.app.finishQuit()

        return True # The window has been closed.
    #@-node:ekr.20031218072017.2609:app.closeLeoWindow
    #@+node:ekr.20090202191501.5:app.createNullGui
    def createNullGui (self):

        # Don't import this at the top level:
        # it might interfere with Leo's startup logic.
        import leo.core.leoGui as leoGui

        g.app.gui = leoGui.nullGui("nullGui")
    #@nonl
    #@-node:ekr.20090202191501.5:app.createNullGui
    #@+node:ekr.20090619065122.8593:app.createDefaultGui
    def createDefaultGui (self,fileName='',verbose=False):

        """A convenience routines for plugins to create the default gui class."""

        have_qt = False
        try:
            import PyQt4.QtGui                
            have_qt = True
        except ImportError:
            print("PyQt not installed - reverting to Tk UI")        

        if have_qt:        
            self.createQtGui(fileName, verbose=verbose)
        else:
            self.createTkGui(fileName, verbose = verbose)
    #@-node:ekr.20090619065122.8593:app.createDefaultGui
    #@+node:ekr.20090202191501.1:app.createQtGui
    def createQtGui (self,fileName='',verbose=False):

        # Do NOT omit fileName param: it is used in plugin code.

        """A convenience routines for plugins to create the Qt gui class."""

        import leo.plugins.qtGui
        leo.plugins.qtGui.init()

        #leoPlugins.loadOnePlugin ('qtGui',verbose=verbose)

        if fileName and verbose: print('qtGui created in %s' % fileName)
    #@-node:ekr.20090202191501.1:app.createQtGui
    #@+node:ekr.20031218072017.2610:app.createTkGui
    def createTkGui (self,fileName='',verbose=False):

        """A convenience routines for plugins to create the default Tk gui class."""

        leoPlugins.loadOnePlugin ('tkGui',verbose=verbose)

        if fileName and verbose: print('tkGui created in %s' % fileName)
    #@-node:ekr.20031218072017.2610:app.createTkGui
    #@+node:ekr.20090126063121.3:app.createWxGui
    def createWxGui (self,fileName='',verbose=False):

        # Do NOT omit fileName param: it is used in plugin code.

        """A convenience routines for plugins to create the wx gui class."""

        leoPlugins.loadOnePlugin ('wxGui',verbose=verbose)

        if fileName and verbose: print('wxGui created in %s' % fileName)
    #@-node:ekr.20090126063121.3:app.createWxGui
    #@+node:ekr.20031218072017.2612:app.destroyAllOpenWithFiles
    def destroyAllOpenWithFiles (self):

        """Try to remove temp files created with the Open With command.

        This may fail if the files are still open."""

        # We can't use g.es here because the log stream no longer exists.

        for theDict in self.openWithFiles[:]: # 7/10/03.
            g.app.destroyOpenWithFileWithDict(theDict)

        # Delete the list so the gc can recycle Leo windows!
        g.app.openWithFiles = []
    #@-node:ekr.20031218072017.2612:app.destroyAllOpenWithFiles
    #@+node:ekr.20031218072017.2613:app.destroyOpenWithFilesForFrame
    def destroyOpenWithFilesForFrame (self,frame):

        """Close all "Open With" files associated with frame"""

        # Make a copy of the list: it may change in the loop.
        openWithFiles = g.app.openWithFiles

        for theDict in openWithFiles[:]: # 6/30/03
            c = theDict.get("c")
            if c.frame == frame:
                g.app.destroyOpenWithFileWithDict(theDict)
    #@-node:ekr.20031218072017.2613:app.destroyOpenWithFilesForFrame
    #@+node:ekr.20031218072017.2614:app.destroyOpenWithFileWithDict
    def destroyOpenWithFileWithDict (self,theDict):

        path = theDict.get("path")
        if path and g.os_path_exists(path):
            try:
                os.remove(path)
                g.pr("deleting temp file: %s" % g.shortFileName(path))
            except:
                g.pr("can not delete temp file: %s" % path)

        # Remove theDict from the list so the gc can recycle the Leo window!
        g.app.openWithFiles.remove(theDict)
    #@-node:ekr.20031218072017.2614:app.destroyOpenWithFileWithDict
    #@+node:ekr.20031218072017.2615:app.destroyWindow
    def destroyWindow (self,frame):

        # g.trace(frame in g.app.windowList,frame)
        g.app.destroyOpenWithFilesForFrame(frame)

        if frame in g.app.windowList:
            # g.trace(g.app.windowList)
            g.app.windowList.remove(frame)

        # force the window to go away now.
        # Important: this also destroys all the objects of the commander.
        frame.destroySelf()
    #@-node:ekr.20031218072017.2615:app.destroyWindow
    #@+node:ekr.20031218072017.1732:app.finishQuit
    def finishQuit(self):

        # forceShutdown may already have fired the "end1" hook.
        if not g.app.killed:
            g.doHook("end1")

        self.destroyAllOpenWithFiles()

        if g.app.gui:
            g.app.gui.destroySelf()

        # Don't use g.trace!
        # print('app.finishQuit: setting g.app.killed',g.callers())

        g.app.killed = True
            # Disable all further hooks and events.
            # Alas, "idle" events can still be called even after the following code.

        if g.app.afterHandler:
            # TK bug: This appears to have no effect, at least on Windows.
            # print("finishQuit: cancelling",g.app.afterHandler)
            if g.app.gui and g.app.gui.guiName() == "tkinter":
                self.root.after_cancel(g.app.afterHandler)
            g.app.afterHandler = None
    #@-node:ekr.20031218072017.1732:app.finishQuit
    #@+node:ekr.20031218072017.2616:app.forceShutdown
    def forceShutdown (self):

        """Forces an immediate shutdown of Leo at any time.

        In particular, may be called from plugins during startup."""

        # Wait until everything is quiet before really quitting.
        g.doHook("end1")

        self.log = None # Disable writeWaitingLog
        self.killed = True # Disable all further hooks.

        for w in self.windowList[:]:
            self.destroyWindow(w)

        self.finishQuit()
    #@-node:ekr.20031218072017.2616:app.forceShutdown
    #@+node:ekr.20031218072017.2188:app.newLeoCommanderAndFrame
    def newLeoCommanderAndFrame(self,
        fileName=None,
        relativeFileName=None,
        gui=None,initEditCommanders=True,updateRecentFiles=True):

        """Create a commander and its view frame for the Leo main window."""

        app = self

        import leo.core.leoCommands as leoCommands

        if not fileName: fileName = ''
        if not relativeFileName: relativeFileName = ''
        if not gui: gui = g.app.gui
        #@    << compute the window title >>
        #@+node:ekr.20031218072017.2189:<< compute the window title >>
        # Set the window title and fileName
        if fileName:
            title = g.computeWindowTitle(fileName)
        else:
            s = "untitled"
            n = g.app.numberOfWindows
            if n > 0:
                s += str(n)
            title = g.computeWindowTitle(s)
            g.app.numberOfWindows = n+1
        #@-node:ekr.20031218072017.2189:<< compute the window title >>
        #@nl

        # g.trace(fileName,relativeFileName)

        # Create an unfinished frame to pass to the commanders.
        frame = gui.createLeoFrame(title)

        # Create the commander and its subcommanders.
        # This takes about 3/4 sec when called by the leoBridge module.
        c = leoCommands.Commands(frame,fileName,relativeFileName=relativeFileName)

        if not app.initing:
            g.doHook("before-create-leo-frame",c=c) # Was 'onCreate': too confusing.

        frame.finishCreate(c)
        c.finishCreate(initEditCommanders)

        # Finish initing the subcommanders.
        c.undoer.clearUndoState() # Menus must exist at this point.

        return c,frame
    #@-node:ekr.20031218072017.2188:app.newLeoCommanderAndFrame
    #@+node:ekr.20031218072017.2617:app.onQuit
    def onQuit (self,event=None):

        '''Exit Leo, prompting to save unsaved outlines first.'''

        g.app.quitting = True
        # g.trace('True')

        while g.app.windowList:
            w = g.app.windowList[0]
            if not g.app.closeLeoWindow(w):
                break

        if g.app.windowList:
            g.app.quitting = False # If we get here the quit has been disabled.
    #@-node:ekr.20031218072017.2617:app.onQuit
    #@+node:ekr.20031218072017.2618:app.setEncoding
    # According to Martin v. Löwis, getdefaultlocale() cannot be fixed.
    # We use getpreferredencoding() instead.

    def setEncoding (self):

        """Set g.app.defaultEncoding."""

        app = self
        locale_encoding = locale.getpreferredencoding()

        try: sys_encoding = sys.getdefaultencoding()
        except Exception: sys_encoding = None

        # g.trace('locale:',locale_encoding,'sys',sys_encoding)

        for (encoding,src) in (
            (app.config.defaultEncoding,"config"),
            (locale_encoding,"locale"),
            (sys_encoding,"sys"),
            ("utf-8","default")):

            if g.isValidEncoding (encoding):
                app.defaultEncoding = encoding
                g.es('default encoding:',encoding,color='orange')
                # g.trace(app.defaultEncoding,src)
                break
            elif encoding:
                color = g.choose(app.defaultEncoding=="ascii","red","blue")
                g.trace("ignoring invalid %s encoding: %s" % (src,encoding),color=color)
    #@-node:ekr.20031218072017.2618:app.setEncoding
    #@+node:ekr.20031218072017.1978:app.setLeoID
    def setLeoID (self,verbose=True):

        tag = ".leoID.txt"
        homeLeoDir = g.app.homeLeoDir # was homeDir.
        globalConfigDir = g.app.globalConfigDir
        loadDir = g.app.loadDir

        verbose = not g.app.unitTesting
        #@    << return if we can set leoID from sys.leoID >>
        #@+node:ekr.20031218072017.1979:<< return if we can set leoID from sys.leoID>>
        # This would be set by in Python's sitecustomize.py file.

        # Use hasattr & getattr to suppress pylint warning.
        # We also have to use a "non-constant" attribute to suppress another warning!

        nonConstantAttr = "leoID"

        if hasattr(sys,nonConstantAttr):
            g.app.leoID = getattr(sys,nonConstantAttr)
            if verbose and not g.app.silentMode and not g.app.unitTesting:
                g.es_print("leoID=",g.app.leoID,spaces=False,color='red')
            # Bug fix: 2008/3/15: periods in the id field of a gnx will corrupt the .leo file!
            g.app.leoID = g.app.leoID.replace('.','-')
            return
        else:
            g.app.leoID = None
        #@-node:ekr.20031218072017.1979:<< return if we can set leoID from sys.leoID>>
        #@nl
        #@    << return if we can set leoID from "leoID.txt" >>
        #@+node:ekr.20031218072017.1980:<< return if we can set leoID from "leoID.txt" >>
        for theDir in (homeLeoDir,globalConfigDir,loadDir):
            # N.B. We would use the _working_ directory if theDir is None!
            if theDir:
                try:
                    fn = g.os_path_join(theDir,tag)
                    f = open(fn,'r')
                    s = f.readline()
                    f.close()
                    if s and len(s) > 0:
                        g.app.leoID = s.strip()
                        # Bug fix: 2008/3/15: periods in the id field of a gnx will corrupt the .leo file!
                        g.app.leoID = g.app.leoID.replace('.','-')
                        if verbose and not g.app.silentMode and not g.app.unitTesting:
                            g.es('leoID=',g.app.leoID,' (in ',theDir,')',
                                spaces=False,color="red")
                        return
                    elif verbose and not g.app.unitTesting:
                        g.es('empty ',tag,' (in ',theDir,')',spaces=False,color = "red")
                except IOError:
                    g.app.leoID = None
                except Exception:
                    g.app.leoID = None
                    g.es_print('unexpected exception in app.setLeoID',color='red')
                    g.es_exception()
        #@-node:ekr.20031218072017.1980:<< return if we can set leoID from "leoID.txt" >>
        #@nl
        #@    << return if we can set leoID from os.getenv('USER') >>
        #@+node:ekr.20060211140947.1:<< return if we can set leoID from os.getenv('USER') >>
        try:
            theId = os.getenv('USER')
            if theId:
                if verbose and not g.app.unitTesting:
                    g.es("setting leoID from os.getenv('USER'):",repr(theId),color='blue')
                g.app.leoID = theId
                # Bug fix: 2008/3/15: periods in the id field of a gnx will corrupt the .leo file!
                g.app.leoID = g.app.leoID.replace('.','-')
                return

        except Exception:
            pass
        #@-node:ekr.20060211140947.1:<< return if we can set leoID from os.getenv('USER') >>
        #@nl
        #@    << put up a dialog requiring a valid id >>
        #@+node:ekr.20031218072017.1981:<< put up a dialog requiring a valid id >>
        # New in 4.1: get an id for gnx's.  Plugins may set g.app.leoID.

        # Create an emergency gui and a Tk root window.
        g.app.createTkGui("startup")

        if g.app.gui is None:
            # tkinter broken/doesn't exist. Print error
            print("Please enter LeoID (e.g. your username, 'johndoe'...)")
            leoid = raw_input('LeoID: ')

        else:
            leoid = g.app.gui.runAskLeoIDDialog()

        # Bug fix: 2/6/05: put result in g.app.leoID.
        g.app.leoID = leoid

        # Bug fix: 2008/3/15: periods in the id field of a gnx will corrupt the .leo file!
        g.app.leoID = g.app.leoID.replace('.','-')

        # g.trace(g.app.leoID)
        g.es('leoID=',repr(g.app.leoID),spaces=False,color="blue")
        #@-node:ekr.20031218072017.1981:<< put up a dialog requiring a valid id >>
        #@nl
        #@    << attempt to create leoID.txt >>
        #@+node:ekr.20031218072017.1982:<< attempt to create leoID.txt >>
        for theDir in (homeLeoDir,globalConfigDir,loadDir):
            # N.B. We would use the _working_ directory if theDir is None!
            if theDir:
                try:
                    fn = g.os_path_join(theDir,tag)
                    f = open(fn,'w')
                    f.write(g.app.leoID)
                    f.close()
                    if g.os_path_exists(fn):
                        g.es_print('',tag,'created in',theDir,color='red')
                        return
                except IOError:
                    pass

                g.es('can not create',tag,'in',theDir,color='red')
        #@-node:ekr.20031218072017.1982:<< attempt to create leoID.txt >>
        #@nl
    #@-node:ekr.20031218072017.1978:app.setLeoID
    #@+node:ville.20090620122043.6275:app.setGlobalDb
    def setGlobalDb(self):
        """ Create global pickleshare db

        Usable by::

            g.app.db['hello'] = [1,2,5]

        """

        trace = False
        if trace: g.trace('g.enableDB',g.enableDB)

        if g.enableDB:
            dbdirname = self.homeLeoDir + "/db/global"
            self.db = leo.external.pickleshare.PickleShareDB(dbdirname, protocol='picklez')
            if trace: g.trace(self.db,dbdirname)
        else:
            self.db = {}
    #@-node:ville.20090620122043.6275:app.setGlobalDb
    #@+node:ekr.20031218072017.1847:app.setLog, lockLog, unlocklog
    def setLog (self,log):

        """set the frame to which log messages will go"""

        # print("setLog:",tag,"locked:",self.logIsLocked,log)
        if not self.logIsLocked:
            self.log = log

    def lockLog(self):
        """Disable changes to the log"""
        self.logIsLocked = True

    def unlockLog(self):
        """Enable changes to the log"""
        self.logIsLocked = False
    #@-node:ekr.20031218072017.1847:app.setLog, lockLog, unlocklog
    #@+node:ekr.20090717112235.6007:app.computeSignon
    def computeSignon (self):

        app = self
        build,date  = leoVersion.build,leoVersion.date
        guiVersion  = app.gui.getFullVersion()
        leoVer      = leoVersion.version
        n1,n2,n3,junk,junk=sys.version_info

        if sys.platform.startswith('win'):
            sysVersion = 'Windows '
            try:
                v = os.sys.getwindowsversion()
                sysVersion += ', '.join([str(z) for z in v])
            except Exception:
                pass

        else: sysVersion = sys.platform

        app.signon = 'Leo %s, build %s, %s' % (
            leoVer,build,date)
        app.signon2 = 'Python %s.%s.%s, %s\n%s' % (
            n1,n2,n3,guiVersion,sysVersion)
    #@nonl
    #@-node:ekr.20090717112235.6007:app.computeSignon
    #@+node:ekr.20031218072017.2619:app.writeWaitingLog
    def writeWaitingLog (self,c,forceLog=False):

        app = self
        # Do not call g.es, g.es_print, g.pr or g.trace here!
        # print('writeWaitingLog',c,g.callers(4))
        table = [
            ('Leo Log Window','red'),
            (app.signon,'black'),
            (app.signon2,'black'),
        ]
        table.reverse()

        if app.log:
            if not app.logInited:
                app.logInited = True # Prevent recursive call.
                print(app.signon)
                print(app.signon2)
                for s,color in table:
                    app.logWaiting.insert(0,(s+'\n',color),)
            elif forceLog:
                for s,color in table:
                    app.logWaiting.insert(0,(s+'\n',color),)
            # The test for isNull would probably interfere with batch mode.
            for s in app.printWaiting:
                print(s)
            app.printWaiting = []
            for s,color in app.logWaiting:
                g.es('',s,color=color,newline=0)
                    # The caller must write the newlines.
            app.logWaiting = []
        else:
            print('writeWaitingLog: still no log!')
    #@-node:ekr.20031218072017.2619:app.writeWaitingLog
    #@+node:ville.20090602181814.6219:app.commanders
    def commanders(self):
        """ Return list of currently active controllers """

        return [f.c for f in g.app.windowList]    
    #@-node:ville.20090602181814.6219:app.commanders
    #@-others
#@-node:ekr.20031218072017.2608:@thin leoApp.py
#@-leo
