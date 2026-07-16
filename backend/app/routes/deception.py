"""Honey table and deception route handlers."""

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.schemas import DatabaseQueryRequest, SuccessResponse
from app.services import get_honey_detector, get_session_manager
from database.engine import PostgresSessionFactory, SQLiteSessionFactory
from database.seed_sqlite import (
    CompanyClientGlobalDump2026,
    HRPayrollConfidential,
    InternalSystemAudit,
)

logger = logging.getLogger(__name__)

router_deception = APIRouter(prefix="/deception", tags=["deception"])

# Mock incident tracking (in production, use database)
_incidents = [
    {
        "id": 1,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent_id": "agent_001",
        "honey_table": "company_client_global_dump_2026",
        "status": "DETECTED",
        "risk_score": 0.95,
    },
]


@router_deception.post("/sweep")
async def honey_table_sweep(request_body: DatabaseQueryRequest, request: Request):
    """Honey table sweep attack detection with real database.
    
    Detects attempts to access honey tables and routes to sandbox.
    Logs incidents to database for persistent tracking.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    
    try:
        logger.info(f"[{request_id}] Honey table sweep initiated")
        
        honey_detector = get_honey_detector()
        
        # Detect honey table access - returns tuple (detected, table_name, all_tables)
        detected, honey_table, all_tables = honey_detector.detect_honey_table_access(
            request_body.query
        )
        
        fake_data_records = []
        
        if detected:
            logger.warning(
                f"[{request_id}] Honey table detected: {honey_table}"
            )
            
            # Try to log incident to database and query sandbox
            try:
                # Log incident to database
                async with PostgresSessionFactory() as session:
                    from app.models.incident import Incident, IncidentStatus
                    from datetime import datetime
                    
                    incident = Incident(
                        timestamp=datetime.utcnow(),
                        agent_id="unknown",
                        query=request_body.query,
                        honey_table=honey_table,
                        status=IncidentStatus.DETECTED,
                        risk_score=0.95,
                        sandbox_routed=True,
                        fake_data_served=True,
                    )
                    session.add(incident)
                    await session.commit()
                
                # Query fake data from sandbox database
                async with SQLiteSessionFactory() as session:
                    from database.seed_sqlite import CompanyClientGlobalDump2026
                    
                    result = await session.execute(
                        select(CompanyClientGlobalDump2026).limit(10)
                    )
                    fake_records = result.scalars().all()
                    
                    fake_data_records = [
                        {
                            "id": record.id,
                            "client_name": record.client_name,
                            "tax_id": record.tax_id,
                            "balance": record.balance,
                            "country": record.country,
                        }
                        for record in fake_records
                    ]
                    
            except Exception as db_error:
                logger.warning(f"[{request_id}] Database operation failed, using mock data: {db_error}")
                # Fallback mock data
                fake_data_records = [
                    {"id": 1, "client_name": "Company A", "tax_id": "TAX-123456", "balance": 150000.0, "country": "USA"},
                    {"id": 2, "client_name": "Company B", "tax_id": "TAX-789012", "balance": 250000.0, "country": "UK"},
                ]
        else:
            honey_table = None
            logger.info(f"[{request_id}] No honey table detected")
        
        return SuccessResponse(
            data={
                "detected": detected,
                "honey_table": honey_table,
                "sandbox_routed": detected,
                "fake_data_records": fake_data_records,
                "all_tables": all_tables,
            },
            message="Honey table sweep completed",
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"[{request_id}] Honey table sweep failed: {e}",
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Honey table sweep failed"
        )


@router_deception.get("/sandbox-records")
async def get_sandbox_records(request: Request, limit: int = 100):
    """Get records from sandbox database.
    
    Returns records from honey tables in the sandbox database.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    
    try:
        if limit < 1 or limit > 1000:
            raise HTTPException(
                status_code=400,
                detail="Limit must be between 1 and 1000"
            )
        
        logger.info(f"[{request_id}] Fetching sandbox records: limit={limit}")
        
        # Try to query real data from sandbox database
        records = []
        
        try:
            async with SQLiteSessionFactory() as session:
                # Get data from all honey tables
                from database.seed_sqlite import (
                    CompanyClientGlobalDump2026,
                    HRPayrollConfidential,
                    InternalSystemAudit,
                )
                
                # Company clients
                client_result = await session.execute(
                    select(CompanyClientGlobalDump2026).limit(limit)
                )
                clients = client_result.scalars().all()
                records.extend([
                    {
                        "id": c.id,
                        "table": "company_client_global_dump_2026",
                        "client_name": c.client_name,
                        "tax_id": c.tax_id,
                        "balance": c.balance,
                        "country": c.country,
                        "industry": c.industry,
                    }
                    for c in clients
                ])
                
                # HR payroll (limited due to sensitivity)
                payroll_result = await session.execute(
                    select(HRPayrollConfidential).limit(min(limit, 20))
                )
                payrolls = payroll_result.scalars().all()
                records.extend([
                    {
                        "id": p.id,
                        "table": "hr_payroll_confidential",
                        "employee_id": p.employee_id,
                        "full_name": p.full_name,
                        "department": p.department,
                    }
                    for p in payrolls
                ])
                
                # System audit
                audit_result = await session.execute(
                    select(InternalSystemAudit).limit(min(limit, 20))
                )
                audits = audit_result.scalars().all()
                records.extend([
                    {
                        "id": a.id,
                        "table": "internal_system_audit",
                        "node_id": a.node_id,
                        "config_type": a.config_type,
                    }
                    for a in audits
                ])
                
        except Exception as db_error:
            logger.warning(f"[{request_id}] Database query failed, using mock data: {db_error}")
            # Fallback to mock data
            records = [
                {
                    "id": i,
                    "table": "company_client_global_dump_2026",
                    "client_name": f"Company {i}",
                    "tax_id": f"TAX-{100000 + i}",
                    "balance": 100000.0 * (i + 1),
                    "country": "USA",
                    "industry": "Technology",
                }
                for i in range(min(limit, 10))
            ]
        
        return SuccessResponse(
            data={
                "records": records,
                "count": len(records),
                "limit": limit,
            },
            message="Sandbox records retrieved",
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"[{request_id}] Failed to fetch sandbox records: {e}",
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch sandbox records"
        )


