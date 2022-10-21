install.packages("pacman")
library(pacman)
pacman::p_load(pacman, dplyr, GGally, ggplot2, ggthemes,ggvis,httr, 
               lubridate,plotly, rio,rmarkdown,shiny,stringr,tidyr)
library(RCurl)
library(data.table)
library(tidyr)
install.packages("moments")

#GET FROM Bitcoincharts

data_from_Bitcoincharts <- utils::read.table("qq1(1).csv", sep = ',', dec = '.', 
                                             header = F, stringsAsFactors = F)
names(data_from_Bitcoincharts) <- c('timestamp', 'close_price')
data_from_Bitcoincharts$timestamp <- as.Date(data_from_Bitcoincharts$timestamp, format="%m/%d/%Y")
saveRDS(data_from_Bitcoincharts, 'bitcoin_data1.rds')
data_from_Bitcoincharts = head(data_from_Bitcoincharts,-1)

#GET FROM coinmetrics
data2_from_coinmetrics <- utils::read.table("qq2(1).csv", sep = ',', dec = '.', 
                                            header = F, stringsAsFactors = F)
names(data2_from_coinmetrics) <- c('timestamp', 'close_price')
data2_from_coinmetrics$timestamp <- as.Date(data2_from_coinmetrics$timestamp, 
                                            format="%m/%d/%Y")
saveRDS(data2_from_coinmetrics, 'bitcoin_data2.rds')


par(mfrow = c(2,1))
plot(data2_from_coinmetrics, type = "l",col = "blue")
lines(data_from_Bitcoincharts, col = "green")
legend("topright", c("data_from_coinmetrics", "data_from_Bitcoincharts"), cex=0.5,
       col = c("blue", "green"),  lwd = 0.5)
df <- data.frame(data2_from_coinmetrics$timestamp, 
                 data2_from_coinmetrics$close_price - data_from_Bitcoincharts$close_price)
names(df) <- c('timestamp', 'the difference between close price')
plot(df, type = "l",col = "red")


#GET FROM Bitcoincharts

bitcoin_charts <- function(name = "bitstampUSD.csv.gz",
                           start_date = "2021-09-17",
                           end_date = "2022-09-17",
                           save_data = FALSE){
  
  link <- 'http://api.bitcoincharts.com/v1/csv/'
  link_to_file <- paste0(link, name)
  temp_file <- tempfile()
  options(timeout = 100)
  utils::download.file(link_to_file, temp_file, "libcurl") 
  data <- utils::read.table(temp_file, sep = ',', dec = '.', header = F, stringsAsFactors = F)
  names(data) <- c('timestamp', 'price', 'volume')
  
  start_date <- as.numeric(as.POSIXct(start_date, origin = '1970-01-01 00:00:00'))
  end_date <- as.numeric(as.POSIXct(end_date, origin = '1970-01-01 00:00:00'))
  
  data <- data[(data$timestamp >= start_date) & (data$timestamp <= end_date)]
  if (save_data) saveRDS(data,"bitcoin_data.rds")
  rm(link,link_to_file,temp_file)
  data
}


data_bitcoin_charts <- bitcoin_charts()
print(data_bitcoin_charts)
data_bitcoin_charts$timestamp <- as.Date(as.POSIXct(data_bitcoin_charts$timestamp,format = "%Y/%m/%d", 
                                                    origin = "1970-01-01"))
data_bitcoin_charts$price <- as.integer(data_bitcoin_charts$price)
print(data_bitcoin_charts)
temp <- data_bitcoin_charts
data_bitcoin_charts <-as.data.frame(summarize(group_by(temp,timestamp), close = last(price),
                               open = first(price),
                               high = max(price), 
                               low = min(price)))

data <- data_bitcoin_charts %>%  mutate(j = data_bitcoin_charts$open - lag(data_bitcoin_charts$close))
data$daily_range <- 0.5 *((data$high - data$low)^(2)) - (2*log(2) - 1)*(log(data$close) - log(data$open))^(2) + (data$j)^(2)
par(mfrow = c(2,1))
plot(data$timestamp, data$daily_range,  main="GK Volatility",xlab="timestamp", ylab="daily range squared", type = "l",col = "blue")
data$daily_range_ln <- log(sqrt(data$daily_range))
data$standart <- scale(data$daily_range_ln, center = TRUE, scale = TRUE)
print(data)
data <- data[-1,]
hist(data$standart, breaks = 100, main="standardized the daily log-returns", xlab = "log- rerturns", freq = FALSE)

data$standart.mean <- mean(data$standart)
data$standart.sd <- sd(data$standart)
print(data)
print(min(data$standart))
x <- seq(min(data$standart), max(data$standart), by = 0.001)
y <- dnorm(x = x, mean = data$standart.mean, sd = data$standart.sd)
lines(x = x,y = y,col = 'red')

library(moments)
print(kurtosis(data$standart))
print(skewness(data$standart))


