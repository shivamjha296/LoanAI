"""
Mock CRM Data for KYC Verification
Contains customer KYC details like phone, address, ID verification status
"""

CRM_DATA = {
    "CUST001": {
        "customer_id": "CUST001",
        "name": "Rajesh Kumar",
        "phone_verified": True,
        "phone": "9876543210",
        "alternate_phone": "9876543200",
        "address": {
            "line1": "Flat 302, Sai Heights",
            "line2": "Andheri West",
            "city": "Mumbai",
            "state": "Maharashtra",
            "pincode": "400058"
        },
        "address_verified": True,
        "pan_verified": True,
        "pan_number": "ABCDE1234F",
        "aadhar_verified": True,
        "aadhar_number": "1234-5678-9012",
        "email_verified": True,
        "kyc_status": "COMPLETED",
        "kyc_completion_date": "2023-06-15"
    },
    "CUST002": {
        "customer_id": "CUST002",
        "name": "Priya Sharma",
        "phone_verified": True,
        "phone": "9876543211",
        "alternate_phone": "9876543201",
        "address": {
            "line1": "House No. 45, Sector 18",
            "line2": "Dwarka",
            "city": "Delhi",
            "state": "Delhi",
            "pincode": "110078"
        },
        "address_verified": True,
        "pan_verified": True,
        "pan_number": "FGHIJ5678K",
        "aadhar_verified": True,
        "aadhar_number": "2345-6789-0123",
        "email_verified": True,
        "kyc_status": "COMPLETED",
        "kyc_completion_date": "2023-08-20"
    },
    "CUST003": {
        "customer_id": "CUST003",
        "name": "Amit Patel",
        "phone_verified": True,
        "phone": "9876543212",
        "alternate_phone": "9876543202",
        "address": {
            "line1": "B-12, Patel Nagar",
            "line2": "Satellite",
            "city": "Ahmedabad",
            "state": "Gujarat",
            "pincode": "380015"
        },
        "address_verified": True,
        "pan_verified": True,
        "pan_number": "KLMNO9012P",
        "aadhar_verified": True,
        "aadhar_number": "3456-7890-1234",
        "email_verified": True,
        "kyc_status": "COMPLETED",
        "kyc_completion_date": "2023-04-10"
    },
    "CUST004": {
        "customer_id": "CUST004",
        "name": "Sunita Verma",
        "phone_verified": True,
        "phone": "9876543213",
        "alternate_phone": "9876543203",
        "address": {
            "line1": "Villa 67, Electronic City",
            "line2": "Phase 1",
            "city": "Bangalore",
            "state": "Karnataka",
            "pincode": "560100"
        },
        "address_verified": True,
        "pan_verified": True,
        "pan_number": "PQRST3456U",
        "aadhar_verified": True,
        "aadhar_number": "4567-8901-2345",
        "email_verified": True,
        "kyc_status": "COMPLETED",
        "kyc_completion_date": "2023-09-05"
    },
    "CUST005": {
        "customer_id": "CUST005",
        "name": "Vikram Singh",
        "phone_verified": True,
        "phone": "9876543214",
        "alternate_phone": "9876543204",
        "address": {
            "line1": "Plot 23, Malviya Nagar",
            "line2": "Near City Palace",
            "city": "Jaipur",
            "state": "Rajasthan",
            "pincode": "302017"
        },
        "address_verified": True,
        "pan_verified": True,
        "pan_number": "UVWXY7890Z",
        "aadhar_verified": True,
        "aadhar_number": "5678-9012-3456",
        "email_verified": True,
        "kyc_status": "COMPLETED",
        "kyc_completion_date": "2023-03-25"
    },
    "CUST006": {
        "customer_id": "CUST006",
        "name": "Neha Gupta",
        "phone_verified": True,
        "phone": "9876543215",
        "alternate_phone": "9876543205",
        "address": {
            "line1": "Flat 501, Jubilee Hills",
            "line2": "Road No. 36",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500033"
        },
        "address_verified": True,
        "pan_verified": True,
        "pan_number": "ABCFG1234H",
        "aadhar_verified": True,
        "aadhar_number": "6789-0123-4567",
        "email_verified": True,
        "kyc_status": "COMPLETED",
        "kyc_completion_date": "2023-07-12"
    },
    "CUST007": {
        "customer_id": "CUST007",
        "name": "Ravi Menon",
        "phone_verified": True,
        "phone": "9876543216",
        "alternate_phone": "9876543206",
        "address": {
            "line1": "House 89, Anna Nagar",
            "line2": "East",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "pincode": "600040"
        },
        "address_verified": True,
        "pan_verified": True,
        "pan_number": "HIJKL5678M",
        "aadhar_verified": True,
        "aadhar_number": "7890-1234-5678",
        "email_verified": True,
        "kyc_status": "COMPLETED",
        "kyc_completion_date": "2023-05-18"
    },
    "CUST008": {
        "customer_id": "CUST008",
        "name": "Anita Desai",
        "phone_verified": True,
        "phone": "9876543217",
        "alternate_phone": "9876543207",
        "address": {
            "line1": "Flat 204, Koregaon Park",
            "line2": "Lane 7",
            "city": "Pune",
            "state": "Maharashtra",
            "pincode": "411001"
        },
        "address_verified": True,
        "pan_verified": True,
        "pan_number": "NOPQR9012S",
        "aadhar_verified": True,
        "aadhar_number": "8901-2345-6789",
        "email_verified": True,
        "kyc_status": "COMPLETED",
        "kyc_completion_date": "2023-10-02"
    },
    "CUST009": {
        "customer_id": "CUST009",
        "name": "Suresh Reddy",
        "phone_verified": True,
        "phone": "9876543218",
        "alternate_phone": "9876543208",
        "address": {
            "line1": "Block C, Salt Lake",
            "line2": "Sector V",
            "city": "Kolkata",
            "state": "West Bengal",
            "pincode": "700091"
        },
        "address_verified": True,
        "pan_verified": True,
        "pan_number": "TUVWX3456Y",
        "aadhar_verified": True,
        "aadhar_number": "9012-3456-7890",
        "email_verified": True,
        "kyc_status": "COMPLETED",
        "kyc_completion_date": "2023-02-28"
    },
    "CUST010": {
        "customer_id": "CUST010",
        "name": "Deepa Nair",
        "phone_verified": False,  # Phone not verified
        "phone": "9876543219",
        "alternate_phone": None,
        "address": {
            "line1": "House 34, Marine Drive",
            "line2": "Ernakulam",
            "city": "Kochi",
            "state": "Kerala",
            "pincode": "682031"
        },
        "address_verified": False,  # Address not verified
        "pan_verified": True,
        "pan_number": "YZABC7890D",
        "aadhar_verified": True,
        "aadhar_number": "0123-4567-8901",
        "email_verified": True,
        "kyc_status": "PARTIAL",  # KYC incomplete
        "kyc_completion_date": None
    },
    "CUST011": {
        "customer_id": "CUST011",
        "name": "Manoj Tiwari",
        "phone_verified": True,
        "phone": "9876543220",
        "alternate_phone": "9876543210",
        "address": {
            "line1": "Bungalow 12, Gomti Nagar",
            "line2": "Extension",
            "city": "Lucknow",
            "state": "Uttar Pradesh",
            "pincode": "226010"
        },
        "address_verified": True,
        "pan_verified": True,
        "pan_number": "DEFGH1234I",
        "aadhar_verified": True,
        "aadhar_number": "1234-8901-2345",
        "email_verified": True,
        "kyc_status": "COMPLETED",
        "kyc_completion_date": "2023-01-15"
    },
    "CUST012": {
        "customer_id": "CUST012",
        "name": "Kavita Joshi",
        "phone_verified": True,
        "phone": "9876543221",
        "alternate_phone": "9876543211",
        "address": {
            "line1": "Plot 78, Vijay Nagar",
            "line2": "Scheme No. 54",
            "city": "Indore",
            "state": "Madhya Pradesh",
            "pincode": "452010"
        },
        "address_verified": True,
        "pan_verified": True,
        "pan_number": "JKLMN5678O",
        "aadhar_verified": True,
        "aadhar_number": "2345-9012-3456",
        "email_verified": True,
        "kyc_status": "COMPLETED",
        "kyc_completion_date": "2023-11-20"
    }
}


