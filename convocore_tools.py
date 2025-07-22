from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime

convocore_bp = Blueprint('convocore', __name__)

# Sample agent configurations for different use cases
SAMPLE_AGENTS = {
    "customer_service": {
        "name": "Customer Service Agent",
        "description": "Comprehensive customer support agent for e-commerce",
        "personality": {
            "tone": "professional",
            "style": "helpful",
            "formality": "moderate"
        },
        "knowledge_base": [
            "Product catalog and specifications",
            "Return and refund policies",
            "Shipping information",
            "Account management procedures",
            "Troubleshooting guides"
        ],
        "channels": ["web_chat", "whatsapp", "email"],
        "features": [
            "Order tracking",
            "Return processing",
            "Live agent handoff",
            "Multilingual support"
        ]
    },
    "sales_assistant": {
        "name": "Sales Assistant Agent",
        "description": "Lead generation and sales support agent",
        "personality": {
            "tone": "enthusiastic",
            "style": "persuasive",
            "formality": "casual"
        },
        "knowledge_base": [
            "Product features and benefits",
            "Pricing and promotions",
            "Competitor comparisons",
            "Customer testimonials",
            "Demo scheduling"
        ],
        "channels": ["web_chat", "facebook", "instagram"],
        "features": [
            "Lead qualification",
            "Product recommendations",
            "Demo booking",
            "CRM integration"
        ]
    },
    "appointment_scheduler": {
        "name": "Appointment Scheduler",
        "description": "Automated appointment booking for healthcare/services",
        "personality": {
            "tone": "professional",
            "style": "efficient",
            "formality": "formal"
        },
        "knowledge_base": [
            "Service descriptions",
            "Provider availability",
            "Booking policies",
            "Preparation instructions",
            "Location information"
        ],
        "channels": ["web_chat", "phone", "sms"],
        "features": [
            "Calendar integration",
            "Automated reminders",
            "Rescheduling",
            "Payment processing"
        ]
    },
    "technical_support": {
        "name": "Technical Support Agent",
        "description": "Advanced technical troubleshooting and support",
        "personality": {
            "tone": "knowledgeable",
            "style": "methodical",
            "formality": "professional"
        },
        "knowledge_base": [
            "Technical documentation",
            "Troubleshooting procedures",
            "System requirements",
            "Error code database",
            "Best practices guides"
        ],
        "channels": ["web_chat", "discord", "email"],
        "features": [
            "Diagnostic tools",
            "Screen sharing",
            "Ticket creation",
            "Escalation procedures"
        ]
    }
}

@convocore_bp.route('/agents/samples', methods=['GET'])
def get_sample_agents():
    """Get all sample agent configurations"""
    return jsonify(SAMPLE_AGENTS)

@convocore_bp.route('/agents/samples/<agent_type>', methods=['GET'])
def get_sample_agent(agent_type):
    """Get specific sample agent configuration"""
    if agent_type in SAMPLE_AGENTS:
        return jsonify(SAMPLE_AGENTS[agent_type])
    return jsonify({"error": "Agent type not found"}), 404

@convocore_bp.route('/knowledge-base/generator', methods=['POST'])
def generate_knowledge_base():
    """Generate sample knowledge base content for different industries"""
    data = request.get_json()
    industry = data.get('industry', 'general')
    use_case = data.get('use_case', 'customer_service')
    
    knowledge_templates = {
        "ecommerce": {
            "customer_service": [
                "How to track your order",
                "Return and refund policy",
                "Shipping options and costs",
                "Product warranty information",
                "Account management help"
            ],
            "sales": [
                "Product catalog overview",
                "Current promotions and discounts",
                "Size and fit guides",
                "Customer reviews and ratings",
                "Gift card information"
            ]
        },
        "healthcare": {
            "appointment_booking": [
                "Available appointment types",
                "Insurance acceptance",
                "Preparation instructions",
                "Location and parking",
                "Cancellation policies"
            ],
            "patient_support": [
                "Common symptoms guide",
                "Medication information",
                "Test result explanations",
                "Emergency procedures",
                "Contact information"
            ]
        },
        "saas": {
            "technical_support": [
                "Getting started guide",
                "Feature documentation",
                "Troubleshooting common issues",
                "API documentation",
                "Billing and subscription help"
            ],
            "sales": [
                "Product features and benefits",
                "Pricing plans comparison",
                "Integration capabilities",
                "Security and compliance",
                "Customer success stories"
            ]
        }
    }
    
    if industry in knowledge_templates and use_case in knowledge_templates[industry]:
        return jsonify({
            "industry": industry,
            "use_case": use_case,
            "knowledge_items": knowledge_templates[industry][use_case]
        })
    
    return jsonify({
        "industry": "general",
        "use_case": "customer_service",
        "knowledge_items": [
            "Frequently asked questions",
            "Company information",
            "Contact details",
            "Service descriptions",
            "General policies"
        ]
    })

