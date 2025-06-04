import os
from dotenv import load_dotenv
import easypost
import requests
from datetime import datetime
import json
import base64
import random

# Load environment variables
load_dotenv()
client = easypost.EasyPostClient(os.getenv("EASYPOST_API_KEY"))


# Carrier account IDs
CARRIER_ACCOUNTS = {
    "FedEx": "ca_e516e5a16b3248acabd34fe7d52e32cf",
    "UPS": "ca_44ae9ed1d77f4d349c82cb1b40903af1",
    "DHL Express": "ca_5e061aecb0f34a51b5781061de6b6dff",
    "DHL eCommerce": "ca_bd6c9fa1565144d19480be61d1ff48f6",
    "USPS": "ca_b9a0c999fddd4132ac8938e8a4d182af"
}

def generate_easypost_label(carrier_account=None):
    """Generate a shipping label using EasyPost API"""
    carrier_name ="EasyPost"
    try:
        # Initialize EasyPost client
        client = easypost.EasyPostClient(os.getenv("EASYPOST_API_KEY"))
        
        # Select appropriate customer, order, and warehouse based on carrier
        if carrier_account == CARRIER_ACCOUNTS["DHL Express"]:
            customer = random.choice(DHL_EXPRESS_CUSTOMERS)
            order = random.choice(DHL_EXPRESS_ORDERS)
            warehouse = DHL_EXPRESS_WAREHOUSE
            print("\nDHL Express Debug Info:")
            print(f"From: {warehouse['street1']}, {warehouse['city']}, {warehouse['state']} {warehouse['zip']} {warehouse['country']}")
            print(f"To: {customer['street1']}, {customer['city']}, {customer['state']} {customer['zip']} {customer['country']}")
            print(f"Package: {order['length']}x{order['width']}x{order['height']} inches, {order['weight']} lbs")
        elif carrier_account == CARRIER_ACCOUNTS["DHL eCommerce"]:
            customer = random.choice(DHL_ECOMMERCE_CUSTOMERS)
            order = random.choice(DHL_ECOMMERCE_ORDERS)
            warehouse = WAREHOUSE_ADDRESS
            print("\nDHL eCommerce Debug Info:")
            print(f"From: {warehouse['street1']}, {warehouse['city']}, {warehouse['state']} {warehouse['zip']} {warehouse['country']}")
            print(f"To: {customer['street1']}, {customer['city']}, {customer['state']} {customer['zip']} {customer['country']}")
            print(f"Package: {order['length']}x{order['width']}x{order['height']} inches, {order['weight']} lbs")
        elif carrier_account == CARRIER_ACCOUNTS["USPS"]:
            customer = random.choice(SAMPLE_CUSTOMERS)
            order = random.choice(SAMPLE_ORDERS)
            warehouse = WAREHOUSE_ADDRESS
            print("\nUSPS Debug Info:")
            print(f"From: {warehouse['street1']}, {warehouse['city']}, {warehouse['state']} {warehouse['zip']} {warehouse['country']}")
            print(f"To: {customer['street1']}, {customer['city']}, {customer['state']} {customer['zip']} {customer['country']}")
            print(f"Package: {order['length']}x{order['width']}x{order['height']} inches, {order['weight']} lbs")
        elif carrier_account == CARRIER_ACCOUNTS["UPS"]:
            customer = random.choice(SAMPLE_CUSTOMERS)
            order = random.choice(SAMPLE_ORDERS)
            warehouse = WAREHOUSE_ADDRESS
            print("\nUPS Debug Info:")
            print(f"From: {warehouse['street1']}, {warehouse['city']}, {warehouse['state']} {warehouse['zip']} {warehouse['country']}")
            print(f"To: {customer['street1']}, {customer['city']}, {customer['state']} {customer['zip']} {customer['country']}")
            print(f"Package: {order['length']}x{order['width']}x{order['height']} inches, {order['weight']} lbs")
        else:
            customer = random.choice(SAMPLE_CUSTOMERS)
            order = random.choice(SAMPLE_ORDERS)
            warehouse = WAREHOUSE_ADDRESS
        
        # Create from address (warehouse)
        from_address = client.address.create(
            name=warehouse["name"],
            company=warehouse["company"],
            street1=warehouse["street1"],
            city=warehouse["city"],
            state=warehouse["state"],
            zip=warehouse["zip"],
            country=warehouse["country"],
            phone=warehouse["phone"],
            email=warehouse.get("email", "")  # Use get() to handle cases where email might not be present
        )

        # Create to address (customer)
        to_address = client.address.create(
            name=customer["name"],
            company=customer["company"],
            street1=customer["street1"],
            street2=customer.get("street2", ""),
            city=customer["city"],
            state=customer["state"],
            zip=customer["zip"],
            country=customer["country"],
            phone=customer["phone"],
            email=customer["email"]
        )

        # Create parcel
        parcel = client.parcel.create(
            length=order["length"],
            width=order["width"],
            height=order["height"],
            weight=order["weight"]
        )

        # Create shipment with optional carrier account
        shipment_params = {
            "from_address": from_address,
            "to_address": to_address,
            "parcel": parcel
        }
        
        if carrier_account:
            shipment_params["carrier_accounts"] = [carrier_account]
            carrier_name = next((name for name, id in CARRIER_ACCOUNTS.items() if id == carrier_account), "Custom Carrier")
        else:
            carrier_name = "EasyPost Default"

        # Add customs info for DHL Express international shipments
        if carrier_account == CARRIER_ACCOUNTS["DHL Express"]:
            customs_info = client.customs_info.create(
                contents_type="merchandise",
                contents_explanation="Electronics and clothing",
                customs_items=[
                    client.customs_item.create(
                        description=item["description"],
                        quantity=item["quantity"],
                        value=item["value"],
                        weight=item["weight"],
                        origin_country=item["origin_country"],
                        hs_tariff_number=item["hs_tariff_number"]
                    ) for item in order["contents"]
                ]
            )
            shipment_params["customs_info"] = customs_info

        try:
            shipment = client.shipment.create(**shipment_params)
        except Exception as e:
            print(f"\nError creating shipment: {str(e)}")
            if carrier_name == "DHL Express":
                print("DHL Express shipment creation failed. This might be due to:")
                print("1. Invalid carrier account configuration")
                print("2. Address verification issues")
                print("3. Package dimensions outside DHL Express limits")
            elif carrier_name == "DHL eCommerce":
                print("DHL eCommerce shipment creation failed. This might be due to:")
                print("1. Invalid carrier account configuration")
                print("2. Package dimensions outside DHL eCommerce limits")
                print("3. Service area restrictions")
            return None

        # Get available rates
        try:
            rates = shipment.rates
            if not rates:
                print(f"\nNo rates found for {carrier_name}")
                if carrier_name == "DHL Express":
                    print("This might be because:")
                    print("1. The route is not serviced by DHL Express")
                    print("2. The package dimensions are outside DHL Express limits")
                    print("3. The carrier account needs additional configuration")
                elif carrier_name == "DHL eCommerce":
                    print("This might be because:")
                    print("1. The route is not serviced by DHL eCommerce")
                    print("2. The package dimensions are outside DHL eCommerce limits")
                    print("3. The carrier account needs additional configuration")
                    print("4. The service level is not available for this route")
                return None
        except Exception as e:
            print(f"\nError getting rates: {str(e)}")
            return None

        # Print available rates
        print(f"\nAvailable {carrier_name} rates:")
        for rate in rates:
            print(f"- {rate.service}: ${rate.rate} ({rate.delivery_days} days)")

        # For DHL Express, try to find specific service levels
        if carrier_name == "DHL Express":
            # Try to find DHL Express Worldwide or similar service
            dhl_rates = [rate for rate in rates if "Worldwide" in rate.service or "Express" in rate.service]
            if dhl_rates:
                selected_rate = dhl_rates[0]  # Take the first matching rate
                print(f"\nSelected DHL Express rate: {selected_rate.service} - ${selected_rate.rate}")
            else:
                selected_rate = shipment.lowest_rate()
                print(f"\nNo specific DHL Express service found, using lowest rate: {selected_rate.service}")
        elif carrier_name == "DHL eCommerce":
            # Try to find DHL eCommerce specific services
            dhl_ecomm_rates = [rate for rate in rates if "eCommerce" in rate.service or "Parcel" in rate.service]
            if dhl_ecomm_rates:
                selected_rate = dhl_ecomm_rates[0]  # Take the first matching rate
                print(f"\nSelected DHL eCommerce rate: {selected_rate.service} - ${selected_rate.rate}")
            else:
                selected_rate = shipment.lowest_rate()
                print(f"\nNo specific DHL eCommerce service found, using lowest rate: {selected_rate.service}")
        else:
            selected_rate = shipment.lowest_rate()
            print(f"\nSelected {carrier_name} rate: {selected_rate.service} - ${selected_rate.rate}")

        # Buy the label using the selected rate
        try:
            client.shipment.buy(shipment.id, rate=selected_rate)
        except Exception as e:
            print(f"\nError buying rate: {str(e)}")
            return None

        # Print the label URL for direct download
        print(f"\n{carrier_name} Label URL: {shipment.postage_label.label_url}")
        print("You can download the label directly from this URL\n")

        # Save the label as PNG
        label_path = f"labels/{carrier_name.lower().replace(' ', '_')}_{order['order_id']}.png"
        os.makedirs("labels", exist_ok=True)
        
        # Download the label with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'image/png'
        }
        response = requests.get(shipment.postage_label.label_url, headers=headers)
        
        if response.status_code == 200:
            with open(label_path, "wb") as f:
                f.write(response.content)
            print(f"{carrier_name} label saved successfully: {label_path}")
            return label_path
        else:
            print(f"Error downloading {carrier_name} label: HTTP {response.status_code}")
            return None

    except Exception as e:
        print(f"Error generating {carrier_name} label: {str(e)}")
        return None

