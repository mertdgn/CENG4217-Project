import subprocess 
import os 
import time
import matplotlib.pyplot as plt 
import matplotlib.pyplot as plt2
import sys
import psutil
import re
import numpy as np

def runManta():
    print("manta started")
    popen=subprocess.Popen(argsConfManta)
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
    
    popen =subprocess.Popen(argsRunManta)
    SLICE_IN_SECONDS = 0.1
    cpuPercent2, rss2, vms2, user2, system2 = 0, 0, 0, 0, 0
    while popen.poll() is None:
        time.sleep(SLICE_IN_SECONDS)
        p = psutil.Process(popen.pid)

        rssTemp = p.memory_info().rss/1024/1024
        vmsTemp = p.memory_info().vms/1024/1024
        if(rssTemp >= rss2):
            rss2=rssTemp
        if(vmsTemp >= vms2):
            vms2=vmsTemp    
         
        cpuTimes2 = (p.cpu_times().user, p.cpu_times().system)
        cpuPercentTemp = p.cpu_percent(interval=1)
        if(cpuPercentTemp >= cpuPercent2):
            cpuPercent2 = cpuPercentTemp
    memStatus2 = (rss2, vms2)                            
    popen.wait()
    memoryDict['manta']=tuple(map(sum, zip(memStatus, memStatus2)))
    cpuTimeDict['manta']=tuple(map(sum, zip(cpuTimes, cpuTimes2)))
    cpuPercentDict['manta']=cpuPercent + cpuPercent2
    print("manta finished")
    return

def runTardis():
    print("tardis started")
    popen=subprocess.Popen(argsTardis)
    
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
    memoryDict['tardis']=memStatus
    cpuTimeDict['tardis']=cpuTimes
    cpuPercentDict['tardis']=cpuPercent
    print("tardis finished")
    return

def runDelly():
    print("delly started")
    popen=subprocess.Popen(argsDelly)
  
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
    memoryDict['delly']=memStatus
    cpuTimeDict['delly']=cpuTimes
    cpuPercentDict['delly']=cpuPercent

    argsToVCF=("bcftools","view", outputName+"Delly.bcf", ">", outputName+"Delly.vcf")
    cwd = os.getcwd()
    os.chdir("./results/delly/")
    popen=subprocess.Popen(argsToVCF, stdout=subprocess.PIPE)
    popen.wait()
    os.chdir(cwd)
    
    print("delly finished")
    return

inputBam = sys.argv[1]
reference = sys.argv[2]
sonic = sys.argv[3]
outputName = sys.argv[4]
excl = "human.hg19.excl.tsv"
argsTardis = ("tardis", "--no-interdup", "--no-mei" , "-i" , inputBam, "--ref", reference, "--sonic", sonic, "--out", "IlluminaResults/tardis/"+outputName+"Tardis")
argsDelly = ("delly", "call", "-o", "IlluminaResults/delly/"+outputName+"Delly.bcf", "-g", reference, inputBam)
argsConfManta = ("configManta.py" , "--bam", inputBam, "--referenceFasta", reference, "--runDir", "IlluminaResults/manta/"+outputName+"Manta")
argsRunManta = ("IlluminaResults/manta/"+outputName+"Manta/runWorkflow.py")
timeDict={'delly':0, 'manta':0, 'tardis':0}
memoryDict = dict()
cpuPercentDict = dict()
cpuTimeDict = dict()

start = time.time()
runDelly()
end = time.time()
timeDict['delly']=end-start

start = time.time()
runTardis()
end = time.time()
timeDict['tardis']=end-start

start = time.time()
runManta()
end = time.time()
timeDict['manta']=end-start

print(timeDict)
print(memoryDict)
print(cpuPercentDict)
print(cpuTimeDict)

left = [1, 2, 3]
height = [timeDict['delly'], timeDict['manta'], timeDict['tardis']]
tick_label = ['delly', 'manta', 'tardis']
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
rss = (memoryDict['delly'][0], memoryDict['manta'][0], memoryDict['tardis'][0])
vms = (memoryDict['delly'][1], memoryDict['manta'][1], memoryDict['tardis'][1])
ind = np.arange(N)
width = 0.5 
plt.figure(2)
bars1 = plt.bar(ind, rss, width, label='RSS')
bars2 = plt.bar(ind + width, vms, width, label='VMS')
plt.ylabel('Memory Usage (MB)')
plt.title('Memory Usages of Tools')

plt.xticks(ind + width / 2, ('delly', 'manta', 'tardis',))
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
height = [float(cpuPercentDict['delly']/4), float(cpuPercentDict['manta']/4), float(cpuPercentDict['tardis']/4)]
tick_label = ['delly', 'manta', 'tardis']
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
user = (cpuTimeDict['delly'][0], cpuTimeDict['manta'][0], cpuTimeDict['tardis'][0])
system = (cpuTimeDict['delly'][1], cpuTimeDict['manta'][1], cpuTimeDict['tardis'][1])
ind = np.arange(N)
width = 0.5 
bars4 = plt.bar(ind, user, width, label='User Time')
bars5 = plt.bar(ind + width, system, width, label='System Time')
plt.ylabel('CPU Time (seconds)')
plt.title('CPU Spent Times of Tools')

plt.xticks(ind + width / 2, ('delly', 'manta', 'tardis',))
plt.legend(loc='best')
for bar in bars4:
    yval = bar.get_height()
    plt.text(bar.get_x()+0.05, 1, "%.2f" % yval + "s")
for bar in bars5:
    yval = bar.get_height()
    plt.text(bar.get_x()+0.05, 1, "%.2f" % yval + "s")
plt.show()