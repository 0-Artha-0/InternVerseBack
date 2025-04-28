"""
Database migration script to add company_id column to InternshipTrack table
"""
import logging
from app import app, db
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_company_id_column():
    """
    Add company_id column to the InternshipTrack table if it doesn't exist
    """
    try:
        with app.app_context():
            # Check if column already exists
            inspect_query = text("PRAGMA table_info(internship_track)")
            result = db.session.execute(inspect_query)
            columns = [row[1] for row in result.fetchall()]
            
            if 'company_id' not in columns:
                # Add the column
                alter_query = text("ALTER TABLE internship_track ADD COLUMN company_id INTEGER REFERENCES company(id)")
                db.session.execute(alter_query)
                db.session.commit()
                logger.info("Successfully added company_id column to internship_track table")
            else:
                logger.info("company_id column already exists in internship_track table")
    except Exception as e:
        logger.error(f"Error during migration: {str(e)}")
        raise

if __name__ == "__main__":
    add_company_id_column()
    logger.info("Migration completed")