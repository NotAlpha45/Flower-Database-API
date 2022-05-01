# Flower-Database-API
 A smiple flower database API with Uvicorn and FastAPI. SQLite3 is the database system.  

## Usage
### To initialize
>python -m uvicorn app:app

By default, uvicorn starts at port 8000. To specify a port (here, port 6969):
>python -m uvicorn app:app --port 6969

To enable reload (for development server):
>python -m uvicorn app:app --reload
### GET Requests
1. Getting a simple message: 
    >/
2. Getting all flowers:
    >/flowers
3. Getting flowers by genus:
    >/flowers/{genus_name}

    Example: `/flowers/lillium`
4. Getting flowers by genus and species
    >/flowers/{genus_name}/{species_name}
    
    Example: `/flowers/lillium/auratum`
5. Getting aggregate results (min, max and avg) of petal count
    >/flowers/{genus_name}/{species_name}/petals/{aggregate_type}

    Example: `/flowers/lillium/auratum/max`, `/flowers/lillium/auratum/avg`

### PUT Requests  
>/flowers

The JSON request body should have the following structure:

    {
        "binomial_nomenclature" : string (NOT NULL),
        "color" : string (NOT NULL),
        "petal_count" : string (NOT NULL)
    }