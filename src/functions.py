import numpy as np

def identity_function(X,y):
    return y

def InverseCustomerSpendingTransformer(X, y):
    #y = np.expm1(y)
    #y *= (X['income'])        
    y *= (X['reported_income'])        
    #y *= (X['credit_limit'])        
    return y
    
def CustomerSpendingLimitTransformer(X, y):
    y = InverseCustomerSpendingTransformer(X,y) / 0.4
    return y
