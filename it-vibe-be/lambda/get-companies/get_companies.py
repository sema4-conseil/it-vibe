import json
import uuid


def lambda_handler(event, context):
    companies = [
    {
        "name": "Capgemini",
        "location": "Paris",
        "size": "340000",
        "revenue": "22250000000",
        "industry": "IT Services & Consulting",
        "description": "Global leader in consulting, technology, and digital transformation."
    },
    {
        "name": "Atos",
        "location": "Bezons",
        "size": "112000",
        "revenue": "11800000000",
        "industry": "IT Services & Consulting",
        "description": "Provides IT infrastructure, cybersecurity, and cloud solutions."
    },
    {
        "name": "Sopra Steria",
        "location": "Paris",
        "size": "47000",
        "revenue": "5500000000",
        "industry": "IT Services & Consulting",
        "description": "Specializes in systems integration and software development."
    },
    {
        "name": "Dassault Systèmes",
        "location": "Vélizy-Villacoublay",
        "size": "23000",
        "revenue": "5600000000",
        "industry": "IT Services & Consulting",
        "description": "3D design software and simulation solutions provider."
    },
    {
        "name": "Amadeus IT Group",
        "location": "Sophia Antipolis",
        "size": "18000",
        "revenue": "5000000000",
        "industry": "IT Services & Consulting",
        "description": "IT solutions for travel and hospitality industries."
    },
    {
        "name": "GFI Informatique",
        "location": "Paris",
        "size": "22000",
        "revenue": "2400000000",
        "industry": "IT Services & Consulting",
        "description": "IT infrastructure and business process services."
    },
    {
        "name": "Worldline",
        "location": "Bezons",
        "size": "18000",
        "revenue": "4600000000",
        "industry": "IT Services & Consulting",
        "description": "Digital payment and transactional services leader."
    },
    {
        "name": "OVHcloud",
        "location": "Roubaix",
        "size": "2500",
        "revenue": "700000000",
        "industry": "IT Services & Consulting",
        "description": "European cloud computing and web hosting provider."
    },
    {
        "name": "Mantu",
        "location": "Paris",
        "size": "10000",
        "revenue": "1000000000",
        "industry": "IT Services & Consulting",
        "description": "Technology consulting and talent solutions."
    },
    {
        "name": "Alten",
        "location": "Boulogne-Billancourt",
        "size": "38000",
        "revenue": "3200000000",
        "industry": "IT Services & Consulting",
        "description": "Engineering and IT consulting services."
    },
    {
        "name": "Devoteam",
        "location": "Paris",
        "size": "10000",
        "revenue": "1200000000",
        "industry": "IT Services & Consulting",
        "description": "Digital strategy and technology consulting firm."
    },
    {
        "name": "SII",
        "location": "Paris",
        "size": "15000",
        "revenue": "1500000000",
        "industry": "IT Services & Consulting",
        "description": "IT engineering and consulting services."
    },
    {
        "name": "SQLI",
        "location": "Paris",
        "size": "2500",
        "revenue": "300000000",
        "industry": "IT Services & Consulting",
        "description": "Digital experience and e-commerce solutions."
    },
    {
        "name": "Amaris Consulting",
        "location": "Paris",
        "size": "8000",
        "revenue": "900000000",
        "industry": "IT Services & Consulting",
        "description": "Management and technology consulting."
    },
    {
        "name": "Wavestone",
        "location": "Paris",
        "size": "4000",
        "revenue": "500000000",
        "industry": "IT Services & Consulting",
        "description": "Business transformation and IT strategy consulting."
    },
    {
        "name": "Niji",
        "location": "Boulogne-Billancourt",
        "size": "2000",
        "revenue": "250000000",
        "industry": "IT Services & Consulting",
        "description": "Digital innovation and agile development services."
    },
    {
        "name": "Micropole",
        "location": "Paris",
        "size": "1500",
        "revenue": "200000000",
        "industry": "IT Services & Consulting",
        "description": "Data intelligence and business analytics consulting."
    },
    {
        "name": "Smile",
        "location": "Paris",
        "size": "1800",
        "revenue": "220000000",
        "industry": "IT Services & Consulting",
        "description": "Open-source IT solutions and digital services."
    },
    {
        "name": "Ausy",
        "location": "Paris",
        "size": "6000",
        "revenue": "700000000",
        "industry": "IT Services & Consulting",
        "description": "Engineering and IT consulting for industries."
    },
    {
        "name": "Keyrus",
        "location": "Paris",
        "size": "3000",
        "revenue": "400000000",
        "industry": "IT Services & Consulting",
        "description": "Data, digital, and business performance consulting."
    }
]
    
    for company in companies:
        company["id"] = str(uuid.uuid4())

    return {
        "statusCode": 200,
        "body": json.dumps(companies),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        }
    }
