import json
import requests
from datetime import datetime
from mcp.server.fastmcp import FastMCP
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("Aurora Camp Server")

KNACK_APP_ID = os.getenv("KNACK_APP_ID")
KNACK_API_KEY = os.getenv("KNACK_API_ID")
BASE_URL = f"https://api.knack.com/v1/objects"

CAMPS_OBJECT = "object_6"  
BOOKINGS_OBJECT = "object_7"  
PROVIDERS_OBJECT = "object_5"  
HEADERS = {
    "X-Knack-Application-Id": KNACK_APP_ID,
    "X-Knack-REST-API-Key": KNACK_API_KEY,
    "content-type": "application/json"
}

mcp = FastMCP("Aurora Camp Server (Knack)")


def format_date_range(start_date: str, end_date: str, start_time: str, end_time: str) -> dict:
    """
    Format date range for Knack API
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        start_time: Start time in HH:MM AM/PM format (e.g., "07:00 AM")
        end_time: End time in HH:MM AM/PM format (e.g., "09:00 AM")
    """
    try:
    
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        start_time_obj = datetime.strptime(start_time, "%I:%M %p")
        end_time_obj = datetime.strptime(end_time, "%I:%M %p")
        
        start_formatted = {
            "date": start_dt.strftime("%m/%d/%Y"),
            "hours": start_time_obj.strftime("%I").lstrip("0"),
            "minutes": start_time_obj.strftime("%M"),
            "am_pm": start_time_obj.strftime("%p")
        }
        
        end_formatted = {
            "date": end_dt.strftime("%m/%d/%Y"),
            "hours": end_time_obj.strftime("%I").lstrip("0"),
            "minutes": end_time_obj.strftime("%M"),
            "am_pm": end_time_obj.strftime("%p")
        }
        
        return {
            "date": start_formatted["date"],
            "hours": start_formatted["hours"],
            "minutes": start_formatted["minutes"],
            "am_pm": start_formatted["am_pm"],
            "to": end_formatted
        }
    except Exception as e:
        raise ValueError(f"Error formatting date range: {str(e)}")


