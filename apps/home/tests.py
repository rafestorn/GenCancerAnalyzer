from django.test import TestCase
from .models import StudyCase, MetaData, DiffExprAnalysisData, EnrichData, RNAExpresion
from rest_framework.test import APIClient
from datetime import datetime

# Create your tests here.

class APITestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.StudyCase1 = StudyCase(title="Test StudyCase", description="Test StudyCase description", project="TCGA-CHOL", data_type="RNAseq")
        self.StudyCase2 = StudyCase(title="Test StudyCase 2", description="Test StudyCase description 2", project="TCGA-CHOL", data_type="miRNAseq")
        self.StudyCase3 = StudyCase(title="Test StudyCase 3", description="Test StudyCase description 3", project="TCGA-HNSC", data_type="RNAseq")

        self.StudyCase1.save()
        self.StudyCase2.save()
        self.StudyCase3.save()

        self.metadata1 = MetaData(
            studyCase=self.StudyCase1,
            creation_date=datetime.now(),
            case_id='CASE001',
            file_name='sample_file_001.txt',
            file_id='file_id_001',
            patient='John Doe',
            sample='Sample A',
            submitter_id='submitter001',
            entity_submitter_id='entity001',
            sample_type='Tissue',
            gender='Male',
            age_at_diagnosis=45,
            tumor_stage='Stage II',
            tumor_grade='Grade 3',
            days_to_death=None,
            days_to_last_follow_up=365,
            vital_status='Alive',
            project_id='project001'
        )

        self.metadata2 = MetaData(
            studyCase=self.StudyCase1,
            creation_date=datetime.now(),
            case_id='CASE002',
            file_name='sample_file_002.txt',
            file_id='file_id_002',
            patient='Jane Smith',
            sample='Sample B',
            submitter_id='submitter002',
            entity_submitter_id='entity002',
            sample_type='Blood',
            gender='Female',
            age_at_diagnosis=50,
            tumor_stage='Stage III',
            tumor_grade='Grade 2',
            days_to_death=120,
            days_to_last_follow_up=None,
            vital_status='Deceased',
            project_id='project002'
        )

        self.diffExpr1 = DiffExprAnalysisData(
            studyCase=self.StudyCase1,
            creation_date=datetime.now(),
            gene_id='gene001',
            symbol='GENE001',
            group='Group A',
            baseMean=100.0,
            logFC=1.0,
            lfcSE=0.5,
            stat=2.0,
            PValue=0.05,
            FDR=0.1
        )
        
        self.diffExpr2 = DiffExprAnalysisData(
            studyCase=self.StudyCase1,
            creation_date=datetime.now(),
            gene_id='gene002',
            symbol='GENE002',
            group='Group B',
            baseMean=90.0,
            logFC=2.0,
            lfcSE=1.5,
            stat=3.0,
            PValue=1.05,
            FDR=0.2
        )

        self.enrich1 = EnrichData(
            studyCase=self.StudyCase1,
            creation_date=datetime.now(),
            terms='Term 1',
            counts=10,
            gene_ratio='10/100',
            bg_ratio='10/100',
            p_value=0.05,
            fdr=0.1,
            fold_enrichment=1.0,
            gene_ids='gene001/gene002',
            gene_symbols='GENE001/GENE002',
            category='Category 1'
        )

        self.enrich2 = EnrichData(
            studyCase=self.StudyCase1,
            creation_date=datetime.now(),
            terms='Term 2',
            counts=20,
            gene_ratio='20/100',
            bg_ratio='20/100',
            p_value=0.1,
            fdr=0.2,
            fold_enrichment=2.0,
            gene_ids='gene003/gene004',
            gene_symbols='GENE003/GENE004',
            category='Category 2'
        )

        self.rnaExpr1 = RNAExpresion(
            studyCase=self.StudyCase1,
            gene_id='gene001',
            data = {
                'sample1': 100.0,
                'sample2': 200.0,
                'sample3': 300.0
            }
        )

        self.rnaExpr2 = RNAExpresion(
            studyCase=self.StudyCase1,
            gene_id='gene002',
            data = {
                'sample1': 200.0,
                'sample2': 300.0,
                'sample3': 100.0
            }
        )

        self.diffExpr1.save()
        self.diffExpr2.save()

        self.metadata1.save()
        self.metadata2.save()

        self.enrich1.save()
        self.enrich2.save()

        self.rnaExpr1.save()
        self.rnaExpr2.save()

        self.client = APIClient()
    
    def tearDown(self):
        super().tearDown()
        self.StudyCase1 = None
        self.StudyCase2 = None
        self.StudyCase3 = None
        self.metadata1 = None
        self.metadata2 = None
        self.diffExpr1 = None
        self.diffExpr2 = None
        self.enrich1 = None
        self.enrich2 = None
        self.rnaExpr1 = None
        self.rnaExpr2 = None
        self.client = None

    def test_studycase_api(self):
        response = self.client.get('/api/studyCase')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['page'], 1)
        self.assertEqual(response.data['items_in_page'], 3)
        self.assertEqual(response.data['total_items'], 3)
        self.assertEqual(response.data['total_pages'], 1)

        response = self.client.get('/api/studyCase?project=TCGA-CHOL')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

        response = self.client.get('/api/studyCase?project=TCGA-CHOL&data_type=RNAseq')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

        response = self.client.get('/api/studyCase?project=TCGA-INVENT')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

    def test_studyCase_byId_api(self):
        response = self.client.get('/api/studyCase/'+str(self.StudyCase1.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.StudyCase1.id)

        response = self.client.get('/api/studyCase/0')
        self.assertEqual(response.status_code, 404)

    def test_metadata_api(self):
        response = self.client.get('/api/studyCase/'+ str(self.StudyCase1.id) +'/metadata')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

        response = self.client.get('/api/studyCase/4/metadata')
        self.assertEqual(response.status_code, 404)

    def test_diffExpr_api(self):
        response = self.client.get('/api/studyCase/'+ str(self.StudyCase1.id) +'/differentialExpression')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

        response = self.client.get('/api/studyCase/'+ str(self.StudyCase2.id) +'/differentialExpression')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/api/studyCase/'+ str(self.StudyCase1.id) +'/differentialExpression?group=Group A')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_enrichment_api(self):
        response = self.client.get('/api/studyCase/'+ str(self.StudyCase1.id) +'/enrichAnalysis')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

        response = self.client.get('/api/studyCase/'+ str(self.StudyCase2.id) +'/enrichAnalysis')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/api/studyCase/'+ str(self.StudyCase1.id) +'/enrichAnalysis?category=Category 1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

        response = self.client.get('/api/studyCase/'+ str(self.StudyCase1.id) +'/enrichAnalysis?orderBy=counts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['terms'], 'Term 1')
        self.assertEqual(response.data['results'][1]['terms'], 'Term 2')

    def test_rna_expr_api(self):
        response = self.client.get('/api/studyCase/'+ str(self.StudyCase1.id) +'/rnaExpression')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

        response = self.client.get('/api/studyCase/'+ str(self.StudyCase2.id) +'/rnaExpression')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/api/studyCase/'+ str(self.StudyCase1.id) +'/rnaExpression?genes_ids=gene001')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['gene_id'], 'gene001')

        response = self.client.get('/api/studyCase/'+ str(self.StudyCase1.id) +'/rnaExpression?genes_ids=gene001,gene002')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)