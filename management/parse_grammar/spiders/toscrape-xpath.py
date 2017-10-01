# -*- coding: utf-8 -*-
import scrapy


class GrammarRuleItem(scrapy.Item):
    difficulty = scrapy.Field()
    name = scrapy.Field()
    theory = scrapy.Field()
    exercises = scrapy.Field()


class ToScrapeGrammar(scrapy.Spider):
    name = 'gramma-parser'
    start_urls = [
        'http://english-lingualeo.blogspot.com/',
        
    ]
    
    def parse(self, response):
        response = response.xpath('//div[@class="index"]')
        links = response.xpath('.//a/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_grammar_rule)

    def parse_grammar_rule(self, response):
        grammar_rule = GrammarRuleItem()
        grammar_rule['name'] = response.xpath('//title/text()').extract()
        grammar_rule['difficulty'] = response.xpath('//span[@class="post-tags"]/text()').extract_first()

        rule_theory = response.xpath('//div[@class="post-body entry-content float-container"]/div/text()').extract()
        rule_theory = ''.join(rule_theory).rstrip('\n')
        grammar_rule['theory'] = rule_theory

        rule_exercises = response.xpath('//span/i/text()').extract()
        rule_exercises = list([rule_exercises[i:i + 2] for i in range(0, len(rule_exercises), 2)])
        grammar_rule['exercises'] = rule_exercises

        yield grammar_rule

