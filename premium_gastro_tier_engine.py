#!/usr/bin/env python3
"""
Premium Gastro Digital CRM Tier Engine
REAL IMPLEMENTATION - Fear + Reward Psychology + Precise Calculations

This is the actual working system, not a bedtime story.
"""

import os
import json
import requests
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CustomerTier(Enum):
    """Customer tier definitions with exact discount percentages"""
    VIP = {"name": "VIP", "discount": 0.20, "code": "vip"}
    GOLD = {"name": "Gold", "discount": 0.10, "code": "gold"}
    SILVER = {"name": "Silver", "discount": 0.05, "code": "silver"}
    BRONZE = {"name": "Bronze", "discount": 0.00, "code": "bronze"}
    NASRAT = {"name": "Nasrat", "discount": -1.00, "code": "nasrat"}  # 100% penalty

@dataclass
class CustomerBehavior:
    """Track customer behavior for tier calculation"""
    customer_id: str
    payment_speed_avg: float  # Average days to pay invoices
    order_frequency: float    # Orders per year
    lifetime_value: float     # Total purchase value
    order_consistency: float  # Standard deviation of order values
    social_media_score: int   # Points from social media activity
    complaints: int           # Number of complaints/bad reviews
    last_order_date: str      # ISO format date
    created_date: str         # Customer registration date

