Manual Quotation
~~~~~~~~~~~~~~~~

To make a manual quotation you must create a quotation, fill in the fields
customer, category, departure date, arrival date, and on the participants tab
load the passengers. After that press **Simulate Quotation** button

Note that the **Simulate Quotation** button is visible only in draft state.


Api REST
~~~~~~~~

**Create a new quotation:**

.. code-block:: html

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


**Validate a quotation:**

.. code-block:: html

    curl -X PUT \
        -H 'API_KEY: 1234567890' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        'http://localhost:8069/insurance/v1/validate/22' \
        -d '{
                "product_id": 1,
                "participants": [
                    {
                        "name":"Juan Carlos Birati",
                        "document":"25324889",
                        "email":"jcbirati@gmail.com",
                        "birth_date":"1970-04-01"
                    },
                    {
                        "name":"Analia Camano",
                        "document":"52478221",
                        "email":"analia.camano@gmail.com",
                        "birth_date":"1958-03-12"
                    },
                    {
                        "name":"Jose Manuel Birati",
                        "document":"34875441",
                        "email":"jmb234@gmail.com",
                        "birth_date":"1966-02-27"
                    }
                ]
            }'
