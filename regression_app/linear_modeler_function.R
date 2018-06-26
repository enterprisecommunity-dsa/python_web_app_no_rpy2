linear_modeler<-function(d){
  #d should be a dataframe with the dependent variable in the first column.
  l<-lm(data=d)
  return(as.numeric(l$coefficients))
}