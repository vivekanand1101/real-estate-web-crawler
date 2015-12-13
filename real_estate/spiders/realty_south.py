import datetime
import scrapy.item
import scrapy.selector
import scrapy.linkextractors
import scrapy.spiders
import scrapy.conf
import scrapy.crawler

import real_estate
import real_estate.items
import real_estate.settings

class RealtySouth(scrapy.spiders.CrawlSpider):
    """ Real Estate web crawler for realtysouth.com """

    name = 'realtysouth'
    allowed_domains = ['www.realtysouth.com']
    cities = real_estate.settings.REALTY_SOUTH_CITIES
    states = real_estate.settings.REALTY_SOUTH_STATES

    start_urls = []
    for state in states:
        for city in cities[state]:
            start_urls += ['http://www.realtysouth.com/homes-for-sale/%s/%s'
                                                            % (state, city)]

    extraction_regex_list = []
    for state in states:
        for city in cities[state]:
            extraction_regex_list += [r'/homes-for-sale/.*-%s-.*' % city]

    extractor = scrapy.linkextractors.LinkExtractor(
            allow = extraction_regex_list,
            restrict_xpaths = (
                '//div[contains(@id, "listinglanding-main")]'
            )
    )

    pagination_regex_list = []
    for state in states:
        for city in cities[state]:
            pagination_regex_list += [r'homes-for-sale/%s/%s/p-.*/s-.*' % (state, city)]

    paginate = scrapy.linkextractors.LinkExtractor(
            allow = pagination_regex_list,
            restrict_xpaths = (
                '//div[contains(@class, "content landing-pagination")]'
            )
    )

    rules = [
        scrapy.spiders.Rule(
            extractor, callback='parse_items', follow=True
        ),
        scrapy.spiders.Rule(
            paginate
        )
    ]

    def parse_items(self, response):
        hxs = scrapy.Selector(response)

        item = real_estate.items.RealEstateItem()
        item['description'] = self.get_description(hxs)
        item['price'] = self.get_price(hxs)
        item['mls_id'] = self.get_mls_id(hxs)
        item['state'] = self.get_state(hxs)
        item['city'] = self.get_city(hxs)
        item['zipcode'] = self.get_zipcode(hxs)
        item['full_address'] = self.get_full_address(hxs)
        item['city_url'] = self.get_city_url(hxs)
        item['state_url'] = self.get_state_url(hxs)
        item['half_bathrooms'] = self.get_half_bathrooms(hxs)
        item['full_bathrooms'] = self.get_full_bathrooms(hxs)
        item['bathrooms'] = self.get_bathrooms(hxs)
        item['bedrooms'] = self.get_bedrooms(hxs)
        item['year_built'] = self.get_year_built(hxs)
        item['property_type'] = self.get_property_type(hxs)
        item['broker_name'] = self.get_broker_name(hxs)
        item['updated_at'] = str(datetime.datetime.utcnow())
        item['url'] = self.get_url(response)
        item['lot_size'] = self.get_lot_size(hxs)
        item['price_currency'] = 'USD'
        item['features'] = self.get_features(hxs)
        item['fees'] = self.get_fees(hxs)
        item['has_picture'] = True
        item['has_thumbs'] = True
        item['searchable'] = True
        yield item

    def get_fees(self, hxs):
        fees_path = hxs.xpath('//td[contains(@class, "details-text-data")]/label[contains(.,"Tax Amount:")]/following-sibling::node()/text()')
        try:
            fees = fees_path.extract()[0].strip()
            fees_dict = {}
            fees_dict["name"] = "property taxes"
            fees_dict["amount"] = fees
            fees_dict["frequence"] = "annually"
            return fees_dict
        except IndexError:
            return ''

    def get_lot_size(self, hxs):
        lot_size_path = hxs.xpath('//td[contains(@class, "details-text-data")]/label[contains(.,"Lot Size:")]/following-sibling::node()/text()')
        try:
            lot_size = lot_size_path.extract()[0].strip()
            lot_size += ' Acres'
            return lot_size
        except IndexError:
            return ''

    def get_features(self, hxs):
        features_list = []
        appliances_path = hxs.xpath('//div[contains(@class, "details-text-data")]/label[contains(.,"Appliances:")]/following-sibling::text()')
        cooling_path = hxs.xpath('//div[contains(@class, "details-text-data")]/label[contains(.,"Cooling:")]/following-sibling::text()')
        flooring_path = hxs.xpath('//div[contains(@class, "details-text-data")]/label[contains(.,"Flooring:")]/following-sibling::text()')
        fireplace_path = hxs.xpath('//div[contains(@class, "details-text-data")]/label[contains(.,"Fireplaces:")]/following-sibling::node()/text()')

        try:
            appliances = appliances_path.extract()[0]
            appliances_list = appliances.split(',')
            for app in appliances_list:
                app = app.strip()
                app_ = app.lower()
                if ' ' in app_:
                    app_ = app_.replace(' ', '-')
                app_dict = {}
                app_dict["name"] = "appliances"
                app_dict["category"] = "interior"
                app_dict["value"] = app
                app_dict["url"] = "appliances, interior, %s" % app_
                features_list.append(app_dict.copy())
        except IndexError:
            pass

        try:
            cooling = cooling_path.extract()[0]
            cooling_list = cooling.split(',')
            for cool in cooling_list:
                cool = cool.strip()
                cool_ = cool.lower()
                if ' ' in cool_:
                    cool_ = cool_.replace(' ', '-')
                cool_dict = {}
                cool_dict["name"] = "general"
                cool_dict["category"] = "cooling"
                cool_dict["value"] = cool
                cool_dict["url"] = "cooling, general, %s" % cool_
                features_list.append(cool_dict.copy())
        except IndexError:
            pass

        try:
            flooring = flooring_path.extract()[0]
            flooring_list = flooring.split(',')
            for floor in flooring_list:
                floor = floor.strip()
                floor_ = floor.lower()
                if ' ' in floor_:
                    floor_ = floor_.replace(' ', '-')
                floor_dict = {}
                floor_dict["name"] = "general"
                floor_dict["category"] = "flooring"
                floor_dict["value"] = floor
                floor_dict["url"] = "general, interior, %s" % floor_
                features_list.append(floor_dict.copy())
        except IndexError:
            pass

        try:
            fireplace = fireplace_path.extract()[0]
            fireplace_dict = {}
            fireplace_dict["name"] = "general"
            fireplace_dict["category"] = "fireplace"
            fireplace_dict["value"] = fireplace.strip()
            fireplace_dict["url"] = "general, interior"
            features_list.append(fireplace_dict.copy())
        except IndexError:
            pass

        return features_list

    def get_full_bathrooms(self, hxs):
        full_bath_path = hxs.xpath('//td[contains(@class, "details-text-data")]/label[text()="Full Baths:"]/following-sibling::text()')
        try:
            return full_bath_path.extract()[0].strip()
        except IndexError:
            return ''

    def get_property_type(self, hxs):
        property_type_path = hxs.xpath('//td[@class="details-header-sub"]/child::text()[contains(., "Property Type:")]')
        property_type = property_type_path.extract()[0].strip()
        try:
            return property_type.replace('Property Type:', '').strip()
        except IndexError:
            return ''

    def get_broker_name(self, hxs):
        broker_name_path = hxs.xpath('//span[contains(@id, "Master_ListingCourtesyOf_bottom_lblCourtesyOf")]/child::node()[contains(.,"Courtesy:")]//text()')
        broker_name = broker_name_path.extract()[0].strip()
        try:
            return broker_name.replace('Courtesy: ', '').strip()
        except IndexError:
            return ''

    def get_half_bathrooms(self, hxs):
        half_bath_path = hxs.xpath('//td[contains(@class, "details-text-data")]/label[text()="1/2 Baths:"]/following-sibling::text()')
        try:
            return half_bath_path.extract()[0].strip()
        except IndexError:
            return 0

    def get_year_built(self, hxs):
        year_built_path = hxs.xpath('//td[contains(@class, "details-text-data")]/label[text()="Year Built:"]/following-sibling::text()')
        try:
            return year_built_path.extract()[0].strip()
        except IndexError:
            return ''

    def get_bathrooms(self, hxs):
        half_baths = self.get_half_bathrooms(hxs)
        full_baths = self.get_half_bathrooms(hxs)
        try:
            return int(full_baths) + 0.5 * int(half_baths)
        except IndexError:
            return 0.00

    def get_bedrooms(self, hxs):
        bedrooms_path = hxs.xpath('//td[contains(@class, "details-text-data")]/label[text()="Bedrooms:"]/following-sibling::text()')
        try:
            return bedrooms_path.extract()[0].strip()
        except IndexError:
            return ''

    def get_url(self, response):
        return response.url

    def get_description(self, hxs):
        desc_path = hxs.xpath('//div[contains(@class, "details-info details-text-data")]//text()')
        try:
            return desc_path.extract()[0]
        except IndexError:
            return ''

    def get_price(self, hxs):
        price_path = hxs.xpath('//div[contains(@class, "price-container")]//span[contains(@class, "price")]//text()')
        try:
            return price_path.extract()[0]
        except IndexError:
            return ''

    def get_mls_id(self, hxs):
        mls_id_path = hxs.xpath('//div[contains(@class, "listing-number")]//text()')
        mls_id_text = mls_id_path.extract()
        try:
            return mls_id_text[0].replace('MLS# ', '')
        except IndexError:
            return ''

    def get_city(self, hxs):
        city_path = hxs.xpath('//span[contains(@class, "city-state-zip")]//text()')
        city_text = city_path.extract()
        try:
            return city_text[0][:city_text[0].find(',')]
        except IndexError:
            return ''

    def get_state(self, hxs):
        state_path = hxs.xpath('//span[contains(@class, "city-state-zip")]//text()')
        state_text = state_path.extract()
        state_with_spaces = state_text[0][state_text[0].find(',')+1:-5]
        try:
            return state_with_spaces.strip()
        except IndexError:
            return ''

    def get_city_url(self, hxs):
        city = self.get_city(hxs)
        state = self.get_state(hxs)
        try:
            return 'http://www.realtysouth.com/homes-for-sale/%s/%s' % (state, city)
        except IndexError:
            return ''

    def get_state_url(self, hxs):
        state = self.get_state(hxs)
        try:
            return 'http://www.realtysouth.com/homes-for-sale/%s' % (state)
        except IndexError:
            return ''

    def get_zipcode(self, hxs):
        zipcode_path = hxs.xpath('//span[contains(@class, "city-state-zip")]//text()')
        zipcode_text = zipcode_path.extract()
        try:
            return zipcode_text[0][-5:]
        except IndexError:
            return ''

    def get_full_address(self, hxs):
        full_address_path = hxs.xpath('//h1[contains(@class, "full-address")]//text()')
        try:
            return full_address_path.extract()[0]
        except IndexError:
            return ''