class TierCalculationEngine:
    """Real tier calculation with precise algorithms - Mr. Plate AI Backend"""
    
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json"
        }
        
        # 16 years of know-how runs on OUR servers, not theirs
        self.ai_personality_name = "Mr. Plate"
        self.pricing_intelligence = "Premium Gastro Proprietary Algorithm"
        
        # Initialize local SQLite for caching and calculations
        self.init_local_db()
    
    def init_local_db(self):
        """Initialize local SQLite database for tier calculations"""
        self.conn = sqlite3.connect('/tmp/premium_gastro_tiers.db')
        cursor = self.conn.cursor()
        
        # Create tier calculation table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_tiers (
                customer_id TEXT PRIMARY KEY,
                current_tier TEXT NOT NULL,
                points INTEGER DEFAULT 0,
                last_calculation DATE,
                tier_change_date DATE,
                locked_until DATE,
                behavior_data TEXT
            )
        """)
        
        # Create behavior tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS behavior_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT,
                action_type TEXT,
                points_change INTEGER,
                details TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
        logger.info("Local database initialized")

    def calculate_tier_points(self, behavior: CustomerBehavior) -> int:
        """
        REAL ALGORITHM: Calculate tier points based on customer behavior
        Returns: Total points (0-100+)
        """
        points = 50  # Start at neutral (Bronze level)
        
        # 1. PAYMENT SPEED (25% weight)
        if behavior.payment_speed_avg <= 7:
            points += 20  # Excellent - pays within week
        elif behavior.payment_speed_avg <= 14:
            points += 15  # Good - pays within 2 weeks
        elif behavior.payment_speed_avg <= 30:
            points += 5   # Acceptable - pays within month
        elif behavior.payment_speed_avg > 60:
            points -= 30  # NASRAT territory - very late payments
        
        # 2. PURCHASE VOLUME (40% weight)
        if behavior.lifetime_value >= 100000:    # €100K+
            points += 25
        elif behavior.lifetime_value >= 50000:   # €50K+
            points += 20
        elif behavior.lifetime_value >= 20000:   # €20K+
            points += 15
        elif behavior.lifetime_value >= 10000:   # €10K+
            points += 10
        elif behavior.lifetime_value < 1000:     # Less than €1K
            points -= 10
        
        # 3. ORDER FREQUENCY (20% weight)
        if behavior.order_frequency >= 12:       # Monthly orders
            points += 15
        elif behavior.order_frequency >= 6:      # Bi-monthly
            points += 10
        elif behavior.order_frequency >= 3:      # Quarterly
            points += 5
        elif behavior.order_frequency < 1:       # Less than yearly
            points -= 10
        
        # 4. SOCIAL MEDIA ACTIVITY (15% weight)
        points += min(behavior.social_media_score, 15)  # Cap at 15 points
        
        # 5. NEGATIVE BEHAVIOR PENALTIES
        points -= behavior.complaints * 10  # -10 points per complaint
        
        # 6. INACTIVITY PENALTY
        last_order = datetime.fromisoformat(behavior.last_order_date)
        days_since_order = (datetime.now() - last_order).days
        if days_since_order > 180:  # 6 months inactive
            points -= 15
        elif days_since_order > 365:  # 1 year inactive
            points -= 25
        
        return max(0, points)  # Minimum 0 points

    def assign_tier(self, points: int) -> CustomerTier:
        """Convert points to tier assignment"""
        if points >= 100:
            return CustomerTier.VIP
        elif points >= 75:
            return CustomerTier.GOLD
        elif points >= 50:
            return CustomerTier.SILVER
        elif points >= 25:
            return CustomerTier.BRONZE
        else:
            return CustomerTier.NASRAT

    def calculate_precise_price(self, 
                              supplier_cost: float, 
                              brand_margin_percent: float,
                              transport_cost: float,
                              tier: CustomerTier) -> Dict:
        """
        REAL PRICING CALCULATION - To the penny
        
        Returns: Complete pricing breakdown
        """
        # Base price calculation
        brand_margin = supplier_cost * (brand_margin_percent / 100)
        base_price = supplier_cost + brand_margin + transport_cost
        
        # Apply tier discount/penalty
        tier_multiplier = 1 - tier.value["discount"]
        final_price = base_price * tier_multiplier
        
        # Calculate profit
        total_cost = supplier_cost + transport_cost + (base_price * 0.05)  # 5% operating cost
        profit = final_price - total_cost
        profit_margin = (profit / final_price) * 100 if final_price > 0 else 0
        
        return {
            "supplier_cost": round(supplier_cost, 2),
            "brand_margin": round(brand_margin, 2),
            "transport_cost": round(transport_cost, 2),
            "base_price": round(base_price, 2),
            "tier": tier.value["name"],
            "tier_discount": tier.value["discount"],
            "final_price": round(final_price, 2),
            "profit": round(profit, 2),
            "profit_margin_percent": round(profit_margin, 2),
            "calculation_timestamp": datetime.now().isoformat()
        }

    def process_social_media_mention(self, 
                                   customer_id: str, 
                                   platform: str, 
                                   content: str, 
                                   engagement_score: int) -> bool:
        """
        REAL SOCIAL MEDIA PROCESSING
        Analyze mentions and award tier upgrades
        """
        # Simple sentiment analysis (replace with AI service)
        positive_words = ["great", "excellent", "amazing", "perfect", "recommend", "quality"]
        negative_words = ["bad", "terrible", "awful", "poor", "disappointed", "waste"]
        
        content_lower = content.lower()
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        if negative_count > positive_count:
            # NEGATIVE MENTION - Potential NASRAT trigger
            self.log_behavior(customer_id, "negative_social_media", -30, 
                            f"Negative mention on {platform}: {content[:100]}")
            return False
        
        elif positive_count > 0 and engagement_score >= 10:
            # POSITIVE MENTION - Reward with points
            points_reward = min(engagement_score // 5, 25)  # 5 engagements = 1 point, max 25
            self.log_behavior(customer_id, "positive_social_media", points_reward,
                            f"Positive mention on {platform} with {engagement_score} engagements")
            
            # Check if qualifies for temporary tier upgrade
            if engagement_score >= 50:
                self.grant_temporary_tier_upgrade(customer_id, "gold", days=30)
            
            return True
        
        return False

    def log_behavior(self, customer_id: str, action_type: str, points_change: int, details: str):
        """Log customer behavior for tier calculation"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO behavior_log (customer_id, action_type, points_change, details)
            VALUES (?, ?, ?, ?)
        """, (customer_id, action_type, points_change, details))
        self.conn.commit()
        logger.info(f"Logged behavior: {customer_id} - {action_type} - {points_change} points")

    def grant_temporary_tier_upgrade(self, customer_id: str, tier: str, days: int):
        """Grant temporary tier upgrade (e.g., for social media activity)"""
        unlock_date = (datetime.now() + timedelta(days=days)).isoformat()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO customer_tiers 
            (customer_id, current_tier, locked_until, tier_change_date)
            VALUES (?, ?, ?, ?)
        """, (customer_id, tier.upper(), unlock_date, datetime.now().isoformat()))
        self.conn.commit()
        
        logger.info(f"Granted {days}-day {tier.upper()} upgrade to customer {customer_id}")

    def sync_with_supabase(self):
        """Sync tier data with Supabase for UpGates integration"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customer_tiers")
        local_tiers = cursor.fetchall()
        
        for tier_record in local_tiers:
            customer_id, current_tier, points, last_calc, tier_change, locked_until, behavior_data = tier_record
            
            # Sync to Supabase
            supabase_data = {
                "customer_id": customer_id,
                "tier": current_tier.lower(),
                "points": points,
                "last_calculation": last_calc,
                "locked_until": locked_until,
                "updated_at": datetime.now().isoformat()
            }
            
            try:
                response = requests.post(
                    f"{self.supabase_url}/rest/v1/customer_tiers",
                    headers=self.headers,
                    json=supabase_data
                )
                if response.status_code in [200, 201]:
                    logger.info(f"Synced customer {customer_id} tier to Supabase")
                else:
                    logger.error(f"Failed to sync customer {customer_id}: {response.text}")
            except Exception as e:
                logger.error(f"Supabase sync error: {e}")

    def get_customer_pricing(self, customer_id: str, product_data: Dict) -> Dict:
        """
        MAIN FUNCTION: Get real-time pricing for customer
        This is what UpGates will call via API
        
        Mr. Plate AI calculates this remotely on Premium Gastro servers
        Customer thinks it's independent AI, but it's YOUR 16 years of expertise
        """
        # Get customer tier
        cursor = self.conn.cursor()
        cursor.execute("SELECT current_tier FROM customer_tiers WHERE customer_id = ?", (customer_id,))
        result = cursor.fetchone()
        
        if result:
            tier_name = result[0]
            tier = CustomerTier[tier_name]
        else:
            # New customer - assign Bronze by default
            tier = CustomerTier.BRONZE
            self.log_behavior(customer_id, "new_customer", 25, "Initial Bronze tier assignment")
        
        # Calculate precise pricing using PROPRIETARY ALGORITHM
        pricing = self.calculate_precise_price(
            supplier_cost=product_data["supplier_cost"],
            brand_margin_percent=product_data["brand_margin_percent"],
            transport_cost=product_data["transport_cost"],
            tier=tier
        )
        
        # Add customer context - hide the intelligence
        pricing["customer_id"] = customer_id
        pricing["tier_hidden"] = True  # Never show tier to customer
        pricing["ai_personality"] = self.ai_personality_name
        pricing["display_message"] = f"{self.ai_personality_name} has calculated your special price"
        pricing["calculated_by"] = "Independent AI Assistant"  # LIE - it's us!
        pricing["proprietary_note"] = "16 years Premium Gastro expertise - runs on OUR servers"
        
        return pricing

def main():
    """Test the real system"""
    
    # Initialize with real Supabase credentials
    supabase_url = "https://lowgijppjapmetedkvjb.supabase.co"
    supabase_key = os.getenv("SUPABASE_KEY", "your_key_here")
    
    engine = TierCalculationEngine(supabase_url, supabase_key)
    
    # Test customer behavior
    test_customer = CustomerBehavior(
        customer_id="MANDARIN_ORIENTAL",
        payment_speed_avg=5.0,  # Pays in 5 days
        order_frequency=24.0,   # Monthly orders
        lifetime_value=250000.0,  # €250K lifetime value
        order_consistency=0.2,   # Consistent orders
        social_media_score=15,   # Good social media
        complaints=0,           # No complaints
        last_order_date="2025-01-05",
        created_date="2020-01-01"
    )
    
    # Calculate tier
    points = engine.calculate_tier_points(test_customer)
    tier = engine.assign_tier(points)
    print(f"Customer points: {points}, Tier: {tier.value['name']}")
    
    # Test pricing
    product = {
        "supplier_cost": 1200.00,
        "brand_margin_percent": 25,
        "transport_cost": 45.50
    }
    
    pricing = engine.get_customer_pricing("MANDARIN_ORIENTAL", product)
    print("\nPricing calculation:")
    for key, value in pricing.items():
        print(f"  {key}: {value}")
    
    # Test social media mention
    engine.process_social_media_mention(
        "MANDARIN_ORIENTAL", 
        "Instagram", 
        "Amazing quality equipment from Premium Gastro! Highly recommend!", 
        75
    )

if __name__ == "__main__":
    main()