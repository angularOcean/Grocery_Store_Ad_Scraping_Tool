This was a hackathon project for Oregon State Univeristy's Winter 2022

This project scrapes grocery store websites for their sales data and builds a google sheet filled with the items and their prices. It will take a users current zip code as a parameter (USA only) and then pull the weekly sales data for the closest store to that zip code for a chosen grocery store. 

Currently the project can only pull data for Whole Foods and Fred Meyer though my ambition is for it to be able to also grab from other major chains. The program will then create a google sheet spreadsheet of the sales data for the stores and populate separate worksheets for it. 

One spreadsheet per store and one worksheet per day. Right now the data is stored in two columns, one for the items name and another for the price. Data for items from Fred Meyer are also cleaned and those that are marked as "2 for 3" etc. are recalculated for their cost as just one item.
