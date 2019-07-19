
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

#adding layer from dataframe to map
#Required map and df object
add_df_tomap = function(map,df){
  if ("arcgis.widgets._mapview.MapView" %in% class(map)){
    map$add_layer(featureset$from_dataframe(df))
    return(map)
  }
  else
    stop("Map format must be argis.widgets type")
}


