from fastapi import FastAPI, Depends
import uvicorn
from sqlalchemy.orm import Session
from models import Leads, get_db
import requests

app = FastAPI(title="Suite crm demo")


@app.get("/leads/")
async def read_leads(
        db: Session = Depends(get_db),
):
    leads = db.query(Leads).all()
    return leads


def fetch_lead_list() -> list:
    import json
    import hashlib
    import urllib.request


    # Login to suitecrmdemo
    encode = hashlib.md5("Demo".encode('utf-8'))
    encoded_password = encode.hexdigest()
    args = {'user_auth': {'user_name': 'Demo', 'password': encoded_password}}
    crmUrl = 'https://suitecrmdemo.dtbc.eu/service/v4/rest.php'
    data = json.dumps(args)
    args = {'method': 'login', 'input_type': 'json',
            'response_type': 'json', 'rest_data': data}
    params = urllib.parse.urlencode(args).encode('utf-8')
    response = urllib.request.urlopen(crmUrl, params)
    data = json.load(response)
    session_id = data["id"]


    response = requests.post(crmUrl, data={
        'method': 'get_entry_list',
        'input_type': 'JSON',
        'response_type': 'JSON',
        'rest_data': f'{{"session": "{session_id}", "module_name": "Leads", "query": "", "order_by": "", "offset": 0, "select_fields": ["phone_work", "first_name", "last_name"], "link_name_to_fields_array": [], "max_results": 200, "deleted": 0}}'
    })

    leads = response.json()['entry_list']
    lead_list = list()
    for lead in leads:
        phone_work = lead['name_value_list']['phone_work']['value']
        first_name = lead['name_value_list']['first_name']['value']
        last_name = lead['name_value_list']['last_name']['value']
        lead_dict = {"phone_work": phone_work, "first_name": first_name, "last_name": last_name}
        lead_obj = Leads(**lead_dict)
        lead_list.append(lead_obj)

    return lead_list


@app.post("/leads/")
async def collect_leads(
    db: Session = Depends(get_db),
):
    lead_list = fetch_lead_list()
    # Add the prices to the session
    db.add_all(lead_list)
    # Commit the session to save the prices to the database
    db.commit()
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True, workers=2)
