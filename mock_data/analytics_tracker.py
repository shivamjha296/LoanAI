"""
Self-Improving Feedback Loop & Analytics Tracker
Logs conversation metrics and tracks performance improvements
"""

import json
import os
from datetime import datetime
from typing import Dict, List
from collections import defaultdict


ANALYTICS_FILE = "analytics_data.json"


def initialize_analytics():
    """Initialize analytics data structure if file doesn't exist."""
    if not os.path.exists(ANALYTICS_FILE):
        data = {
            "conversations": [],
            "weekly_stats": {},
            "objection_outcomes": defaultdict(list),
            "strategy_performance": defaultdict(list),
            "conversion_funnel": defaultdict(int)
        }
        save_analytics(data)
    return load_analytics()


def load_analytics() -> Dict:
    """Load analytics data from file."""
    try:
        if os.path.exists(ANALYTICS_FILE):
            with open(ANALYTICS_FILE, 'r') as f:
                return json.load(f)
        return initialize_analytics()
    except:
        return initialize_analytics()


def save_analytics(data: Dict):
    """Save analytics data to file."""
    try:
        with open(ANALYTICS_FILE, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    except Exception as e:
        print(f"Warning: Could not save analytics: {e}")


def log_conversation(session_data: Dict):
    """
    Log a completed conversation for analytics.
    
    Args:
        session_data: Complete session state with conversation details
    """
    analytics = load_analytics()
    
    # Extract key metrics
    conversation_log = {
        "timestamp": datetime.now().isoformat(),
        "customer_id": session_data.get("customer_id"),
        "customer_profile": session_data.get("customer_profile_key", "UNKNOWN"),
        "campaign_source": session_data.get("campaign_source", "Unknown"),
        "application_status": session_data.get("application_status", "NOT_STARTED"),
        "loan_amount": session_data.get("loan_application", {}).get("loan_amount", 0),
        "approval_status": "APPROVED" if session_data.get("loan_approved") else "REJECTED",
        "detected_objections": session_data.get("detected_objections", []),
        "sentiment_evolution": session_data.get("sentiment_history", []),
        "drop_off_stage": get_drop_off_stage(session_data),
        "time_to_decision": calculate_time_to_decision(session_data),
        "interaction_count": len(session_data.get("interaction_history", [])),
        "cross_sell_offered": session_data.get("cross_sell_offered", False),
        "cross_sell_accepted": session_data.get("cross_sell_accepted", False)
    }
    
    analytics["conversations"].append(conversation_log)
    
    # Update weekly stats
    week_key = datetime.now().strftime("%Y-W%U")
    if week_key not in analytics["weekly_stats"]:
        analytics["weekly_stats"][week_key] = {
            "total_conversations": 0,
            "approvals": 0,
            "rejections": 0,
            "drop_offs": 0,
            "avg_time_to_decision": 0,
            "objections_handled": 0,
            "sentiment_avg": 0.0
        }
    
    week_stats = analytics["weekly_stats"][week_key]
    week_stats["total_conversations"] += 1
    
    if conversation_log["approval_status"] == "APPROVED":
        week_stats["approvals"] += 1
    elif conversation_log["approval_status"] == "REJECTED":
        week_stats["rejections"] += 1
    else:
        week_stats["drop_offs"] += 1
    
    week_stats["objections_handled"] += len(conversation_log["detected_objections"])
    
    # Update conversion funnel
    analytics["conversion_funnel"]["total_starts"] += 1
    
    if session_data.get("application_initiated"):
        analytics["conversion_funnel"]["applications_initiated"] += 1
    
    if session_data.get("kyc_verified"):
        analytics["conversion_funnel"]["kyc_completed"] += 1
    
    if session_data.get("loan_approved"):
        analytics["conversion_funnel"]["approvals"] += 1
    
    if session_data.get("sanction_letter"):
        analytics["conversion_funnel"]["sanction_letters"] += 1
    
    save_analytics(analytics)
    return conversation_log


def get_drop_off_stage(session_data: Dict) -> str:
    """Identify at which stage customer dropped off."""
    if session_data.get("sanction_letter"):
        return "COMPLETED"
    elif session_data.get("loan_approved"):
        return "POST_APPROVAL"
    elif session_data.get("kyc_verified"):
        return "POST_KYC"
    elif session_data.get("application_initiated"):
        return "POST_APPLICATION"
    else:
        return "INITIAL_CONVERSATION"


def calculate_time_to_decision(session_data: Dict) -> int:
    """Calculate time from start to approval/rejection in seconds."""
    history = session_data.get("interaction_history", [])
    if len(history) < 2:
        return 0
    
    # Approximate: count interactions × avg 15 seconds per interaction
    return len(history) * 15


def get_performance_dashboard() -> Dict:
    """
    Generate performance dashboard with week-over-week improvements.
    
    Returns:
        dict: Dashboard data with metrics and trends
    """
    analytics = load_analytics()
    
    # Get last 4 weeks
    weeks = sorted(analytics.get("weekly_stats", {}).keys())[-4:]
    
    if not weeks:
        return {
            "status": "insufficient_data",
            "message": "Not enough data for dashboard. Complete more conversations."
        }
    
    # Calculate metrics
    dashboard = {
        "period": f"{weeks[0]} to {weeks[-1]}",
        "weekly_comparison": [],
        "overall_trends": {},
        "top_objections": get_top_objections(analytics),
        "conversion_funnel": calculate_conversion_rates(analytics),
        "strategy_effectiveness": analyze_strategy_effectiveness(analytics)
    }
    
    # Week-over-week comparison
    for week in weeks:
        stats = analytics["weekly_stats"][week]
        conversion_rate = (stats.get("approvals", 0) / max(stats.get("total_conversations", 1), 1)) * 100
        
        dashboard["weekly_comparison"].append({
            "week": week,
            "conversations": stats.get("total_conversations", 0),
            "approvals": stats.get("approvals", 0),
            "conversion_rate": round(conversion_rate, 1),
            "avg_time": stats.get("avg_time_to_decision", 0),
            "objections_handled": stats.get("objections_handled", 0)
        })
    
    # Calculate improvement trends
    if len(weeks) >= 2:
        first_week = dashboard["weekly_comparison"][0]
        last_week = dashboard["weekly_comparison"][-1]
        
        dashboard["overall_trends"] = {
            "conversion_improvement": round(last_week["conversion_rate"] - first_week["conversion_rate"], 1),
            "volume_change": last_week["conversations"] - first_week["conversations"],
            "efficiency_improvement": "IMPROVING" if last_week["conversion_rate"] > first_week["conversion_rate"] else "STABLE"
        }
    
    return dashboard


def get_top_objections(analytics: Dict) -> List[Dict]:
    """Get most common objections and their resolution rates."""
    objection_stats = defaultdict(lambda: {"count": 0, "resolved": 0})
    
    for conv in analytics.get("conversations", []):
        for obj in conv.get("detected_objections", []):
            obj_type = obj.get("type", "UNKNOWN")
            objection_stats[obj_type]["count"] += 1
            
            # Consider resolved if conversation ended in approval
            if conv.get("approval_status") == "APPROVED":
                objection_stats[obj_type]["resolved"] += 1
    
    # Convert to list and calculate resolution rate
    top_objections = []
    for obj_type, stats in objection_stats.items():
        resolution_rate = (stats["resolved"] / max(stats["count"], 1)) * 100
        top_objections.append({
            "type": obj_type.replace("_", " ").title(),
            "count": stats["count"],
            "resolution_rate": round(resolution_rate, 1)
        })
    
    # Sort by count
    top_objections.sort(key=lambda x: x["count"], reverse=True)
    return top_objections[:5]


def calculate_conversion_rates(analytics: Dict) -> Dict:
    """Calculate conversion rates at each funnel stage."""
    funnel = analytics.get("conversion_funnel", {})
    
    total = max(funnel.get("total_starts", 1), 1)
    
    return {
        "total_starts": funnel.get("total_starts", 0),
        "application_rate": round((funnel.get("applications_initiated", 0) / total) * 100, 1),
        "kyc_completion_rate": round((funnel.get("kyc_completed", 0) / total) * 100, 1),
        "approval_rate": round((funnel.get("approvals", 0) / total) * 100, 1),
        "completion_rate": round((funnel.get("sanction_letters", 0) / total) * 100, 1)
    }


def analyze_strategy_effectiveness(analytics: Dict) -> List[Dict]:
    """Analyze which persuasion strategies work best."""
    strategy_stats = defaultdict(lambda: {"used": 0, "conversions": 0})
    
    for conv in analytics.get("conversations", []):
        profile = conv.get("customer_profile", "UNKNOWN")
        strategy_stats[profile]["used"] += 1
        
        if conv.get("approval_status") == "APPROVED":
            strategy_stats[profile]["conversions"] += 1
    
    # Calculate success rates
    strategies = []
    for profile, stats in strategy_stats.items():
        success_rate = (stats["conversions"] / max(stats["used"], 1)) * 100
        strategies.append({
            "strategy": profile.replace("_", " ").title(),
            "times_used": stats["used"],
            "success_rate": round(success_rate, 1)
        })
    
    strategies.sort(key=lambda x: x["success_rate"], reverse=True)
    return strategies


def display_performance_dashboard():
    """Display formatted performance dashboard in console."""
    from utils import Colors
    
    dashboard = get_performance_dashboard()
    
    if dashboard.get("status") == "insufficient_data":
        print(f"\n{Colors.YELLOW}{dashboard['message']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}📈 SELF-IMPROVING FEEDBACK LOOP - PERFORMANCE DASHBOARD{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*80}{Colors.RESET}")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}📊 WEEKLY PERFORMANCE COMPARISON{Colors.RESET}")
    print(f"{Colors.CYAN}Period: {dashboard['period']}{Colors.RESET}\n")
    
    print(f"{'Week':<15} {'Conversations':<15} {'Approvals':<12} {'Conv. Rate':<15} {'Objections':<12}")
    print(f"{'-'*80}")
    
    for week_data in dashboard["weekly_comparison"]:
        conv_rate_color = Colors.GREEN if week_data["conversion_rate"] >= 50 else Colors.YELLOW
        print(f"{week_data['week']:<15} {week_data['conversations']:<15} "
              f"{week_data['approvals']:<12} "
              f"{conv_rate_color}{week_data['conversion_rate']}%{Colors.RESET:<10} "
              f"{week_data['objections_handled']:<12}")
    
    # Overall trends
    if dashboard.get("overall_trends"):
        trends = dashboard["overall_trends"]
        print(f"\n{Colors.GREEN}{Colors.BOLD}📈 OVERALL TRENDS{Colors.RESET}")
        
        improvement = trends["conversion_improvement"]
        improvement_color = Colors.GREEN if improvement > 0 else Colors.RED
        print(f"  Conversion Rate Change: {improvement_color}{improvement:+.1f}%{Colors.RESET}")
        print(f"  Volume Change: {trends['volume_change']:+d} conversations")
        print(f"  Efficiency Status: {Colors.GREEN}{trends['efficiency_improvement']}{Colors.RESET}")
    
    # Top objections
    print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  TOP 5 OBJECTIONS & RESOLUTION RATES{Colors.RESET}")
    for idx, obj in enumerate(dashboard["top_objections"], 1):
        res_color = Colors.GREEN if obj["resolution_rate"] >= 60 else Colors.YELLOW
        print(f"  {idx}. {obj['type']}: {obj['count']} times | "
              f"Resolution: {res_color}{obj['resolution_rate']}%{Colors.RESET}")
    
    # Conversion funnel
    print(f"\n{Colors.BLUE}{Colors.BOLD}🎯 CONVERSION FUNNEL{Colors.RESET}")
    funnel = dashboard["conversion_funnel"]
    print(f"  Total Conversations: {funnel['total_starts']}")
    print(f"  Application Rate: {Colors.GREEN}{funnel['application_rate']}%{Colors.RESET}")
    print(f"  KYC Completion: {Colors.GREEN}{funnel['kyc_completion_rate']}%{Colors.RESET}")
    print(f"  Approval Rate: {Colors.GREEN}{funnel['approval_rate']}%{Colors.RESET}")
    print(f"  Full Completion: {Colors.GREEN}{funnel['completion_rate']}%{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}\n")
