# change the objectives for defect prediction
ABCD = False
PDPF = True
GF = False
ACC = False


# change the distribution
# options: UNIFORM, GAUSSIAN
GALE_DISTRIBUTION = "GAUSSIAN"

# SMOTE the training data
SMOTE = False
SMOTE_BINARY_CLASSIFICATION = True  # consider all the rows as either bugs or not bugs

CULLING = True  # having a culling policy in check pd = 66 and pf = 33
NEW_DE = True   # traditional DE algorithm

