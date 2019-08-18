Cotizacion Manual
~~~~~~~~~~~~~~~~~

Api REST
~~~~~~~~

Create a new quotation:

curl -X POST \
    -H 'API_KEY: 1234567890' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    'http://localhost:8069/insurance/v1/quotation/create' \
    -d '{
            "category_id": 1,
            "lead_id": 5,
            "departure_date": "2019-02-01",
            "return_date": "2019-03-01",
            "birth_dates": ["1970-04-01","1958-03-12","1966-02-30"]
        }'
