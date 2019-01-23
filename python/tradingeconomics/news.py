import json
import itertools
import urllib 
import pandas as pd
import sys
from datetime import *
from dateutil.relativedelta import relativedelta
from . import functions as fn
from . import glob
import ssl

PY3 = sys.version_info[0] == 3

if PY3: # Python 3+
    from urllib.request import urlopen
    from urllib.parse import quote
else: # Python 2.X
    from urllib import urlopen
    from urllib import quote

class ParametersError(ValueError):
    pass

class DateError(ValueError):
    pass

class CredentialsError(ValueError):
    pass

class LoginError(AttributeError):
    pass

class WebRequestError(ValueError):
    pass

def checkIndex(linkAPI, start):
    if start != None:
        linkAPI += '&start={0}'.format(start)  
    return linkAPI

def checkLimit(linkAPI, limit):
    if limit != None:
        linkAPI += '&limit={0}'.format(limit)
    return linkAPI


def checkNewsIndic(indicator): 
    linkAPI = 'https://api.tradingeconomics.com/news/indicator/'      
    if type(indicator) is str:
        linkAPI += '/' + quote(indicator, safe="")
    else:
        linkAPI += '/' + quote(",".join(indicator), safe="")
    return linkAPI

def checkNewsCountry(country):
    linkAPI = 'https://api.tradingeconomics.com/news/country/'      
    if type(country) is str:
        linkAPI +=  '/' + quote(country, safe="")
    else:
        linkAPI += '/' + quote(",".join(country), safe="")
    return linkAPI

def getNewsLink(country, indicator):
    linkAPI = 'https://api.tradingeconomics.com/news/country/'    
    if type(country) is str:
        linkAPI += quote(country, safe="")
    else: 
        linkAPI += quote(",".join(country), safe="") 
    if type(indicator) is str:
        linkAPI += '/' + quote(indicator, safe="")
    else: 
        linkAPI += '/' + quote(",".join(indicator), safe="") 
    return linkAPI
  
def getNewsResults(webResults, country):
        names = ['id', 'title', 'date', 'description', 'country', 'category', 'symbol', 'url']
        names2 = ['id', 'title', 'date', 'description', 'country', 'category', 'symbol', 'url']
        maindf = pd.DataFrame()  
        for i in range(len(names)):
            names[i] = [d[names2[i]]  for d in webResults]
            maindf = pd.concat([maindf, pd.DataFrame(names[i], columns = [names2[i]])], axis = 1) 
            maindf['country'] =  maindf['country'].map(lambda x: x.strip())


def checkArticleLink (country, indicator):
    linkAPI = 'https://api.tradingeconomics.com/articles/country/'    
    if type(country) is str:
        linkAPI += quote(country)
    else: 
        linkAPI += quote(",".join(country), safe="") 
    if type(indicator) is str:
        linkAPI += '/' + quote(indicator, safe="")
    else: 
        linkAPI += '/' + quote(",".join(indicator), safe="") 
    return linkAPI

def checkArticleCountry(country):
    linkAPI = 'https://api.tradingeconomics.com/articles/country'      
    if country != None:
        if type(country) == str:
            linkAPI += '/' + quote(country, safe="")
        else:    
            linkAPI += '/' + quote(",".join(country), safe="")
     
    return linkAPI

def checkArticleIndic(indicator): 
    linkAPI = 'https://api.tradingeconomics.com/articles/indicator/'      
    if indicator != None:
        if type(indicator) == str:
            linkAPI += '/' + indicator
        else:    
            linkAPI += '/' + quote(",".join(indicator), safe="")

    return linkAPI

def checkArticleLimit(linkAPI, lim):
    if lim != None:
        linkAPI += '&lim={0}'.format(lim)
    return linkAPI

def getArticleResults(webResults, id):
        names = ['id', 'title', 'date', 'description', 'content', 'country', 'category', 'symbol', 'url']
        names2 = ['id', 'title', 'date', 'description', 'content', 'country', 'category', 'symbol', 'url']
        maindf = pd.DataFrame()  
        for i in range(len(names)):
            names[i] = [d[names2[i]]  for d in webResults]
            maindf = pd.concat([maindf, pd.DataFrame(names[i], columns = [names2[i]])], axis = 1) 
            maindf['category'] =  maindf['category'].map(lambda x: x.strip())

def checkArticleId(id):
    linkAPI = 'https://api.tradingeconomics.com/articles/id/'      
    if type(id) is str:
        linkAPI +=  '/' + quote(str(id))
    else:
        linkAPI += '/' + quote(",".join(str(id)))
    return linkAPI




