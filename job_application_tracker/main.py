from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from models import JobApplication, JobApplicationCreate, Status
from file_handler import read_applications, write_applications, backup_applications
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Job Application Tracker API",
    description="API to manage and search job applications",
    version="1.0.0"
)

def generate_id(application: JobApplicationCreate) -> str:
    """
    Generate a unique ID for a job application.
    
    Args:
        application: JobApplicationCreate instance
        
    Returns:
        Unique string ID based on name, company, and position
    """
    try:
        return f"{application.name}_{application.company}_{application.position}".replace(" ", "_").lower()
    except Exception as e:
        logger.error(f"Error generating ID: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate application ID")

@app.post("/applications/", response_model=JobApplication)
async def create_application(application: JobApplicationCreate):
    """
    Create a new job application.
    
    Args:
        application: Job application data
        
    Returns:
        Created job application with generated ID
        
    Raises:
        HTTPException: If application already exists or creation fails
    """
    try:
        # Read existing applications
        applications = read_applications()
        
        # Generate unique ID
        app_id = generate_id(application)
        
        # Check if application already exists
        if app_id in applications:
            raise HTTPException(
                status_code=400, 
                detail=f"Application already exists for {application.name} at {application.company} for {application.position}"
            )

        # Create backup before making changes
        backup_applications()
        
        # Create new application
        app_data = JobApplication(**application.model_dump(), id=app_id)
        applications[app_id] = app_data.model_dump()
        
        # Save to file
        write_applications(applications)
        
        logger.info(f"Created application: {app_id}")
        return app_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating application: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create application: {str(e)}")

@app.get("/applications/", response_model=List[JobApplication])
async def get_applications():
    """
    Get all job applications.
    
    Returns:
        List of all job applications
        
    Raises:
        HTTPException: If applications cannot be retrieved
    """
    try:
        applications = read_applications()
        result = [JobApplication(**data) for data in applications.values()]
        logger.info(f"Retrieved {len(result)} applications")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving applications: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve applications: {str(e)}")

@app.get("/applications/search", response_model=List[JobApplication])
async def search_applications(status: Optional[Status] = Query(None, description="Filter by application status")):
    """
    Search job applications by status.
    
    Args:
        status: Optional status filter (pending, accepted, rejected, interview, withdrawn)
        
    Returns:
        List of job applications matching the status filter
        
    Raises:
        HTTPException: If search fails
    """
    try:
        applications = read_applications()
        
        # If no status filter, return all applications
        if not status:
            result = [JobApplication(**data) for data in applications.values()]
            logger.info(f"Retrieved all {len(result)} applications")
            return result
        
        # Filter by status
        filtered_applications = [
            JobApplication(**data)
            for data in applications.values()
            if data.get('status', '').lower() == status.value.lower()
        ]
        
        logger.info(f"Found {len(filtered_applications)} applications with status '{status.value}'")
        return filtered_applications
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching applications: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to search applications: {str(e)}")

@app.get("/applications/stats")
async def get_application_stats():
    """
    Get statistics about job applications.
    
    Returns:
        Dictionary with application statistics
        
    Raises:
        HTTPException: If stats cannot be calculated
    """
    try:
        applications = read_applications()
        
        if not applications:
            return {
                "total": 0,
                "by_status": {},
                "companies": []
            }
        
        # Calculate statistics
        total = len(applications)
        status_counts = {}
        companies = set()
        
        for app_data in applications.values():
            status = app_data.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
            companies.add(app_data.get('company', 'Unknown'))
        
        stats = {
            "total": total,
            "by_status": status_counts,
            "companies": sorted(list(companies))
        }
        
        logger.info(f"Generated stats for {total} applications")
        return stats
        
    except Exception as e:
        logger.error(f"Error generating stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate statistics: {str(e)}")