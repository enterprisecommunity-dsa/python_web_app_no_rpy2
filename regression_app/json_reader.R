# Written to be called on the command line with two arguments:
#	1. path of a file on which to run regression
#	2. <name> where regression coefficients should be saved as "regression-app/reg_results/<name>_coefficients.json"
# Runs a linear regression, prints the regression summary to stdout, and saves the regression coefficients to a json file
#	as described above.

library(rjson)
cmdargs <- commandArgs( trailingOnly = TRUE)

dd<-fromJSON(file =cmdargs[1])
df<-data.frame(dd)
d <-lm(df)
coef_filename <-paste0(cmdargs[2], "_coefficients.json")
coef_filename <-paste0("regression_app/reg_results/", coef_filename)
write(toJSON(d$coefficients), coef_filename)
print(summary(d))