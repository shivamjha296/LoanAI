"""
Synthetic Customer Data for BFSI Loan Chatbot
Contains details for 10+ customers including name, age, city, current loans, credit score, and pre-approved limits
"""

CUSTOMERS = {
    "CUST001": {
        "customer_id": "CUST001",
        "name": "Rajesh Kumar",
        "age": 35,
        "city": "Mumbai",
        "phone": "9876543210",
        "email": "rajesh.kumar@email.com",
        "pan_number": "ABCDE1234F",
        "aadhar_number": "1234-5678-9012",
        "occupation": "Software Engineer",
        "employer": "TCS",
        "monthly_salary": 85000,
        "current_loans": [
            {"type": "Home Loan", "amount": 2500000, "emi": 22000, "remaining_tenure": 180}
        ],
        "credit_score": 780,
        "pre_approved_limit": 500000,
        "account_number": "SBI1234567890",
        "bank_name": "State Bank of India"
    },
    "CUST002": {
        "customer_id": "CUST002",
        "name": "Priya Sharma",
        "age": 28,
        "city": "Delhi",
        "phone": "9876543211",
        "email": "priya.sharma@email.com",
        "pan_number": "FGHIJ5678K",
        "aadhar_number": "2345-6789-0123",
        "occupation": "Marketing Manager",
        "employer": "Infosys",
        "monthly_salary": 95000,
        "current_loans": [],
        "credit_score": 820,
        "pre_approved_limit": 750000,
        "account_number": "HDFC9876543210",
        "bank_name": "HDFC Bank"
    },
    "CUST003": {
        "customer_id": "CUST003",
        "name": "Amit Patel",
        "age": 42,
        "city": "Ahmedabad",
        "phone": "9876543212",
        "email": "amit.patel@email.com",
        "pan_number": "KLMNO9012P",
        "aadhar_number": "3456-7890-1234",
        "occupation": "Business Owner",
        "employer": "Self Employed",
        "monthly_salary": 150000,
        "current_loans": [
            {"type": "Car Loan", "amount": 800000, "emi": 15000, "remaining_tenure": 48}
        ],
        "credit_score": 750,
        "pre_approved_limit": 1000000,
        "account_number": "ICICI5678901234",
        "bank_name": "ICICI Bank"
    },
    "CUST004": {
        "customer_id": "CUST004",
        "name": "Sunita Verma",
        "age": 31,
        "city": "Bangalore",
        "phone": "9876543213",
        "email": "sunita.verma@email.com",
        "pan_number": "PQRST3456U",
        "aadhar_number": "4567-8901-2345",
        "occupation": "Data Scientist",
        "employer": "Wipro",
        "monthly_salary": 120000,
        "current_loans": [],
        "credit_score": 810,
        "pre_approved_limit": 800000,
        "account_number": "AXIS1234509876",
        "bank_name": "Axis Bank"
    },
    "CUST005": {
        "customer_id": "CUST005",
        "name": "Vikram Singh",
        "age": 45,
        "city": "Jaipur",
        "phone": "9876543214",
        "email": "vikram.singh@email.com",
        "pan_number": "UVWXY7890Z",
        "aadhar_number": "5678-9012-3456",
        "occupation": "Government Employee",
        "employer": "Indian Railways",
        "monthly_salary": 75000,
        "current_loans": [
            {"type": "Personal Loan", "amount": 300000, "emi": 8000, "remaining_tenure": 36}
        ],
        "credit_score": 720,
        "pre_approved_limit": 400000,
        "account_number": "PNB7890123456",
        "bank_name": "Punjab National Bank"
    },
    "CUST006": {
        "customer_id": "CUST006",
        "name": "Neha Gupta",
        "age": 29,
        "city": "Hyderabad",
        "phone": "9876543215",
        "email": "neha.gupta@email.com",
        "pan_number": "ABCFG1234H",
        "aadhar_number": "6789-0123-4567",
        "occupation": "CA",
        "employer": "Deloitte",
        "monthly_salary": 110000,
        "current_loans": [],
        "credit_score": 800,
        "pre_approved_limit": 700000,
        "account_number": "KOTAK4567890123",
        "bank_name": "Kotak Mahindra Bank"
    },
    "CUST007": {
        "customer_id": "CUST007",
        "name": "Ravi Menon",
        "age": 38,
        "city": "Chennai",
        "phone": "9876543216",
        "email": "ravi.menon@email.com",
        "pan_number": "HIJKL5678M",
        "aadhar_number": "7890-1234-5678",
        "occupation": "Doctor",
        "employer": "Apollo Hospitals",
        "monthly_salary": 200000,
        "current_loans": [
            {"type": "Home Loan", "amount": 5000000, "emi": 45000, "remaining_tenure": 240}
        ],
        "credit_score": 790,
        "pre_approved_limit": 1500000,
        "account_number": "BOB8901234567",
        "bank_name": "Bank of Baroda"
    },
    "CUST008": {
        "customer_id": "CUST008",
        "name": "Anita Desai",
        "age": 33,
        "city": "Pune",
        "phone": "9876543217",
        "email": "anita.desai@email.com",
        "pan_number": "NOPQR9012S",
        "aadhar_number": "8901-2345-6789",
        "occupation": "HR Manager",
        "employer": "Tech Mahindra",
        "monthly_salary": 90000,
        "current_loans": [],
        "credit_score": 770,
        "pre_approved_limit": 600000,
        "account_number": "YES0123456789",
        "bank_name": "Yes Bank"
    },
    "CUST009": {
        "customer_id": "CUST009",
        "name": "Suresh Reddy",
        "age": 50,
        "city": "Kolkata",
        "phone": "9876543218",
        "email": "suresh.reddy@email.com",
        "pan_number": "TUVWX3456Y",
        "aadhar_number": "9012-3456-7890",
        "occupation": "Professor",
        "employer": "IIT Kharagpur",
        "monthly_salary": 130000,
        "current_loans": [
            {"type": "Car Loan", "amount": 600000, "emi": 12000, "remaining_tenure": 42}
        ],
        "credit_score": 760,
        "pre_approved_limit": 900000,
        "account_number": "UCO2345678901",
        "bank_name": "UCO Bank"
    },
    "CUST010": {
        "customer_id": "CUST010",
        "name": "Deepa Nair",
        "age": 27,
        "city": "Kochi",
        "phone": "9876543219",
        "email": "deepa.nair@email.com",
        "pan_number": "YZABC7890D",
        "aadhar_number": "0123-4567-8901",
        "occupation": "Software Developer",
        "employer": "UST Global",
        "monthly_salary": 70000,
        "current_loans": [],
        "credit_score": 680,
        "pre_approved_limit": 300000,
        "account_number": "FED3456789012",
        "bank_name": "Federal Bank"
    },
    "CUST011": {
        "customer_id": "CUST011",
        "name": "Manoj Tiwari",
        "age": 40,
        "city": "Lucknow",
        "phone": "9876543220",
        "email": "manoj.tiwari@email.com",
        "pan_number": "DEFGH1234I",
        "aadhar_number": "1234-8901-2345",
        "occupation": "Lawyer",
        "employer": "Self Employed",
        "monthly_salary": 180000,
        "current_loans": [
            {"type": "Home Loan", "amount": 3500000, "emi": 32000, "remaining_tenure": 200}
        ],
        "credit_score": 740,
        "pre_approved_limit": 1200000,
        "account_number": "IDBI4567890123",
        "bank_name": "IDBI Bank"
    },
    "CUST012": {
        "customer_id": "CUST012",
        "name": "Kavita Joshi",
        "age": 36,
        "city": "Indore",
        "phone": "9876543221",
        "email": "kavita.joshi@email.com",
        "pan_number": "JKLMN5678O",
        "aadhar_number": "2345-9012-3456",
        "occupation": "Bank Manager",
        "employer": "Canara Bank",
        "monthly_salary": 100000,
        "current_loans": [],
        "credit_score": 830,
        "pre_approved_limit": 850000,
        "account_number": "CAN5678901234",
        "bank_name": "Canara Bank"
    }
}


def get_customer_by_phone(phone: str) -> dict | None:
    """Retrieve customer data by phone number"""
    for customer_id, customer in CUSTOMERS.items():
        if customer["phone"] == phone:
            return customer
    return None


def get_customer_by_id(customer_id: str) -> dict | None:
    """Retrieve customer data by customer ID"""
    return CUSTOMERS.get(customer_id)


def get_all_customers() -> dict:
    """Retrieve all customers"""
    return CUSTOMERS
