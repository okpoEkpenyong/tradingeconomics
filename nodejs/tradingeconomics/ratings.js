'use strict'

const auth = require('./auth.js');
const func = require('./functions.js');
const fetch = require('node-fetch');

//setting global variables to be used outside this module
global.country = null;
global.historical = null;

//This function builds the path to get the API request:
/****************************************************************************************************************************  
  WITHOUT PARAMETERS A LIST OF ALL CREDIT RATINGS WILL BE PROVIDED
  parameters:
    String or list: country, historical(in this case we will put the country of who we want historical data from)

  example:
    getRatings();
    getRatings(country ='china');
    getRatings(country =['china', 'japan']);
    getRatings(historical ='united states');             

******************************************************************************************************************************/

function getRatings(){

  var url = '';
  var Data = '';
   
  if (country != null){    
      url = '/ratings/' + country;    
  }
  if (historical != null){    
      url =  '/ratings/historical/' + historical;    
  }
  if (historical === null && country === null){
      url = '/ratings';
  }

  Data = url_base + url + '?c=' + apikey.replace (' ','%20');
  
  return fetch(Data)
  .then(func.handleErrors)   
  .then(function(response) {    
      return response.json(); // process it inside the `then` when calling the function       
  }).catch(function (err) {
      return err.message;
  });
 

}

module.exports.getRatings = getRatings;









