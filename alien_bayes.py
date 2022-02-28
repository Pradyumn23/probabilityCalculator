import random


class BooleanVariableNode(object):
    """Class representing a single node in a Bayesian network.

    The conditional probability table (CPT) is stored as a dictionary, keyed by tuples of parent
    node values.
    """

    def __init__(self, var, parent_vars, cpt_entries):
        """Constuctor for node class.

        Args:
            var: string variable name
            parent_vars: a sequence of strings specifying the parent variable names
            cpt_entries: a dictionary specifying the CPT, keyed by a tuple of parent values, 
                with values specifying the prob that this variable=true
        """
        self.parents = parent_vars
        self.target = var
        self.cpt = {}  # (parent_val1, parent_val2, ...) => prob
        for parent_vals, prob in cpt_entries:
            key = tuple(parent_vals)
            self.cpt[key] = prob

    def get_parents(self):
        return self.parents
    
    def get_var(self):
        return self.target

    def get_prob_true(self, parent_vals):
        key = tuple(parent_vals)
        return self.cpt[key]

    def get_prob_false(self, parent_vals):
        return 1.0 - self.get_prob_true(parent_vals)


class SimpleSampler(object):
    """Sampler that generates samples with no evidence."""
    
    def __init__(self, nodes):
        self.nodes = nodes
    
    def generate_sample(self):
        """Create a single sample instance, returns a dictionary."""
        sample_vals = {}  # variable => value
        while len(sample_vals) < len(ALIEN_NODES):       
            for node in ALIEN_NODES:
                var = node.get_var()
                if node not in sample_vals:  # we haven't generated a value for this var
                    parent_vars = node.get_parents()
                    if all([ p in sample_vals for p in parent_vars ]):  # all parent vals generated
                        parent_vals = tuple([ sample_vals[par] for par in parent_vars ])
                        prob_true = node.get_prob_true(parent_vals)
                        sample_vals[var] = random.random() < prob_true
        return sample_vals
        
    def generate_samples(self, n):
        """Create multiple samples, returns a list of dictionaries."""
        return [ self.generate_sample() for x in range(n) ]
    
    def get_prob(self, query_vals, num_samples):
        """Return the (joint) probability of the query variables.
        
        Args:
            query_vals: dictionary mapping { variable => value }
            num_samples: number of simple samples to generate for the calculation

        Returns: empirical probability of query values
        """
        # 
        # fill in the function body here
        #
        sample_vals = self.generate_samples(num_samples)
        myNumber = 0

        for sampleVal in sample_vals:
            checker = True
            for each in query_vals:
                if(sampleVal[each]!=query_vals[each]):
                    checker=False
                    break
            if(checker==True):
                myNumber+=1
        





        

        return float(myNumber)/float(len(sample_vals))

        
class RejectionSampler(SimpleSampler):
    """Sampler that generates samples given evidence using rejection sampling."""

    def generate_samples(self, n, evidence_vals={}):
        """Return simple samples that agree with evidence (may be less than n)."""
        unfiltered = super().generate_samples(n)
        keeps = []
        for sample in unfiltered:  # get rid of anything that doesn't match the evidence
            if all(sample.get(var, None) == val for var, val in evidence_vals.items()):
                keeps.append(sample)
        return keeps

    def get_prob(self, query_vals, evidence_vals, num_samples):
        """Return the conditional probability of the query variables, given evidence.
        
        Args:
            query_vals: dictionary mapping { variable => value }
            num_samples: number of simple samples to generate for the calculation (the number
                "kept" that agree with evidence will be significantly lower)

        Returns: empirical conditional probability of query values given evidence
        """
        # 
        # fill in the function body here
        #
        sample_vals = self.generate_samples(num_samples,evidence_vals)
        myNumber = 0

        for sampleVal in sample_vals:
            checker = True
            for each in query_vals:
                if(sampleVal[each]!=query_vals[each]):
                    checker=False
                    break
            if(checker==True):
                myNumber+=1
        





        

        return float(myNumber)/float(len(sample_vals))


