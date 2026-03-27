# Link Safety & Detection Rules 🔍

## Description
Security protocols and pattern matching rules for identifying malicious links, shortened URLs, and phishing indicators within the AI OS ecosystem.

## 1. Shortened Link Indicators (Shorteners)
Below are regex patterns to identify common shortening services:
- `bit\.ly\/[a-zA-Z0-9]+`
- `t\.co\/[a-zA-Z0-9]+`
- `tinyurl\.com\/[a-zA-Z0-9]+`
- `goo\.gl\/[a-zA-Z0-9]+`
- `rebrand\.ly\/[a-zA-Z0-9]+`

## 2. Homograph Attack Indicators
Warning if the domain contains special characters or looks like major domains but uses different characters:
- `goog[lI]e\.com`
- `face[b0]ok\.com`
- `app[lI]e\.com`
- `paypa[lI]\.com`

## 3. Tracking Parameters
List of parameters to remove to protect privacy:
- `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`
- `fbclid` (Facebook)
- `gclid` (Google Ads)
- `_ga`, `_gid` (Google Analytics)
- `mc_eid` (Mailchimp)

## 4. Blacklist Patterns
- Domains containing keywords: `phish`, `malware`, `verify-account`, `login-update`.
- High-risk TLDs: `.xyz`, `.top`, `.loan`, `.win` (when accompanying major brand names).
