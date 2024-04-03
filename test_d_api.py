import logging
import json
from flask.testing import FlaskClient
import pytest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

decoder_endpoint_v1="/api/v1/decoder/"

def common_assertions_for200(response,expected_code,expected_key,expected_value):
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    logger.debug(json.loads(response.data))

    json_payload = json.loads(response.data)
    assert json_payload['data'] is not None
    assert json_payload['data']['parameters'] is not None
    assert len(json_payload['data']['parameters']) > 0

    parameters = json_payload['data']['parameters']
    body_type = None
    for parameter in parameters:
        logger.debug(f"{parameter['code']}\t: {parameter['value']}")
        if parameter['code'] == expected_code:
            body_type = parameter
            break

    assert body_type is not None
    assert body_type['value'] == expected_value
    assert body_type['key'] == expected_key
   
    
def common_assertions_for400(response,error_value,error_messsage):
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    logger.debug(json.loads(response.data))

    json_payload = json.loads(response.data)
    assert json_payload['errors'] is not None
    assert len(json_payload['errors']) > 0
    assert json_payload['errors'][0]['error_code'] == error_value
    assert json_payload['errors'][0]['error_description'] == error_messsage
    
    def api_request(client: FlaskClient, model: str, varcod: str, expected_code: str, expected_key: str, expected_value: str, error_value: int = None, error_message: str = None):
    data = {
        "model": model,
        "varcod": varcod
    }

    headers = {'Content-Type': 'application/json'}  
     # Debugging print statements
    #print(f"URL: {decoder_endpoint_v1}")
    #print(f"Headers: {headers}")
    #print(f"Data: {data}")
    
    response = client.post(decoder_endpoint_v1, json=data, headers=headers)
    
    #print(f"Response Status Code: {response.status_code}")
    #print(f"Response Data: {response.data}")
       
    if response.status_code == 200:
        common_assertions_for200(response, expected_code, expected_key, expected_value)
    elif response.status_code == 400:
        common_assertions_for400(response, error_value, error_message)
    else:
        raise ValueError("Invalid expected_status value. Use 200 or 400.")
    
def api_forEmptyrequest(client: FlaskClient, error_value:int, error_messsage:str):
    headers = {'Content-Type': 'application/json'}
    response = client.post(decoder_endpoint_v1, json={}, headers=headers)
    common_assertions_for400(response,error_value,error_messsage)   
    

def test_api_it_should_be_c_model(client: FlaskClient):
   api_request(client, "C", "0000000000000000000000000000000000000000000000000000000000000000", 'VEHICLE_BODY_TYPE','C', '1')


def test_api_it_should_return_invalid_model_error(client: FlaskClient):
    api_request(client,"S", "0000000000000000000000000000000000000000000000000000000000000000",None, None, None,8001,"Invalid model value.")

def test_api_it_should_return_invalid_model_varcod_value_is_null(client: FlaskClient):
    api_request(client,"CSU", "",None, None, None,8102,"Model varcod is null.")

def test_api_it_should_return_invalid_model_value_is_null(client: FlaskClient):
    api_request(client,"", "0000000000000000000000000000000000000000000000000000000000000000",None, None, None,8101,"Model value is null.")
        
def test_api_it_should_return_invalid_for_emty_request(client: FlaskClient):
    api_forEmptyrequest(client,8101,"Model value is null.")   

    
def test_api_it_should_be_market_name_is_Turkiye(client: FlaskClient):
    api_request(client, "C", "00000000000000000000000000000000000000000000000000000000000000004700", 'MARKET_NAME','TURKIYE','198')    
 
               
