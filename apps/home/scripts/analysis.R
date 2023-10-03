library(GDCRNATools)

project <- 'TCGA-CHOL'
rnadir <- paste(project, 'RNAseq', sep='/')
mirdir <- paste(project, 'miRNAs', sep='/')

####### Download RNAseq data #######
gdcRNADownload(project.id     = 'TCGA-CHOL', 
               data.type      = 'RNAseq', 
               write.manifest = FALSE,
               method         = 'gdc-client',
               directory      = rnadir)

####### Download mature miRNA data #######
gdcRNADownload(project.id     = 'TCGA-CHOL', 
               data.type      = 'miRNAs', 
               write.manifest = FALSE,
               method         = 'gdc-client',
               directory      = mirdir)

####### Parse RNAseq metadata #######
metaMatrix.RNA <- gdcParseMetadata(project.id = 'TCGA-CHOL',
                                   data.type  = 'RNAseq', 
                                   write.meta = FALSE)

####### Filter duplicated samples in RNAseq metadata #######
metaMatrix.RNA <- gdcFilterDuplicate(metaMatrix.RNA)

####### Filter non-Primary Tumor and non-Solid Tissue Normal samples in RNAseq metadata #######
metaMatrix.RNA <- gdcFilterSampleType(metaMatrix.RNA)

####### Parse miRNAs metadata #######
metaMatrix.MIR <- gdcParseMetadata(project.id = 'TCGA-CHOL',
                                   data.type  = 'miRNAs', 
                                   write.meta = FALSE)

####### Filter duplicated samples in miRNAs metadata #######
metaMatrix.MIR <- gdcFilterDuplicate(metaMatrix.MIR)

####### Filter non-Primary Tumor and non-Solid Tissue Normal samples in miRNAs metadata #######
metaMatrix.MIR <- gdcFilterSampleType(metaMatrix.MIR)

####### Merge RNAseq data #######
rnaCounts <- gdcRNAMerge(metadata  = metaMatrix.RNA, 
                         path      = rnadir, # the folder in which the data stored
                         organized = FALSE, # if the data are in separate folders
                         data.type = 'RNAseq')

####### Merge miRNAs data #######
mirCounts <- gdcRNAMerge(metadata  = metaMatrix.MIR,
                         path      = mirdir, # the folder in which the data stored
                         organized = FALSE, # if the data are in separate folders
                         data.type = 'miRNAs')

####### Download clinical data #######
clinicaldir <- paste(project, 'Clinical', sep='/')
gdcClinicalDownload(project.id     = 'TCGA-CHOL', 
                    write.manifest = FALSE,
                    method         = 'gdc-client',
                    directory      = clinicaldir)


####### Merge clinical data #######
clinicalDa <- gdcClinicalMerge(path = clinicaldir, key.info = TRUE)
clinicalDa[1:6,5:10]