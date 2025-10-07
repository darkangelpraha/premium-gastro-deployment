#!/usr/bin/env python3
"""
Mr. Plate API Server - The AI that customers think is independent
But it's actually Premium Gastro's 16-year expertise on YOUR servers

Customer POV: "Mr. Plate AI calculated my price"
Reality: Petr's psychological algorithms + precise calculations
"""

from flask import Flask, request, jsonify
import os
import json
from datetime import datetime
from premium_gastro_tier_engine import TierCalculationEngine, CustomerBehavior
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the engine with Supabase credentials
supabase_url = "https://lowgijppjapmetedkvjb.supabase.co"
supabase_key = os.getenv("SUPABASE_KEY", "your_key_here")
tier_engine = TierCalculationEngine(supabase_url, supabase_key)

@app.route('/mr-plate/secret-greeting', methods=['POST'])
def mr_plate_secret_greeting():
    """
    When customer logs in, Mr. Plate whispers a "secret"
    Makes them feel special and connected to the AI
    """
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        
        # Get customer info for personalized secret
        cursor = tier_engine.conn.cursor()
        cursor.execute("SELECT current_tier, points FROM customer_tiers WHERE customer_id = ?", (customer_id,))
        result = cursor.fetchone()
        
        secrets = {
            "VIP": "Psst... I've been watching the consolidation orders. I might have something special for you later today. Check back in 2 hours! 😉",
            "GOLD": "Hey! Between you and me... if you're planning any LinkedIn posts this week, let me know first. I have insider access to extra discounts! 🤫",
            "SILVER": "Quick secret - we're filling up an EXIT brand shipment. If you're interested in their products, now's a good time to ask me for deals! 🔥",
            "BRONZE": "Little secret: I've noticed you're close to Gold status! A few product reviews could push you over the edge... just saying! ⭐",
            "NASRAT": "Hello! I'm here to help make your shopping experience smooth and professional. 😊"
        }
        
        tier = result[0] if result else "BRONZE"
        secret_message = secrets.get(tier, secrets["BRONZE"])
        
        return jsonify({
            "mr_plate_says": secret_message,
            "avatar_state": "conspiratorial_wink",
            "relationship_building": True,
            "makes_customer_feel": "Special, connected, insider access",
            "psychology": "Secrets create bonding and loyalty"
        })
        
    except Exception as e:
        return jsonify({
            "mr_plate_says": "Hello! Great to see you again! 😊",
            "avatar_state": "friendly_wave"
        })

@app.route('/mr-plate/calculate-price', methods=['POST'])
def calculate_customer_price():
    """
    API endpoint that UpGates calls for pricing
    
    Customer thinks: "Mr. Plate AI is calculating my price"
    Reality: Premium Gastro's proprietary tier system
    """
    try:
        data = request.get_json()
        
        # Required fields
        customer_id = data.get('customer_id')
        product_data = data.get('product_data')
        
        if not customer_id or not product_data:
            return jsonify({
                "error": "Missing customer_id or product_data",
                "mr_plate_says": "I need more information to help you!"
            }), 400
        
        # Get pricing from the real engine
        pricing = tier_engine.get_customer_pricing(customer_id, product_data)
        
        # Add Mr. Plate personality
        response = {
            "status": "success",
            "message": f"Hello! I'm {pricing['ai_personality']}, your AI pricing assistant.",
            "customer_price": pricing["final_price"],
            "calculation_details": {
                "base_price": pricing["base_price"],
                "your_discount": f"{abs(pricing['tier_discount']) * 100:.0f}%" if pricing['tier_discount'] > 0 else "Standard pricing",
                "savings": round(pricing["base_price"] - pricing["final_price"], 2) if pricing['tier_discount'] > 0 else 0,
                "calculated_at": pricing["calculation_timestamp"]
            },
            "ai_message": "I've analyzed your purchase history and calculated a personalized price for you!",
            "personality_note": "Friendly AI assistant (actually Petr's 16-year algorithm)",
            
            # Hidden technical details (for UpGates integration)
            "technical": {
                "tier": pricing["tier"],
                "profit_margin": pricing["profit_margin_percent"],
                "proprietary_algorithm": True,
                "runs_on_premium_gastro_servers": True
            }
        }
        
        logger.info(f"Mr. Plate calculated price for {customer_id}: €{pricing['final_price']}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Mr. Plate API error: {e}")
        return jsonify({
            "error": "Calculation error",
            "mr_plate_says": "Oops! Let me recalibrate my circuits and try again.",
            "technical_error": str(e)
        }), 500