def getNews(country = None, indicator = None, start= None, limit = None, output_type = None):
    """
    Return a list of all news, indicators by country, limit or start index.
    =================================================================================

    Parameters:
    -----------
    country: string or list.
             String for one country information. List of strings for 
             several countrys, for example country = ['country_name', 'country_name'].
    indicators: string or list.
             String for one indicator. List of strings for several indicators, for example 
             indicators = 'indicator_name' or 
             indicators = ['indicator_name', 'indicator_name']
    output_type: string.
             'dict'(default) for dictionary format output, 'df' for data frame,
             'raw' for list of dictionaries directly from the web. 

    Notes
    -----
    All parameters are optional. Without parameters a list of all news will be provided. 

    Example
    -------
    getNews(country = 'United States', indicator = 'Imports', start = 10, limit = 20, output_type = 'df')

    getNews(country = ['United States', 'Portugal'], indicator = ['Imports','Exports'])
    """          
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    if country != None and indicator != None:
        linkAPI = getNewsLink(country, indicator) 
    elif country != None and indicator == None:
        linkAPI = checkNewsCountry(country)      
    elif country == None and indicator != None:
        linkAPI = checkNewsIndic(indicator)
    else:
        linkAPI = 'https://api.tradingeconomics.com/news/' 
             
    try:
        linkAPI += '?c=' + glob.apikey
    except AttributeError:
        raise LoginError('You need to do login before making any request')

    linkAPI = checkLimit(linkAPI, limit)
    linkAPI = checkIndex(linkAPI, start)
  
    try:
        code = urlopen(linkAPI)
        code = code.getcode() 
        webResults = json.loads(urlopen(linkAPI).read().decode('utf-8'))
    except ValueError:
        raise WebRequestError ('Something went wrong. Error code = ' + str(code)) 

    if len(webResults) > 0:
            names = ['id', 'title', 'date', 'description', 'country', 'category', 'symbol', 'url']
            names2 = ['id', 'title', 'date', 'description', 'country', 'category', 'symbol', 'url']
            maindf = pd.DataFrame(webResults, columns=names2)    
    
    else:
        raise ParametersError ('No data available for the provided parameters.')

    if output_type == None or output_type =='dict':
        output = maindf
    elif output_type == 'df': 
        output = maindf
    elif output_type == 'raw':
        output = webResults
    else:
        raise ParametersError ('output_type options : df for data frame, dict(default) for dictionary by country, raw for results directly from web.')      
    return output    
   

