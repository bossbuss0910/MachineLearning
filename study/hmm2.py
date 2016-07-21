def forward(A, B, O):
    """
    forward algo
    """
    alpha = [[0.0 for j in range(len(A))] for t in range(len(O))]
    alpha[0][0] = 1.0
    for t in range(1, len(alpha)):
        for j in range(len(alpha[t])):
            if j < len(alpha[t])-1:
                alpha[t][j] += alpha[t-1][j] * A[j][j] * B[j][O[t-1]]
            if j > 0:
                alpha[t][j] += alpha[t-1][j-1] * A[j-1][j] * B[j-1][O[t-1]]
    return alpha


def backward(A, B, O):
    """
    backward algo
    """
    beta = [[0.0 for j in range(len(A))] for t in range(len(O))]
    beta[-1][-1] = 1.0
    for t in range(len(beta)-2, -1, -1):
        for j in range(len(beta)-1, -1, -1):
            if j < len(beta[t])-1:
                beta[t][j] = beta[t+1][j+1] * A[j][j+1] * B[j][O[t]] + beta[t+1][j] * A[j][j] * B[j][O[t]]
    return beta


def expectation(A, B, O, alpha, beta):
    """
    step 
    """
    gamma = [[[0.0 for j in range(len(A))] for i in range(len(A))] for t in range(len(O))]
    for t in range(len(gamma)):
        for i in range(len(gamma[t])):
            for j in range(len(gamma[t][i])):
                gamma[t][i][j] = alpha[t][i]*A[i][j]*B[i][O[t]]*beta[t][j] / alpha[-1][-1]
    return gamma


def maximization(A, B, O, gamma):
    for i in range(len(A)):
        for j in range(len(A[i])):
            a, b = 0, 0
            for t in range(len(gamma)):
                a += gamma[t][i][j]
                for _j in range(len(A[i])):
                    b += gamma[t][i][_j]
            A[i][j] = a / b

    for j in range(len(B)):
        for o in range(len(B[j])):
            a, b = 0, 0
            for t in range(len(gamma)):
                for k in range(len(gamma[t][j])):
                    if o == O[t]:
                        a += gamma[t][j][k]
                    b += gamma[t][j][k]
            B[j][o] = a / b


def learning(N, K, O, max_step):
    A = [[1.0/(N) for j in range(N)] for i in range(N)]
    B = [[1.0/K for j in range(K)] for i in range(N)]
    
    prev_likelihood = 0
    step = 0
    while step<max_step:
	for user in O:
		alpha = forward(A, B, user)
		beta = backward(A, B, user)
		if not prev_likelihood < beta[0][0]:
			break
		prev_likelihood = beta[0][0]
		gamma = expectation(A, B, user, alpha, beta)
		maximization(A, B, user, gamma)
	step += 1
    return A, B

