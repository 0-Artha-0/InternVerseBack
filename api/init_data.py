from backend.app import db
from backend.models.models import Industry, Company
import logging

def initialize_data():
    """Initialize database with default data if tables are empty"""
    try:
        # Check if industries table is empty
        if Industry.query.first() is None:
            logging.info("Initializing industries data...")
            
            # Default industries
            default_industries = [
                {
                    "name": "Technology & IT",
                    "description": "Experience the fast-paced world of technology, developing software, managing IT infrastructure, or designing digital solutions.",
                    "icon": "bi-cpu"
                },
                {
                    "name": "Business & Finance",
                    "description": "Dive into the world of business strategy, financial analysis, marketing, and corporate operations.",
                    "icon": "bi-cash-coin"
                },
                {
                    "name": "Healthcare",
                    "description": "Explore careers in health services, medical research, healthcare administration, or public health.",
                    "icon": "bi-hospital"
                },
                {
                    "name": "Education",
                    "description": "Discover roles in teaching, curriculum development, educational technology, or academic administration.",
                    "icon": "bi-book"
                },
                {
                    "name": "Environmental Science & Sustainability",
                    "description": "Work on projects related to environmental conservation, renewable energy, sustainability consulting, or climate research.",
                    "icon": "bi-tree"
                },
                {
                    "name": "Media & Communications",
                    "description": "Develop skills in journalism, digital media production, public relations, or content creation.",
                    "icon": "bi-camera"
                },
                {
                    "name": "Law & Government",
                    "description": "Experience legal research, policy analysis, public administration, or compliance work.",
                    "icon": "bi-bank"
                },
                {
                    "name": "Arts & Design",
                    "description": "Explore creative roles in graphic design, user experience, product design, or multimedia production.",
                    "icon": "bi-palette"
                },
                {
                    "name": "Engineering",
                    "description": "Work on projects in mechanical, civil, electrical, or other engineering disciplines.",
                    "icon": "bi-gear"
                },
                {
                    "name": "Hospitality & Tourism",
                    "description": "Experience roles in hotel management, tourism development, event planning, or customer service.",
                    "icon": "bi-airplane"
                }
            ]
            
            for industry_data in default_industries:
                industry = Industry(**industry_data)
                db.session.add(industry)
            
            db.session.commit()
            logging.info(f"Added {len(default_industries)} industries")
        
        # Check if companies table is empty
        if Company.query.first() is None and Industry.query.first() is not None:
            logging.info("Initializing companies data...")
            
            # Map industry names to their IDs
            industry_map = {industry.name: industry.id for industry in Industry.query.all()}
            
            # Default companies
            default_companies = [
                {
                    "name": "TechNova Solutions",
                    "industry_id": industry_map.get("Technology & IT"),
                    "description": "A leading technology firm specializing in cloud solutions, AI development, and enterprise software."
                },
                {
                    "name": "Global Finance Partners",
                    "industry_id": industry_map.get("Business & Finance"),
                    "description": "A multinational financial services company offering investment banking, asset management, and financial advisory."
                },
                {
                    "name": "MediCare Innovations",
                    "industry_id": industry_map.get("Healthcare"),
                    "description": "A healthcare technology company developing digital health solutions and medical devices."
                },
                {
                    "name": "EduTech Pioneers",
                    "industry_id": industry_map.get("Education"),
                    "description": "An educational technology company creating learning platforms and digital curriculum."
                },
                {
                    "name": "GreenEarth Sustainability",
                    "industry_id": industry_map.get("Environmental Science & Sustainability"),
                    "description": "A consulting firm focused on sustainability strategies, environmental impact assessments, and renewable energy."
                },
                {
                    "name": "MediaSphere Global",
                    "industry_id": industry_map.get("Media & Communications"),
                    "description": "A digital media company producing content across multiple platforms and offering marketing services."
                },
                {
                    "name": "LegalEdge Associates",
                    "industry_id": industry_map.get("Law & Government"),
                    "description": "A law firm specializing in corporate law, intellectual property, and regulatory compliance."
                },
                {
                    "name": "Creative Design Studio",
                    "industry_id": industry_map.get("Arts & Design"),
                    "description": "A design agency working on brand identity, user experience, and product design for various clients."
                },
                {
                    "name": "Innovate Engineering",
                    "industry_id": industry_map.get("Engineering"),
                    "description": "An engineering firm that designs and implements infrastructure, products, and systems across various industries."
                },
                {
                    "name": "Horizon Hospitality Group",
                    "industry_id": industry_map.get("Hospitality & Tourism"),
                    "description": "A hospitality management company operating hotels, resorts, and tourism experiences worldwide."
                }
            ]
            
            # Only add companies if we have valid industry IDs
            companies_to_add = [company for company in default_companies if company["industry_id"] is not None]
            
            for company_data in companies_to_add:
                company = Company(**company_data)
                db.session.add(company)
            
            db.session.commit()
            logging.info(f"Added {len(companies_to_add)} companies")
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error initializing data: {str(e)}")