def kfold_split(num_objects, num_folds):
    x = np.arange(num_objects)
    list_return = []
    for i in range(num_folds - 1):
        list_return.append((np.delete(x, i).ravel(), np.array([i])))
    list_return.append((x[:num_folds-1], x[num_folds-1:]))
    return list_return


def knn_cv_score(
    X,
    y,
    parameters,
    score_function,
    folds,
    knn_class,
):
    out = {}
    score = 0
    normalizers = parameters["normalizers"]
    del parameters["normalizers"]
    print(parameters)
    for pair in product(*parameters.values()):
        for i in range(len(folds)):
            di = dict(zip(list(parameters), list(pair)))
            s = knn_class(**di)
            s.fit(X[folds[i][0]], y[folds[i][0]])
            print("***")
            print(X[folds[i][1]])
            print("---")
            predict = s.predict(X[folds[i][1]])
            x = score_function(y[folds[i][1]], predict)
            score += x
            out[tuple([pair])] = score / len(folds)
        
    return out
