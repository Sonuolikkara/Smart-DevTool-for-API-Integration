"""History Routes - Retrieve and manage analysis and generation history."""
from fastapi import APIRouter, HTTPException
from typing import Optional
from services.history_service import HistoryService

router = APIRouter(tags=["history"])
history_service = HistoryService()


@router.get("/analyses")
async def get_analyses_history(limit: int = 20):
    """Get recent analysis history.
    
    Args:
        limit: Maximum number of records to return
        
    Returns:
        List of recent analyses
    """
    try:
        analyses = history_service.get_analysis_history(limit=limit)
        return {
            "status": "success",
            "count": len(analyses),
            "analyses": analyses
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/generations")
async def get_generations_history(limit: int = 20):
    """Get recent generation history.
    
    Args:
        limit: Maximum number of records to return
        
    Returns:
        List of recent code generations
    """
    try:
        generations = history_service.get_generation_history(limit=limit)
        return {
            "status": "success",
            "count": len(generations),
            "generations": generations
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/analyses/{analysis_id}")
async def get_analysis(analysis_id: str):
    """Get specific analysis by ID.
    
    Args:
        analysis_id: Analysis ID
        
    Returns:
        Full analysis record
    """
    analysis = history_service.get_analysis_by_id(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {
        "status": "success",
        "analysis": analysis
    }


@router.get("/generations/{generation_id}")
async def get_generation(generation_id: str):
    """Get specific generation by ID.
    
    Args:
        generation_id: Generation ID
        
    Returns:
        Full generation record with complete code
    """
    generation = history_service.get_generation_by_id(generation_id)
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    return {
        "status": "success",
        "generation": generation
    }


@router.get("/analyses/{analysis_id}/generations")
async def get_analysis_generations(analysis_id: str):
    """Get all code generations from an analysis.
    
    Args:
        analysis_id: Analysis ID
        
    Returns:
        List of related code generations
    """
    try:
        generations = history_service.get_related_generations(analysis_id)
        return {
            "status": "success",
            "count": len(generations),
            "generations": generations
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/statistics")
async def get_history_statistics():
    """Get statistics about analysis and generation history.
    
    Returns:
        Statistics including counts and aggregates
    """
    try:
        stats = history_service.get_statistics()
        return {
            "status": "success",
            "statistics": stats
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/clear")
async def clear_history():
    """Clear all history (careful!).
    
    Returns:
        Success status
    """
    try:
        success = history_service.clear_history()
        return {
            "status": "success" if success else "failed",
            "message": "History cleared" if success else "Failed to clear history"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
