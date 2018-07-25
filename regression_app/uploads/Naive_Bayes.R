#Installing the requisite packages
install.packages("dummies")
install.packages("caret")
install.packages("class")
install.packages('e1071', dependencies=TRUE)

#loading the data
cred <- read.csv("C:/Users/omelia/Documents/Python Scripts/Credit.csv")
cred$OBS. <-NULL


#creating the dependent variable based on the NPV
tabnew <- ifelse(cred$NPV>0, 1,0)

#combinging the new column with the dataset
df <- data.frame(tabnew)
crednew <- cbind(cred,df)

#remving the NPV column
crednew[,22] <- NULL

#converting the following columns into factors
crednew$CHK_ACCT <- as.factor(crednew$CHK_ACCT)
crednew$SAV_ACCT <- as.factor(crednew$SAV_ACCT)
crednew$NUM_CREDITS <- as.factor(crednew$NUM_CREDITS)
crednew$HISTORY <- as.factor(crednew$HISTORY)
crednew$PRESENT_RESIDENT <- as.factor(crednew$PRESENT_RESIDENT)
crednew$EMPLOYMENT <- as.factor(crednew$EMPLOYMENT)
crednew$JOB <- as.factor(crednew$JOB)
crednew$NUM_DEPENDENTS <- as.factor(crednew$NUM_DEPENDENTS)
crednew$RENT <- as.factor(crednew$RENT)
crednew$INSTALL_RATE <- as.factor(crednew$INSTALL_RATE)
crednew$GUARANTOR <- as.factor(crednew$GUARANTOR)
crednew$OTHER_INSTALL <- as.factor(crednew$OTHER_INSTALL)
crednew$OWN_RES <- as.factor(crednew$OWN_RES)
crednew$TELEPHONE <- as.factor(crednew$TELEPHONE)
crednew$FOREIGN <- as.factor(crednew$FOREIGN)
crednew$REAL_ESTATE <- as.factor(crednew$REAL_ESTATE)
crednew$TYPE <- as.factor(crednew$TYPE)

#setting the seed
library(caret)
set.seed(12345)

#partitionaing the data into training and validation
inTrain <- createDataPartition(crednew$tabnew, p=0.7, list=FALSE)
#inTrain <- 1:700
dftrain <- data.frame(crednew[inTrain,])
dfvalidation <- data.frame(crednew[-inTrain,])


#implementing Naive Bayes'
library(e1071)
model <- naiveBayes(as.factor(tabnew)~., data=dftrain)
#model
prediction <- predict(model, newdata = dfvalidation[,-22])
table(dfvalidation$tabnew,prediction,dnn=list('actual','predicted'))
model$apriori
predicted.probability <- predict(model, newdata = dfvalidation[,-22], type="raw")
predicted.probability

#predicting probability of new data
newdat2 <- data.frame(
  "AGE" = 27, "CHK_ACCT" = 1, "SAV_ACCT" = 4, "NUM_CREDITS" = 1, "DURATION" = 12, "HISTORY" = 1, "PRESENT_RESIDENT" = 1, "EMPLOYMENT = 1", "JOB" = 2, "NUM_DEPENDENTS" = 1, "RENT" = 1, 
  "INSTALL_RATE" = 3, "GUARANTOR" = 0, "OTHER_INSTALL" = 0, "OWN_RES" = 0, "TELEPHONE" = 1, "AMOUNT_REQUESTED" = 4500)
predicted.probability <- predict(model, newdata = newdat2, type="raw")



