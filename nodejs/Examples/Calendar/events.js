// DOCUMENTATION:
// http://docs.tradingeconomics.com/?javascript#events

// Pacakge Installation: npm install tradingeconomics
const te = require('tradingeconomics')

// Login with client key or leave it blank, you can get your free key here: http://developer.tradingeconomics.com
// Note: without a client key only a small sample of data will be given.
te.login()

//===============================================================================================================
//Get all calendar events (You can pass importance parameter or date parameters (yyyy-mm-dd) for specific data )

te.getCalendar()
  .then((data) => {
    console.log('All calendar events:', '\n', data, '\n')
  })
  .catch((err) => console.log(err))

te.getCalendar(
  (start_date = '2016-12-02'),
  (end_date = '2016-12-03'),
  (importance = '3')
)
  .then((data) => {
    console.log(
      'All calendar events with specific parameters:',
      '\n',
      data,
      '\n'
    )
  })
  .catch((err) => console.log(err))

//===============================================================================================================
//Get all calendar events for specific country (You can pass importance parameter or date parameters (yyyy-mm-dd) for specific data )

te.getCalendar((country = 'united states'))
  .then((data) => {
    console.log(
      'All calendar events for a country/countries:',
      '\n',
      data,
      '\n'
    )
  })
  .catch((err) => console.log(err))

te.getCalendar(
  (country = 'united states'),
  (start_date = '2016-02-01'),
  (end_date = '2016-02-10'),
  (importance = '3')
)
  .then((data) => {
    console.log(
      'Country/countries events with specific parameters:',
      '\n',
      data,
      '\n'
    )
  })
  .catch((err) => console.log(err))

// Note: For multiple countries use country = ['united states', 'china']

//===============================================================================================================
//Get all calendar events for specific indicator (You can pass importance parameter or date parameters (yyyy-mm-dd) for specific data)
te.getCalendar((indicator = 'inflation rate'))
  .then((data) => {
    console.log(
      'All calendar events for a indicator/indicators:',
      '\n',
      data,
      '\n'
    )
  })
  .catch((err) => console.log(err))

te.getCalendar(
  (indicator = 'inflation rate'),
  (start_date = '2016-02-01'),
  (end_date = '2016-02-10'),
  (importance = '2')
)
  .then((data) => {
    console.log('Indicator events with specific parameters:', '\n', data, '\n')
  })
  .catch((err) => console.log(err))

//===============================================================================================================
//Get all calendar events for specific indicator and country (You can pass date parameters (yyyy-mm-dd) for specific data)

te.getCalendar(
  (country = 'united states'),
  (indicator = 'initial jobless claims'),
  (start_date = '2016-12-01'),
  (end_date = '2017-02-25')
)
  .then((data) => {
    console.log('Events for a indicator and country:', '\n', data, '\n')
  })
  .catch((err) => console.log(err))

//===============================================================================================================
//Get all events for specific calendar ID

te.getCalendar((id = ['174108', '160025', '160030']))
  .then(function (data) {
    console.log('Events for a specific ID:', '\n', data, '\n')
  })
  .catch((err) => console.log(err))

//===============================================================================================================
//Get all events for specific ticker/tickers (You can pass date parameters (yyyy-mm-dd) for specific data)

te.getCalendar((ticker = ['IJCUSA', 'SPAINFACORD', 'BAHRAININFNRATE']))
  .then(function (data) {
    console.log('Events for a specific ticker:', '\n', data, '\n')
  })
  .catch((err) => console.log(err))

//===============================================================================================================
//Get all calendar updates

te.getCalendarUpdates()
  .then(function (data) {
    console.log('Last calendar updates:', '\n', data, '\n')
  })
  .catch((err) => console.log(err))

//===============================================================================================================
//Get calendar events for multiple countries filtered by importance and date (date format is yyyy-mm-dd)

async function getCalendarEventsByImportanceDate(
  eventImportance,
  startDate,
  endDate,
  ...countries
) {
  try {
    const data = await te.getCalendar(
      (importance = eventImportance),
      (start_date = startDate),
      (end_date = endDate),
      (country = countries)
    )
    console.log(
      'All calendar events according to the specified parameters:',
      '\n',
      data
    )
  } catch (error) {
    console.log(error)
  }
}
getCalendarEventsByImportanceDate(
  '2',
  '2022-08-01',
  '2022-09-01',
  'south korea',
  'japan'
)
