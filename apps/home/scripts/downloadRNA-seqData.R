library(GDCRNATools)

getMetaMatrix <- function(projectID, dataType) {
  metaMatrix.RNA <- gdcParseMetadata(project.id = projectID,
                                    data.type = dataType, 
                                    write.meta = FALSE)

  # Filter duplicates
  metaMatrix.RNA <- gdcFilterDuplicate(metaMatrix.RNA)

  # Filter non-Primary Tumor and non-Solid Tissue Normal samples in RNAseq metadata
  metaMatrix.RNA <- gdcFilterSampleType(metaMatrix.RNA)
  return(metaMatrix.RNA)
}

# Call the R function and save the result to a variable
result <- getMetaMatrix('TCGA-CHOL', 'RNAseq')

# Print the result
write.csv(re, file = "{projectID}/metaMatrix.csv", row.names = TRUE)

