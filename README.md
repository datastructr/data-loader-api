# data-loader-api

The main purpose for the _data-loader-api_ is to allow for a dynamic frontend client to interact with a powerful, yet lightweight, backend API.

The upload process will have capabilities to read and write to any schema that the API is configured with.  

Based on shear fact that data ingestion, at it's core is a pain - we are out to solve a complex problem with a simple solution. The backend RESTful API will make for a fast and efficient way for client applications to send and recieve data from multiple endpoints.

## Configurations

* Python 3.5+
* PostgreSQL

## Features

* Three Endpoints
    1. A specific table's schema - the _table_name_ passed through the URL
    2. A full database's schema (all tables with their unique schemas)
    3. A upload endpoint that will take a specifically structure JSON Object that will be sent through from the client application.

## Future Iteration Features

- [ ] Securing and validating the ingestion data
- [ ] Inserting the full respected data "post" check constraints/validation
- [ ] Allowing for multiple database connections
- [ ] JSON Web Token authentication (right now we are leaving client-side developers handle authentication)
