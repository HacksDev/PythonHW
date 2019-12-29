def CtoF(degree, direct_order=True):
    return (degree * 9/5 + 32) if (direct_order) else ((degree - 32) * 5/9)
