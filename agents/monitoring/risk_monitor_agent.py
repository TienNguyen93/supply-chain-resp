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
    

    def _generate_recommendations(self, disruption: Disruption, risk_score: float) -> List[str]:
        """
        Generate recommended actions based on disruption type and severity
        """
        recommendations = []
        
        if risk_score >= 70:
            recommendations.append("URGENT: Activate emergency response team")
            recommendations.append("Notify executive leadership immediately")
        
        if disruption.severity in [SeverityLevel.HIGH, SeverityLevel.CRITICAL]:
            recommendations.append("Identify alternative suppliers immediately")
            recommendations.append("Increase safety stock for affected items")
        
        if disruption.type == DisruptionType.WEATHER:
            recommendations.append("Monitor weather patterns for route planning")
            recommendations.append("Consider alternative transportation routes")
        
        if disruption.type == DisruptionType.SUPPLIER:
            recommendations.append("Review supplier contracts and SLAs")
            recommendations.append("Contact backup suppliers")
        
        if disruption.estimated_cost_per_day > 100000:
            recommendations.append("Prepare financial impact report")
            recommendations.append("Update stakeholder communications")
        
        if not recommendations:
            recommendations.append("Continue monitoring situation")
            recommendations.append("Document disruption for future analysis")
        
        return recommendations
    

    def _determine_urgency(self, risk_score: float) -> str:
        """Determine urgency level based on risk score"""
        if risk_score >= 80:
            return "CRITICAL - Immediate Action Required"
        elif risk_score >= 60:
            return "HIGH - Action Required Within 4 Hours"
        elif risk_score >= 40:
            return "MEDIUM - Action Required Within 24 Hours"
        else:
            return "LOW - Monitoring Required"
        

    def get_active_disruptions(self) -> List[Dict]:
        """Get all currently active disruptions"""
        return [
            {
                "id": d.id,
                "type": d.type.value,
                "title": d.title,
                "severity": d.severity.value,
                "location": d.location,
                "timestamp": d.timestamp.isoformat()
            }
            for d in self.active_disruptions.values()
        ]
    

    def generate_summary_report(self) -> Dict:
        """Generate summary report of all monitored disruptions"""
        total_disruptions = len(self.active_disruptions)
        
        severity_counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }
        
        total_estimated_cost = 0
        
        for disruption in self.active_disruptions.values():
            severity_counts[disruption.severity.value] += 1
            total_estimated_cost += (
                disruption.estimated_impact_days * disruption.estimated_cost_per_day
            )
        
        return {
            "agent_id": self.agent_id,
            "report_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_active_disruptions": total_disruptions,
                "critical_alerts": severity_counts["CRITICAL"],
                "high_alerts": severity_counts["HIGH"],
                "medium_alerts": severity_counts["MEDIUM"],
                "low_alerts": severity_counts["LOW"],
                "total_estimated_cost": f"${total_estimated_cost:,.2f}",
                "total_alerts_generated": len(self.alert_history)
            },
            "active_disruptions": self.get_active_disruptions()
        }
    


#------------ Demo function ---------------#
def demo_risk_monitor():
    """Demonstrate the risk monitoring agent with sample disruptions"""
    print("Supply Chain Disruption Response System - Demo")
    print("=" * 60)
    
    # Create agent
    agent = RiskMonitorAgent()
    
    # Sample disruptions
    sample_disruptions = [
        Disruption(
            id="DISRUPT_001",
            type=DisruptionType.WEATHER,
            title="Hurricane Milton Approaching Florida Coast",
            description="Category 4 hurricane expected to impact major shipping ports",
            severity=SeverityLevel.CRITICAL,
            location="Florida, USA",
            affected_regions=["Southeast US", "Gulf Coast"],
            affected_suppliers=["Port of Miami", "Jacksonville Port Authority"],
            estimated_impact_days=7,
            estimated_cost_per_day=500000,
            timestamp=datetime.now(),
            source="National Weather Service",
            confidence=0.95
        ),
        Disruption(
            id="DISRUPT_002",
            type=DisruptionType.SUPPLIER,
            title="Semiconductor Manufacturer Maintenance Shutdown",
            description="Taiwan-based chip supplier scheduled maintenance",
            severity=SeverityLevel.MEDIUM,
            location="Taiwan",
            affected_regions=["Asia Pacific", "North America"],
            affected_suppliers=["TSMC Fab 18"],
            estimated_impact_days=14,
            estimated_cost_per_day=75000,
            timestamp=datetime.now(),
            source="Supplier Communication",
            confidence=1.0
        ),
        Disruption(
            id="DISRUPT_003",
            type=DisruptionType.TRANSPORTATION,
            title="Suez Canal Traffic Delays",
            description="Container ship experiencing mechanical issues causing backlog",
            severity=SeverityLevel.HIGH,
            location="Suez Canal, Egypt",
            affected_regions=["Europe", "Asia", "Middle East"],
            affected_suppliers=["Multiple shipping lines"],
            estimated_impact_days=3,
            estimated_cost_per_day=250000,
            timestamp=datetime.now(),
            source="Maritime Traffic Monitor",
            confidence=0.85
        ),
        Disruption(
            id="DISRUPT_004",
            type=DisruptionType.GEOPOLITICAL,
            title="Port Strike in Los Angeles",
            description="Dockworkers union strike affecting West Coast operations",
            severity=SeverityLevel.CRITICAL,
            location="Los Angeles, California",
            affected_regions=["West Coast US"],
            affected_suppliers=["Port of LA", "Port of Long Beach"],
            estimated_impact_days=10,
            estimated_cost_per_day=800000,
            timestamp=datetime.now(),
            source="Labor Relations Board",
            confidence=0.90
        )
    ]

     # Process each disruption
    print("\nProcessing Disruptions...\n")
    for disruption in sample_disruptions:
        alert = agent.monitor_disruption(disruption)
        
        print(f"{alert['disruption']['title']}")
        print(f"   Severity: {alert['disruption']['severity']}")
        print(f"   Risk Score: {alert['risk_assessment']['risk_score']}/100")
        print(f"   Urgency: {alert['urgency']}")
        print(f"   Estimated Cost: ${alert['risk_assessment']['total_estimated_cost']:,.2f}")
        print(f"   Top Recommendation: {alert['recommended_actions'][0]}")
        print()
    
    # Generate summary report
    print("=" * 60)
    report = agent.generate_summary_report()
    print("\nSUMMARY REPORT")
    print(f"Total Active Disruptions: {report['summary']['total_active_disruptions']}")
    print(f"Critical Alerts: {report['summary']['critical_alerts']}")
    print(f"High Alerts: {report['summary']['high_alerts']}")
    print(f"Total Estimated Cost: {report['summary']['total_estimated_cost']}")
    
    print("\n✅ Demo completed! Agent is working correctly.")
    print("\nNext: Build Streamlit interface to visualize these alerts!")



if __name__ == "__main__":
  demo_risk_monitor()