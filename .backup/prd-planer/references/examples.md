# Documentation Examples

## Example 1: E-commerce Checkout Feature

### User Story

**As a** returning customer
**I want** a streamlined checkout process
**So that** I can complete purchases quickly without re-entering information

### Acceptance Criteria

**Given** I am a logged-in user with saved payment information
**When** I add items to cart and click "Checkout"
**Then** I see my shipping address and payment method pre-filled

**Given** I am at the checkout page
**When** I click "Edit" next to my shipping address
**Then** I can modify my address and save the changes

**Given** I have completed all required checkout fields
**When** I click "Place Order"
**Then** my order is processed and I receive a confirmation email within 2 minutes

### Technical Requirements

- Integrate with Stripe API for payment processing
- Store encrypted payment tokens (never raw card data)
- Implement address validation using Google Places API
- Support guest checkout (no account required)
- Calculate tax rates based on shipping address
- Apply promotional codes and calculate discounts

### Success Metrics

- Checkout completion rate > 85%
- Average checkout time < 90 seconds
- Payment success rate > 98%
- Cart abandonment rate < 30%

---

## Example 2: User Authentication System

### Overview

Implement a secure, user-friendly authentication system supporting email/password, OAuth providers (Google, GitHub), and two-factor authentication.

### Functional Requirements

**FR-1: Email/Password Registration**
- Users can create accounts with email and password
- Password must meet complexity requirements (min 8 chars, 1 uppercase, 1 number, 1 special)
- Email verification required before first login
- Verification link expires after 24 hours

**FR-2: OAuth Login**
- Support Google OAuth 2.0
- Support GitHub OAuth
- Auto-create user accounts from OAuth providers
- Link OAuth accounts to existing email accounts

**FR-3: Two-Factor Authentication (2FA)**
- Optional TOTP-based 2FA
- QR code setup process
- Backup codes generated (10 single-use codes)
- 2FA can be disabled by entering current password + 2FA code

**FR-4: Password Reset**
- "Forgot password" flow via email
- Reset link expires after 1 hour
- Cannot reuse last 5 passwords
- Invalidate all sessions on password reset

### Technical Architecture

**Components:**
- Auth Service (Node.js/Express)
- Redis (session storage)
- PostgreSQL (user data)
- SendGrid (email service)

**API Endpoints:**

```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/refresh-token
POST /api/auth/reset-password
POST /api/auth/verify-email
GET  /api/auth/oauth/google
GET  /api/auth/oauth/github
POST /api/auth/2fa/setup
POST /api/auth/2fa/verify
POST /api/auth/2fa/disable
```

### Data Model

```sql
users {
  id: UUID PRIMARY KEY
  email: VARCHAR(255) UNIQUE NOT NULL
  password_hash: VARCHAR(255) -- null if OAuth-only
  email_verified: BOOLEAN DEFAULT FALSE
  created_at: TIMESTAMP
  updated_at: TIMESTAMP
}

oauth_accounts {
  id: UUID PRIMARY KEY
  user_id: UUID REFERENCES users(id)
  provider: VARCHAR(50) -- 'google' | 'github'
  provider_user_id: VARCHAR(255)
  access_token: TEXT
  refresh_token: TEXT
}

two_factor_auth {
  user_id: UUID PRIMARY KEY REFERENCES users(id)
  secret: VARCHAR(32) -- encrypted TOTP secret
  backup_codes: TEXT[] -- array of hashed codes
  enabled: BOOLEAN DEFAULT FALSE
}
```

### Security Considerations

- Hash passwords with bcrypt (cost factor 12)
- Store sessions in Redis with 24-hour expiration
- JWT tokens for API authentication (15-min access, 7-day refresh)
- Rate limit login attempts (5 per IP per 15 minutes)
- Require HTTPS for all auth endpoints
- Implement CSRF protection
- Log all authentication events

---

## Example 3: Real-time Dashboard Feature

### Executive Summary

Build a real-time analytics dashboard that displays key business metrics with live updates, customizable widgets, and data export capabilities. Target users: product managers and executives needing instant visibility into system performance.

### Goals

- **Primary**: Provide real-time visibility into 10 core KPIs
- **Secondary**: Enable custom dashboard configurations per user
- **Success Criteria**: 
  - Page load < 2 seconds
  - Data updates < 5 second latency
  - 90% user satisfaction score

### User Personas

**Sarah - Product Manager**
- Needs: Quick overview of user engagement metrics
- Pain Points: Currently relies on static reports updated daily
- Technical Level: Medium (comfortable with basic SQL)

**Alex - Executive**
- Needs: High-level business metrics at a glance
- Pain Points: Waits for weekly reports, data always outdated
- Technical Level: Low (prefers visual dashboards)

### Core Features

**F-1: Real-time Metric Tiles**
- Display up to 12 metrics per dashboard
- Auto-refresh every 5 seconds
- Color-coded trend indicators (green up, red down)
- Drill-down capability to detailed views

**F-2: Customizable Layouts**
- Drag-and-drop widget positioning
- Resize widgets (1x1, 2x1, 2x2 grid)
- Save multiple dashboard layouts
- Share dashboard configuration via link

**F-3: Time Range Selector**
- Presets: Last hour, Today, Last 7 days, Last 30 days, Custom
- Comparison mode (e.g., compare this week vs last week)

**F-4: Data Export**
- Export visible data to CSV
- Schedule automated email reports (daily/weekly)
- PDF snapshot of current dashboard

### Technical Implementation

**Architecture:**
- Frontend: React + D3.js for charts
- Backend: Node.js + WebSocket for real-time updates
- Data Layer: TimescaleDB for time-series data
- Cache: Redis for aggregated metrics

**Data Pipeline:**
```
Event Streams → Kafka → Stream Processor → TimescaleDB
                           ↓
                       Redis Cache ← WebSocket Server → React Client
```

### Performance Requirements

- Support 1000 concurrent dashboard users
- Aggregate 1M events per minute
- Keep Redis cache fresh (< 5 second staleness)
- Page initial load < 2 seconds
- WebSocket reconnection automatic

### Testing Plan

**Unit Tests:**
- Widget rendering
- Data formatting
- State management

**Integration Tests:**
- WebSocket connection handling
- Data aggregation accuracy
- Export functionality

**Performance Tests:**
- Load test with 1000 simulated users
- Stress test data pipeline with 10M events
- Network latency simulation

---

## Best Practices Demonstrated

### Writing Clear Requirements

**Good Example:**
"When a user clicks 'Submit Order', the system shall validate all required fields, charge the payment method, send a confirmation email within 2 minutes, and display an order confirmation page with the order number."

**Bad Example:**
"The system should process orders properly and let users know it worked."

### Defining Acceptance Criteria

**Good Example:**
```
Given I am on the product page
When I click "Add to Cart"
Then the item appears in my cart
And the cart count increases by 1
And I see a success notification
And the notification disappears after 3 seconds
```

**Bad Example:**
"Adding to cart should work correctly."

### Specifying Non-Functional Requirements

**Good Example:**
"API response time: p95 < 200ms, p99 < 500ms under normal load (1000 req/min)"

**Bad Example:**
"The API should be fast enough for users."
