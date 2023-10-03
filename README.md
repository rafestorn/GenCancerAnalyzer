# GenCancerAnalyzer
The application is the result of a Bachelor's Thesis (TFG) titled "Web Application for TCGA Data Analysis" made by the student Rafael Estrada Ornedo, which aims to conduct analyses on TCGA projects and present the results through visual plots.

The thesis is tutored by:
 - María del Mar Martínez Ballesteros
 - Manuel Jesús Jiménez Navarro (Co-supervisor)

How the Analysis is Performed:

GenCancerAnalyzer utilizes the "gdcRNATools" library, an R/Bioconductor package, to perform the majority of the analyses. Users can select the GDC project and the type of gene expression (RNA or miRNAs) to analyze.

Features:

 - Analyze Projects: By selecting the project and data type, get the project metadata and results from the differential expression analysis, enrichment analysis (Only for RNA type), and univariate survival analysis. You can also consult the results from analyses already made by other users.

 - Download Results: Download the analysis results in CSV or Excel file format.

 - Plots: Visualize the results as plots to gain a better understanding of the information.

 - Access the API: Discover the GenCancerAnalyzerAPI to access the stored data from the analysis.

Contact:

For any questions or suggestions, please contact:

 - Email: rafaestrada3@gmail.com
    
