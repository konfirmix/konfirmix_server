def getRowFromTable(list,columnName,columnValue):
        for i in range(0,len(list)):
            if(list[i][columnName] == columnValue):
               return list[i]
        return None

def table_to_dict (out,header=None,skip=0):
    out=out.strip()
    if('\n' in header[0]):
         noOfLinesToOmit = header[0].count('\n')                
         newHeader = []
         newOut = []
         resHeader = []
         for hString in header:
            newHeader.append(hString.split('\n')[0])
            resHeader.append(hString.replace('\n',''))       
         skip = noOfLinesToOmit
         header = newHeader
    else:              
         resHeader = header
         
    out.replace('\r',"")
    lines = out.split("\n")
    if (skip != 0 ):
       lines =lines[skip:]
    first_line = lines[0]
    if len(first_line.split()) == 0:
      first_line = lines[1]
      lines = lines[2:]
    else:
      lines = lines[1:]
    
    if header == None :
       header = first_line.split()
       #print "header is : "+str(header)
    #num_header = len(header) - 1
    num_header = len(header)
    
    row_count = 0
    headerpos=[]
    table = dict()    
     
    startpos=0
    for i in range(len(header)):
        headerpos.append(out.index(header[i],startpos))
        startpos=headerpos[i]+1
    #print headerpos


    headerLength = len(headerpos)
    header = resHeader
    #print headerpos
    for line in lines:	    
            tempObj = {}
	    for i in range(0,headerLength):
	      if(i == headerLength-1):
		endPos = len(line)
                tempObj[header[i]] = line[headerpos[i]:endPos].strip()
	        
	      else:  
                 
                 endPos = headerpos[i+1]
                 tempObj[header[i]] = line[headerpos[i]:endPos].strip()
                 
            
            table[row_count] = tempObj
            row_count+=1 
        
    return table 


if __name__ == '__main__':
      

      output = '''
Address          Interface                Ver/   Nbr    Query  DR      DR
                                          Mode   Count  Intvl  Prior
172.16.8.1       FastEthernet0/0          v2/S   0      30     1       172.16.8.2  
            '''
      header = ["Address\n","Interface\n","Ver\n/Mode","Nbr\nCount","Query\nIntvl","DR\nPrior","DR\n"]
      output = table_to_dict1(output,header)
      print output
