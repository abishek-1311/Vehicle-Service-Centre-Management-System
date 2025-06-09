import requests
import json

URL = "http://127.0.0.1:8000"

def create_booking():
    customer_name = input("Enter customer name: ")
    vehicle_number = input("Enter vehicle number: ")
    service_type = input("Enter service type: ")
    booking_date = input("Enter booking date (YYYY-MM-DD): ")
    payload = {
        "customer_name": customer_name,
        "vehicle_number": vehicle_number,
        "service_type": service_type,
        "booking_date": booking_date
    }
    response = requests.post(f"{URL}/bookings/", json=payload)
    print(json.dumps(response.json(),indent=4))
    

def get_all_bookings():
    try:
        response = requests.get(f'{URL}/bookings/get-all')
        print(json.dumps(response.json(),indent=4))

    except Exception as e:
        print(f'Error occured ->{e}')

def get_bookings_ById():
    try:
        booking_id = input('enter booking id:')
        response = requests.get(f'{URL}/bookings/{booking_id}')
        print(json.dumps(response.json(),indent=4))

    except Exception as e:
        print(f'Error Occured ->{e}')

def delete_by_id():
    try:
        booking_id = input('enter booking id:')
        response = requests.delete(f'{URL}/bookings/delete/{booking_id}')
        print(response.json())

    except Exception as e:
        print(f'Error Occured ->{e}')

def update_bookings():
    try:
        booking_id = input('enter booking id:')

        print("just press enter if it doesn't need to update")
        customer_name = input("enter updated customer name: ").strip()
        vehicle_number = input("enter updated vehicle number: ").strip()
        service_type = input("enter updated service type: ").strip()
        booking_date = input("enter updated booking date (YYYY-MM-DD): ").strip()

        update_data = {}
        if customer_name:
            update_data["customer_name"] = customer_name
        if vehicle_number:
            update_data["vehicle_number"] = vehicle_number
        if service_type:
            update_data["service_type"] = service_type
        if booking_date:
            update_data["booking_date"] = booking_date

        if not update_data:
            print("No fields to update. Exiting.")
            return
        
        response = requests.put(f"{URL}/bookings/update/{booking_id}", json=update_data)
        print(json.dumps(response.json(),indent=4))

    except Exception as e:
        print(f'Error Occured ->{e}')


def main():
    while True:
        print("\n Vehicle Service Centre API")
        print("1. create new booking")
        print("2. Get all bookings")
        print("3. Get a booking by ID")
        print("4. Update a booking")
        print("5. Delete a booking")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            create_booking()
        elif choice == "2":
            get_all_bookings()
        elif choice == "3":
            get_bookings_ById()
        elif choice == "4":
            update_bookings()
        elif choice == "5":
            delete_by_id()
        elif choice == "6":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()