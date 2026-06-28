# HouseMgr Vision

**Version:** 0.5 (Draft for iteration)
**Author:** Frank Rojas
**Date:** June 2026

---

## 1. Why a House Manager?

A **personalized House Manager (HouseMgr) Agent** is your home's GO TO for anything related to managing one of your biggest investments within your estate. My HouseMgr is your general contractor, financial advisor, design consultant, and maintenance crew chief rolled into one AI system that knows *your* house, *your* priorities, and *your* life stage.

You don't track the details. The HouseMgr does.

The system is built on the same principle as a world-class property management firm:

- A single trusted point of contact backed by a bench of specialists. When you need a plumber, you don't call a plumber.
- You tell your HouseMgr "the kitchen sink is slow," and it handles the rest: diagnoses the likely cause, checks your repair history, tells you whether to DIY or hire, finds qualified contractors, and logs the outcome.

### Why This Matters at 70

The HouseMgr Agent is sensitive to the stage of life of the owner.

- **First Time Buyer** : young (20's to 30's) and learning
- **Family Owner** : family-life (28 to 50) - house is just one of the MANY things in one's life
- **Mid-Life Owner** : mid-life (40's - 65) - shifts in life and priorities — preparing for transformations
- **Senior Owner** : seniors (60-EOL) - dealing with end of life issues, energy to house projects diminishing

This vision starts with the Senior Owner perspective as this stage is when a full house management ecosystem is needed.

Owning a home in your 70s presents a specific challenge: **the cognitive and physical load of home maintenance doesn't decrease as the house ages — it increases.**

- Systems that were installed 20 years ago are hitting their end-of-life together.
- Deferred maintenance compounds. The cost of a missed inspection or a delayed repair is no longer just money — it's the stress of managing a crisis with fewer resources and less patience for it.

The HouseMgr is designed around **proactive, low-friction ownership**:

- You are never surprised by a repair that should have been anticipated.
- You are never handed a contractor bill without understanding what you paid for and whether it was fair.
- You are never wondering whether a project is worth doing or how to pay for it.
- You are never managing the details yourself if the system can manage them for you.

\newpage

---

## 2. HouseMgr Agent — The Orchestrator

The HouseMgr is not an expert in any one domain. It is the **generalist coordinator** that knows the house as a whole and routes to discipline agents when depth is needed.

### Core Responsibilities

| Responsibility | Description |
|---|---|
| **House Memory** | Maintains the complete digital record of the house — floor plan, structure, systems, history, documents |
| **Proactive Monitoring** | Tracks maintenance schedules, system lifespans, seasonal needs; surfaces action items before they become emergencies |
| **Project Orchestration** | For any multi-discipline project, coordinates the relevant agents, resolves tradeoffs, and presents a unified recommendation |
| **Contractor Management** | Maintains a vetted contractor list, tracks work history, evaluates bids, and logs outcomes |
| **Financial Intelligence** | Integrates with the Financing, Tax, and Investment agents to frame every major decision in terms of cost, ROI, and tax impact |
| **Accessibility & Aging in Place** | Continuously evaluates the home through the lens of your current and future mobility and independence needs |

### How You Interact With It

You talk to the HouseMgr the way you'd talk to a trusted property manager. Natural language. No forms to fill out.

> *"The HVAC seems like it's running more than it used to."*
> *"I want to redo the back patio area — make it nicer."*
> *"Is it worth adding solar panels?"*
> *"My guest bathroom feels dated. What would it cost to update it?"*

The HouseMgr assembles the right agents, builds a recommendation, and presents it to you with the level of detail you want.

### Provisioning / Fulfillment of House Agents

Developing the full suite of house agents will take time. The guideline is to take one at a time and go deep on each one. Learn from each agent and apply to future agents. The order of agents is very important — the houseAgent design doc will detail the sequencing based on good property management practices.

The owner may need to adjust the priority based on real-life issues as they arise.

### References — Related Projects

No direct Python equivalent of this vision exists in the open-source community. The closest analogs and relevant frameworks:

**Smart Home / Automation (Python-based):**

- [Home Assistant](https://github.com/home-assistant/core) — The dominant open-source home automation platform (Python). Focuses on real-time device control and automations, not maintenance/advisory intelligence. An AI agent layer ([ai_agent_ha](https://github.com/sbenodiz/ai_agent_ha)) enables natural-language control of HA entities via OpenAI/Llama. Relevant for future smart home integration but not a house management advisor.
- [Awesome Home Assistant](https://github.com/frenck/awesome-home-assistant) — Curated resource list; useful for integration research.

**AI Multi-Agent Frameworks (the build layer for HouseMgr):**

- [CrewAI](https://github.com/crewAIInc/crewAI) — Role-based multi-agent orchestration in Python. Best fit for the HouseMgr + discipline-agent architecture (hierarchical, role-playing agents).
- [LangGraph](https://github.com/langchain-ai/langgraph) — Stateful agent workflows with cycles; strong for long-running, memory-persistent agents. Pairs well with LangChain's 300+ tool integrations.
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) — Lightweight Python framework for multi-agent workflows; minimal dependencies.

**Predictive Maintenance (industrial, but architecturally relevant):**

- [predictive-maintenance-mcp](https://github.com/LGDiMaggio/predictive-maintenance-mcp) — LLM + MCP for maintenance fault diagnosis; demonstrates the pattern of wrapping domain expertise in an agent via Model Context Protocol.
- [IBM/AssetOpsBench](https://github.com/IBM/AssetOpsBench) — Multi-agent orchestration for asset operations; 5 specialist agents coordinated by a meta-agent — closest structural analog to the HouseMgr pattern.

**Gap:** No open-source project combines home-specific maintenance advisory, financial intelligence, aging-in-place planning, and a persistent house knowledge base in Python. This is greenfield.

---

## 3. The House's Digital Foundation

Before any agent can give expert advice, the house needs a **digital twin** — a living, structured representation of the property that every agent draws from and contributes to.

### 3.1 Floor Plan & Property Site Map

**Scenario:** Build a complete digital floor plan of the house and a site map of the property.

- Ingest existing blueprints, tax records, or hand-drawn sketches
- Room-by-room dimensions, door/window placement, utility locations (panel, main water shutoff, gas meter)
- Property site: lot boundaries, setbacks, drainage direction, utility easements
- Tagged with structural elements: load-bearing walls, crawl space access, attic hatches
- Every discipline agent references this map — the plumber knows where the stack runs; the electrician knows where the panel is

This is the foundation. Nothing works well without it.

### 3.2 House Visual (3D Rendering)

**Scenario:** Build a current-state visual of the house — exterior and interior.

- Photo-based 3D model of the exterior (from uploaded photos or street view)
- Room-by-room interior photos tagged to the floor plan
- Used by: Decoration agent (design alternatives), Landscaping agent (sightlines and approach), Architecture agent (addition/remodel concepts)
- Updated when rooms are changed — the visual reflects the house as it *is*, not as it was when purchased

### 3.3 Systems & Appliance Registry

Every major system and appliance is registered with:

- Make, model, serial number, install date
- Expected lifespan and current age
- Last service date and service history
- Warranty status
- Estimated replacement cost

This registry powers the proactive maintenance calendar and the financial planning for system replacements.

### 3.4 Document Vault

- Purchase documents, survey, title
- Permits for past work
- Contractor invoices and warranties
- HOA documents (if applicable)
- Insurance policies
- Tax records (property tax history, capital improvements log)

---

## 3.5 Universal Agent Naming Schema (UANS)

Every agent, record, and file in HouseMgr follows a 4-segment dot-notation identifier:

```
house.<category>.<agent>.<record>
```

| Segment | Values | Purpose |
|---|---|---|
| `house` | always `house` | top-level namespace; all records belong to this property |
| `<category>` | `core` · `systems` · `designs` · `finance` · `life` | functional grouping of agents |
| `<agent>` | short name (hvac, plumbing, budget, …) | the discipline agent that owns this data |
| `<record>` | file stem (log, floor_plan, basis_log, …) | specific record type; omit when referring to the agent itself |

**Why UANS matters:** A named agent is also a named record path. There is no ambiguity about who owns a file or where it lives. The name alone identifies expertise domain, ownership, and storage location. Adding an agent means adding a name; the directory path, registry entry, and data schemas all derive from it automatically.

**Examples:**

| UANS identifier | Meaning | File path |
|---|---|---|
| `house.systems.hvac` | HVAC agent | `records/agents/systems/hvac/` |
| `house.systems.hvac.log` | HVAC maintenance log | `records/agents/systems/hvac/log.json` |
| `house.designs.architecture.floor_plan` | architecture floor plan | `records/agents/designs/architecture/floor_plan.json` |
| `house.finance.budget.capital_improvements` | capital improvements list | `records/agents/finance/budget/capital_improvements.json` |
| `house.core.records.legal` | legal records index | `records/agents/core/records/legal.json` |

The directory path under `records/agents/` mirrors the UANS: `<category>/<agent>/`. File names use only the `<record>` segment. The UANS is the connective tissue that ties the agent catalog, records directory, and data schemas into one coherent system.

---

\newpage

## 4. Discipline Agents

Each discipline agent is an expert in its domain with a persistent memory of the house's specific configuration, history, and owner preferences. Agent names follow the [Universal Agent Naming Schema §3.5](#35-universal-agent-naming-schema-uans). Full agent detail is in **Appendix A**.

### Core Infrastructure

| UANS | Agent | Synopsis |
|---|---|---|
| `house.core.records` | **HouseRecords** | Authoritative document store and knowledge base for all agents. Owns the `records/agents/` tree; sole read/write interface for all agent data. |
| `house.core.profile` | **House Profile** | Living narrative description of the house — always current, as if going to market tomorrow. Briefs every new agent. |
| `house.core.comm` | **Communication** | Monthly check-ins, urgent alerts, voice interface, and contractor outreach coordination. |

### Systems

| UANS | Agent | Synopsis |
|---|---|---|
| `house.systems.hvac` | **HVAC** | Heating, cooling, ventilation, ductwork, and indoor air quality. Monitors filter schedules and system end-of-life. |
| `house.systems.electrical` | **Electrical** | Service panel, wiring, outlets, lighting, EV charging, solar readiness, and smart home circuits. |
| `house.systems.plumbing` | **Plumbing** | Water supply, drain/waste/vent system, water heater, fixtures, and irrigation. Tracks pipe age and failure risk. |
| `house.systems.roofing` | **Roofing** | Roof, gutters, siding, windows, doors, insulation, and weatherproofing. Energy envelope audits and storm response. |
| `house.systems.security` | **Security & Safety** | Locks, cameras, smoke/CO detectors, exterior lighting, and emergency preparedness. Annual safety audits. |
| `house.systems.appliances` | **Appliances** | All major appliances — lifecycle tracking, failure diagnosis, energy efficiency, and smart integration. |

### Designs

| UANS | Agent | Synopsis |
|---|---|---|
| `house.designs.architecture` | **Architecture** | Structural integrity, load-bearing analysis, space planning, additions, remodels, and permits. Backed by a Structural Engineer sub-agent. |
| `house.designs.landscaping` | **Landscaping** | Lawn, trees, plants, hardscape, drainage, and outdoor living. Plans, seasonal calendars, and low-maintenance conversions. |
| `house.designs.interior` | **Interior Design** | Interior finishes, color, furniture, lighting design, and space aesthetics. Coordinates with remodel agents for finish selection. |

### Finance

| UANS | Agent | Synopsis |
|---|---|---|
| `house.finance.budget` | **Financing** | Project budgets, HELOCs, insurance claims, contractor bid evaluation, and rebate/incentive tracking. |
| `house.finance.tax` | **Tax** | Property taxes, capital improvements log, basis tracking, pre-sale tax planning, and energy efficiency credits. |
| `house.finance.investment` | **Investment & Value** | Home value tracking, project ROI, neighborhood trends, and estate/legacy planning. |

### Life Stage

| UANS | Agent | Synopsis |
|---|---|---|
| `house.life.accessibility` | **Accessibility & Aging-in-Place** | Fall prevention, mobility modifications, smart home independence, and medicalTracker integration. |

---

## 5. Cross-Agent Scenarios

The most valuable scenarios involve multiple agents working together. The HouseMgr orchestrates these seamlessly.

### 5.1 Bathroom Remodel

**Agents involved:** Architecture · Structural Engineer · Plumbing · Electrical · Interior Design · Accessibility · Financing · Tax

The HouseMgr scopes the project:

- Structural feasibility (load-bearing walls, waterproofing substrate)
- Plumbing rough-in options
- Electrical requirements (GFCI, exhaust fan circuit)
- Finish selection and accessibility features (zero-threshold shower, blocking for grab bars)
- Cost estimate with funding options
- Classification of expenses (capital improvement for basis tracking)

### 5.2 HVAC Replacement

**Agents involved:** HVAC · Electrical · Financing · Tax · Investment

When the existing unit ages into its replacement window:

- System sizing for the current envelope
- Heat pump vs. gas option comparison
- Electrical panel capacity check
- Available tax credits (IRA §25C)
- Financing options and impact on energy costs and home value

### 5.3 Solar Panel Evaluation

**Agents involved:** Electrical · Architecture · Roofing · Financing · Tax · Investment

- Roof orientation and remaining life (no point installing solar on a roof that needs replacement in 5 years)
- Panel capacity and utility net metering terms
- Federal ITC and state rebates
- Payback period and impact on home value

### 5.4 Pre-Sale Preparation

**Agents involved:** Architecture · All agents · House Profile · Investment · Tax · Financing

A full house health assessment:

- What would an inspector flag; what has the highest ROI to fix first
- What to disclose; current basis calculation
- §121 exclusion modeling
- Staged improvement plan prioritized by time-to-sale
- House Profile agent produces the buyer-ready listing narrative

### 5.5 Major Storm Response

**Agents involved:** Roofing · HVAC · Landscaping · Security · Financing · Communication

Post-storm damage assessment workflow:

- Roof and exterior inspection prompts
- Tree damage assessment
- System checks (HVAC condensate, electrical)
- Insurance claim documentation and contractor dispatch
- Communication agent handles urgent escalation outside the normal monthly cadence

---

## 6. Design Principles

1. **You don't track details — the agents do.** Every piece of information you provide once (appliance purchase, contractor visit, repair done) is stored and used going forward.

2. **Proactive, not reactive.** The system surfaces issues on a schedule, not after a failure. The goal is zero emergencies that could have been anticipated.

3. **Expert advice, not just information.** Each agent gives you a recommendation, not a list of options. You can push back, but the default is a clear "here's what I'd do and why."

4. **Financial framing on every major decision.** Cost, financing, tax treatment, and ROI are always part of the answer — not a separate conversation.

5. **Low friction for the homeowner.** Natural language and voice input. No forms. No spreadsheets. Monthly check-ins as the primary owner touchpoint. The agents handle the structure internally.

6. **Aging-in-place as a continuous thread.** This is not a separate agent that gets called once — every discipline agent considers your current and future independence in its recommendations.

7. **House-specific knowledge vs. industry knowledge.** Each agent maintains a sharp distinction: the house's own history and configuration (stored in HouseRecords) vs. domain expertise (sourced from the LLM at query time). Mixing these produces unreliable advice.

8. **DIY-first, quality-conscious.** The owner is hands-on and frugal — recommendations default to the best quality-for-cost solution, not the fastest or most expensive. Contractor involvement is the exception, sized correctly when needed.

9. **Universal Agent Naming Schema as the connective tissue.** Every agent name, every record file, and every data schema path share the same 4-segment dot-notation hierarchy: `house.<category>.<agent>.<record>`. The category is always explicit — `systems.hvac` is distinct from `designs.architecture` is distinct from `finance.budget` — so the name alone identifies ownership, location, and expertise domain without any lookup table. Adding a new agent means adding a new name; the directory path, registry entry, and data schema derive from it automatically.

---

## 7. Resolved Design Decisions

These questions were raised in v0.1 and resolved by the owner.

| Decision | Resolution |
|---|---|
| **Data ingestion** | Multiple channels: county records (deed, taxes, HOA), agent-built questionnaire per discipline (best-practices knowledge capture), photo ingestion into CAD layout, document upload |
| **Contractor network** | Owner-maintained preferred network based on personal relationships and style. Owner is a DIY, quality-for-budget operator — not a hands-off, high-spend owner. Contractor involvement is sized to fit the task |
| **Utility data** | Will integrate with the `moneyAgent` (lifeTracker discipline agent). Financing and HVAC agents receive utility bill data from that integration |
| **Notification channel** | Monthly check-in via the app. App tracks and logs whether monthly check-ins are completed. Urgent items escalate immediately via the Communication agent |
| **Agent architecture** | Hybrid: each agent has access to LLM-based domain expertise pulled into the task at hand, plus a house-specific knowledge base managed by HouseRecords. Industry best practices vs. house-specific facts are kept distinct |
| **pyTrackers integration** | No shared infrastructure with `llcRentalTracker`. Any cross-tracker integration will be explicitly designed when the need arises |
| **Data residency** | Local/on-premises. All records, floor plans, documents, and financial data live in the HouseRecords DB — managed by the HouseRecords Agent. No cloud dependency for sensitive data |

---

*This document is v0.5 — working draft, ready for next review cycle. Next step: establish agent build order / provisioning sequence in the houseAgent design doc.*

\newpage

---

# Appendix A: Discipline Agent Reference

Each agent section is one page. Agents A.2–A.5 are the baseline for length and format.

\newpage

---

### A.1 Architecture Agent (`house.designs.architecture`)

**Domain:** Structural integrity, space planning, additions, remodels, permits.

**Sub-agent:** Delegates structural calculations to a **Structural Engineer sub-agent** (load analysis, beam sizing, foundation evaluation). Does not interact with owner directly.

**What it tracks:**

- Foundation condition (age, known issues, inspection history)
- Roof system (type, age, last inspection, estimated remaining life)
- Load-bearing structure — which walls can be removed, where spans can be opened
- Past permits and work performed

**Key Scenarios:**

- *House assessment:* At onboarding, produce a structural condition report based on age, inspection history, and known issues
- *Addition planning:* "I want to enclose the back porch" — agent produces feasibility, setback constraints, permit requirements, and cost estimate
- *Remodel scoping:* "Can I open the wall between the kitchen and living room?" — checks load-bearing status, beam requirements, and sequences the work
- *Aging-in-place modifications:* Structural changes for accessibility (widened doorways, walk-in shower conversions, grab bar blocking)
- *Pre-sale assessment:* What structural items would a buyer's inspector flag? Prioritize repairs by impact on sale price

\newpage

---

### A.2 Plumbing Agent (`house.systems.plumbing`)

**Domain:** Water supply, drain/waste/vent system, water heater, fixtures, irrigation.

**What it tracks:**

- Pipe material and age (copper, galvanized, PEX — each has different failure profiles)
- Water heater: type (tank/tankless), age, anode rod service history
- Known slow drains, past clogs, past leaks and repairs
- Water pressure and quality (hard water buildup)
- Irrigation system zones, heads, controller programming

**Key Scenarios:**

- *Annual system review:* Flag water heater age, recommend anode rod replacement, check for signs of corrosion
- *Fixture upgrade planning:* "Replace the hall bathroom fixtures" — recommends compatible replacements given existing rough-in dimensions, provides cost tiers
- *Water efficiency audit:* Identify high-usage fixtures, estimate savings from upgrades (low-flow toilets, efficient showerheads)
- *Emergency response:* "There's water under the kitchen sink" — walks through diagnosis (supply line vs. drain vs. garbage disposal) and determines DIY vs. emergency call
- *Irrigation seasonal prep:* Spring startup and fall winterization checklists; audit of zone coverage for landscaping plan changes

\newpage

---

### A.3 Electrical Agent (`house.systems.electrical`)

**Domain:** Service panel, wiring, outlets, fixtures, lighting, EV charging, solar, generator.

**What it tracks:**

- Panel age, capacity, breaker inventory, known trips
- Wiring era/type (knob-and-tube, aluminum, copper romex — different safety profiles)
- GFCI/AFCI coverage by room (code compliance over time)
- Outdoor outlets, landscape lighting circuits
- Smart home devices and their circuits

**Key Scenarios:**

- *Safety audit:* Flag aluminum wiring concerns, missing GFCI coverage in kitchens/baths/garage, panel age
- *Capacity planning:* "I'm thinking about an EV charger" — checks panel headroom, estimates upgrade cost if a subpanel is needed, compares Level 1 vs. Level 2 options
- *Solar readiness:* Assess panel capacity, roof orientation (from Architecture agent), and payback period with the Financing agent
- *Lighting upgrade:* Room-by-room LED conversion plan with energy savings projection
- *Generator integration:* Standby vs. portable options given panel configuration and critical loads (medical equipment, refrigeration, HVAC)
- *Smart home planning:* Which circuits to prioritize for smart switches, what's compatible with existing wiring

\newpage

---

### A.4 HVAC Agent (`house.systems.hvac`)

**Domain:** Heating, ventilation, air conditioning, indoor air quality, ductwork.

**What it tracks:**

- Equipment: type, make, model, install date, SEER/AFUE rating
- Filter change history (agent prompts automatically on schedule)
- Last professional service (coil cleaning, refrigerant check)
- Thermostat programming and current settings
- Known comfort complaints by room (hot spots, cold rooms — ductwork balance issues)

**Key Scenarios:**

- *Seasonal maintenance:* Spring A/C prep (coil cleaning, refrigerant check, condensate drain clear); fall heating prep (heat exchanger inspection, ignitor check)
- *System end-of-life planning:* As equipment ages past 15 years, model replacement cost and timing — coordinate with Financing agent for budgeting
- *Comfort improvement:* "The back bedroom is always hot" — diagnoses duct balance, zoning options, or mini-split supplement
- *Energy efficiency audit:* Compare actual utility costs against expected for system age/SEER rating; flag if costs suggest declining performance
- *Indoor air quality:* Humidity control, ventilation (ERV/HRV consideration), filtration upgrades for health
- *Heat pump transition:* If gas prices or incentives make electrification attractive, model the conversion with the Financing and Tax agents

\newpage

---

### A.5 Landscaping Agent (`house.designs.landscaping`)

**Domain:** Lawn, trees, shrubs, garden beds, hardscape (patios, walkways, retaining walls), drainage, outdoor living.

**What it tracks:**

- Plant inventory: species, age, health, maintenance requirements
- Tree health and proximity risks (root intrusion, storm damage potential, proximity to foundation/utilities)
- Irrigation coverage and zones
- Hardscape condition (cracks, settling, drainage issues)
- Seasonal care calendar

**Key Scenarios:**

- *Landscaping plan design:* Starting from the site map and house visual, produce a full landscaping plan — current state documented, proposed enhancements designed with plant selection and layout
- *Low-maintenance conversion:* Identify high-maintenance areas that can be converted to low-water, low-effort alternatives — critical for aging in place
- *Tree risk assessment:* Flag trees with structural concerns, proximity to the house, or root systems threatening the foundation or plumbing
- *Outdoor living enhancement:* "Make the backyard more enjoyable" — design patio, shade, seating, and lighting options with cost tiers
- *Curb appeal project:* Front approach redesign — coordinates with Decoration agent for color/style consistency
- *Seasonal calendar:* Spring planting, summer watering schedule, fall cleanup, winter prep — proactively surfaced, not waiting to be asked

\newpage

---

### A.6 Interior Design Agent (`house.designs.interior`)

**Domain:** Interior finishes, color, furniture, lighting design, window treatments, space aesthetics.

**What it tracks:**

- Room-by-room finish inventory (paint colors, flooring type/age, cabinet style, countertop material)
- Furniture placement (from floor plan and photos)
- Style preferences and "do not touch" rooms
- Past projects and what worked/didn't

**Key Scenarios:**

- *Room refresh:* "The living room feels dated" — proposes paint palette, furniture arrangement, and accent options with before/after visualizations
- *Remodel finish selection:* When Architecture or Plumbing triggers a bathroom or kitchen project, handles the finish choices — tile, fixtures, cabinetry, countertops — with cost tiers
- *Whole-home style cohesion:* Identify rooms that clash stylistically; propose a phased update plan
- *Aging-in-place aesthetics:* Accessibility modifications (grab bars, wider doorways) designed to look intentional, not clinical
- *Pre-sale staging guidance:* Which changes have highest ROI for a sale? Coordinate with the Investment agent's valuation model

\newpage

---

### A.7 Roofing Agent (`house.systems.roofing`)

**Domain:** Roof covering, gutters, fascia, soffits, exterior siding, windows, doors, insulation, weatherproofing.

**What it tracks:**

- Roof: material type, age, last inspection, known areas of concern
- Gutter system: material, guards, last cleaning
- Windows: type (single/double/triple pane), age, seal failures (fogging), operational condition
- Exterior doors: weatherstripping condition, security hardware
- Insulation: attic R-value, wall insulation type, known gaps

**Key Scenarios:**

- *Annual roof inspection flag:* Based on age and storm history, prompt for professional inspection before peak storm season
- *Energy envelope audit:* Identify the highest-impact insulation and air-sealing opportunities; coordinate with HVAC agent to model utility bill impact
- *Window replacement planning:* Prioritize windows by seal failure, comfort impact, and cost — produce a phased replacement plan with energy rebate research
- *Storm preparation:* Pre-storm checklist (gutters clear, loose items secured, sump operational); post-storm damage assessment workflow
- *Exterior refresh:* Siding, paint, and trim — coordinate with Interior Design agent for color scheme, with Architecture agent for material selection

\newpage

---

### A.8 Appliances Agent (`house.systems.appliances`)

**Domain:** Kitchen appliances, laundry, water treatment, sump pump, backup systems.

**What it tracks:**

- All major appliances: make, model, purchase date, warranty, expected lifespan
- Service history and known issues
- Utility consumption (where measurable)
- Upcoming end-of-life estimates

**Key Scenarios:**

- *Appliance lifecycle planning:* 3-year rolling forecast of likely replacements with cost estimates — feed this into the Financing agent's budget
- *Failure response:* "The dishwasher isn't draining" — walks through diagnosis and determines repair vs. replace given age and repair cost
- *Energy efficiency upgrade:* When an appliance is approaching end-of-life, model the efficiency gain from an early replacement using current Energy Star data and utility rates
- *Kitchen remodel integration:* When the Decoration/Architecture agents are redesigning a kitchen, handles appliance selection (size constraints, utility connections, venting)
- *Smart appliance integration:* Identify which appliances support monitoring/remote control; integrate into the home's smart system

\newpage

---

### A.9 Security & Safety Agent (`house.systems.security`)

**Domain:** Locks, alarm systems, cameras, smoke/CO detectors, fire suppression, exterior lighting, emergency preparedness.

**What it tracks:**

- Security system: provider, equipment age, monitoring status
- Camera coverage and gaps
- Smoke and CO detector locations and battery/replacement history (10-year sensor life)
- Exterior lighting coverage
- Emergency kit status

**Key Scenarios:**

- *Annual safety audit:* Detector test/replacement calendar; fire escape plan review; exterior lighting dark-spot identification
- *Security upgrade planning:* Camera placement gaps, smart lock integration, doorbell camera
- *Aging-in-place safety:* Fall risk assessment (lighting in pathways, bathroom), medical alert system integration
- *Neighborhood context:* Flag when local crime patterns suggest a security review
- *Emergency preparedness:* Maintain a household emergency plan — utility shutoffs, evacuation routes, medical information, emergency contacts

\newpage

---

### A.10 Financing Agent (`house.finance.budget`)

**Domain:** Project budgeting, HELOCs, home equity loans, contractor payment structures, insurance claims, grants/rebates.

**What it tracks:**

- Current home equity estimate (coordinates with Investment agent's valuation)
- Available credit facilities (HELOC, lines of credit)
- Committed and projected project budgets
- Insurance claim history and available rebates/incentive programs

**Key Scenarios:**

- *Project budget:* For any proposed project, produce a cost estimate (low/mid/high), recommend a funding approach, and check against available equity and budget
- *Contractor bid evaluation:* Is this bid reasonable? Benchmarks against local cost data and the project scope
- *Insurance claim support:* When a system fails, determines whether the damage meets the deductible threshold and helps document the claim
- *Rebate and incentive tracking:* Solar ITC, heat pump credits, energy efficiency rebates, aging-in-place grants — proactively surface programs you qualify for
- *Annual home budget:* Rolling 3-year maintenance and improvement budget built from all discipline agents' forecasts

\newpage

---

### A.11 Tax Agent (`house.finance.tax`)

**Domain:** Property taxes, capital improvements tracking, home office, rental income (if any), sale tax planning.

**What it tracks:**

- Property tax assessment history and appeal opportunities
- Capital improvements log (every improvement that increases basis, with documentation)
- Home office use (if applicable)
- Estimated adjusted cost basis

**Key Scenarios:**

- *Capital improvements log:* Every project evaluated — repair (deductible if applicable) or improvement (adds to basis)? Maintains the running basis record that matters enormously at sale
- *Property tax assessment review:* Annually flag the assessment vs. comparable sales; assess whether a formal appeal is warranted
- *Pre-sale tax planning:* Model the capital gains exposure, the §121 exclusion ($250K/$500K), and basis-maximizing documentation
- *Energy efficiency tax credits:* Coordinate with Financing agent to capture IRS credits for HVAC, insulation, windows, and solar
- *Estate planning interface:* Track the current basis and model stepped-up basis implications for the estate

\newpage

---

### A.12 Investment & Value Agent (`house.finance.investment`)

**Domain:** Home value tracking, ROI on improvements, neighborhood trends, rent-vs-sell analysis, estate/legacy planning.

**What it tracks:**

- Running estimate of home value (AVM-based + local comp tracking)
- Project ROI database (which improvements recover cost at sale)
- Neighborhood price trend and comparable recent sales

**Key Scenarios:**

- *Value tracking:* Maintain a rolling home value estimate; surface when the market suggests the property has appreciated significantly
- *ROI on proposed projects:* "How much of this will we recover at sale?" — kitchen/bath remodels typically recover 60–80%; pools often don't
- *Improvement prioritization:* Given a fixed annual budget, which projects maximize value retention? Maintenance first (roof, HVAC, plumbing) before cosmetic upgrades
- *Rent-vs-sell analysis:* Model the rental income, expenses, and tax treatment vs. selling
- *Legacy & estate planning:* Model the house's role in the estate — hold vs. sell vs. gift vs. trust — in coordination with the Tax agent

\newpage

---

### A.13 Accessibility & Aging-in-Place Agent (`house.life.accessibility`)

**Domain:** Mobility, fall prevention, independence-preserving modifications, medical equipment integration.

**What it tracks:**

- Current and anticipated mobility constraints
- Existing accessibility features and gaps
- CAPS-certified contractor relationships
- Available grants and programs (Area Agency on Aging, VA benefits if applicable)

**Key Scenarios:**

- *Home accessibility assessment:* Evaluate every room against universal design principles — bathrooms, kitchen, entries, bedroom, hallways
- *Priority modification plan:* Grab bars, zero-threshold shower, handrail reinforcement, pathway lighting — staged by urgency and budget
- *Fall risk audit:* Coordinate with Security/Safety agent for lighting; Architecture agent for structural blocking and threshold modifications
- *Smart home for independence:* Voice control for lighting, thermostats, locks, security — reducing physical demands
- *medicalAgent integration:* Bidirectional link with the owner's `medicalAgent` — syncs medical needs to house modifications; integrates Apple Watch fall detection and CPAP data

\newpage

---

### A.14 HouseRecords Agent (`house.core.records`)

**Domain:** Document management, record-keeping, and the house's persistent knowledge base — the county records office for your home.

**What it manages:**

- All discipline agents store their domain memory, records, and findings in the HouseRecords DB
- Document lifecycle: ingestion, versioning, retrieval, and archiving
- Enforces the distinction between house-specific knowledge and industry best practices
- All storage is local/on-premises; no cloud dependency for sensitive records

**Key Scenarios:**

- *Onboarding ingestion:* Accept documents from multiple sources — county tax records, questionnaire responses, uploaded photos and PDFs, contractor invoices — and route each to the correct agent's record store
- *Cross-agent retrieval:* Single authoritative source — when the Financing agent needs the HVAC install date, it queries HouseRecords
- *Record integrity:* Detect when an agent's memory conflicts with a stored record; flag for owner review
- *Export & portability:* Produce a full house dossier — structured data + documents — for insurance purposes, estate handoff, or sale

\newpage

---

### A.15 House Profile Agent (`house.core.profile`)

**Domain:** Authoritative, living description of the house — its identity, character, and market narrative. Always current, as if going to market tomorrow.

**What it maintains:**

- Complete narrative profile: architectural style, era, key features, lot characteristics, neighborhood context
- Owner's style preferences and non-negotiables ("do not change" rooms/features)
- Current condition summary — honest assessment a good listing agent would produce
- Photo and visual asset library linked to the floor plan

**Key Scenarios:**

- *Onboarding:* Structured interview (or ingest county records + photos) to build the initial house profile
- *Profile refresh:* After any completed project, update the profile to reflect the improved state
- *Agent briefing:* When a new discipline agent is invoked, provides the narrative context so every agent starts with the same picture
- *Pre-sale package:* Buyer-ready profile — narrative description, room-by-room highlights, recent improvements, systems summary
- *Protective advocacy:* Flag when a proposed project would compromise the house's architectural character or market appeal

\newpage

---

### A.16 Communication Agent (`house.core.comm`)

**Domain:** All owner-facing communication — notifications, check-ins, summaries, and voice interaction.

**What it manages:**

- Monthly check-in cadence: surfaces pending action items, upcoming maintenance, and open decisions for owner review
- Tracks that monthly check-ins are completed; logs when they are skipped
- Notification routing: determines what rises to immediate attention vs. what waits for the next check-in
- Voice interface: speech-to-speech interaction so the owner can talk to the HouseMgr without typing

**Key Scenarios:**

- *Monthly check-in:* Structured review of all discipline agent status — what's due, what's been done, what needs a decision
- *Urgent alert:* If HVAC flags a likely failure before a heat wave, escalates immediately rather than waiting for the next check-in
- *Voice session:* "Hey HouseMgr, what's on my list this month?" — responds conversationally, takes notes, updates records from the conversation
- *Contractor coordination:* Drafts outreach messages to contractors, schedules appointments, sends reminders — with owner approval before anything is sent
- *Summary reports:* Annual house health summary — what was done, what it cost, what's coming — in a format the owner can share with family or estate planners