def getArticles(country = None, indicator = None, initDate = None, endDate = None, start = None, lim = None, output_type = None):
    """
    Return a list of all articles, article by indicators by country with date interval, and list by limit or start index.
    =================================================================================

    Parameters:
    -----------
    country: string or list.
            List of strings for one country or several countries, for example: 
            country = ['country_name', 'country_name']
            country = 'country_name'
            List of strings for several countries and indicators or one country and one indicator, for example: 
            country = ['country_name', 'country_name'], indicator = ['inflation rate', 'interest rate']
            country = 'country_name', indicator = 'inflation rate'
            list of strings for one or more countries with date interval, example: 
            country = 'country_name', initDate = '2015-10-10', endDate = '2017-10-10' 
            country = ['country_name', 'country_name], initDate = '2015-10-10', endDate = '2017-10-10'
    indicators: string or list.
            List of strings for several indicators or one indicator, for example: 
            indicator = 'indicator_name'  
            indicator = ['indicator_name', 'indicator_name']
    start and lim: string or list.
            articles list by start index and/or by limit for example:
            country = 'country_name', start = 20, lim = 100
            indicator = 'indicator_name', start = 20, lim = 100
            country = 'country_name', indicator = 'indicator_name', start = 20, lim = 100            
    initDate: string with format: YYYY-MM-DD.
            For example: '2011-01-01' 
    endDate: string with format: YYYY-MM-DD.            
    output_type: string.
            'dict'(default) for dictionary format output, 'df' for data frame,
            'raw' for list of dictionaries directly from the web. 

    Notes
    -----
     Without parameters a list of articles will be provided. 

    Example
    -------
    getArticles(country = ['United States', 'Portugal'], indicator = ['Imports','Exports'])

    getArticles(country = 'United States', indicator = 'Imports', start = 10, lim = 20, output_type = 'df')

    getArticles(country = 'United States', indicator = None, initDate = '2015-10-10', endDate = '2017-10-10', start = 10, lim = 20, output_type = 'df')

    """          

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    if country != None and indicator != None:
        linkAPI = checkArticleLink(country, indicator) 
    elif country != None and indicator == None:
        linkAPI = checkArticleCountry(country)      
    elif country == None and indicator != None:
        linkAPI = checkArticleIndic(indicator)
    else:
        linkAPI = 'https://api.tradingeconomics.com/articles/'
    
    if (initDate != None) and (endDate != None) :
        try: 
            fn.validate(initDate)
        except ValueError:
            raise DateError ('Incorrect initDate format, should be YYYY-MM-DD or MM-DD-YYYY.')
        try: 
            fn.validate(endDate)
        except ValueError:
            raise DateError ('Incorrect endDate format, should be YYYY-MM-DD or MM-DD-YYYY.')
        try:        
            fn.validatePeriod(initDate, endDate)
        except ValueError:
            raise DateError ('Invalid time period.')
        linkAPI += '/from' + '/' + initDate + '/' + endDate
    
    elif (initDate != None) and endDate == None :        
        try: 
            fn.validate(initDate)
        except ValueError:
            raise DateError ('Incorrect initDate format, should be YYYY-MM-DD or MM-DD-YYYY.')
            if initDate > str(date.today()):
                raise DateError ('Initial date out of range.')
        linkAPI += '/from' + initDate
    
    elif initDate == None and (endDate != None):
        initDate = (datetime.str(endDate, '%Y-%m-%d') - relativedelta(months=6)).strftime('%Y-%m-%d')
        linkAPI += '/from' + '/' + initDate + '/' + endDate 
     
    try:
        linkAPI += '?c=' + glob.apikey
    except AttributeError:
        raise LoginError('You need to do login before making any request')
    
    linkAPI = checkArticleLimit(linkAPI, lim)
    linkAPI = checkIndex(linkAPI, start)

    print (linkAPI)
    try:
        code = urlopen(linkAPI)
        code = code.getcode() 
        webResults = json.loads(urlopen(linkAPI).read().decode('utf-8'))
    except ValueError:
        raise WebRequestError ('Something went wrong. Error code = ' + str(code)) 

    if len(webResults) > int(0):
            names = ['id', 'title', 'date', 'description', 'country', 'category', 'symbol', 'url']
            names2 = ['id', 'title', 'date', 'description', 'country', 'category', 'symbol', 'url']
            maindf = pd.DataFrame(webResults, columns=names2)    
    else:
        raise ParametersError ('No data available for the provided parameters.')

    if output_type == None or output_type =='dict':
        output = maindf
    elif output_type == 'df': 
        output = maindf
    elif output_type == 'raw':
        output = webResults
    else:
        raise ParametersError ('output_type options : df for data frame, dict(default) for dictionary by country, raw for results directly from web.')      
    return output    
     

def getArticleId(id = None, output_type = None):
    """
    Return one id of an article.
    =================================================================================

    Parameters:
    -----------
    id: string.
            Information of one article searched by it's identifier.
    output_type: string.
             'dict'(default) for dictionary format output, 'df' for data frame,
             'raw' for list of dictionaries directly from the web. 

    Notes
    -----
    To get results it must have a given id. 

    Example
    -------
    getArticleId(id = '20580', output_type = None)
    
    """ 
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    if type(id) !=None:        
        linkAPI =  checkArticleId(id)
            
    try:
        linkAPI += '?c=' + glob.apikey
    except AttributeError:
        raise LoginError('You need to do login before making any request')

    try:
        code = urlopen(linkAPI)
        code = code.getcode() 
        webResults = json.loads(urlopen(linkAPI).read().decode('utf-8'))
    except ValueError:
        raise WebRequestError ('Something went wrong. Error code = ' + str(code)) 

    if len(webResults) > 0:
            names = ['id', 'title', 'date', 'description', 'content', 'country', 'category', 'symbol', 'url']
            names2 = ['id', 'title', 'date', 'description', 'content', 'country', 'category', 'symbol', 'url']
            maindf = pd.DataFrame(webResults, columns=names2)    
    
    else:
        raise ParametersError ('No data available for the provided parameters.')

    if output_type == None or output_type =='dict':
        output = maindf
    elif output_type == 'df': 
        output = maindf
    elif output_type == 'raw':
        output = webResults
    else:
        raise ParametersError ('output_type options : df for data frame, dict(default) for dictionary by country, raw for results directly from web.')      
    return output     

