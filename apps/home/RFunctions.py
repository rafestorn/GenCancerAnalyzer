from apps.home.rpy2_helper import get_robjects
get_robjects()

from rpy2 import robjects

def downloadRNA(projectID, dataType):
    r_script = f'''
        library(GDCRNATools)
        download_RNAseq_data <- function(projectID, dataType) {{
            

            # Definir el directorio de destino
            rnadir <- paste('DATA', projectID, dataType, 'data', sep='/')
            
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

        ruta_completa <- "DATA/{projectID}/{dataType}/results"
        dir.create(ruta_completa)

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

        rnadir <- paste('DATA', '{projectID}', '{dataType}', 'data', sep='/')
        
        # Guardar el DataFrame en un archivo CSV

        ####### Merge RNAseq data #######
        rnaCounts <- gdcRNAMerge(metadata  = metaMatrix.RNA, 
                            path      = rnadir, # the folder in which the data stored
                            organized = FALSE, # if the data are in separate folders
                            data.type = '{dataType}')
        
        ####### Normalization of RNAseq data #######
        rnaExpr <- gdcVoomNormalization(counts = rnaCounts, filter = FALSE)

        result <- gdcDEAnalysis(counts = rnaCounts, 
                        group      = metaMatrix.RNA$sample_type, 
                        comparison = 'PrimaryTumor-SolidTissueNormal', 
                        method     = 'DESeq2',
                        filter=TRUE)
                    

        if ('{dataType}' == 'RNAseq') {{

            filterDE <- gdcDEReport(deg = result, gene.type = 'all')
        
            enrichOutput <- gdcEnrichAnalysis(gene = rownames(filterDE), simplify = TRUE)        
            survivalOutput <- gdcSurvivalAnalysis(gene = rownames(filterDE), 
                                  method   = 'KM', 
                                  rna.expr = rnaExpr, 
                                  metadata = metaMatrix.RNA, 
                                  sep      = 'median')

            write.csv(enrichOutput, file = paste('DATA', '{projectID}', '{dataType}', 'results', 'ENRICH_ANALYSIS.csv', sep = '/'), row.names = TRUE)
            write.csv(survivalOutput, file = paste('DATA', '{projectID}', '{dataType}', 'results', 'survival_results.csv', sep='/'), row.names = TRUE)
        }}

        write.csv(result, file = paste('DATA', '{projectID}', '{dataType}', 'results', 'DEGALL_CHOL.csv', sep = '/'), row.names = TRUE)
        write.csv(rnaExpr, file = paste('DATA', '{projectID}', '{dataType}', 'results', 'RNA_EXPR.csv', sep = '/'), row.names = TRUE)
        write.csv(rnaCounts, file = paste('DATA', '{projectID}', '{dataType}', 'results', 'rnaCounts.csv', sep = '/'), row.names = TRUE)
        write.csv(metaMatrix.RNA, file = paste('DATA', '{projectID}', '{dataType}', 'results', 'metaMatrix_RNA.csv', sep = '/'), row.names = TRUE)
        '''
    robjects.r(r_script)

    return True