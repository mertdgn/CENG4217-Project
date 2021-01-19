import subprocess 
import os 
import time
import matplotlib.pyplot as plt 
import sys
import psutil
import re
import numpy as np

def runSVIM():
    print("svim started")
    popen=subprocess.Popen(argsSVIM)
    SLICE_IN_SECONDS = 0.1
    cpuPercent, rss, vms, user, system = 0, 0, 0, 0, 0    
    while popen.poll() is None:
        time.sleep(SLICE_IN_SECONDS)
        p = psutil.Process(popen.pid)
        rssTemp = p.memory_info().rss/1024/1024
        vmsTemp = p.memory_info().vms/1024/1024
        if(rssTemp >= rss):
            rss=rssTemp
        if(vmsTemp >= vms):
            vms=vmsTemp    
        
        cpuTimes = (p.cpu_times().user, p.cpu_times().system)
    
        cpuPercentTemp = p.cpu_percent(interval=1)
        if(cpuPercentTemp >= cpuPercent):
            cpuPercent = cpuPercentTemp
    memStatus = (rss, vms)
    popen.wait()

    memoryDict['svim']=memStatus
    cpuTimeDict['svim']=cpuTimes
    cpuPercentDict['svim']=cpuPercent
    print("svim finished")
    return

def runSniffles():
    print("Sniffles started")
    popen=subprocess.Popen(argsSniffles)
    
    SLICE_IN_SECONDS = 0.1
    cpuPercent, rss, vms, user, system = 0, 0, 0, 0, 0
    while popen.poll() is None:
        time.sleep(SLICE_IN_SECONDS)
        p = psutil.Process(popen.pid)
        
        rssTemp = p.memory_info().rss/1024/1024
        vmsTemp = p.memory_info().vms/1024/1024
        if(rssTemp >= rss):
            rss=rssTemp
        if(vmsTemp >= vms):
            vms=vmsTemp  
        
        cpuTimes = (p.cpu_times().user, p.cpu_times().system)
        cpuPercentTemp = p.cpu_percent(interval=1)
        if(cpuPercentTemp >= cpuPercent):
            cpuPercent = cpuPercentTemp
    memStatus = (rss, vms)
    popen.wait()
    memoryDict['sniffles']=memStatus
    cpuTimeDict['sniffles']=cpuTimes
    cpuPercentDict['sniffles']=cpuPercent
    popen=subprocess.Popen(("mv", outputName+"Sniffles.vcf", "./NanoporeResults/sniffles/"), stdout=subprocess.PIPE)
    
    print("Sniffles finished")
    return

def runCuteSV():
    print("cuteSV started")
    popen=subprocess.Popen(argsCuteSV)   
    SLICE_IN_SECONDS = 0.1
    cpuPercent, rss, vms, user, system = 0, 0, 0, 0, 0
    while popen.poll() is None:
        time.sleep(SLICE_IN_SECONDS)
        p = psutil.Process(popen.pid)
        
        rssTemp = p.memory_info().rss/1024/1024
        vmsTemp = p.memory_info().vms/1024/1024
        if(rssTemp >= rss):
            rss=rssTemp
        if(vmsTemp >= vms):
            vms=vmsTemp  

        cpuTimes = (p.cpu_times().user, p.cpu_times().system)
        cpuPercentTemp = p.cpu_percent(interval=1)
        if(cpuPercentTemp >= cpuPercent):
            cpuPercent = cpuPercentTemp        
    memStatus = (rss, vms) 
    popen.wait()
    memoryDict['cuteSV']=memStatus
    cpuTimeDict['cuteSV']=cpuTimes
    cpuPercentDict['cuteSV']=cpuPercent
    popen=subprocess.Popen(("mv", outputName+"CuteSV.vcf", "./NanoporeResults/cutesv/"), stdout=subprocess.PIPE)
    print("cuteSV finished")
    return


inputBam = sys.argv[1]
reference = sys.argv[2]
outputName = sys.argv[3]

