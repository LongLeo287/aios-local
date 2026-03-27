# Schema Markup — Complete Reference with JSON-LD Examples

## TABLE OF CONTENTS
1. [Schema Basics](#basics)
2. [FAQPage Schema](#faq)
3. [HowTo Schema](#howto)
4. [Article / NewsArticle Schema](#article)
5. [Organization Schema](#organization)
6. [Person Schema](#person)
7. [Product Schema](#product)
8. [BreadcrumbList Schema](#breadcrumb)
9. [DefinedTerm Schema](#definedterm)
10. [Speakable Schema](#speakable)
11. [Dataset Schema](#dataset)
12. [LocalBusiness Schema](#localbusiness)
13. [Review / AggregateRating Schema](#review)
14. [Event Schema](#event)
15. [SiteLinks Searchbox](#sitelinks)
16. [Implementation & Validation](#implementation)

---

## 1. SCHEMA BASICS {#basics}

Schema markup is structured data added to HTML that tells search engines and AI systems what your content means, not just what it says.

**Implementation method:** JSON-LD (recommended — place in `<script>` tag in `<head>` or `<body>`)

**Basic JSON-LD wrapper:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "[SchemaType]",
  ... properties ...
}
</script>
```

**Multiple schemas on one page:**
```html
<script type="application/ld+json">
[
  {
    "@context": "https://schema.org",
    "@type": "Article",
    ...
  },
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    ...
  }
]
</script>
```

---

## 2. FAQPAGE SCHEMA {#faq}

**Use on:** Any page with Q&A sections. Maximum AI citation impact.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is Answer Engine Optimization (AEO)?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Answer Engine Optimization (AEO) is the practice of structuring and formatting digital content to be cited, quoted, or recommended by AI-powered answer engines such as ChatGPT, Perplexity, Google AI Overviews, and Claude. Unlike traditional SEO, which focuses on ranking in search result pages, AEO focuses on being the source that AI synthesizes into its generated answers."
      }
    },
    {
      "@type": "Question",
      "name": "How is AEO different from SEO?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO (Search Engine Optimization) focuses on ranking web pages in traditional search results like Google's blue links. AEO (Answer Engine Optimization) focuses on being cited by AI systems that generate direct answers to user queries. AEO requires direct-answer content structures, clean HTML extractability, entity authority, and llms.txt implementation — elements less critical for traditional SEO."
      }
    }
  ]
}
```

**Best practices:**
- Match schema questions exactly to H2/H3 heading text on page
- Answers in schema should match visible page content
- No minimum or maximum number of questions, but 3–10 is typical
- Keep answer text under 300 words per question

---

## 3. HOWTO SCHEMA {#howto}

**Use on:** Step-by-step instructional content, tutorials, processes.

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Implement llms.txt for AI Search Optimization",
  "description": "A step-by-step guide to creating and deploying a llms.txt file that helps AI systems navigate your website content.",
  "totalTime": "PT30M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "0"
  },
  "step": [
    {
      "@type": "HowToStep",
      "name": "Audit your most important pages",
      "text": "Review your website and identify the 20–50 pages with the highest value for AI citation: definition pages, how-to guides, original research, and pillar content.",
      "position": 1
    },
    {
      "@type": "HowToStep",
      "name": "Create the llms.txt file",
      "text": "Create a Markdown file at yourdomain.com/llms.txt. Include your brand description, then organized sections linking to your priority pages with one-line descriptions.",
      "position": 2
    },
    {
      "@type": "HowToStep",
      "name": "Deploy and verify",
      "text": "Upload the file to your root domain. Verify it is accessible at yourdomain.com/llms.txt and returns a 200 status code.",
      "position": 3
    },
    {
      "@type": "HowToStep",
      "name": "Test AI visibility",
      "text": "Search your brand name and core topics in ChatGPT, Perplexity, and Gemini to check if AI systems are correctly representing your content.",
      "position": 4
    }
  ]
}
```

---

## 4. ARTICLE / NEWSARTICLE SCHEMA {#article}

**Use on:** Blog posts, guides, news articles — any editorial content.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "The Complete Guide to AI Search Optimization in 2025",
  "description": "A comprehensive guide to optimizing content for AI-powered answer engines including ChatGPT, Perplexity, Google AI Overviews, and Claude.",
  "image": {
    "@type": "ImageObject",
    "url": "https://yourdomain.com/images/ai-seo-guide-2025.jpg",
    "width": 1200,
    "height": 630
  },
  "datePublished": "2025-01-15",
  "dateModified": "2025-06-01",
  "author": {
    "@type": "Person",
    "name": "Jane Smith",
    "url": "https://yourdomain.com/author/jane-smith",
    "sameAs": [
      "https://www.linkedin.com/in/janesmith",
      "https://twitter.com/janesmith"
    ]
  },
  "publisher": {
    "@type": "Organization",
    "name": "Revenue Experts",
    "logo": {
      "@type": "ImageObject",
      "url": "https://yourdomain.com/logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://yourdomain.com/ai-search-optimization-guide"
  }
}
```

---

## 5. ORGANIZATION SCHEMA {#organization}

**Use on:** Homepage, About page. Critical for entity recognition by AI systems.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Revenue Experts",
  "alternateName": "Revenue Experts Inc.",
  "url": "https://revenueexperts.ai",
  "logo": {
    "@type": "ImageObject",
    "url": "https://revenueexperts.ai/logo.png"
  },
  "description": "Revenue Experts is an AI consulting and automation company specializing in AI agents, n8n workflows, RAG pipelines, and Answer Engine Optimization (AEO) services for B2B clients.",
  "foundingDate": "2023",
  "founder": [
    {
      "@type": "Person",
      "name": "Elizabeta Kuzevska"
    },
    {
      "@type": "Person",
      "name": "John Bush"
    },
    {
      "@type": "Person",
      "name": "Peter Von Moltke"
    }
  ],
  "address": {
    "@type": "PostalAddress",
    "addressCountry": "CA"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer support",
    "url": "https://revenueexperts.ai/contact"
  },
  "sameAs": [
    "https://www.linkedin.com/company/revenue-experts",
    "https://twitter.com/revenueexperts"
  ],
  "knowsAbout": [
    "Answer Engine Optimization",
    "AI Search Visibility",
    "n8n Automation",
    "RAG Pipelines",
    "AI Consulting"
  ]
}
```

---

## 6. PERSON SCHEMA {#person}

**Use on:** Author profile pages, About pages for personal brands.

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Jane Smith",
  "jobTitle": "AI SEO Strategist",
  "description": "Jane Smith is an AI search optimization specialist with 10+ years of experience in digital marketing and B2B content strategy.",
  "url": "https://yourdomain.com/author/jane-smith",
  "image": "https://yourdomain.com/images/jane-smith.jpg",
  "email": "jane@yourdomain.com",
  "sameAs": [
    "https://www.linkedin.com/in/janesmith",
    "https://twitter.com/janesmith",
    "https://www.instagram.com/janesmith"
  ],
  "worksFor": {
    "@type": "Organization",
    "name": "Your Company",
    "url": "https://yourdomain.com"
  },
  "knowsAbout": [
    "SEO",
    "Answer Engine Optimization",
    "Content Marketing",
    "AI Search"
  ],
  "hasCredential": {
    "@type": "EducationalOccupationalCredential",
    "name": "Google Analytics Certified",
    "credentialCategory": "certification"
  }
}
```

---

## 7. PRODUCT SCHEMA {#product}

**Use on:** Product and service pages with pricing.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "AI Search Visibility Audit",
  "description": "Comprehensive AI search visibility audit covering 8 specialist analysis areas including LLM visibility, technical infrastructure, content structure, and citation potential.",
  "brand": {
    "@type": "Brand",
    "name": "Revenue Experts"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://revenueexperts.llmauditpro.com",
    "priceCurrency": "USD",
    "price": "297",
    "priceValidUntil": "2025-12-31",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "Revenue Experts"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "47"
  }
}
```

---

## 8. BREADCRUMBLIST SCHEMA {#breadcrumb}

**Use on:** All non-homepage pages.

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://yourdomain.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "AEO Resources",
      "item": "https://yourdomain.com/aeo-resources"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "What is AEO?",
      "item": "https://yourdomain.com/aeo-resources/what-is-aeo"
    }
  ]
}
```

---

## 9. DEFINEDTERM SCHEMA {#definedterm}

**Use on:** Glossary pages, definition pages — extremely valuable for AEO.

```json
{
  "@context": "https://schema.org",
  "@type": "DefinedTerm",
  "name": "Answer Engine Optimization",
  "alternateName": "AEO",
  "description": "Answer Engine Optimization (AEO) is the practice of structuring digital content to maximize citation by AI-powered answer systems such as ChatGPT, Perplexity, Google AI Overviews, and Claude. AEO encompasses content architecture, entity optimization, schema markup, and llms.txt implementation.",
  "inDefinedTermSet": {
    "@type": "DefinedTermSet",
    "name": "AI Marketing Glossary",
    "url": "https://yourdomain.com/glossary"
  }
}
```

---

## 10. SPEAKABLE SCHEMA {#speakable}

**Use on:** News articles, informational pages — marks sections optimized for voice/AI reading.

```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "AI Search Is Replacing Traditional SEO: What Marketers Need to Know",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".article-intro", ".key-takeaways"]
  },
  "url": "https://yourdomain.com/ai-search-seo-marketers"
}
```

---

## 11. DATASET SCHEMA {#dataset}

**Use on:** Original research pages, data studies — extremely high AI citation value.

```json
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "2025 AI Search Visibility Benchmark Report",
  "description": "Survey data from 500 B2B marketers measuring AI search citation rates, content optimization practices, and AEO ROI across industries.",
  "url": "https://yourdomain.com/research/ai-search-benchmark-2025",
  "creator": {
    "@type": "Organization",
    "name": "Revenue Experts"
  },
  "datePublished": "2025-03-01",
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "variableMeasured": [
    "AI citation rate",
    "Content optimization score",
    "AEO implementation rate"
  ]
}
```

---

## 12. LOCALBUSINESS SCHEMA {#localbusiness}

**Use on:** Homepage and contact page for local businesses.

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Your Business Name",
  "image": "https://yourdomain.com/logo.png",
  "url": "https://yourdomain.com",
  "telephone": "+1-555-123-4567",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main Street",
    "addressLocality": "Your City",
    "addressRegion": "State",
    "postalCode": "12345",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  ],
  "sameAs": [
    "https://www.google.com/maps?cid=YOURPLACEID",
    "https://www.yelp.com/biz/your-business"
  ]
}
```

---

## 13. REVIEW / AGGREGATERATING SCHEMA {#review}

**Use on:** Product pages, service pages, homepage — only if you have real reviews.

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "AI Revenue Acceleration System",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "bestRating": "5",
    "worstRating": "1",
    "ratingCount": "62"
  },
  "review": [
    {
      "@type": "Review",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "5"
      },
      "author": {
        "@type": "Person",
        "name": "Michael Torres"
      },
      "reviewBody": "The AI search visibility audit identified gaps we had missed for months. Implementation was smooth and citations increased within 6 weeks."
    }
  ]
}
```

---

## 14. EVENT SCHEMA {#event}

**Use on:** Webinars, workshops, live events, courses with sessions.

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "AEO Masterclass: Optimizing for AI Search",
  "startDate": "2025-09-15T10:00:00-05:00",
  "endDate": "2025-09-15T12:00:00-05:00",
  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
  "eventStatus": "https://schema.org/EventScheduled",
  "location": {
    "@type": "VirtualLocation",
    "url": "https://yourdomain.com/webinar/aeo-masterclass"
  },
  "description": "A 2-hour live masterclass covering AEO implementation, llms.txt deployment, schema markup for AI, and entity optimization strategies.",
  "organizer": {
    "@type": "Organization",
    "name": "Revenue Experts",
    "url": "https://revenueexperts.ai"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://yourdomain.com/webinar/register",
    "price": "0",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  }
}
```

---

## 15. SITELINKS SEARCHBOX {#sitelinks}

**Use on:** Homepage only — enables Google Sitelinks search box.

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "url": "https://yourdomain.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://yourdomain.com/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

---

## 16. IMPLEMENTATION & VALIDATION {#implementation}

### Where to Place Schema
- In `<head>` section (recommended for critical schema)
- Or at bottom of `<body>` before `</body>`
- WordPress: Use Yoast SEO, RankMath, or Schema Pro plugins
- Custom code: Inject via GTM or hardcode in template

### Validation Tools
1. **Google Rich Results Test**: search.google.com/test/rich-results
2. **Schema Markup Validator**: validator.schema.org
3. **Bing Markup Validator**: bing.com/webmaster/tools
4. **Google Search Console → Enhancements**: See indexed rich results by type

### Priority Implementation Order
1. Organization (homepage) — entity recognition
2. FAQPage (all content pages) — AI citation
3. Article (all blog/guide pages) — E-E-A-T signals
4. BreadcrumbList (all pages) — navigation signals
5. HowTo (tutorial pages) — AI structured extraction
6. Product/Service (conversion pages) — commercial signals
7. DefinedTerm (glossary pages) — topical authority
8. Dataset (research pages) — original data citation

### Common Mistakes to Avoid
- ❌ Schema content that doesn't match visible page content
- ❌ Fake or inflated review counts
- ❌ Using schema on content hidden from users
- ❌ Missing required properties (use validator to check)
- ❌ Duplicate schema types on same page (exception: multiple FAQPage items are fine)
- ❌ Placing schema behind JavaScript that blocks crawling
