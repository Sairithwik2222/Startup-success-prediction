def get_business_models():
    """Get all business models with explanations"""
    return {
        "B2B (Business-to-Business)": {
            "description": "Selling products or services to other businesses",
            "examples": "SaaS platforms, wholesale suppliers, enterprise software"
        },
        "B2C (Business-to-Consumer)": {
            "description": "Selling directly to individual consumers",
            "examples": "Retail stores, restaurants, consumer apps"
        },
        "SaaS (Software as a Service)": {
            "description": "Cloud-based software with subscription pricing",
            "examples": "Salesforce, Slack, Zoom, Microsoft 365"
        },
        "Marketplace": {
            "description": "Platform connecting buyers and sellers",
            "examples": "Amazon, Uber, Airbnb, Etsy"
        },
        "Freemium": {
            "description": "Free basic version with paid premium features",
            "examples": "Spotify, LinkedIn, Dropbox"
        },
        "E-commerce": {
            "description": "Online retail selling physical or digital products",
            "examples": "Online stores, D2C brands"
        },
        "Franchise": {
            "description": "Licensed business model replication",
            "examples": "McDonald's, Subway, 7-Eleven"
        },
        "Subscription": {
            "description": "Recurring payment for ongoing product/service access",
            "examples": "Netflix, Dollar Shave Club, meal kits"
        },
        "Hybrid": {
            "description": "Combination of multiple business models",
            "examples": "Amazon (e-commerce + marketplace + subscription)"
        }
    }

