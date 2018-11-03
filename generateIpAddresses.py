for i in range(51,101):
    for j in range(1,101):
        if(j%5==0):
            print '10.0.' + str(j) + '.' + str(i) + ',' + 'b'
        else:
            print '10.0.' + str(j) + '.' + str(i) + ',' + 'n'
