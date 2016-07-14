import glob, os, sys, getopt, shutil

class Compiler():

    targetPath      = None
    compiledPath    = None

    def __init__(self, argv):
        if self.input(argv) == True:
            self.compile()
        else:
            print "Fatal error."

    def compile(self):

        os.chdir(self.targetPath)
        for file in glob.glob("*.py"):
            if os.system('python -m py_compile '+ file) == 0:
                print file +' compiled.'

        if len(glob.glob("*.py")) < 1:
            print "No .py file found in target path."
            os.system('PAUSE')
            sys.exit()

        for compiledFile in glob.glob("*.pyc"):
            try:
                shutil.move('./' + compiledFile, self.compiledPath +'/'+ compiledFile)
                print "moving compiled " + compiledFile + ' to ./compiled/'
            except Exception as e:
                print str(e)

    def input(self, argv):
        targetPath      = None
        compiledPath    = None

        try:
            opts, args = getopt.getopt(argv, "hi:o:", ["help=", "usage=", "targetPath=", "compiledPath="])
        except getopt.GetoptError:
            print 'compiler.py -i <targetPath> -o <compiledPath>'
            os.system('PAUSE')
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--help", "--usage"):
                print 'compiler.py -i <targetPath> -o <compiledPath>'
                sys.exit()
            elif opt in ("-i", "--targetPath"):
                targetPath = arg
            elif opt in ("-o", "--compiledPath"):
                compiledPath = arg

        if targetPath == None:
            print "Assuming default target path. For custom paths type compiler.py --usage"
            targetPath = './'
        if compiledPath == None:
            print "Assuming default compiled path. For custom paths type compiler.py --usage"
            compiledPath = './compiled'

        return self.pathsExists(targetPath, compiledPath)


    def pathsExists(self, tPath, cPath):

        if tPath == None or os.path.isdir(tPath) != True:
            print "Target path is not a valid path."
            os.system('PAUSE')
            sys.exit(1)

        if cPath == None or os.path.isdir(cPath) != True:
            if os.mkdir(cPath) == False:
                print "Unable to create compiled directory"
                os.system('PAUSE')
                sys.exit(1)
            else:
                print cPath +" directory created."

        self.targetPath     = tPath
        self.compiledPath   = cPath
        return True

Compiler(sys.argv[1:])
os.system('PAUSE')