argsSVIM=("svim", "alignment", "NanoporeResults/svim/"+outputName+"SVIM", inputBam, reference)
argsSniffles=("sniffles", "-m", inputBam, "-v", outputName+"Sniffles.vcf")
argsCuteSV=("cuteSV", inputBam, reference, outputName+"CuteSV.vcf", "./NanoporeResults/cutesv/")
timeDict={'svim':0, 'sniffles':0, 'cuteSV':0}
memoryDict = dict()
cpuPercentDict = dict()
cpuTimeDict = dict()

start = time.time()
runSVIM()
end = time.time()
timeDict['svim']=end-start

start = time.time()
runSniffles()
end = time.time()
timeDict['sniffles']=end-start

start = time.time()
runCuteSV()
end = time.time()
timeDict['cuteSV']=end-start

print(timeDict)
print(memoryDict)
print(cpuPercentDict)
print(cpuTimeDict)

left = [1, 2, 3]
height = [timeDict['cuteSV'], timeDict['sniffles'], timeDict['svim']]
tick_label = ['cuteSV', 'sniffles', 'svim']
plt.figure(1)
bars = plt.bar(left, height, tick_label = tick_label, 
        width = 0.8, color = ['red', 'green', 'mediumturquoise']) 
plt.ylabel('time elapsed (seconds)') 
plt.title('Run Times of Tools')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x()+0.2, 1, "%.2f" % yval + "s")
plt.show()


N = 3
rss = (memoryDict['cuteSV'][0], memoryDict['sniffles'][0], memoryDict['svim'][0])
vms = (memoryDict['cuteSV'][1], memoryDict['sniffles'][1], memoryDict['svim'][1])
ind = np.arange(N)
width = 0.5 
plt.figure(2)
bars1 = plt.bar(ind, rss, width, label='RSS')
bars2 = plt.bar(ind + width, vms, width, label='VMS')
plt.ylabel('Memory Usage (MB)')
plt.title('Memory Usages of Tools')

plt.xticks(ind + width / 2, ('cuteSV', 'sniffles', 'svim',))
plt.legend(loc='best')
for bar in bars1:
    yval = bar.get_height()
    plt.text(bar.get_x(), 1, "%.2f" % yval + "MB")
for bar in bars2:
    yval = bar.get_height()
    plt.text(bar.get_x(), 1, "%.2f" % yval + "MB")
plt.show()

plt.figure(3)
left = [1, 2, 3]
height = [float(cpuPercentDict['cuteSV']/4), float(cpuPercentDict['sniffles']/4), float(cpuPercentDict['svim']/4)]
tick_label = ['cuteSV', 'sniffles', 'svim']
bars3 = plt.bar(left, height, tick_label = tick_label, 
        width = 0.8, color = ['red', 'green', 'mediumturquoise']) 
plt.ylabel('CPU usage %') 
plt.title('Percentage of CPU Usages')
for bar in bars3:
    yval = bar.get_height()
    plt.text(bar.get_x()+0.2, 1, "%.2f" % yval + "%")
plt.show()

plt.figure(4)
N = 3
user = (cpuTimeDict['cuteSV'][0], cpuTimeDict['sniffles'][0], cpuTimeDict['svim'][0])
system = (cpuTimeDict['cuteSV'][1], cpuTimeDict['sniffles'][1], cpuTimeDict['svim'][1])
ind = np.arange(N)
width = 0.5 
bars4 = plt.bar(ind, user, width, label='User Time')
bars5 = plt.bar(ind + width, system, width, label='System Time')
plt.ylabel('CPU Time (seconds)')
plt.title('CPU Spent Times of Tools')

plt.xticks(ind + width / 2, ('cuteSV', 'sniffles', 'svim',))
plt.legend(loc='best')
for bar in bars4:
    yval = bar.get_height()
    plt.text(bar.get_x()+0.05, 1, "%.2f" % yval + "s")
for bar in bars5:
    yval = bar.get_height()
    plt.text(bar.get_x()+0.05, 1, "%.2f" % yval + "s")
plt.show()
