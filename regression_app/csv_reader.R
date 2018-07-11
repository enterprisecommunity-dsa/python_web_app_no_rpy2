cmdargs <- commandArgs( trailingOnly = TRUE)
df <-read.csv(cmdargs)
d <-lm(df)
print(summary(d))