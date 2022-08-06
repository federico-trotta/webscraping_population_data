import scrapy
import os
import csv

#creating a csv for recap, if it does not exist
if not os.path.exists("recap.csv"):
    recap = open ("recap.csv", "w") 
    writer = csv.writer(recap, delimiter=";")
    writer.writerow(["Country", "Population", "Year"]) #defining the header
else:
    recap = open ("recap.csv", "a") 
    writer = csv.writer(recap, delimiter=";")

#class by which get the links to get inside and scrape the infos
class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath('//td/a') #getting countries
        for country in countries:
            name = country.xpath('.//text()').get() #getting countries names
            link = country.xpath('.//@href').get() #getting link for the next function

            #yielding links
            yield response.follow(url=link, callback=self.parse_country, meta={'country_name':name})

#scraping the infos and append them in the csv
    def parse_country(self, response):
        name = response.request.meta['country_name'] #getting names of countries
        rows = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        for row in rows:
            year = row.xpath('.//td[1]/text()').get() #getting year
            population = row.xpath('.//td[2]/strong/text()').get() #getting population
            pop = population.replace(',', "") #removing commas from population values
        
            info_list = [name, pop, year] #appending info in a list
            writer.writerow(info_list) #writing info in csv

