# MYPCS.IN — Multi-Tenant & Future-Proofing Notes

## Future-Proofing Decisions (01-Mar-2026)

### 1. Multi-Exam Support
Current: UPPCS only
Future: BPSC, MPPCS, RAS, UPSC
Rule: Never hardcode "UPPCS" in models. Use exam_type field when needed.
Our hierarchy (Subject>Unit>Part>Chapter) works for ANY exam.

### 2. Multi-Language
Current: English only
Rule: Every model with a 'name' field also has 'name_hi' (Hindi).
Phase 3: Populate Hindi fields, add Urdu for AMU area.

### 3. Multi-Tenant (White Label)
Current: Single platform
Rule: All content comes from database, not code.
Phase 4: Add Organization model, per-org content.

### 4. Content Marketplace
Future idea: Let teachers upload their own content packs.
Rule: Keep content models generic — any teacher could create
Subject>Unit>Part>Chapter hierarchy for their coaching.

### 5. API-First Design
Current: Django Admin for data entry
Future: Mobile app, third-party integrations
Rule: Build DRF APIs for every model. Admin is just one client.

### 6. Payment Flexibility
Current: ₹999/year via Razorpay
Future: Per-subject pricing, institutional licensing, EMI
Rule: Keep Subscription model flexible — don't hardcode ₹999.

### 7. Offline Support
Target user: Rural UP, 2G internet
Rule: PWA with service worker. Keep API responses small.
All content should be cacheable.

### 8. Analytics Export
Future: Coaching centers want student reports
Rule: Keep all analytics in separate tables, easy to export.

## REMINDER: Don't build any of this now. Just follow the rules while building MVP.
