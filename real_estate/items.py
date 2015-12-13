# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class RealEstateItem(scrapy.Item):
    description = scrapy.Field()
    price = scrapy.Field()
    mls_id = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zipcode = scrapy.Field()
    city_url = scrapy.Field()
    state_url = scrapy.Field()
    full_address = scrapy.Field()
    has_thumbs = scrapy.Field()
    has_picture = scrapy.Field()
    price_currency = scrapy.Field()
    url = scrapy.Field()
    searchable = scrapy.Field()
    year_built = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    half_bathrooms = scrapy.Field()
    full_bathrooms = scrapy.Field()
    property_type = scrapy.Field()
    broker_name = scrapy.Field()
    updated_at = scrapy.Field()
    features = scrapy.Field()
    lot_size = scrapy.Field()
    fees = scrapy.Field()

    medias = scrapy.Field()

    id = scrapy.Field()
    created_at = scrapy.Field()
    display_address = scrapy.Field()
    listing_address = scrapy.Field()
    property_type_sub = scrapy.Field()
    transaction_type = scrapy.Field()
    agent_id = scrapy.Field()
    office_mls_id = scrapy.Field()
    agent_mls_id = scrapy.Field()
    mls_name = scrapy.Field()
    mls_board_id = scrapy.Field()
    company_owned = scrapy.Field()
    account_id = scrapy.Field()
    virtual_tour = scrapy.Field()
    geocoded = scrapy.Field()
    neighborhood = scrapy.Field()
    neighborhood_url = scrapy.Field()
    price_history = scrapy.Field()
    coordinates = scrapy.Field()
    geocoded_metadata = scrapy.Field()
    history_changed_at = scrapy.Field()
    processed_at = scrapy.Field()