def get_kyc_data(customer_id: str) -> dict | None:
    """Retrieve KYC data for a customer from CRM"""
    return CRM_DATA.get(customer_id)


def verify_phone(customer_id: str, phone: str) -> dict:
    """Verify if the phone number matches the customer record"""
    crm_record = CRM_DATA.get(customer_id)
    if not crm_record:
        return {"status": "error", "message": "Customer not found in CRM"}
    
    if crm_record["phone"] == phone:
        return {"status": "success", "verified": True, "message": "Phone number verified successfully"}
    return {"status": "success", "verified": False, "message": "Phone number does not match records"}


def verify_address(customer_id: str, pincode: str) -> dict:
    """Verify if the pincode matches the customer's address record"""
    crm_record = CRM_DATA.get(customer_id)
    if not crm_record:
        return {"status": "error", "message": "Customer not found in CRM"}
    
    if crm_record["address"]["pincode"] == pincode:
        return {"status": "success", "verified": True, "message": "Address verified successfully"}
    return {"status": "success", "verified": False, "message": "Address pincode does not match records"}


def get_kyc_status(customer_id: str) -> dict:
    """Get overall KYC verification status for a customer"""
    crm_record = CRM_DATA.get(customer_id)
    if not crm_record:
        return {"status": "error", "message": "Customer not found in CRM"}
    
    return {
        "status": "success",
        "customer_id": customer_id,
        "name": crm_record["name"],
        "kyc_status": crm_record["kyc_status"],
        "phone_verified": crm_record["phone_verified"],
        "address_verified": crm_record["address_verified"],
        "pan_verified": crm_record["pan_verified"],
        "aadhar_verified": crm_record["aadhar_verified"],
        "email_verified": crm_record["email_verified"]
    }
