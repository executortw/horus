import logilab.hmm.hmm as hmm                                                                                                                                                   
import os                                                                                                                                                                        
import Identify_module
from numpy import array, allclose, zeros, take                                                                                                                                   
hmmKlass = hmm.HMM                                                                                                                                                               
Horushmm = hmmKlass(['Normal','Intrusion','JointAttack'],['1','2','3','4','5'],                                                                                                  
                    array([[0.8,0.2,0],[0,0.3,0.7],[0,0.2,0.8]]),                                                                                                                
#                   array([[0.616,0.013,0,0.371,0],[0,0.7,0.3,0,0],[0,0,0.5,0,0.5]]),                                                                                            
                    array([[0.616,0,0],[0.013,0.7,0],[0,0.3,0.5],[0.371,0,0],[0,0,0.5]]),                                                                                        
                    array([0.812,0.188,0]))                                                                                                                                 
                                                                                                                                                                                 
Horushmm.dump()                                                                                                                                                                  
                                                                                                                                                                                 
def Detection(IP,Observations):
    Result = Horushmm.analyze(Observations)
    try:
	JA = Result.index("JointAttack")
	return 1
#	print "JA! Put Alert raiser here!"
    except ValueError:
	try:
	    Intru = Result.index("Intrusion")
	    Identify_module.Identify_mod(IP)
	    return 1
	    #print "Intrusion! Put Alert raiser here!"
	except ValueError:
	    print "normal"
	    return 0

#    print Result