class LikelihoodWeightingSampler(SimpleSampler):
    """Sampler that generates samples given evidence using likelihood weighting."""

    def generate_sample(self, evidence_vals):
        """Create a single sample instance that agrees with evidence.
        
        Returns a dictionary containing the sample and the corresponding weight."""
        sample_vals = {}  # variable => value
        weight = 1.0

        while len(sample_vals) < len(ALIEN_NODES):    
            for node in ALIEN_NODES:
                var = node.get_var()
                if node not in sample_vals:
                    parent_vars = node.get_parents()
                    if all([ p in sample_vals for p in parent_vars ]):
                        parent_vals = tuple([ sample_vals[par] for par in parent_vars ])
                        if var in evidence_vals:  # if evidence, adjust the weight by the likelihood
                            val = evidence_vals[var]
                            sample_vals[var] = val
                            p = node.get_prob_true(parent_vals) if val else node.get_prob_false(parent_vals)
                            weight *= p
                        else:  # generate a value using the CPT
                            prob_true = node.get_prob_true(parent_vals)
                            sample_vals[var] = random.random() < prob_true
        return sample_vals, weight

    def generate_samples(self, n, evidence_vals={}):
        """Create multiple samples, returns a list of dictionary/weight tuples."""
        return [ self.generate_sample(evidence_vals) for x in range(n) ]

    def get_prob(self, query_vals, evidence_vals, num_samples):
        """Return the conditional probability of the query variables, given evidence.
        
        Args:
            query_vals: dictionary mapping { variable => value }
            num_samples: number of simple samples to generate for the calculation 

        Returns: empirical conditional probability of query values given evidence
        """
        # 
        # fill in the function body here
        #
        sample_vals = self.generate_samples(num_samples,evidence_vals)
        myNumber = 0
        total = 0

        for sampletuple in sample_vals:
            sampleVal = sampletuple[0]
            checker = True
            for each in query_vals:
                if(sampleVal[each]!=query_vals[each]):
                    checker=False
                    break
            if(checker==True):
                myNumber+=sampletuple[1]
            total+=sampletuple[1]
        





        

        return float(myNumber)/float(total)
    


ALIEN_NODES = [
    BooleanVariableNode('A', (), [         [(),             0.03] ]),
    BooleanVariableNode('T', (), [         [(),             0.55] ]),
    BooleanVariableNode('M', ('A',), [     [(True,),        0.90], 
                                           [(False,),       0.15] ]),
    BooleanVariableNode('B', ('A', 'T'), [ [(True, True),   0.95], 
                                           [(True, False),  0.70], 
                                           [(False, True),  0.65], 
                                           [(False, False), 0.02] ])
]


##########################################
if __name__ == '__main__':

    n = 100000
    sampler_simp = SimpleSampler(ALIEN_NODES)
    sampler_reject = RejectionSampler(ALIEN_NODES)
    sampler_like = LikelihoodWeightingSampler(ALIEN_NODES)

    print("P(abduct, toast)")
    query = { 'A': True, 'T': True }
    print("simple:     {:.4f}".format(sampler_simp.get_prob(query, n)))
    print("rejection:  {:.4f}".format(sampler_reject.get_prob(query, {}, n)))
    print("likelihood: {:.4f}\n".format(sampler_like.get_prob(query, {}, n)))

    print("P(-abduct, toast)")
    query = { 'A': False, 'T': True }
    print("simple:     {:.4f}".format(sampler_simp.get_prob(query, n)))
    print("rejection:  {:.4f}".format(sampler_reject.get_prob(query, {}, n)))
    print("likelihood: {:.4f}\n".format(sampler_like.get_prob(query, {}, n)))
    
    print("P(abduct | memory)")
    query = { 'A': True }
    evidence = { "M": True }
    print("rejection:  {:.4f}".format(sampler_reject.get_prob(query, evidence, n)))
    print("likelihood: {:.4f}\n".format(sampler_like.get_prob(query, evidence, n)))

    print("P(abduct | -memory)")
    query = { 'A': True }
    evidence = { "M": False }
    print("rejection:  {:.4f}".format(sampler_reject.get_prob(query, evidence, n)))
    print("likelihood: {:.4f}\n".format(sampler_like.get_prob(query, evidence, n)))

    print("P(abduct | memory, burn)")
    query = { 'A': True }
    evidence = { 'M': True, 'B': True }
    print("rejection:  {:.4f}".format(sampler_reject.get_prob(query, evidence, n)))
    print("likelihood: {:.4f}\n".format(sampler_like.get_prob(query, evidence, n)))
    
    print("P(abduct | memory, burn, toast)")
    query = { 'A': True }
    evidence = { 'M': True, 'B': True, 'T': True }
    print("rejection:  {:.4f}".format(sampler_reject.get_prob(query, evidence, n)))
    print("likelihood: {:.4f}\n".format(sampler_like.get_prob(query, evidence, n)))

    print("P(abduct | memory, burn, -toast)")
    query = { 'A': True }
    evidence = { 'M': True, 'B': True, 'T': False }
    print("rejection:  {:.4f}".format(sampler_reject.get_prob(query, evidence, n)))
    print("likelihood: {:.4f}\n".format(sampler_like.get_prob(query, evidence, n)))

