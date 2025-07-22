#!/usr/bin/env python3
"""
Convocore Implementation Helper Scripts
Utility functions for setting up and managing Convocore agents
"""

import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Any

class ConvocoreAgentBuilder:
    """Helper class for building Convocore agent configurations"""
    
    def __init__(self):
        self.config = {
            "agent_name": "",
            "description": "",
            "personality": {},
            "knowledge_base": {"sources": [], "categories": []},
            "conversation_flows": {},
            "integrations": [],
            "channels": []
        }
    
    def set_basic_info(self, name: str, description: str):
        """Set basic agent information"""
        self.config["agent_name"] = name
        self.config["description"] = description
        return self
    
    def set_personality(self, tone: str, style: str, formality: str, empathy_level: str = "medium"):
        """Configure agent personality"""
        self.config["personality"] = {
            "tone": tone,
            "style": style,
            "formality": formality,
            "empathy_level": empathy_level
        }
        return self
    
    def add_knowledge_source(self, source_type: str, content: str, description: str):
        """Add a knowledge base source"""
        source = {
            "type": source_type,
            "content": content,
            "description": description
        }
        self.config["knowledge_base"]["sources"].append(source)
        return self
    
    def add_knowledge_categories(self, categories: List[str]):
        """Add knowledge base categories"""
        self.config["knowledge_base"]["categories"].extend(categories)
        return self
    
    def add_conversation_flow(self, flow_name: str, flow_config: Dict[str, Any]):
        """Add a conversation flow"""
        self.config["conversation_flows"][flow_name] = flow_config
        return self
    
    def add_integration(self, integration_type: str, purpose: str):
        """Add an integration"""
        integration = {
            "type": integration_type,
            "purpose": purpose
        }
        self.config["integrations"].append(integration)
        return self
    
    def add_channel(self, channel_type: str, settings: Dict[str, Any]):
        """Add a deployment channel"""
        channel = {
            "type": channel_type,
            "settings": settings
        }
        self.config["channels"].append(channel)
        return self
    
    def export_config(self, filename: str = None):
        """Export configuration to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"agent_config_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.config, f, indent=2)
        
        return filename
    
    def get_config(self):
        """Get the current configuration"""
        return self.config.copy()

class KnowledgeBaseManager:
    """Helper class for managing knowledge base content"""
    
    @staticmethod
    def create_faq_from_csv(csv_file: str, output_file: str = None):
        """Convert CSV file to FAQ format for knowledge base"""
        faqs = []
        
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                faq = {
                    "question": row.get("question", ""),
                    "answer": row.get("answer", ""),
                    "category": row.get("category", "General"),
                    "keywords": row.get("keywords", "").split(",") if row.get("keywords") else []
                }
                faqs.append(faq)
        
        if not output_file:
            output_file = "knowledge_base_faqs.json"
        
        with open(output_file, 'w') as f:
            json.dump({"faqs": faqs}, f, indent=2)
        
        return output_file
    
    @staticmethod
    def generate_sample_knowledge_base(industry: str, use_case: str):
        """Generate sample knowledge base content"""
        templates = {
            "ecommerce": {
                "customer_service": [
                    {
                        "question": "How can I track my order?",
                        "answer": "You can track your order by entering your order number on our tracking page or by logging into your account.",
                        "category": "Order Management",
                        "keywords": ["track", "order", "shipping", "delivery"]
                    },
                    {
                        "question": "What is your return policy?",
                        "answer": "We offer a 30-day return policy for most items. Items must be in original condition with tags attached.",
                        "category": "Returns & Refunds",
                        "keywords": ["return", "refund", "exchange", "policy"]
                    },
                    {
                        "question": "How long does shipping take?",
                        "answer": "Standard shipping takes 3-5 business days. Express shipping is available for 1-2 day delivery.",
                        "category": "Shipping & Delivery",
                        "keywords": ["shipping", "delivery", "time", "fast"]
                    }
                ]
            },
            "healthcare": {
                "appointment_booking": [
                    {
                        "question": "How do I book an appointment?",
                        "answer": "You can book an appointment online through our patient portal, by calling our office, or through this chat.",
                        "category": "Appointment Booking",
                        "keywords": ["book", "appointment", "schedule", "visit"]
                    },
                    {
                        "question": "What insurance do you accept?",
                        "answer": "We accept most major insurance plans including Blue Cross, Aetna, Cigna, and Medicare.",
                        "category": "Insurance & Billing",
                        "keywords": ["insurance", "coverage", "billing", "payment"]
                    }
                ]
            },
            "saas": {
                "technical_support": [
                    {
                        "question": "How do I reset my password?",
                        "answer": "Click 'Forgot Password' on the login page and follow the instructions sent to your email.",
                        "category": "Account Management",
                        "keywords": ["password", "reset", "login", "account"]
                    },
                    {
                        "question": "How do I integrate with my CRM?",
                        "answer": "Go to Settings > Integrations and select your CRM from the available options. Follow the setup wizard.",
                        "category": "Integrations",
                        "keywords": ["crm", "integration", "connect", "setup"]
                    }
                ]
            }
        }
        
        return templates.get(industry, {}).get(use_case, [])

class ConversationFlowBuilder:
    """Helper class for building conversation flows"""
    
    @staticmethod
    def create_greeting_flow(agent_name: str, quick_replies: List[str]):
        """Create a standard greeting flow"""
        return {
            "greeting": {
                "message": f"Hi! I'm {agent_name}. How can I help you today?",
                "quick_replies": quick_replies,
                "type": "message"
            }
        }
    
    @staticmethod
    def create_escalation_flow(escalation_message: str = None):
        """Create a human escalation flow"""
        if not escalation_message:
            escalation_message = "I'll connect you with a human agent who can better assist you."
        
        return {
            "escalation": {
                "triggers": [
                    "user_frustrated",
                    "complex_issue",
                    "human_request"
                ],
                "message": escalation_message,
                "action": "transfer_to_human",
                "type": "escalation"
            }
        }
    
    @staticmethod
    def create_data_collection_flow(fields: List[Dict[str, str]]):
        """Create a data collection flow"""
        flow = {
            "data_collection": {
                "intro_message": "I'll need to gather some information to help you better.",
                "fields": fields,
                "type": "form"
            }
        }
        return flow

class DeploymentHelper:
    """Helper class for deployment tasks"""
    
    @staticmethod
    def generate_deployment_checklist(channels: List[str], features: List[str]):
        """Generate a deployment checklist"""
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
        
        # Channel-specific requirements
        channel_requirements = {
            "whatsapp": ["Verify WhatsApp Business account", "Test media sharing"],
            "phone": ["Configure phone number", "Test voice quality"],
            "web_chat": ["Embed chat widget", "Test responsive design"],
            "facebook": ["Connect Facebook page", "Test messenger integration"],
            "instagram": ["Link Instagram account", "Verify DM functionality"]
        }
        
        for channel in channels:
            if channel in channel_requirements:
                checklist["channel_specific"].extend(channel_requirements[channel])
        
        # Feature-specific requirements
        feature_requirements = {
            "live_handoff": ["Configure human agent routing", "Test escalation"],
            "calendar_integration": ["Connect calendar system", "Test booking"],
            "payment_processing": ["Set up payment gateway", "Test transactions"],
            "crm_integration": ["Configure CRM connection", "Test data sync"]
        }
        
        for feature in features:
            if feature in feature_requirements:
                checklist["feature_specific"].extend(feature_requirements[feature])
        
        return checklist
    
    @staticmethod
    def estimate_costs(monthly_conversations: int, voice_minutes: int, 
                      knowledge_base_size: int, channels: List[str]):
        """Estimate monthly costs"""
        base_cost = 20  # Pay-as-you-go plan
        conversation_cost = monthly_conversations * 0.001
        voice_cost = voice_minutes * 0.025  # Average STT + TTS
        kb_cost = (knowledge_base_size / 10000) * 0.001
        channel_cost = len(channels) * 0.001 * monthly_conversations
        
        total_cost = base_cost + conversation_cost + voice_cost + kb_cost + channel_cost
        
        return {
            "base_plan": base_cost,
            "conversations": conversation_cost,
            "voice_minutes": voice_cost,
            "knowledge_base": kb_cost,
            "channels": channel_cost,
            "total_monthly": round(total_cost, 2)
        }

# Example usage functions
def create_customer_service_agent():
    """Example: Create a customer service agent configuration"""
    builder = ConvocoreAgentBuilder()
    
    agent = (builder
             .set_basic_info("Customer Service Bot", "Comprehensive customer support agent")
             .set_personality("friendly", "helpful", "casual", "high")
             .add_knowledge_source("url", "https://help.company.com", "Help center")
             .add_knowledge_source("document", "faq.pdf", "Frequently asked questions")
             .add_knowledge_categories(["Orders", "Shipping", "Returns", "Products"])
             .add_conversation_flow("greeting", {
                 "message": "Hi! How can I help you today?",
                 "quick_replies": ["Track order", "Return item", "Product info"]
             })
             .add_integration("crm", "Customer data access")
             .add_integration("order_system", "Order tracking")
             .add_channel("web_chat", {"proactive_greeting": True})
             .add_channel("whatsapp", {"business_profile": True}))
    
    return agent.get_config()

def create_appointment_scheduler():
    """Example: Create an appointment scheduling agent"""
    builder = ConvocoreAgentBuilder()
    
    agent = (builder
             .set_basic_info("Appointment Scheduler", "Automated booking system")
             .set_personality("professional", "efficient", "formal", "medium")
             .add_knowledge_source("direct_input", "Available services and pricing", "Service catalog")
             .add_knowledge_categories(["Booking", "Cancellation", "Rescheduling"])
             .add_conversation_flow("booking", {
                 "steps": ["Collect info", "Check availability", "Confirm booking"]
             })
             .add_integration("calendar", "Real-time availability")
             .add_integration("payment", "Booking deposits")
             .add_channel("phone", {"voice_recognition": True})
             .add_channel("sms", {"appointment_reminders": True}))
    
    return agent.get_config()

if __name__ == "__main__":
    # Example usage
    print("Creating sample customer service agent...")
    cs_agent = create_customer_service_agent()
    print(json.dumps(cs_agent, indent=2))
    
    print("\nGenerating deployment checklist...")
    checklist = DeploymentHelper.generate_deployment_checklist(
        ["web_chat", "whatsapp"], 
        ["live_handoff", "crm_integration"]
    )
    print(json.dumps(checklist, indent=2))
    
    print("\nEstimating costs...")
    costs = DeploymentHelper.estimate_costs(1000, 100, 50000, ["web_chat", "whatsapp"])
    print(json.dumps(costs, indent=2))

