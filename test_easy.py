
import easypost

easypost.api_key = "EZTK25f033c95dfe448787b5d796ba12a7beMvT4Iv90oIvcI70msNq8jg"

shipment = easypost.Shipment.create(
    to_address={
        "name": "Jane Doe",
        "street1": "123 Main St",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94105",
        "country": "US",
        "phone": "415-123-4567"
    },
    from_address={
        "name": "Warehouse",
        "street1": "456 Warehouse Rd",
        "city": "Oakland",
        "state": "CA",
        "zip": "94607",
        "country": "US",
        "phone": "510-987-6543"
    },
    parcel={
        "length": 10,
        "width": 8,
        "height": 4,
        "weight": 16
    }
)

print(shipment)
