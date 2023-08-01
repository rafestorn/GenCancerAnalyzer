# suppress warnings (to include warnings,set warn to 0)
options(warn=-1)

library(GDCRNATools)
library(dplyr)
library(tidyr)


# download RNA-seq quantification files of project TCGA-CHOL
# downloaded files will be stored under TCGA-CHOL_0406/RNAseq folder, respectively
project <- 'TCGA-CHOL_0406'
rnadir <- paste(project, 'RNAseq', sep='/')

# Download RNAseq data 
gdcRNADownload(project.id     = 'TCGA-CHOL', 
               data.type      = 'RNAseq', 
               write.manifest = FALSE,
               method         = 'gdc-client',
               directory      = rnadir)




# Query metadata(e.g. patient gender, vital status) from GDC graph
# Metadata associated with RNA-seq quantification file
metaMatrix.RNA <- gdcParseMetadata(project.id = 'TCGA-CHOL',
                                   data.type  = 'RNAseq', 
                                   write.meta = FALSE)
# Filter duplicates
metaMatrix.RNA <- gdcFilterDuplicate(metaMatrix.RNA)

# Filter non-Primary Tumor and non-Solid Tissue Normal samples in RNAseq metadata
metaMatrix.RNA <- gdcFilterSampleType(metaMatrix.RNA)

metaMatrix.RNA[1:5,]

metaMatrix.RNA[,c("age_at_diagnosis", "days_to_death", "days_to_last_follow_up")] %>% summary()



# Counts of few factor variables in metadata
gender_counts <-metaMatrix.RNA %>% group_by(gender) %>% tally()
sample_type_counts <- metaMatrix.RNA %>% group_by(sample_type) %>% tally()
vital_status_counts <- metaMatrix.RNA %>% group_by(vital_status) %>% tally()
# modify three tables 
gender_counts$category <- c("gender","gender")
colnames(gender_counts)[1] <- "value"
sample_type_counts$category <- c("sample_type","sample_type")
colnames(sample_type_counts)[1] <- "value"
vital_status_counts$category <- c("vital_status","vital_status")
colnames(vital_status_counts)[1] <- "value"
# coombined 3 tables
combined_counts <-rbind(gender_counts, sample_type_counts, vital_status_counts)
combined_counts <- combined_counts[,c("category","value", "n")]
combined_counts

# Define the function to merge all RNAseq quantification files into one datadrame
merge_rna <-function(metadata, fdir){
    filelist <- list.files(fdir, pattern="*.tsv$", 
                        recursive = TRUE, full.names=TRUE)
    for (i in 1:length(filelist)){
        iname <- basename(filelist[i])
        isamplename <- metadata[metadata$file_name==iname, "sample"]
        idf <- read.csv(filelist[i], sep="\t", skip=1, header=TRUE)
        # remove first 4 rows
        remove <- 1:4
        idf_subset <- idf[-remove, c("gene_id","unstranded")]
        rm(idf)
        names(idf_subset)[2] <- isamplename
        #print(dim(idf_subset))
        if (i==1){
            combined_df <- idf_subset
            rm(idf_subset)
        } else {
            combined_df <- merge(combined_df, idf_subset, by.x='gene_id', by.y="gene_id", all=TRUE)
            rm(idf_subset)
        }
    }
    # remove certain gene ids
    combined_df <- combined_df[!(grepl("PAR_Y", combined_df$gene_id, fixed=TRUE)),]
    # modify gene_id
    combined_df$gene_id <- sapply(strsplit(combined_df$gene_id,"\\."), `[`, 1)
    # use gene_id as row names and remove gene_id column
    rownames(combined_df) <- combined_df$gene_id
    combined_df <- combined_df[,-which(names(combined_df) %in% c("gene_id"))]
    return(combined_df)
}

rnaCounts <-  merge_rna(metaMatrix.RNA, "TCGA-CHOL_0406/RNAseq")
rnaCounts[1:5,]

dim(rnaCounts)


# Normalization of RNAseq data 
rnaExpr <- gdcVoomNormalization(counts = rnaCounts, filter = FALSE)



DEGAll_CHOL<- gdcDEAnalysis(counts = rnaCounts, 
                        group      = metaMatrix.RNA$sample_type, 
                        comparison = 'PrimaryTumor-SolidTissueNormal', 
                        method     = 'DESeq2',
                        filter=TRUE)

DEGAll_CHOL[1:5,]

gdcVolcanoPlot(DEGAll_CHOL)

