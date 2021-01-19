import subprocess 
import os 

os.system('ls *vcf > all_vcf.txt')

vcfs = open("all_vcf.txt", "r")
result = open("results.txt", "wb")

for name in vcfs:
    vcfName=name.strip('\n')
    argsStats=("SURVIVOR", "stats", vcfName, "-1", "-1", "-1", "stat"+vcfName.replace(".vcf",""))
    popen = subprocess.Popen(argsStats, stdout=subprocess.PIPE)
    text=popen.communicate()[0]
    popen.wait
    result.write((vcfName+":\n").encode())
    result.write(text)
    result.write("\n".encode())

os.system('rm stat*')
