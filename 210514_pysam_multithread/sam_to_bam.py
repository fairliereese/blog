import pysam
import time
import seaborn as sns
import pandas as pd
import hashlib
import matplotlib.pyplot as plt


sam = 'c2c12_500k.sam'

def benchmark_write(samfile, threads):
    bamfile = samfile[:-4]+'.bam'
    infile = pysam.AlignmentFile(samfile, 'r', threads=threads)
    outfile = pysam.AlignmentFile(bamfile, mode='wb',
                                    template=infile, threads=threads)
    for s in infile:
        outfile.write(s)
        
df = pd.DataFrame(data=[i for i in range(1,17)], columns=['threads'])

for i in range(10):
    times = []
    
    for j in range(1,17):
        start = time.time()
        benchmark_write(sam, j)
        times.append(time.time()-start)
    df[i] = times
    
df = df.melt(id_vars='threads', value_vars=[i for i in range(10)])
df.rename({'value':'time (seconds)'}, axis=1, inplace=True)
sns.lineplot(data=df, x='threads', y='time (seconds)')
plt.savefig('pysam_multithread.png')

# sort to ensure sequences are in the same order
# convert to sam without the headers
pref = samfile[:-4]

# control - made with `samtools view -Sb sam > bam`
infile = pref+'.bam'
ofile = pref+'_sorted.bam'
pysam.sort('-o', ofile, infile)
ofile_sam = pref+'_sorted.sam'
pysam.view('-o', ofile_sam, ofile, save_stdout=ofile_sam)

# pysam multithreaded bam we just wrote
infile = pref+'_pysam.bam'
ofile = pref+'_pysam_sorted.bam'
pysam.sort('-o', ofile, infile)
ofile_sam = pref+'_pysam_sorted.sam'
pysam.view('-o', ofile_sam, ofile, save_stdout=ofile_sam)

# compare md5sums
ctrl_md5 = hashlib.md5(open(pref+'_sorted.sam','rb').read()).hexdigest()
pysam_md5 = hashlib.md5(open(pref+'_pysam_sorted.sam','rb').read()).hexdigest()

print(ctrl_md5 == pysam_md5)