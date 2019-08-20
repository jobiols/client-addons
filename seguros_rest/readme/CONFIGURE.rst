**Install the module**

**Add the key users_to_notify in odoo.conf**

.. code-block:: html

    users_to_notify = user1,user2,user3

is a list with the login names of the users that must be notified when a sales order is entered from the API

**Add the keys rest_api_key and rest_api_user in odoo.conf**

.. code-block:: html

    rest_api_key = my_secret_api_key
    rest_api_user = admin

if these keys are not found odoo will assume the default values, i.e. rest_api_key = 1234567890 rest_api_user = admin