@convocore_bp.route('/conversation-flows/templates', methods=['GET'])
def get_conversation_templates():
    """Get conversation flow templates"""
    templates = {
        "greeting_flow": {
            "name": "Greeting and Welcome Flow",
            "description": "Standard greeting with user intent identification",
            "nodes": [
                {
                    "id": "welcome",
                    "type": "message",
                    "content": "Hello! I'm here to help you today. What can I assist you with?"
                },
                {
                    "id": "intent_capture",
                    "type": "input",
                    "prompt": "Please describe what you need help with"
                },
                {
                    "id": "intent_routing",
                    "type": "condition",
                    "conditions": [
                        {"keyword": "order", "route": "order_support"},
                        {"keyword": "return", "route": "return_process"},
                        {"keyword": "product", "route": "product_info"},
                        {"default": "general_help"}
                    ]
                }
            ]
        },
        "escalation_flow": {
            "name": "Human Agent Escalation",
            "description": "Smooth handoff to human agents when needed",
            "nodes": [
                {
                    "id": "escalation_check",
                    "type": "condition",
                    "trigger": "user_frustrated OR complex_issue"
                },
                {
                    "id": "escalation_offer",
                    "type": "message",
                    "content": "I understand this might be complex. Would you like me to connect you with a human agent?"
                },
                {
                    "id": "handoff_process",
                    "type": "action",
                    "action": "transfer_to_human",
                    "context_transfer": True
                }
            ]
        },
        "data_collection": {
            "name": "Information Collection Flow",
            "description": "Systematic data gathering for support or sales",
            "nodes": [
                {
                    "id": "data_intro",
                    "type": "message",
                    "content": "I'll need to gather some information to help you better."
                },
                {
                    "id": "collect_name",
                    "type": "input",
                    "prompt": "What's your name?",
                    "validation": "required"
                },
                {
                    "id": "collect_email",
                    "type": "input",
                    "prompt": "What's your email address?",
                    "validation": "email"
                },
                {
                    "id": "confirmation",
                    "type": "message",
                    "content": "Thank you! I have your information and will help you now."
                }
            ]
        }
    }
    
    return jsonify(templates)

@convocore_bp.route('/deployment/checklist', methods=['POST'])
def get_deployment_checklist():
    """Generate deployment checklist based on configuration"""
    data = request.get_json()
    channels = data.get('channels', [])
    features = data.get('features', [])
    
    checklist = {
        "pre_deployment": [
            "Test agent responses with sample queries",
            "Validate knowledge base content accuracy",
            "Configure agent personality and tone",
            "Set up conversation flows and logic",
            "Test error handling and fallback responses"
        ],
        "channel_specific": [],
        "feature_specific": [],
        "post_deployment": [
            "Monitor initial user interactions",
            "Review conversation logs for issues",
            "Gather user feedback",
            "Optimize based on real usage patterns",
            "Set up ongoing maintenance schedule"
        ]
    }
    
    # Add channel-specific items
    channel_requirements = {
        "whatsapp": ["Verify WhatsApp Business account", "Test media sharing capabilities"],
        "phone": ["Configure phone number", "Test voice quality and clarity"],
        "web_chat": ["Embed chat widget on website", "Test responsive design"],
        "facebook": ["Connect Facebook page", "Test messenger integration"],
        "instagram": ["Link Instagram business account", "Verify DM functionality"]
    }
    
    for channel in channels:
        if channel in channel_requirements:
            checklist["channel_specific"].extend(channel_requirements[channel])
    
    # Add feature-specific items
    feature_requirements = {
        "live_handoff": ["Configure human agent routing", "Test escalation procedures"],
        "calendar_integration": ["Connect calendar system", "Test booking functionality"],
        "payment_processing": ["Set up payment gateway", "Test transaction flow"],
        "crm_integration": ["Configure CRM connection", "Test data synchronization"]
    }
    
    for feature in features:
        if feature in feature_requirements:
            checklist["feature_specific"].extend(feature_requirements[feature])
    
    return jsonify(checklist)

@convocore_bp.route('/analytics/metrics', methods=['GET'])
def get_analytics_metrics():
    """Get sample analytics metrics and KPIs"""
    metrics = {
        "conversation_metrics": {
            "total_conversations": 1250,
            "completion_rate": 87.5,
            "average_duration": "3m 45s",
            "user_satisfaction": 4.2,
            "escalation_rate": 12.3
        },
        "channel_performance": {
            "web_chat": {"conversations": 650, "satisfaction": 4.3},
            "whatsapp": {"conversations": 400, "satisfaction": 4.1},
            "phone": {"conversations": 200, "satisfaction": 4.0}
        },
        "top_intents": [
            {"intent": "order_status", "count": 320, "success_rate": 92},
            {"intent": "product_info", "count": 280, "success_rate": 88},
            {"intent": "return_request", "count": 150, "success_rate": 85},
            {"intent": "technical_support", "count": 120, "success_rate": 78}
        ],
        "knowledge_base_usage": {
            "most_accessed": [
                "Shipping policies",
                "Return procedures",
                "Product specifications",
                "Account management"
            ],
            "gaps_identified": [
                "International shipping",
                "Bulk order discounts",
                "Technical troubleshooting"
            ]
        }
    }
    
    return jsonify(metrics)

@convocore_bp.route('/cost-calculator', methods=['POST'])
def calculate_costs():
    """Calculate estimated costs based on usage parameters"""
    data = request.get_json()
    
    monthly_conversations = data.get('monthly_conversations', 1000)
    voice_minutes = data.get('voice_minutes', 0)
    knowledge_base_size = data.get('knowledge_base_size', 10000)  # characters
    channels = data.get('channels', ['web_chat'])
    
    # Base pricing (simplified)
    base_cost = 20  # Pay-as-you-go plan
    
    # Conversation costs
    conversation_cost = monthly_conversations * 0.001
    
    # Voice costs (using average provider pricing)
    voice_cost = voice_minutes * 0.025  # Average of STT + TTS
    
    # Knowledge base costs
    kb_cost = (knowledge_base_size / 10000) * 0.001
    
    # Channel costs
    channel_cost = len(channels) * 0.001 * monthly_conversations
    
    total_cost = base_cost + conversation_cost + voice_cost + kb_cost + channel_cost
    
    breakdown = {
        "base_plan": base_cost,
        "conversations": conversation_cost,
        "voice_minutes": voice_cost,
        "knowledge_base": kb_cost,
        "channels": channel_cost,
        "total_monthly": round(total_cost, 2)
    }
    
    return jsonify(breakdown)

