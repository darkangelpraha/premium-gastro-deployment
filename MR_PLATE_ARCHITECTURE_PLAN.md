# MR. PLATE AI - SYSTEM ARCHITECTURE PLAN
**Before implementing anything - WHERE does it run?**

## CURRENT REALITY CHECK

### ❓ UNKNOWN VARIABLES (Need Answers)
1. **Docker Environment**: What Docker containers do you already have?
2. **UpGates Integration**: Does UpGates have webhooks? API endpoints we can call?
3. **Database**: Where does customer data live? Supabase only? 
4. **Server Infrastructure**: What servers are available? Where can we deploy?
5. **Frontend**: How does customer interact with Mr. Plate? UpGates UI? Custom widget?

### 🏗️ WHAT WE HAVE SO FAR (Code in /tmp)
- `premium_gastro_tier_engine.py` - Core psychology + calculation engine
- `mr_plate_api_server.py` - Flask API server (but WHERE does this run?)
- Strategy documents - The psychology and theory

## PROPOSED ARCHITECTURE (Needs Validation)

### Option A: Docker Container Stack
```
┌─────────────────────┐
│   UpGates Frontend  │ ← Customer sees this
└──────────┬──────────┘
           │ API calls
┌─────────────────────┐
│  Mr. Plate API      │ ← Flask server in Docker
│  (Docker Container) │
└──────────┬──────────┘
           │
┌─────────────────────┐
│   Supabase DB      │ ← Customer tiers, behavior
└─────────────────────┘
```

### Option B: UpGates Plugin/Widget
```
┌─────────────────────────────────┐
│      UpGates Dashboard          │
│  ┌─────────────────────────┐   │ ← Mr. Plate widget embedded
│  │    Mr. Plate Widget     │   │
│  │   "Ask for discount?"   │   │
│  └─────────────────────────┘   │
└─────────────────────────────────┘
           │
  Calls YOUR server API
```

## CRITICAL QUESTIONS BEFORE BUILDING

### 1. DEPLOYMENT
- **WHERE** will Mr. Plate API run?
  - Your existing Docker setup?
  - New dedicated server?
  - Cloud container?

### 2. INTEGRATION POINTS
- **HOW** does UpGates call Mr. Plate?
  - Webhook when customer asks for discount?
  - JavaScript widget that calls your API?
  - UpGates custom integration?

### 3. CUSTOMER INTERFACE
- **WHERE** does customer see Mr. Plate?
  - Inside UpGates interface?
  - Popup widget?
  - Separate chat window?
  - Avatar on product pages?

### 4. DATA FLOW
- **WHEN** does tier calculation happen?
  - Real-time when customer logs in?
  - Batch processing nightly?
  - On-demand when they ask for pricing?

## STEP-BY-STEP IMPLEMENTATION PLAN

### Phase 1: Infrastructure Audit
1. Check existing Docker containers
2. Identify available ports/services
3. Test Supabase connection from Docker
4. Map UpGates API capabilities

### Phase 2: Minimal Integration
1. Deploy Mr. Plate API in Docker
2. Create simple test endpoint
3. Test connection from UpGates (if possible)
4. Verify Supabase data flow

### Phase 3: Customer Interface
1. Build customer interaction method
2. Test avatar/animation system
3. Implement choice psychology interface
4. Test negotiation flow

### Phase 4: Production Deploy
1. Connect to real customer data
2. Monitor tier calculations
3. Track customer behavior
4. Measure psychological impact

## DOCUMENTATION NEEDED

### Technical Specs
- Docker compose file
- API endpoint documentation  
- Database schema
- Integration requirements

### Business Logic
- Tier calculation rules
- Negotiation response logic
- Choice psychology implementation
- Avatar behavior specifications

---

**STOP POINT**: Don't implement until we answer the infrastructure questions!

**NEXT**: Map out your existing Docker environment and UpGates integration capabilities