def get_fedex_oauth_token():
    """Get OAuth token from FedEx"""
    try:
        url = "https://apis-sandbox.fedex.com/oauth/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": os.getenv('FEDEX_API_KEY'),
            "client_secret": os.getenv('FEDEX_API_SECRET')
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"Error getting FedEx OAuth token: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error getting FedEx OAuth token: {str(e)}")
        return None

def generate_fedex_label():
    """Generate a shipping label using FedEx API through EasyPost"""
    return generate_easypost_label(carrier_account=CARRIER_ACCOUNTS["FedEx"])

def generate_ups_label():
    """Generate a shipping label using UPS API through EasyPost"""
    return generate_easypost_label(carrier_account=CARRIER_ACCOUNTS["UPS"])

def generate_dhl_label():
    """Generate a shipping label using DHL Express API through EasyPost"""
    return generate_easypost_label(carrier_account=CARRIER_ACCOUNTS["DHL Express"])

def generate_ryder_label():
    """Generate a shipping label using Ryder/Whiplash API"""
    print("Ryder/Whiplash integration temporarily disabled - waiting for correct API endpoint")
    return None

def generate_dhl_ecommerce_label():
    """Generate a shipping label using DHL eCommerce API through EasyPost with specific handling"""
    try:
        # Initialize EasyPost client
        client = easypost.EasyPostClient(os.getenv("EASYPOST_API_KEY"))
        
        # Select customer and order
        customer = random.choice(DHL_ECOMMERCE_CUSTOMERS)
        order = random.choice(DHL_ECOMMERCE_ORDERS)
        warehouse = WAREHOUSE_ADDRESS
        
        print("\nDHL eCommerce Debug Info:")
        print(f"From: {warehouse['street1']}, {warehouse['city']}, {warehouse['state']} {warehouse['zip']} {warehouse['country']}")
        print(f"To: {customer['street1']}, {customer['city']}, {customer['state']} {customer['zip']} {customer['country']}")
        print(f"Package: {order['length']}x{order['width']}x{order['height']} inches, {order['weight']} lbs")
        
        # Validate package dimensions
        if order['weight'] > 70:  # DHL eCommerce weight limit
            print("Error: Package weight exceeds DHL eCommerce limit of 70 lbs")
            return None
            
        if order['length'] > 48 or order['width'] > 48 or order['height'] > 48:  # DHL eCommerce dimension limit
            print("Error: Package dimensions exceed DHL eCommerce limit of 48 inches")
            return None
            
        # Create from address (warehouse) with email
        try:
            from_address = client.address.create(
                name=warehouse["name"],
                company=warehouse["company"],
                street1=warehouse["street1"],
                city=warehouse["city"],
                state=warehouse["state"],
                zip=warehouse["zip"],
                country=warehouse["country"],
                phone=warehouse["phone"],
                email=warehouse["email"]
            )
        except Exception as e:
            print(f"Error creating from address: {str(e)}")
            return None

        # Create to address (customer)
        try:
            to_address = client.address.create(
                name=customer["name"],
                company=customer["company"],
                street1=customer["street1"],
                street2=customer.get("street2", ""),
                city=customer["city"],
                state=customer["state"],
                zip=customer["zip"],
                country=customer["country"],
                phone=customer["phone"],
                email=customer["email"]
            )
        except Exception as e:
            print(f"Error creating to address: {str(e)}")
            return None

        # Create parcel with DHL eCommerce specific validation
        try:
            parcel = client.parcel.create(
                length=order["length"],
                width=order["width"],
                height=order["height"],
                weight=order["weight"]
            )
        except Exception as e:
            print(f"Error creating parcel: {str(e)}")
            return None

        # Create customs info for DHL eCommerce
        try:
            customs_info = client.customs_info.create(
                contents_type="merchandise",
                contents_explanation="Electronics and clothing",
                customs_items=[
                    client.CustomsItem.create(
                        description=item["description"],
                        quantity=item["quantity"],
                        value=item["value"],
                        weight=item["weight"],
                        origin_country=item["origin_country"],
                        hs_tariff_number=item["hs_tariff_number"],
                        code=item["code"],
                        manufacturer=item["manufacturer"]
                    ) for item in order["contents"]
                ]
            )
        except Exception as e:
            print(f"Error creating customs info: {str(e)}")
            return None

        # Create shipment with DHL eCommerce specific parameters
        try:
            shipment = client.shipment.create(
                from_address=from_address,
                to_address=to_address,
                parcel=parcel,
                customs_info=customs_info,
                carrier_accounts=[CARRIER_ACCOUNTS["DHL eCommerce"]],
                service="ParcelSelect",  # Specify DHL eCommerce service level
                options={
                    "merchant_id": "Y5238D"  # Add merchant ID for DHL eCommerce
                }
            )
        except Exception as e:
            print(f"Error creating shipment: {str(e)}")
            print("Possible reasons:")
            print("1. Invalid carrier account configuration")
            print("2. Service level not available for this route")
            print("3. Address validation failed")
            return None

        # Get available rates with specific error handling
        try:
            rates = shipment.rates
            if not rates:
                print("\nNo rates found for DHL eCommerce")
                print("Possible reasons:")
                print("1. The route is not serviced by DHL eCommerce")
                print("2. The service level is not available for this route")
                print("3. The carrier account needs additional configuration")
                return None
        except Exception as e:
            print(f"Error getting rates: {str(e)}")
            return None

        # Print available rates
        print("\nAvailable DHL eCommerce rates:")
        for rate in rates:
            print(f"- {rate.service}: ${rate.rate} ({rate.delivery_days} days)")

        # Select appropriate rate
        try:
            # Try to find DHL eCommerce specific services
            dhl_ecomm_rates = [rate for rate in rates if "eCommerce" in rate.service or "Parcel" in rate.service]
            if dhl_ecomm_rates:
                selected_rate = dhl_ecomm_rates[0]
                print(f"\nSelected DHL eCommerce rate: {selected_rate.service} - ${selected_rate.rate}")
            else:
                selected_rate = shipment.lowest_rate()
                print(f"\nNo specific DHL eCommerce service found, using lowest rate: {selected_rate.service}")
        except Exception as e:
            print(f"Error selecting rate: {str(e)}")
            return None

        # Buy the label
        try:
            bought_shipment = client.shipment.buy(shipment.id, rate=selected_rate)
            if not bought_shipment or not bought_shipment.postage_label:
                print("Failed to purchase shipment or retrieve label.")
                return None
            label_url = bought_shipment.postage_label.label_url
            return label_url
        except Exception as e:
            print(f"Error buying rate: {str(e)}")
            return None

        # Print the label URL
        print(f"\nDHL eCommerce Label URL: {shipment.postage_label.label_url}")
        print("You can download the label directly from this URL\n")

        # Save the label
        label_path = f"labels/dhl_ecommerce_{order['order_id']}.png"
        os.makedirs("labels", exist_ok=True)
        
        # Download the label
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'image/png'
        }
        response = requests.get(shipment.postage_label.label_url, headers=headers)
        
        if response.status_code == 200:
            with open(label_path, "wb") as f:
                f.write(response.content)
            print(f"DHL eCommerce label saved successfully: {label_path}")
            return label_path
        else:
            print(f"Error downloading DHL eCommerce label: HTTP {response.status_code}")
            return None

    except Exception as e:
        print(f"Error generating DHL eCommerce label: {str(e)}")
        return None

def generate_usps_label():
    """Generate a shipping label using USPS API through EasyPost"""
    return generate_easypost_label(carrier_account=CARRIER_ACCOUNTS["USPS"])

def main():
    # Create labels directory if it doesn't exist
    os.makedirs("labels", exist_ok=True)

    # Generate labels
    print("Generating shipping labels...")
    easypost_label = generate_easypost_label()  # Default carrier
    fedex_label = generate_fedex_label()  # FedEx through EasyPost
    ups_label = generate_ups_label()  # UPS through EasyPost
    dhl_label = generate_dhl_label()  # DHL Express through EasyPost
    dhl_ecomm_label = generate_dhl_ecommerce_label()  # DHL eCommerce through EasyPost
    usps_label = generate_usps_label()  # USPS through EasyPost
    ryder_label = generate_ryder_label()

if __name__ == "__main__":
    main() 