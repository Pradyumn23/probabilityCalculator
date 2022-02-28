from matplotlib import pyplot as plt
import alien_bayes


def two_line_plot(xvals1, yvals1, label1, xvals2, yvals2, label2, title, outfile_path):
    plt.plot(xvals1, yvals1, label=label1, color='blue', marker='.', linestyle='solid')
    plt.plot(xvals2, yvals2, label=label2, color='green', marker='.', linestyle='solid')
    plt.title(title)
    plt.legend()
    plt.savefig(outfile_path)

nodes = alien_bayes.ALIEN_NODES

# 
# Fill in this script to empirically calculate P(A=true | M=true, B=true) using the rejection
# sampling and likelihood weighting code found in alien_bayes.py.
#
# Use the two_line_plot() function above to generate a line graph with one line for each 
# approximation technique.  The x-axis should represent different n, the number of samples 
# generated, with the probability estimate for the conditional probability above on the y-axis.  
# 
# You should generate estimates using at least 100 different values of n, and increase it to 
# the point that the estimates appear to stabilize.  Note that for rejection sampling, n should
# represent the number of simple samples created, not the number retained after rejecting those
# that do not agree with the evidence.  
# 
# Your script should produce a plot named "alien_bayes.pdf". 
#  

if __name__ == '__main__':  

    sampler_reject = alien_bayes.RejectionSampler(alien_bayes.ALIEN_NODES)
    sampler_like = alien_bayes.LikelihoodWeightingSampler(alien_bayes.ALIEN_NODES)

    query = { 'A': True }
    evidence = { "M": True , "B": True}
    i =1
    xvals=[]
    yvals1=[]
    yvals2=[]

    while(i<=150):
        n= i*100*2
        xvals.append(n)
        yvals1.append(sampler_reject.get_prob(query, evidence, n))
        yvals2.append(sampler_like.get_prob(query, evidence, n))
        i+=1
    print(len(xvals))
    print(len(yvals1))

    two_line_plot(xvals,yvals1,"rejection sampling",xvals,yvals2,"likelihood weighting","rejection sampling/likelihood weighting vs number of samples","alien_bayes.pdf")



