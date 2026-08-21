def dureza(c_edta, v_edta, v_amostra):
    if v_amostra == 0:
        return None
    dureza=((c_edta*v_edta)/v_amostra)*10000
    return dureza 

def std(mi, mf, volume):
    if volume == 0:
        return None
    sdt = (((mf-mi))/volume)*1000
    return sdt

def salinidade(condutividade):
    return condutividade*0.00065

def turbidez(absorbancia, inclinação_reta, intercepto_reta):
    if intercepto_reta == 0:
        return None
    turbidez = (absorbancia - intercepto_reta) / inclinação_reta
    return turbidez
       
# Análise estatística

def media (lista):
    if len(lista) == 0:
        return None
    media = sum(lista)/len(lista) 
    return media

def variancia(lista):
    if len(lista) == 0:
        return None

    m = media(lista)
    variancia = sum((x - m)**2 for x in lista) / len(lista)
    return variancia

def desvio_padrao(lista):
    
    v = variancia(lista)
    if v is None:
        return None
    dp = v ** 0.5
    return dp
 
def dpr(lista):
    dp = desvio_padrao(lista)
    m = media(lista)
    
    if dp is None or m is None or m == 0:
        return None
    
    dpr = (dp/m)*100
    return dpr
     

def amplitude(lista):
    if len(lista) == 0:
        return None
    
    amplitude = max(lista)-min(lista)
    
    return amplitude

