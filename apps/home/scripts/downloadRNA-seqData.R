options(warn=-1)

library(GDCRNATools)
library(dplyr)
library(tidyr)

download_RNAseq_data <- function(project_id, data_type) {
  # Definir el directorio de destino
  rnadir <- paste(project_id, 'data/RNAseq', sep='/')
  
  # Descargar RNAseq data 
  gdcRNADownload(project.id     = project_id, 
                 data.type      = data_type, 
                 write.manifest = FALSE,
                 method         = 'gdc-client',
                 directory      = rnadir)
}

download_RNAseq_data('TCGA-CHOL', 'RNA-Seq')