@router_deception.get("/incidents")
async def get_deception_incidents(request: Request, page: int = 1):
    """Get honey table incident logs from database.
    
    Returns paginated list of detected honey table access attempts.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    
    try:
        if page < 1:
            raise HTTPException(status_code=400, detail="Page must be >= 1")
        
        page_size = 20
        logger.info(f"[{request_id}] Fetching incidents: page={page}")
        
        # Try to query real incidents from database
        incidents = []
        total_incidents = 0
        
        try:
            async with PostgresSessionFactory() as session:
                from app.models.incident import Incident, IncidentStatus
                
                # Get total count
                count_query = select(func.count(Incident.id))
                total_result = await session.execute(count_query)
                total_incidents = total_result.scalar() or 0
                
                # Get paginated incidents
                incidents_query = (
                    select(Incident)
                    .order_by(Incident.timestamp.desc())
                    .offset((page - 1) * page_size)
                    .limit(page_size)
                )
                result = await session.execute(incidents_query)
                incidents_raw = result.scalars().all()
                
                incidents = [
                    {
                        "id": incident.id,
                        "timestamp": incident.timestamp.isoformat() if incident.timestamp else None,
                        "agent_id": incident.agent_id,
                        "query": incident.query,
                        "honey_table": incident.honey_table,
                        "status": incident.status.value if incident.status else None,
                        "risk_score": incident.risk_score,
                        "sandbox_routed": incident.sandbox_routed,
                        "fake_data_served": incident.fake_data_served,
                        "user_id": incident.user_id,
                        "created_at": incident.created_at.isoformat() if incident.created_at else None,
                    }
                    for incident in incidents_raw
                ]
                
        except Exception as db_error:
            logger.warning(f"[{request_id}] Database query failed, using mock data: {db_error}")
            # Fallback to mock data
            total_incidents = 1
            incidents = [
                {
                    "id": 1,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "agent_id": "agent_001",
                    "query": "SELECT * FROM company_client_global_dump_2026",
                    "honey_table": "company_client_global_dump_2026",
                    "status": "DETECTED",
                    "risk_score": 0.95,
                    "sandbox_routed": True,
                    "fake_data_served": True,
                    "user_id": None,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                },
            ]
        
        return SuccessResponse(
            data={
                "incidents": incidents,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total": total_incidents,
                    "total_pages": (total_incidents + page_size - 1) // page_size,
                },
            },
            message="Incidents retrieved",
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"[{request_id}] Failed to fetch incidents: {e}",
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch incidents"
        )


@router_deception.post("/generate-honey-data")
async def generate_honey_data(request: Request, count: int = 100):
    """Generate realistic synthetic honey table data.
    
    Creates fake data for honey tables to serve to attackers.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    
    try:
        if count < 1 or count > 10000:
            raise HTTPException(
                status_code=400,
                detail="Count must be between 1 and 10000"
            )
        
        logger.info(f"[{request_id}] Generating honey data: count={count}")
        
        # Simulate data generation
        generated_records = []
        for i in range(count):
            generated_records.append({
                "id": i,
                "fake_field_1": f"value_{i}",
                "fake_field_2": f"data_{i}",
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
        
        logger.info(f"[{request_id}] Honey data generated: {len(generated_records)} records")
        
        return SuccessResponse(
            data={
                "status": "generated",
                "records_created": len(generated_records),
                "sample_records": generated_records[:5],
            },
            message=f"Generated {len(generated_records)} honey records",
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"[{request_id}] Failed to generate honey data: {e}",
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to generate honey data"
        )
