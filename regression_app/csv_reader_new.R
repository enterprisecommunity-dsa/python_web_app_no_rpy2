# Gathers the command line arguments using commandArgs() and then calls the defined functions 
# using the call main()

x<-commandArgs(trailingOnly = TRUE)
fill_data_frame <-function(x){
  # Takes a character vector formatted like the following:
  #   "Variable_A", "A_1", "A_2",..., "Variable_B", "B_1", "B_2", ... 
  # Returns a data frame with each variable in a unique column. 
  
  
  list_of_vectors<-list()
  for(i in x){
    if(is.na(suppressWarnings(as.numeric(i)))){
      list_of_vectors[[i]] <-c()
      current_name <- i
      
    }
    else{
     list_of_vectors[[current_name]] <- append(list_of_vectors[[current_name]], as.numeric(i))
    }
      
  }
  return(data.frame(list_of_vectors))
}

return_formula<-function(dframe, dependent_var){
  # Takes a dataframe and the name of the column to be treated as the dependent variable, and
  # returns an object of class 'formula' describing the dependent variable as a function 
  # of all of the other columns.
  # 
  independent_vars <-colnames(dframe)[!colnames(dframe) == dependent_var]
  independent_vars_str<-paste(independent_vars, collapse = '+')
  form_str <-paste0(dependent_var, '~', independent_vars_str)
  return(as.formula(form_str))
}

print_lm<-function(dframe, form){
  model<-lm(form, data = dframe)
  print(summary(model))
  library(rjson)
  writeLines(toJSON(model$coefficients))
}

main<-function(x){
  # Takes the character vector supplied by commandArgs(), strips the first argument, which signifies the
  # dependent variable name, and then makes calls to fill_data_frame(), return_formula(), and print_lm()
  # 
  dep_var <-x[1]
  df <- fill_data_frame(x[-1])
  frm <- return_formula(df, dep_var)
  print_lm(df, frm)
}

main(x)