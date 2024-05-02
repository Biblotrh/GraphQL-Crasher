# GraphQL-Crasher
Example of code to crash MovieStarPlanet2 microservices/servers using GraphQl vulnerabilities

# Disclaimer: Educational Use Only

The code logging into a MovieStarPlanet2 account and executing a GraphQL query to retrieve the top User-Generated Contents (UGCs). The original query has a limit of 500 items per pageIndex. By utilizing aliases, the query can be duplicated to fetch over 5,000 UGCs in a single request and makes the server overload.
/!\ Therefore, this code should not be used for exploiting APIs or causing disruptions to services.
