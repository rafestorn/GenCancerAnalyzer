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