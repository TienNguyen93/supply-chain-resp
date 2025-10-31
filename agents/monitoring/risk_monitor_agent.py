"""
Detects and assesses supply chain disruptions from multiple sources
"""

from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DisruptionType(Enum):
    WEATHER = "weather"
    GEOPOLITICAL = "geopolitical"
    SUPPLIER = "supplier"
    TRANSPORTATION = "transportation"
    NATURAL_DISASTER = "natural_disaster"
    PANDEMIC = "pandemic"
    CYBER = "cyber_security"


class SeverityLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass
class Disruption:
    """represents a supply chain disruption event"""
    id: str
    type: DisruptionType
    title: str
    description: str
    severity: SeverityLevel
    location: str
    affected_regions: List[str]
    affected_suppliers: List[str]
    estimated_impact_days: int
    estimated_cost_per_day: float
    timestamp: datetime
    source: str
    confidence: float  # 0.0 to 1.0

class RiskMonitorAgent:
    """
    Agent responsible for monitoring and detecting supply chain disruptions.
    Analyzes multiple data sources and generates risk alerts.
    """

    def __init__(self, agent_id: str = "risk_monitor_001"):
        self.agent_id = agent_id
        self.active_disruptions: Dict[str, Disruption] = {}
        self.alert_history: List[Dict] = []
        logger.info(f"Risk Monitor Agent {agent_id} initialized")


    def monitor_disruption(self, disruption: Disruption) -> Dict:
        """
        Process and monitor a new disruption event
        """
        try:
            # Add to active disruptions
            self.active_disruptions[disruption.id] = disruption
            
            # Calculate risk score
            risk_score = self._calculate_risk_score(disruption)
            
            # Generate alert
            alert = self._generate_alert(disruption, risk_score)
            self.alert_history.append(alert)
            
            logger.info(
                f"New disruption detected: {disruption.title} "
                f"(Severity: {disruption.severity.value}, Risk Score: {risk_score:.2f})"
            )
            return alert
            
        except Exception as e:
            logger.error(f"Error monitoring disruption: {e}")
            return {"error": str(e)}
        
    def _calculate_risk_score(self, disruption: Disruption) -> float:
        """
        Calculate overall risk score (0-100) based on multiple factors
        """
        # Base score from severity
        severity_scores = {
            SeverityLevel.LOW: 20,
            SeverityLevel.MEDIUM: 40,
            SeverityLevel.HIGH: 70,
            SeverityLevel.CRITICAL: 90
        }
        base_score = severity_scores[disruption.severity]
        
        # Impact factor (days + cost)
        impact_factor = min(disruption.estimated_impact_days / 10.0, 1.0) * 10
        cost_factor = min(disruption.estimated_cost_per_day / 1000000, 1.0) * 10
        
        # Confidence adjustment
        confidence_adjustment = disruption.confidence * 10
        
        # Calculate final score
        risk_score = min(
            base_score + impact_factor + cost_factor + confidence_adjustment,
            100
        )
        
        return risk_score
    
    def _generate_alert(self, disruption: Disruption, risk_score: float) -> Dict:
        """
        Generate structured alert for the disruption
        """
        return {
            "alert_id": f"ALERT_{disruption.id}",
            "timestamp": datetime.now().isoformat(),
            "disruption": {
                "id": disruption.id,
                "type": disruption.type.value,
                "title": disruption.title,
                "description": disruption.description,
                "severity": disruption.severity.value,
                "location": disruption.location,
                "affected_regions": disruption.affected_regions,
                "affected_suppliers": disruption.affected_suppliers
            },
            "risk_assessment": {
                "risk_score": round(risk_score, 2),
                "estimated_impact_days": disruption.estimated_impact_days,
                "estimated_daily_cost": disruption.estimated_cost_per_day,
                "total_estimated_cost": disruption.estimated_impact_days * disruption.estimated_cost_per_day,
                "confidence": disruption.confidence
            },
            "recommended_actions": self._generate_recommendations(disruption, risk_score),
            "urgency": self._determine_urgency(risk_score)
        }