# About the data

The dataset is about the biggest companies in the world by turnover. The date was published by „fortune global 500“ . The fortune global 500 publishes the 100 biggest companies by order of annual turnover. 
I chose this data because I find it exciting to find out about international companies In general. It tells us how important and powerful these companies are compared to medium-sized or smaller European countries like Italy or Greece (Italy- GDP 1,281 Billions USD, Greece-GDP 189,4 Millions USD).

# Development process
- started with scraping a wikipedia page with bs4
- as the tables of wikipedia most often don't have an id, it was hard to get the correct selector for the table
- when scraping the info boxes of the wikipedia pages it came clear that not all pages had the same set of (reasonable interesting) data
- after the basics of the script worked, I did some enhancement to the code and took also some of the hints into account
- - using the request-cache module
 -- reordering the code, so that the steps become more clear
 - moved the variable declaration to the top of the script
 - added and refined the comments
