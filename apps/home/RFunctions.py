from apps.home.rpy2_helper import get_robjects
get_robjects()

from rpy2 import robjects

def downloadRNA(projectID, dataType):
    r_script = f'''
        library(GDCRNATools)
        download_RNAseq_data <- function(projectID, dataType) {{
            

            # Definir el directorio de destino
            rnadir <- paste(projectID, 'data/RNAseq', sep='/')
            
            # Descargar RNAseq data 
            gdcRNADownload(project.id     = projectID, 
                            data.type      = dataType, 
                            write.manifest = FALSE,
                            method         = 'gdc-client',
                            directory      = rnadir)
            }}
        download_RNAseq_data('{projectID}', '{dataType}')
    '''
    robjects.r(r_script)
    return True

def analysisRNA(projectID, dataType):

    r_script = f'''
        library(GDCRNATools)
        library(dplyr)
        library(tidyr)

        getMetaMatrix <- function(projectID, dataType) {{
            metaMatrix.RNA <- gdcParseMetadata(project.id = projectID,
                                               data.type = dataType, 
                                               write.meta = FALSE)

            # Filter duplicates
            metaMatrix.RNA <- gdcFilterDuplicate(metaMatrix.RNA)

            # Filter non-Primary Tumor and non-Solid Tissue Normal samples in RNAseq metadata
            metaMatrix.RNA <- gdcFilterSampleType(metaMatrix.RNA)
            return(metaMatrix.RNA)
        }}

        # Call the R function and save the result to a variable
        metaMatrix.RNA <- getMetaMatrix('{projectID}', '{dataType}')

        rnadir <- paste('{projectID}', 'data/RNAseq', sep='/')
        
        # Guardar el DataFrame en un archivo CSV
        write.csv(metaMatrix.RNA, file = "{projectID}/metaMatrix_RNA.csv", row.names = TRUE)

        ####### Merge RNAseq data #######
        rnaCounts <- gdcRNAMerge(metadata  = metaMatrix.RNA, 
                            path      = rnadir, # the folder in which the data stored
                            organized = FALSE, # if the data are in separate folders
                            data.type = '{dataType}')
        
        write.csv(rnaCounts, file = "{projectID}/rnaCounts.csv", row.names = TRUE)

        ####### Normalization of RNAseq data #######
        rnaExpr <- gdcVoomNormalization(counts = rnaCounts, filter = FALSE)
        write.csv(rnaExpr, file = "{projectID}/RNA_EXPR.csv", row.names = TRUE)

        result <- gdcDEAnalysis(counts = rnaCounts, 
                        group      = metaMatrix.RNA$sample_type, 
                        comparison = 'PrimaryTumor-SolidTissueNormal', 
                        method     = 'DESeq2',
                        filter=TRUE)
                    
        write.csv(result, file = "{projectID}/DEGALL_CHOL.csv", row.names = TRUE)

        enrichOutput <- gdcEnrichAnalysis(gene = rownames(result), simplify = TRUE)

        write.csv(enrichOutput, file = "{projectID}/ENRICH_ANALYSIS.csv", row.names = TRUE)
        '''
    robjects.r(r_script)

    return True