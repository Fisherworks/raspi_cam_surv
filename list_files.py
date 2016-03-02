import os

def listFiles(path):
    fileStr = []
    for root, dirs, files in os.walk( path ):
        #print 'root', root
        #print 'dirs', dirs
        #print 'files', files
        if root == path:
            for fn in sorted(files, reverse=True):
                fileStr.append(fn)
        else:
            pass
    return fileStr

def main():
    print listFiles('/home/pi/git_proj/flask/static')

if __name__ == "__main__":
    main()
