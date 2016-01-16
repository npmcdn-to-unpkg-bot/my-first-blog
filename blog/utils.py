from pint import UnitRegistry,UndefinedUnitError
ureg = UnitRegistry()
Q_=ureg.Quantity

from math import log10
import re

def sigfigs(x,n):
    l10 = 1+round(log10(x),0)
    x = round(x, int(n-l10))
    if (x==round(x)):
        return int(x)
    else:
        return x

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def getScaleFactor(multiple):
    if multiple == "T":
        scale = 12
    elif multiple == "G":    
        scale = 9
    elif multiple == "M":    
        scale = 6
    elif multiple == "k":    
        scale = 3
    elif multiple == "U":
        scale = 0
    else:
        scale = 0
    return scale, 10**scale

std_units = {
    "":"i",
    "$":"USD",
    "£":"GBP",
    "€":"EUR",
    "¥":"JPY",
    "miles":"mile",
    "yards":"yard",
    "yd":"yard",
    "feet":"foot",
    "ft":"foot",
    "inches":"inch",
    "in":"inch",
    "years":"yr",
    "y":"year",
    "months":"month",
    "mth":"month",
    "weeks":"week",
    "wk":"week",
    "days":"day",
    "dy":"dy",
    "d":"d",
    "hours":"hour",
    "hrs":"hour",
    "hr":"hour",
    "h":"hour",
    "minutes":"minute",
    "mins":"minute",
    "min":"minute",
    "mn":"minute",
    "seconds":"second",
    "secs":"second",
    "sec":"second",
    "s":"second",
}

std_multiples = {
    "thousand":"k",
    "thou":"k",
    "grand":"k",
    "m":"M",
    "mil":"M",
    "million":"M",
    "b":"G",
    "bn":"G",
    "billion":"G",
    "t":"T",
    "trillion":"T",
}

def normalise(parsed):
    magnitude, multiple, unit = parsed
    if unit in std_units.keys():
        unit = std_units[unit]
    measure = getMeasure(unit)   
    if multiple in std_multiples.keys():
        multiple = std_multiples[multiple]
    #if multiple == 'b':
        #multiple = 'G'
    #elif multiple == 'bn':
        #multiple = 'G'
    #elif multiple == 'billion':
        #multiple = 'G'
    #elif multiple == 't':
        #multiple = 'T'
    #elif multiple == 'tn':
        #multiple = 'T'
    #elif multiple == 'trillion':
        #multiple = 'T'
    return magnitude, multiple, unit, measure 

def getMeasure(unit):
    try:
        dim = ureg.parse_expression(unit).dimensionality 
        if dim == ureg.parse_expression('m').dimensionality :
            return "e"
        elif dim == ureg.parse_expression('s').dimensionality :
            return "d"
        elif dim == ureg.parse_expression('kg').dimensionality :
            return "m"
        else:
            return "?"
    except UndefinedUnitError:
        p = re.compile("^[A-Z]{3}$")
        m=p.match(unit)
        if m!=None:
            return "a"
        else:
            return "c"



def parseNumber(big_number, regex):
    p = re.compile(regex)
    m=p.match(big_number)
    if (m==None):
        return m
    else:        
        magnitude = m.group('magnitude')
        unit = m.group('unit')
        multiple = 'U'
        try:
            multiple = m.group('multiple')
        except:
            pass
        return normalise((magnitude, multiple, unit))


def parseBigNumber(big_number):
    print(big_number)
    parsed = parseNumber(big_number,"^(?P<magnitude>[\-0-9\.]+)\s*(?P<unit>[a-zA-Z/£$€¥]*(\^-?[0-9]*)?)$")
    if (parsed != None):
        return parsed
    parsed = parseNumber(big_number,"^(?P<unit>[a-zA-Z\/£$€¥](\^-?[0-9]*)?)\s*(?P<magnitude>[\-0-9\.]+)$")
    if (parsed != None):
        return parsed
    parsed = parseNumber(big_number,"^(?P<magnitude>[\-0-9\.]+)\s*(?P<multiple>[a-zA-Z]*)\s*(?P<unit>[a-zA-Z/£$€¥]*(\^-?[0-9]*)?)$")
    if (parsed != None):
        return parsed
    parsed = parseNumber(big_number,"^(?P<unit>[a-zA-Z/£$€¥]*(\^-?[0-9]*)?)\s*(?P<magnitude>[\-0-9\.]+)\s*(?P<multiple>[a-zA-Z]*)$")
    if (parsed != None):
        return parsed
    parsed = parseNumber(big_number,"^(?P<magnitude>[\-0-9\.]+)$")
    if (parsed != None):
        return parsed


def tests():
    parsed = parseBigNumber("100 thou GBP")
    print(parsed)
    #parsed = parseBigNumber("100kg")
    #print(parsed)
    #parsed = parseBigNumber("100m/s")
    #print(parsed)
    #parsed = parseBigNumber("10m/s^2")
    #print(parsed)
    #parsed = parseBigNumber("USD25.56")
    #print(parsed)
    #parsed = parseBigNumber("USD 25.56")
    #print(parsed)
    parsed = parseBigNumber("$25.56")
    print(parsed)
    parsed = parseBigNumber("£25.56")
    print(parsed)
    parsed = parseBigNumber("25.56$")
    print(parsed)
    parsed = parseBigNumber("25.56 £")
    print(parsed)
    #parsed = parseBigNumber("2.5 bn people")
    #print(parsed)
    #parsed = parseBigNumber("2.5bn people")
    #print(parsed)
    #parsed = parseBigNumber("$25.56m")
    #print(parsed)
    #parsed = parseBigNumber("GBP 25.56m")
    #print(parsed)
    #parsed = parseBigNumber("AUD 25.56 bn")
    #print(parsed)
    #parsed = parseBigNumber("25.56")
    #print(parsed)
    #parsed = parseBigNumber("2556000000")
    #print(parsed)

#tests()