library(rjson)
cmdargs <- commandArgs( trailingOnly = TRUE)
dd<-fromJSON(file = cmdargs)
df<-data.frame(dd)
d <-lm(df)

print(summary(d))
