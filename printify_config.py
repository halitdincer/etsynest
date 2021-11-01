# DYNAMIC CONFIG

# Printify API KEY
PRINTIFY_API_KEY="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjAwZmNiMjJkZDE2YjRkYmFjZThkMTVhZGExMWY5ZWM3ZGVkMGY5OWI3YjEzNDZmYTlmMGVmMzlkMWFlNzNiZGUwY2M3ZmI5Y2MxZTRhYjcyIn0.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6IjAwZmNiMjJkZDE2YjRkYmFjZThkMTVhZGExMWY5ZWM3ZGVkMGY5OWI3YjEzNDZmYTlmMGVmMzlkMWFlNzNiZGUwY2M3ZmI5Y2MxZTRhYjcyIiwiaWF0IjoxNjA4NTgyODY1LCJuYmYiOjE2MDg1ODI4NjUsImV4cCI6MTY0MDExODg2NSwic3ViIjoiNzIyMzI2NiIsInNjb3BlcyI6WyJzaG9wcy5tYW5hZ2UiLCJzaG9wcy5yZWFkIiwiY2F0YWxvZy5yZWFkIiwib3JkZXJzLnJlYWQiLCJvcmRlcnMud3JpdGUiLCJwcm9kdWN0cy5yZWFkIiwicHJvZHVjdHMud3JpdGUiLCJ3ZWJob29rcy5yZWFkIiwid2ViaG9va3Mud3JpdGUiLCJ1cGxvYWRzLnJlYWQiLCJ1cGxvYWRzLndyaXRlIiwicHJpbnRfcHJvdmlkZXJzLnJlYWQiXX0.Ac2LrBveIhJO9tt7WaTDHaf8GbmIUeg3BwBy8SeCY9uG-t2jxSgjcGwM_DdYqJwrGy80HkPCwOHRAZmlyRQ"

# Printify Shop ID
PRINTIFY_SHOP_ID = "1820622"

# STATIC CONFIG

# Printify Shop URL
PRINTIFY_URL = "https://api.printify.com/v1/shops/"+ PRINTIFY_SHOP_ID+ "/"

# Printify API Status Codes
PRINTIFY_STATUS = {
    'in-production' : "In Production",
    'has-issues' : "Has Issues",
    'pending' : "Pending",
    'fulfilled' : "Fulfilled",
    'canceled' : "Canceled",
    'partially-fulfilled' : "Partially Fulfilled",
    'on-hold': "On Hold",
    'checking-quality' : 'Checking Quality',
    'quality-declined' : "Quality Declined",
    'quality-approved' : "Quality Approved",
    'ready-for-production' : "Ready for Production",
    'payment-not-received' : "Payment Not Received",
    'callback-received' : "Callback Received",
}
# Printify API Provider Codes
PRINTIFY_PROVIDERS = {
    26: 'Textildruck Europa</br>',
    41: 'Duplium</br>',
    29: 'Monster Digital</br>',
    37: 'Big Oven Tees United States</br>',
    38: 'Big Oven Tees Canada</br>',
    16: 'MyLocker</br>',
    45: 'Awkward Styles</br>',
    6: 'T-shirt and Sons</br>',
    3: 'The Dream Junction</br>',
    42: 'Drive Fulfillment</br>',
    52: 'Stakes Manufacturing</br>',
    39: 'SwiftPOD</br>',
    27: 'PrintGeek</br>',
}