# core/strategy_effects.py

strategy_effects = {
    "paid_ads": {
        "CAC_multiplier": 1.2,
        "LTV_multiplier": 1.1,
        "retention_multiplier": 0.9,
        "conversion_rate_multiplier": 1.1,
        "revenue_per_customer_multiplier": 1.05
    },
    "referral_program": {
        "CAC_multiplier": 0.8,
        "LTV_multiplier": 1.3,
        "retention_multiplier": 1.1,
        "conversion_rate_multiplier": 1.2,
        "revenue_per_customer_multiplier": 1.1
    },
    "localization": {
        "CAC_multiplier": 1.0,
        "LTV_multiplier": 1.2,
        "retention_multiplier": 1.2,
        "conversion_rate_multiplier": 1.15,
        "revenue_per_customer_multiplier": 1.05
    },
    "influencer_marketing": {
        "CAC_multiplier": 1.1,
        "LTV_multiplier": 1.3,
        "retention_multiplier": 1.0,
        "conversion_rate_multiplier": 1.25,
        "revenue_per_customer_multiplier": 1.0
    },
    "freemium_model": {
        "CAC_multiplier": 0.9,
        "LTV_multiplier": 1.0,
        "retention_multiplier": 1.3,
        "conversion_rate_multiplier": 0.95,
        "revenue_per_customer_multiplier": 1.2
    },
}
