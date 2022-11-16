def sum_non_neg_diag(x):
    sum = 0
    f = 0
    for i in range(len(x)):
        for j in range(len(x[i])):
            if(i == j and x[i][j] >= 0 ):
                f = 1
                sum += x[i][j]
    return sum if f else -1

def are_multisets_equal(x, y):
    if len(x) == len(y):
        f = 0
        count = 0
        for i in range(len(x)):
            count += f
            f = 0
            for k in range(len(y)):
                if x[i] == y[k]:
                    f = 1
        count +=f
        if count == len(x):
            return True
        else: return False
    else: return False
    
def max_prod_mod_3(x):
    f = 0
    max_m = -1
    curr = 1
    for i in range(len(x)):
        curr *= x[i]
        if curr%3 == 0 and curr > max_m:
            max_m = curr
            f = 1
        if(curr == 0):
            curr = 1
    return max_m if f else -1


def convert_image(image, weights):
    out = []
    a = 0
    for i in image:
        p = []
        a = 0
        for k in i:
            for j in range(len(weights)):
                a = a + k[j] * weights[j]
            p.append(a)
            a = 0
        out.append(p)
    return out

def rle_scalar(x, y):
    x_1 = []
    y_1 = []
    for i in x:
        for j in range(i[1]):
            x_1.append(i[0])
    for i in y:
        for j in range(i[1]):
            y_1.append(i[0])
    if len(x_1) == len(y_1):
        xy = [x_1[i]*y_1[i] for i in range(len(x_1))]
        return sum(xy)
    else: retur -1
        
def cosine_distance(x,y):
    m = []
    for i in range(len(x)):
        m.append([])
        for j in range(len(y)):
            xy = sum([x[i][k]*y[j][k] for k in range(len(x[i]))])
            xx = sum([x[i][k]*x[i][k] for k in range(len(x[i]))])
            yy = sum([y[j][k]*y[j][k] for k in range(len(y[i]))])
            if xx * yy == 0:
                a = 1
            else:
                a = xy/(xx**0.5 * yy**0.5)
            m[i].append(a)
    return m 
