library(reticulate)

(function(){
  plist = installed.packages()[,1]
  if("reticulate" %in% plist){
    library(reticulate)}
  else{
    install.packages("httr")
    library(httr)
  }
})()
