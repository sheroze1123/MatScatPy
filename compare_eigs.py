def compare_eigs(ll1, ll2, tol):
    """
    Compare the results of two eigenvalue vectors (ll1 and ll2).

    Input:
      ll1, ll2 -- Eigenvalue lists
      tol      -- Matching tolerance
    Output:
      ll       -- All elements of ll1 within tol of some element of ll2
      diff     -- diff(i) is min(abs(ll1(i) - ll2));
    """
    if ll1.shape(0) is 1:
        ll1 = np.transpose(ll1)
    else:
        ll2 = np.transpose(ll2)

    e1 = np.ones(ll1.shape)
    e2 = np.ones(ll2.shape)

    diff = np.amin(np.abs(np.dot(ll1, e2) - np.dot(ll2, e1)), 1)
