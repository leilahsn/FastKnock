def read_file_for(f_name , rec , t , num):
    
    j = 1
    with open(f_name , 'r') as f:
        for line in f:
            if line not in ['\n' , '\r\n' , '\t']:
                line = line.replace('\n' , '')
                line = line.replace('\t' , '')
                temp = line.split(' ')
            
                if temp[5+num] > t:
                    rec.append(line)
    return rec

def read_file(f_name , rec):
    
    with open(f_name , 'r') as f:
        for line in f:
            if line not in ['\n' , '\r\n' , '\t']:
                line = line.replace('\n' , '')
                line = line.replace('\t' , '')
                rec.append(line)
    return rec

def merge(processors, target_level):

    for i in range(target_level):
        f_names = []
        for j in range(processors):
            a = str("p")+ str(j+1)+ str("_") + str(i+1)+str('.txt')
            f_names.append(a)

            all_record = []
            for k in f_names:
                all_record = read_file(k , all_record)

            res_name = str("knockoutStrategy_") + str(i+1)+str('.txt')
            with open (res_name, 'w') as f:
                for r in all_record:
                    f.write(str(r))
                    f.write('\n')
            f.close()
    
               

    
