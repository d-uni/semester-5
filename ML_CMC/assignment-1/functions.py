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
        x_ch = []
        y_ch = []
        f = 0
        for i in range(len(y)):
            x_ch.append(0)
            y_ch.append(0)
        for i in range(len(y)):
            s_x = 0
            s_y = 0
            for j in range(len(y)):
                if(x[i] == x[j]):
                    s_x +=1
                if(y[i] == y[j]):
                    s_y +=1
            x_ch[i] = s_x
            y_ch[i] = s_y
        for i in range(len(y)):
            for j in range(len(y)):
                if(x[i] == y[j]):
                    if(x_ch[i] != y_ch[j]):
                        f = 1
        return False if f else True
    else: return False
    
def max_prod_mod_3(x):
    max_m = -1
    for i in range(len(x) - 1):
        if(x[i]*x[i+1] > max_m and x[i]*x[i+1] % 3 == 0):
            max_m = x[i]*x[i+1]
        
    return max_m 


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
    else: return -1
        
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

