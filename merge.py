print("IncreFile version 1.1")
import os,sys
import hashlib
from shutil import move

if not os.path.exists("destination"):
    os.mkdir("destination")
if not os.path.exists("shalist.txt"): open("shalist.txt","w").close()

fshalist=open("shalist.txt","r+")
shalist=set(fshalist.read().split("\n"))
def fsha1(filepath):
    with open(filepath,'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        return hash

dest=sys.argv[1]
print("增量文件位置: "+dest)
filelist=os.listdir(dest)
fileindex=0
filecount=len(filelist)
newfilecount=0
for file in filelist:
    fileindex+=1
    prog=str("%.2f"%(fileindex/filecount*100))+"%(第"+str(fileindex)+"/"+str(filecount)+"个): "
    path=os.path.join(dest+"/",file)
    if os.path.isfile(path):
        print("\r"+prog+"正在分析文件 "+file+"   ",end="")
        sha=fsha1(path)
        repeatFlag=False
        for d in shalist:
            if sha == d.split(" ")[0]:
                repeatFlag=True
        if not repeatFlag:
            print("\r"+prog+"新文件 "+file+" sha1="+sha+", 正在移动")
            newfilecount+=1
            shalist.add(sha+" "+file)
            if not os.path.exists("./destination/"+file):
                move(path,"./destination/"+file)
            else:
                frename="./destination/"+sha+"-"+file
                print(" - 重名的文件 "+file+" 已重命名为 "+sha+"-"+file)
                move(path,frename)
            fshalist.seek(0)
            fshalist.write('\n'.join(list(shalist)))
            
print("\n已处理完成。新增文件"+str(newfilecount)+"个")