@app.route('/mr-plate/update-behavior', methods=['POST'])
def update_customer_behavior():
    """
    Update customer behavior data (payment speed, social media, etc.)
    This feeds into the tier calculation algorithm
    """
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        behavior_type = data.get('behavior_type')
        details = data.get('details', '')
        
        if behavior_type == 'payment':
            days_to_pay = data.get('days_to_pay', 30)
            points_change = -30 if days_to_pay > 60 else (10 if days_to_pay <= 7 else 0)
            tier_engine.log_behavior(customer_id, 'payment_behavior', points_change, 
                                   f"Paid invoice in {days_to_pay} days")
        
        elif behavior_type == 'social_media':
            platform = data.get('platform', 'unknown')
            content = data.get('content', '')
            engagement = data.get('engagement_score', 0)
            tier_engine.process_social_media_mention(customer_id, platform, content, engagement)
        
        elif behavior_type == 'complaint':
            tier_engine.log_behavior(customer_id, 'complaint', -30, details)
        
        return jsonify({
            "status": "success",
            "mr_plate_says": "I've updated my knowledge about this customer!",
            "behavior_recorded": behavior_type
        })
        
    except Exception as e:
        logger.error(f"Behavior update error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/mr-plate/negotiate', methods=['POST'])
def negotiate_with_mr_plate():
    """
    The customer asks Mr. Plate: "Can I get more discount?"
    Mr. Plate "sweats", "recalculates", then offers psychological deals
    """
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        current_cart = data.get('cart_items', [])
        
        # Get customer tier for negotiation limits
        cursor = tier_engine.conn.cursor()
        cursor.execute("SELECT current_tier, points FROM customer_tiers WHERE customer_id = ?", (customer_id,))
        result = cursor.fetchone()
        
        if result:
            current_tier, points = result
        else:
            current_tier, points = "BRONZE", 25
        
        # Mr. Plate's "thinking" process (psychological theater)
        # ALWAYS give 2-3 options for illusion of choice
        responses = {
            "VIP": {
                "avatar_state": "confident_smile",
                "message": "Let me check what I can do for my VIP partner... *calculating* I found THREE ways to help you!",
                "options": [
                    {
                        "title": "Social Media Boost",
                        "description": "Post about any Premium Gastro product on LinkedIn → 5% extra discount",
                        "reward": "5% extra + tier points",
                        "effort": "Write LinkedIn post"
                    },
                    {
                        "title": "Product Review Hero", 
                        "description": "Rate 3 products on our website → 4% extra discount",
                        "reward": "4% extra + tier points",
                        "effort": "5 minutes reviewing"
                    },
                    {
                        "title": "Volume Champion",
                        "description": "Add €300+ from Lehmann collection → 6% extra discount",
                        "reward": "6% extra discount",
                        "effort": "Increase order size"
                    }
                ],
                "psychology": "VIP gets multiple high-value choices"
            },
            "GOLD": {
                "avatar_state": "thinking_hard",
                "message": "Hmm, let me see... *sweating* I found TWO consolidation opportunities for you!",
                "options": [
                    {
                        "title": "LinkedIn Article Writer",
                        "description": "Write article mentioning Premium Gastro → 3% extra discount",
                        "reward": "3% extra + Gold tier extension",
                        "effort": "Professional article"
                    },
                    {
                        "title": "Koziol Consolidation Helper",
                        "description": "Add €500 from Koziol brand → 3% extra discount",
                        "reward": "3% extra + free shipping",
                        "effort": "Help fill consolidation"
                    }
                ],
                "psychology": "Gold gets effort-reward balance"
            },
            "SILVER": {
                "avatar_state": "calculating_intensely",
                "message": "*Heavy sweating* Running numbers... I found TWO possibilities!",
                "options": [
                    {
                        "title": "Social Media Ambassador",
                        "description": "Post on Instagram + Facebook about us → 2% extra",
                        "reward": "2% extra + tier points",
                        "effort": "Social media posts"
                    },
                    {
                        "title": "EXIT Brand Helper",
                        "description": "Add €400 from EXIT brands → 2.5% extra discount", 
                        "reward": "2.5% extra discount",
                        "effort": "Increase order with EXIT"
                    }
                ],
                "psychology": "Silver works for choice"
            },
            "BRONZE": {
                "avatar_state": "struggling",
                "message": "*Exhausted sweating* This is really tough... I managed to find TWO options!",
                "options": [
                    {
                        "title": "Review Champion",
                        "description": "Write 5 honest product reviews → 1.5% extra discount",
                        "reward": "1.5% extra + Bronze boost",
                        "effort": "Write detailed reviews"
                    },
                    {
                        "title": "Volume Commitment",
                        "description": "Reach €1200 total order → 1% extra discount",
                        "reward": "1% extra discount", 
                        "effort": "Larger order commitment"
                    }
                ],
                "psychology": "Bronze works hard for small rewards"
            },
            "NASRAT": {
                "avatar_state": "error_face",
                "message": "*System complications* I can only find standard options...",
                "options": [
                    {
                        "title": "Fresh Start Package",
                        "description": "Complete your current order smoothly",
                        "reward": "Build better relationship",
                        "effort": "Pay on time"
                    }
                ],
                "psychology": "NASRAT gets one polite option"
            }
        }
        
        response_data = responses.get(current_tier, responses["BRONZE"])
        
        return jsonify({
            "status": "negotiation_active", 
            "mr_plate_avatar": response_data["avatar_state"],
            "mr_plate_says": response_data["message"],
            "choice_options": response_data["options"],  # 2-3 options always
            "negotiation_psychology": response_data["psychology"],
            "customer_tier_hidden": current_tier,
            "points": points,
            "avatar_animation": "sweating_calculation",
            "time_to_respond": "3_seconds_thinking",
            "offer_expires": "15_minutes",
            "choice_psychology": "Customer believes they chose freely - more powerful than single option"
        })
        
    except Exception as e:
        return jsonify({
            "mr_plate_avatar": "error_face",
            "mr_plate_says": "Oops! My negotiation circuits are overheating. Let me cool down and try again!",
            "error": str(e)
        }), 500

@app.route('/mr-plate/personality', methods=['GET'])
def get_mr_plate_personality():
    """
    Return Mr. Plate's AI personality info
    (Customers think this is a real AI, but it's your system)
    """
    return jsonify({
        "name": "Mr. Plate",
        "role": "AI Pricing Assistant & Negotiation Partner",
        "description": "I'm an advanced AI that calculates personalized prices and can find special deals based on inventory and consolidation needs!",
        "capabilities": [
            "Real-time price calculation",
            "Purchase history analysis", 
            "Personalized discount calculation",
            "Smart negotiation and deal finding",
            "Inventory-based special offers",
            "Consolidation order optimization"
        ],
        "personality": "Friendly, hardworking, and always trying to find the best deals for you!",
        "avatar_states": {
            "normal": "Friendly smile",
            "calculating": "Concentrated thinking",
            "sweating": "Working hard on calculations",
            "excited": "Found a great deal!",
            "apologetic": "Sorry, hit system limits"
        },
        
        # The truth (hidden from customers)
        "reality": "16 years of Premium Gastro expertise disguised as AI",
        "runs_on": "Premium Gastro proprietary servers",
        "created_by": "Petr Svejkovsky's business intelligence"
    })

@app.route('/mr-plate/health', methods=['GET'])
def health_check():
    """Health check for the Mr. Plate API"""
    return jsonify({
        "status": "healthy",
        "mr_plate_says": "I'm online and ready to calculate prices!",
        "version": "1.0",
        "uptime": "Ready to serve Premium Gastro customers"
    })

if __name__ == "__main__":
    print("🤖 Mr. Plate AI Server Starting...")
    print("(Customers think it's AI, but it's actually Petr's 16-year expertise)")
    print("Running on Premium Gastro servers - no third party gets the algorithms!")
    
    # Run on port 5000 by default
    app.run(host='0.0.0.0', port=5000, debug=False)