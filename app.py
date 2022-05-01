#  - GET / that returns some kind of Hello World message: it could be an introduction the dataset, a rough description, etc.
#  - PUT /flowers that takes a Flower and stores it in the database (that you need to create as well)
#  - GET /flowers that takes no parameters and returns all Flowers currently in the database
#  - GET /flowers/{genus} that takes a genus of flower and returns all observations of that genus
#  - GET /flowers/{genus}/{species} that takes a species of flower and returns all observations of that species
#  - GET /flowers/{genus}/{species}/petals/avg that takes a species of flower and returns the average petal count across observations
#  - GET /flowers/{genus}/{species}/petals/min that takes a species of flower and returns the minimum petal count across observations
#  - GET /flowers/{genus}/{species}/petals/max that takes a species of flower and returns the maximum petal count across observations

# A Flower should only be accepted with
# - its binomial nomenclature (Genus species, with Genus being capitalized, a space, and then species) as a string
# - a count of how many petals observed (positive integers and 0)
# - a color as a string

import sqlite3
from fastapi import FastAPI, HTTPException, Request


cursor = sqlite3.connect("flowers.db")


def get_col_names():
    '''
    Fetches the column name from the description of the cursor when a
    query has been executed. \n
    The column name is the first data in the description.
    '''
    return [colname[0] for colname in cursor.execute(
        f'''
        SELECT * FROM Flowers LIMIT 1;
        '''
    ).description]


# Formatting the query result in the structure intended.
def response_formatter(query_result):
    '''
    This converts the query result produced by SQLite3 (List of Tuples)
    into List of dictionaries, as the response intends. 
    '''
    response_list = []
    colnames = get_col_names()

    # Convert the query result into a list of dictionary,
    # just like the response structure shown.
    for result in query_result:
        result_dict = dict()

        for index in range(len(result)):
            result_dict[colnames[index]] = result[index]

        response_list.append(result_dict)

    return response_list


# Note, to deploy, use python -m uvicorn app:app --reload
app = FastAPI()


@app.get('/')
async def get_root():
    return {
        "Hello": "World"
    }


@app.get('/flowers')
async def get_all_flowers():
    '''
    A simple query from Flowers table
    '''
    query_result = cursor.execute(
        '''SELECT * FROM Flowers'''
    ).fetchall()
    print(query_result)
    response = response_formatter(query_result)

    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get('/flowers/{genus}')
async def get_all_flowers(genus):
    '''
    In any request, we can send path parameters (In This case it is genus).
    This function makes queries according to the path parameters.
    '''
    query_result = cursor.execute(
        f'''SELECT * FROM Flowers WHERE genus=?''',
        [genus]
    ).fetchall()

    response = response_formatter(query_result)

    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get('/flowers/{genus}/{species}')
async def get_all_flowers(genus, species):

    '''
    In any request, we can send path parameters (In This case it is genus and species).
    This function makes queries according to the path parameters.
    '''

    query_result = cursor.execute(
        f'''SELECT * FROM Flowers 
            WHERE genus=? AND species = ?''',
        [genus, species]
    ).fetchall()

    response = response_formatter(query_result)

    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get('/flowers/{genus}/{species}/petals/{aggregation_type}')
async def get_aggregate_result(genus, species, aggregation_type):
    '''
    MAX, MIN and AVERAGE are aggregate function. We can utilize a single function
    If we take in the aggregation type as a URL or path parameter.
    '''
    if aggregation_type.lower() == "avg":
        return cursor.execute(
            f'''SELECT AVG(petal_count) FROM Flowers 
            WHERE genus=? AND species = ?''',
            [genus, species]
        ).fetchall()[0][0]

    if aggregation_type.lower() == "min":
        return cursor.execute(
            f'''SELECT MIN(petal_count) FROM Flowers 
            WHERE genus=? AND species = ?''',
            [genus, species]
        ).fetchall()[0][0]

    if aggregation_type.lower() == "max":
        return cursor.execute(
            f'''SELECT MAX(petal_count) FROM Flowers 
            WHERE genus=? AND species = ?''',
            [genus, species]
        ).fetchall()[0][0]


@app.put('/flowers')
async def put_flower(flower_data: Request):
    '''
    PUT request sends a Request body alongside the path.\n
    The Request class or datatype needs to be explicitly mentioned here.\n
    The Request body may come asynchronusly, therefore, we need to lock thread
    with await to confirm the arrival of Request body.

    '''
    flower_data = await flower_data.json()

    flower_id_sequence = cursor.execute(
        '''
        SELECT MAX(flower_id) FROM Flowers
        '''
    ).fetchall()[0][0]

    if flower_id_sequence is None:
        flower_id_sequence = 0

    flower_id = flower_id_sequence + 1

    # Segmenting out the first and second section of the binomial nominclature
    flower_nomiclature = flower_data["binomial_nomenclature"].split()
    flower_genus = flower_nomiclature[0]
    flower_species = flower_nomiclature[1]
    flower_color = flower_data['color']
    flower_petal_count = int(flower_data['petal_count'])

    cursor.execute(
        '''
        INSERT INTO Flowers
        VALUES (?, ?, ?, ?, ?)
        ''',
        [flower_id, flower_genus, flower_species, flower_petal_count, flower_color]
    )
    cursor.commit()

    return flower_data
