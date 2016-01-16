import os

def listFiles(path):
    fileStr = []
    for root, dirs, files in os.walk( path ):
        for fn in files:
            fileStr.append(fn)
    return fileStr

def main():
    print listFiles('/home/pi/git_proj/flask/static')

if __name__ == "__main__":
    main()