def get_industry_specific_fields(industry):
    """Get industry-specific input fields"""
    
    industries = {
        "Food & Restaurants": {
            "fields": [
                {"name": "nearby_restaurants", "label": "Number of Nearby Restaurants (within 1 km)", "type": "number", "min": 0, "max": 100, "default": 5},
                {"name": "cuisine_type", "label": "Cuisine Type", "type": "select", "options": ["Fast Food", "Fine Dining", "Casual Dining", "Cafe", "Bakery", "Street Food", "Multi-Cuisine", "Specialty Cuisine"]},
                {"name": "avg_cost_per_person", "label": "Average Cost Per Person", "type": "number", "min": 50, "max": 10000, "default": 500},
                {"name": "seating_capacity", "label": "Seating Capacity", "type": "number", "min": 10, "max": 500, "default": 50},
                {"name": "food_quality_rating", "label": "Expected Food Quality (1-10)", "type": "slider", "min": 1, "max": 10, "default": 7},
                {"name": "location_foot_traffic", "label": "Foot Traffic Level", "type": "select", "options": ["Very Low", "Low", "Medium", "High", "Very High"]},
                {"name": "parking_available", "label": "Parking Available", "type": "select", "options": ["Yes", "No", "Limited"]},
                {"name": "delivery_services", "label": "Delivery Service Integration", "type": "select", "options": ["Yes - Multiple platforms", "Yes - Single platform", "No"]}
            ]
        },
        "Software & IT": {
            "fields": [
                {"name": "tech_stack", "label": "Primary Tech Stack", "type": "select", "options": ["Web (React/Angular/Vue)", "Mobile (iOS/Android)", "Backend/API", "AI/ML", "Cloud Services", "Desktop Apps", "Full Stack"]},
                {"name": "team_tech_experience", "label": "Team Average Tech Experience (years)", "type": "number", "min": 0, "max": 30, "default": 5},
                {"name": "target_market_size", "label": "Target Market Size", "type": "select", "options": ["Niche (<10K users)", "Small (10K-100K)", "Medium (100K-1M)", "Large (1M-10M)", "Mass Market (>10M)"]},
                {"name": "has_mvp", "label": "MVP Status", "type": "select", "options": ["Not started", "In development", "Completed", "Beta testing", "Launched"]},
                {"name": "monthly_active_users", "label": "Current Monthly Active Users", "type": "number", "min": 0, "max": 10000000, "default": 0},
                {"name": "revenue_model", "label": "Revenue Model", "type": "select", "options": ["Subscription", "One-time purchase", "Freemium", "Advertising", "Transaction fees", "Not monetized yet"]},
                {"name": "competitors_count", "label": "Number of Direct Competitors", "type": "number", "min": 0, "max": 100, "default": 5},
                {"name": "unique_value_proposition", "label": "Unique Advantage", "type": "select", "options": ["Strong", "Moderate", "Weak", "None yet"]}
            ]
        },
        "Education": {
            "fields": [
                {"name": "education_type", "label": "Education Type", "type": "select", "options": ["School (K-12)", "College/University", "Coaching Center", "Online Learning", "Vocational Training", "Skill Development"]},
                {"name": "student_capacity", "label": "Student Capacity", "type": "number", "min": 10, "max": 10000, "default": 100},
                {"name": "accreditation_status", "label": "Accreditation Status", "type": "select", "options": ["Fully Accredited", "In Process", "Not Required", "Not Accredited"]},
                {"name": "faculty_experience", "label": "Average Faculty Experience (years)", "type": "number", "min": 0, "max": 30, "default": 5},
                {"name": "placement_rate", "label": "Expected Placement Rate (%)", "type": "slider", "min": 0, "max": 100, "default": 70},
                {"name": "fee_structure", "label": "Annual Fee Range", "type": "select", "options": ["Budget (<50K)", "Moderate (50K-2L)", "Premium (2L-5L)", "Luxury (>5L)"]},
                {"name": "nearby_education_centers", "label": "Nearby Competing Institutions", "type": "number", "min": 0, "max": 50, "default": 5},
                {"name": "digital_infrastructure", "label": "Digital Infrastructure", "type": "select", "options": ["Excellent", "Good", "Basic", "None"]}
            ]
        },
        "Healthcare": {
            "fields": [
                {"name": "healthcare_type", "label": "Healthcare Type", "type": "select", "options": ["Hospital", "Clinic", "Diagnostic Center", "Pharmacy", "Telemedicine", "Home Healthcare", "Specialty Care"]},
                {"name": "bed_capacity", "label": "Bed Capacity (if applicable)", "type": "number", "min": 0, "max": 1000, "default": 0},
                {"name": "doctor_count", "label": "Number of Doctors", "type": "number", "min": 1, "max": 200, "default": 5},
                {"name": "specializations", "label": "Number of Specializations", "type": "number", "min": 1, "max": 30, "default": 3},
                {"name": "insurance_accepted", "label": "Insurance Acceptance", "type": "select", "options": ["Yes - Multiple", "Yes - Limited", "No"]},
                {"name": "emergency_services", "label": "Emergency Services Available", "type": "select", "options": ["Yes - 24/7", "Yes - Limited hours", "No"]},
                {"name": "nearby_hospitals", "label": "Nearby Healthcare Facilities", "type": "number", "min": 0, "max": 50, "default": 5},
                {"name": "medical_equipment", "label": "Medical Equipment Quality", "type": "select", "options": ["State-of-the-art", "Modern", "Standard", "Basic"]}
            ]
        },
        "Manufacturing": {
            "fields": [
                {"name": "manufacturing_type", "label": "Manufacturing Type", "type": "select", "options": ["Electronics", "Textiles", "Automotive Parts", "Food Processing", "Chemicals", "Machinery", "Consumer Goods", "Pharmaceuticals"]},
                {"name": "production_capacity", "label": "Monthly Production Capacity (units)", "type": "number", "min": 100, "max": 1000000, "default": 1000},
                {"name": "automation_level", "label": "Automation Level", "type": "select", "options": ["Fully Automated", "Semi-Automated", "Manual with some automation", "Mostly Manual"]},
                {"name": "quality_certifications", "label": "Quality Certifications", "type": "select", "options": ["ISO + Multiple", "ISO only", "In process", "None"]},
                {"name": "raw_material_access", "label": "Raw Material Access", "type": "select", "options": ["Excellent", "Good", "Moderate", "Difficult"]},
                {"name": "skilled_labor_availability", "label": "Skilled Labor Availability", "type": "select", "options": ["Abundant", "Available", "Limited", "Scarce"]},
                {"name": "export_capability", "label": "Export Capability", "type": "select", "options": ["Yes - Active", "Yes - Planning", "No - Domestic only"]},
                {"name": "sustainability_practices", "label": "Sustainability Practices", "type": "select", "options": ["Comprehensive", "Moderate", "Basic", "None"]}
            ]
        },
        "Fintech": {
            "fields": [
                {"name": "fintech_type", "label": "Fintech Type", "type": "select", "options": ["Digital Payments", "Lending", "Investment Platform", "Insurance Tech", "Personal Finance", "Cryptocurrency", "Banking as a Service"]},
                {"name": "regulatory_compliance", "label": "Regulatory Compliance Status", "type": "select", "options": ["Fully Compliant", "In Progress", "Planning", "Not Started"]},
                {"name": "security_measures", "label": "Security Infrastructure", "type": "select", "options": ["Bank-grade", "Industry Standard", "Basic", "Under Development"]},
                {"name": "user_base", "label": "Current User Base", "type": "number", "min": 0, "max": 10000000, "default": 0},
                {"name": "transaction_volume", "label": "Monthly Transaction Volume", "type": "select", "options": ["High (>1M)", "Medium (100K-1M)", "Low (10K-100K)", "Minimal (<10K)"]},
                {"name": "partnerships", "label": "Banking/Financial Partnerships", "type": "select", "options": ["Multiple established", "Single partner", "In negotiation", "None"]},
                {"name": "technology_maturity", "label": "Technology Platform Maturity", "type": "select", "options": ["Production-ready", "Beta", "Alpha", "Development"]},
                {"name": "fraud_prevention", "label": "Fraud Prevention System", "type": "select", "options": ["Advanced AI-based", "Standard", "Basic", "None"]}
            ]
        },
        "Agritech": {
            "fields": [
                {"name": "agritech_type", "label": "Agritech Type", "type": "select", "options": ["Precision Farming", "Supply Chain", "Marketplace", "Farm Management Software", "IoT/Sensors", "Drone Technology", "Organic Farming"]},
                {"name": "farmer_network", "label": "Number of Farmers Connected", "type": "number", "min": 0, "max": 100000, "default": 0},
                {"name": "technology_adoption", "label": "Farmer Technology Adoption Rate", "type": "select", "options": ["High", "Moderate", "Low", "Very Low"]},
                {"name": "crop_coverage", "label": "Crop Types Covered", "type": "number", "min": 1, "max": 50, "default": 3},
                {"name": "geographic_coverage", "label": "Geographic Coverage", "type": "select", "options": ["Multi-state", "Single state", "Regional", "Local"]},
                {"name": "government_support", "label": "Government Support/Subsidies", "type": "select", "options": ["Yes - Significant", "Yes - Some", "Applied", "No"]},
                {"name": "supply_chain_integration", "label": "Supply Chain Integration", "type": "select", "options": ["End-to-end", "Partial", "Minimal", "None"]},
                {"name": "sustainability_impact", "label": "Sustainability Impact", "type": "select", "options": ["High", "Medium", "Low", "Measuring"]}
            ]
        },
        "Retail & E-commerce": {
            "fields": [
                {"name": "retail_type", "label": "Retail Type", "type": "select", "options": ["Online Only", "Brick & Mortar", "Omnichannel", "Pop-up Store", "Wholesale"]},
                {"name": "product_category", "label": "Product Category", "type": "select", "options": ["Fashion", "Electronics", "Home & Living", "Beauty & Personal Care", "Sports & Fitness", "Books & Media", "Groceries", "Multi-category"]},
                {"name": "inventory_size", "label": "Inventory Size (SKUs)", "type": "number", "min": 10, "max": 100000, "default": 100},
                {"name": "avg_order_value", "label": "Average Order Value", "type": "number", "min": 100, "max": 100000, "default": 1000},
                {"name": "monthly_orders", "label": "Monthly Orders", "type": "number", "min": 0, "max": 100000, "default": 0},
                {"name": "logistics_partner", "label": "Logistics Partnership", "type": "select", "options": ["Multiple partners", "Single partner", "Own logistics", "Planning"]},
                {"name": "return_rate", "label": "Expected Return Rate (%)", "type": "slider", "min": 0, "max": 50, "default": 5},
                {"name": "customer_acquisition", "label": "Customer Acquisition Strategy", "type": "select", "options": ["Strong marketing plan", "Moderate plan", "Basic plan", "To be developed"]}
            ]
        }
    }
    
    return industries.get(industry, {"fields": []})

def get_all_industries():
    """Get list of all industries"""
    return [
        "Food & Restaurants",
        "Software & IT",
        "Education",
        "Healthcare",
        "Manufacturing",
        "Fintech",
        "Agritech",
        "Retail & E-commerce"
    ]