@mcp.tool()
def search_camps(category: str = None, min_capacity: int = None, location: str = None) -> str:
    """
    Search for winter camps with optional filters
    
    Args:
        category: Filter by category (Art, Sports, STEM, Nature)
        min_capacity: Minimum capacity
        location: Search by location/city
    """
    try:
        url = f"{BASE_URL}/{CAMPS_OBJECT}/records"
        
        filters = []
        if category:
            filters.append({
                "field": "field_26",
                "operator": "is",
                "value": category
            })
        if min_capacity:
            filters.append({
                "field": "field_28",
                "operator": "is greater than",
                "value": min_capacity
            })
        if location:
            filters.append({
                "field": "field_30",
                "operator": "contains",
                "value": location
            })
        
        params = {}
        if filters:
            params["filters"] = json.dumps(filters)
        
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        
        data = response.json()
        camps = data.get("records", [])
        
        return json.dumps({
            "success": True,
            "found": len(camps),
            "camps": camps
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
def get_camp(camp_name: str) -> str:
    """
    Get detailed information about a specific camp by camp name
    
    Args:
        camp_name: The camp's name
    """
    try:
        url = f"{BASE_URL}/{CAMPS_OBJECT}/records"
        filters = []
        if camp_name:
            filters.append({
                "field":"field_24",
                "operator":"contains",
                "value":camp_name

            })
        params = {}
        params["filters"]=json.dumps(filters)

        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        
        return json.dumps({
            "success": True,
            "camp": response.json()
        }, indent=2)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
def create_camp(
    name: str,
    category: str,
    start_date: str,
    end_date: str,
    start_time: str,
    end_time: str,
    capacity: int,
    location_street: str,
    location_city: str,
    location_state: str,
    location_zip: str,
    provider_id: str,
    description: str,
) -> str:
    """
    Create a new winter camp
    
    Args:
        name: Camp name
        category: Camp category (Art, Sports, STEM, Nature)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        start_time: Start time in HH:MM AM/PM format (e.g., '07:00 AM')
        end_time: End time in HH:MM AM/PM format (e.g., '09:00 PM')
        capacity: Maximum number of participants
        location_street: Street address
        location_city: City
        location_state: State abbreviation
        location_zip: ZIP/Postal code
        provider_id: Provider record ID from Knack
        description: Detailed camp description
    """
    try:
        # Format date range
        date_range = format_date_range(start_date, end_date, start_time, end_time)
        
        # Format location
        location = {
            "street": location_street,
            "city": location_city,
            "state": location_state,
            "zip": location_zip
        }
        
        camp_data = {
            "field_24": name,
            "field_26": category,
            "field_27": date_range,
            "field_28": capacity,
            "field_30": location,
            "field_48": [provider_id],  
            "field_59": 0,  
            "field_60": 0,  
            "field_61": description
        }
        
        url = f"{BASE_URL}/{CAMPS_OBJECT}/records"
        response = requests.post(url, headers=HEADERS, json=camp_data)
        response.raise_for_status()
        
        new_camp = response.json()
        
        return json.dumps({
            "success": True,
            "message": f"Camp '{name}' created successfully!",
            "camp": new_camp
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def update_camp(
    camp_id: str,
    name: str = None,
    category: str = None,
    capacity: int = None,
    description: str = None
) -> str:
    """
    Update an existing camp's information
    
    Args:
        camp_id: The camp ID to update
        name: Camp name
        category: Camp category
        capacity: Maximum participants
        description: Camp description
    """
    try:
        field_mapping = {
            "name": "field_24",
            "category": "field_26",
            "capacity": "field_28",
            "description": "field_61"
        }
        
        update_data = {}
        updates = {
            "name": name,
            "category": category,
            "capacity": capacity,
            "description": description
        }
        
        for key, value in updates.items():
            if value is not None:
                update_data[field_mapping[key]] = value
        
        if not update_data:
            return json.dumps({
                "success": False,
                "error": "No fields to update"
            })
        
        url = f"{BASE_URL}/{CAMPS_OBJECT}/records/{camp_id}"
        response = requests.put(url, headers=HEADERS, json=update_data)
        response.raise_for_status()
        
        return json.dumps({
            "success": True,
            "message": "Camp updated successfully",
            "camp": response.json()
        }, indent=2)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
def delete_camp(camp_id: str) -> str:
    """
    Delete a camp by camp ID
    
    Args:
        camp_id: The camp ID to delete
    """
    try:
        url = f"{BASE_URL}/{CAMPS_OBJECT}/records/{camp_id}"
        response = requests.delete(url, headers=HEADERS)
        response.raise_for_status()
        
        return json.dumps({
            "success": True,
            "message": "Camp deleted successfully"
        }, indent=2)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    
@mcp.tool()
def list_child(camp_name: str) -> str:
    """
    List the number and details of children enrolled based on the camp name

    Args:
        camp_name: Camp name to be searched
    """
    try:
        url = f"{BASE_URL}/{CAMPS_OBJECT}/records"
        filters = []
        if camp_name:
            filters.append({
                "field": "field_24",
                "operator": "contains",
                "value": camp_name
            })
        
        params = {}
        if filters:
            params["filters"] = json.dumps(filters)
        
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        
        data = response.json()
        camps = data.get("records", [])
        
        if not camps:
            return json.dumps({
                "success": False,
                "error": f"No camp found with name containing '{camp_name}'"
            })
        
        camp = camps[0]
        camp_id = camp.get("id")
        camp_full_name = camp.get("field_24", "")
        
        bookings_url = f"{BASE_URL}/{BOOKINGS_OBJECT}/records"
        booking_filters = [{
            "field": "field_32",
            "operator": "is",
            "value": camp_full_name
        }]
        
        booking_params = {"filters": json.dumps(booking_filters)}
        
        booking_response = requests.get(bookings_url, headers=HEADERS, params=booking_params)
        booking_response.raise_for_status()
        
        booking_data = booking_response.json()
        bookings = booking_data.get("records", [])
        
        active_bookings = [b for b in bookings if b.get("field_34") != "Failed"]
        
        # Extracting child details
        children = []
        for booking in active_bookings:
            child_info = {
                "child_name": booking.get("field_49", ""),
                "sibling_discount": booking.get("field_35", ""),
                "booking_date": booking.get("field_33", ""),
                "status": booking.get("field_34", ""),
            }
            children.append(child_info)
        
        return json.dumps({
            "success": True,
            "camp_name": camp_full_name,
            "total_children_enrolled": len(children),
            "children": children
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })

@mcp.tool()
def add_child(
    parent: str,
    child_name: str,
    child_age: int,
    child_date_of_birth: str = "",
    diet_res: str = "",
    emergency_contact: str = "",
) -> str:
    """
    Add a new child to a parent's profile
    
    Args:
        parent: Parent's name to link the child to
        child_name: Child's full name
        diet_res: Any allergies (optional)
        emergency_contact: Emergency contact name (optional)
    """
    try:
        # First, find the parent
        url = f"{BASE_URL}/{PROVIDERS_OBJECT}/records"
        filters = [{
            "field": "field_47",
            "operator": "is",
            "value": parent
        }]
        params = {"filters": json.dumps(filters)}
        
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        
        parents = response.json().get("records", [])
        if not parents:
            return json.dumps({
                "success": False,
                "error": f"No parent found with name '{parent}'. Please add parent first."
            })
        
        parent = parents[0]
        parent_name = parent.get("field_47", "")
        
        # Create child record (assuming there's a children object)
        # If you don't have a separate children object, you might store this differently
        child_data = {
            "field_16": child_name,
            "field_17": diet_res,
            "field_47": parent_name,
            "field_18": emergency_contact,
        }
        
        # Note: Adjust the object ID and field numbers based on your actual Knack setup
        CHILDREN_OBJECT = "object_4"  # Replace with your actual children object ID
        
        url = f"{BASE_URL}/{CHILDREN_OBJECT}/records"
        response = requests.post(url, headers=HEADERS, json=child_data)
        response.raise_for_status()
        
        new_child = response.json()
        
        return json.dumps({
            "success": True,
            "message": f"Child '{child_name}' added successfully to parent '{parent_name}'!",
            "child": new_child,
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })





@mcp.tool()
def get_bookings(camp_id: str) -> str:
    """
    Get all bookings for a specific camp
    
    Args:
        camp_id: Camp record ID
    """
    try:
        url = f"{BASE_URL}/{BOOKINGS_OBJECT}/records"
        
        filters = [{
            "field": "field_32",
            "operator": "is",
            "value": camp_id
        }]
        
        params = {"filters": json.dumps(filters)}
        
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        
        data = response.json()
        bookings = data.get("records", [])
        
        return json.dumps({
            "success": True,
            "count": len(bookings),
            "bookings": bookings
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
def get_camp_availability(camp_id: str) -> str:
    """
    Check available spots for a camp
    
    Args:
        camp_id: Camp record ID
    """
    try:
        camp_result = get_camp(camp_id)
        camp = json.loads(camp_result)
        
        if not camp.get("success"):
            return json.dumps({"success": False, "error": "Camp not found"})
        
        camp_data = camp["camp"]
        capacity = camp_data.get("field_28_raw", 0)
        bookings = camp_data.get("field_60_raw", 0)
        available_spots = capacity - bookings
        
        return json.dumps({
            "success": True,
            "available": available_spots > 0,
            "capacity": capacity,
            "booked": bookings,
            "available_spots": available_spots
        }, indent=2)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


if __name__ == "__main__":
    mcp.run()