# Croatian Bank Foriegn Exchange Rates Aggregated RESTfull service#

* Croatian banks havea hodge podge of solutions for publishing their daily exchange rates.
** Fixed length data files
** XML files
** Just web pages

- Built this microservice so we dont have to check all over the place....

For now only the data file based banks (fixed width and XML) are covered, but will do the rest soon.




## Usage

http://fx.autaut.rocks/[bankname|all]

will return the current days data from the bank sites (if any).

# Return format.

```json
{
   "fxdate": {
      "$date": 1426053880719
   },
   "banks": [
      {
         "status": "OK",
         "fetchurl": "http://www.pbz.hr/Downloads/PBZteclist.xml",
         "rates": [
            {
               "sell_exchange": 5.552767,
               "buy_exchange": 5.308987,
               "codenum": "036",
               "sell_cc": 5.608295,
               "middle": 5.417334,
               "multiply": 1,
               "codeiso": "AUD",
               "buy_cc": 5.255897
            },
            {
               "sell_exchange": 5.739910,
               "buy_exchange": 5.487914,
               "codenum": "124",
               "sell_cc": 5.797309,
               "middle": 5.599912,
               "multiply": 1,
               "codeiso": "CAD",
               "buy_cc": 5.433035
            },
            .....
             ],
         "statusdetail": {
            "content-length": "4685",
            "via": "1.0 int21.pbz.hr (squid)",
            "content-location": "http://www.pbz.hr/Downloads/PBZteclist.xml",
            "x-cache": "MISS from int21.pbz.hr",
            "x-powered-by": "ASP.NET",
            "accept-ranges": "bytes",
            "last-modified": "Tue, 10 Mar 2015 17:00:00 GMT",
            "connection": "close",
            "etag": "\"e4e866a5535bd01:d960\"",
            "date": "Wed, 11 Mar 2015 05:36:28 GMT",
            "content-type": "text/xml",
            "x-cache-lookup": "MISS from int21.pbz.hr:8280"
         },
         "bankname": "PBZ"
      }
   ],
   "info": "Croatian Bank Exchange Rates Data - Brought to you by Aut Aut"
}
```
 
