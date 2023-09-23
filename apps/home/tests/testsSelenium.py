from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from ..tasks import analisis
from ..models import StudyCase
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# class SeleniumTest(StaticLiveServerTestCase):

#     def setUp(self):
#         super().setUp()
#         self.StudyCase1 = StudyCase(project="TCGA-CHOL", data_type="RNAseq", state="DONE")
#         self.StudyCase1.save()
#         self.StudyCase2 = StudyCase(project="TCGA-CHOL", data_type="miRNAs")
#         self.StudyCase2.save()
#         options = webdriver.FirefoxOptions()
#         options.headless = False  
#         driver = webdriver.Firefox(options=options)
#         self.driver = driver

#     def tearDown(self):
#         super().tearDown()
#         self.StudyCase1 = None
#         self.StudyCase2 = None
#         self.driver.quit()
    
#     def test_init(self):
#         self.driver.get(f'{self.live_server_url}/')
#         self.assertTrue(self.driver.find_element('id', 'id_projects'))

#     def test_navbar(self):
#         self.driver.get(f'{self.live_server_url}/')
#         self.driver.set_window_size(550, 692)
#         self.driver.find_element(By.CSS_SELECTOR, ".navbar-toggler-icon").click()
#         self.driver.find_element(By.LINK_TEXT, "Analyze").click()
#         self.assertEqual(self.driver.current_url, f'{self.live_server_url}/')
#         self.driver.find_element(By.CSS_SELECTOR, ".navbar-toggler-icon").click()
#         self.driver.find_element(By.LINK_TEXT, "Analyzed Projects").click()
#         self.assertEqual(self.driver.current_url, f'{self.live_server_url}/analyzedProjects')
#         self.driver.find_element(By.CSS_SELECTOR, ".navbar-toggler-icon").click()
#         self.driver.find_element(By.LINK_TEXT, "API").click()
#         self.assertEqual(self.driver.current_url, f'{self.live_server_url}/aboutApi')
#         self.driver.find_element(By.CSS_SELECTOR, ".navbar-toggler-icon").click()
#         self.driver.find_element(By.LINK_TEXT, "Web Information").click()
#         self.assertEqual(self.driver.current_url, f'{self.live_server_url}/webInfo')
#         self.driver.close()

#     def test_filter_analyzed_projects(self):
#         self.driver.get(f'{self.live_server_url}/')
#         self.driver.set_window_size(720, 700)
#         self.driver.find_element(By.CSS_SELECTOR, ".navbar-toggler-icon").click()
#         self.driver.find_element(By.LINK_TEXT, "Analyzed Projects").click()
#         self.driver.find_element(By.ID, "project-select").click()
#         dropdown = self.driver.find_element(By.ID, "project-select")
#         dropdown.find_element(By.XPATH, "//option[. = 'TCGA-CHOL']").click()
#         self.driver.find_element(By.CSS_SELECTOR, "#project-select > option:nth-child(2)").click()
#         self.driver.find_element(By.CSS_SELECTOR, ".btn-block").click()

#         self.assertTrue(len(self.driver.find_elements(By.CLASS_NAME, "card-body")), 2)

#         self.driver.find_element(By.ID, "datatype-select").click()
#         dropdown = self.driver.find_element(By.ID, "datatype-select")
#         dropdown.find_element(By.XPATH, "//option[. = 'RNAseq']").click()
#         self.driver.find_element(By.CSS_SELECTOR, "#datatype-select > option:nth-child(2)").click()
#         self.driver.find_element(By.CSS_SELECTOR, ".btn-block").click()

#         self.assertTrue(len(self.driver.find_elements(By.CLASS_NAME, "card-body")), 1)

#         self.driver.find_element(By.ID, "datatype-select").click()
#         dropdown = self.driver.find_element(By.ID, "datatype-select")
#         dropdown.find_element(By.XPATH, "//option[. = 'miRNAs']").click()
#         self.driver.find_element(By.CSS_SELECTOR, "option:nth-child(3)").click()
#         self.driver.find_element(By.CSS_SELECTOR, ".btn-block").click()
#         self.driver.find_element(By.ID, "datatype-select").click()
#         self.driver.find_element(By.CSS_SELECTOR, "#datatype-select > option:nth-child(1)").click()
#         self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

#         self.assertTrue(len(self.driver.find_elements(By.CLASS_NAME, "card-body")), 2)

#         self.driver.find_element(By.CSS_SELECTOR, "html").click()
#         self.driver.close()

#     def test_analyze_inanalisisproject(self):
#         self.driver.get(f'{self.live_server_url}/')
#         self.driver.set_window_size(720, 700)
#         self.driver.find_element(By.ID, "id_data_type").click()
#         dropdown = self.driver.find_element(By.ID, "id_data_type")
#         dropdown.find_element(By.XPATH, "//option[. = 'miRNAs']").click()
#         self.driver.find_element(By.CSS_SELECTOR, "#id_data_type > option:nth-child(2)").click()
#         self.driver.find_element(By.ID, "select2-id_projects-container").click()
#         self.driver.find_element(By.CSS_SELECTOR, ".select2-search__field").click()
#         self.driver.find_element(By.CSS_SELECTOR, ".select2-search__field").send_keys("tcga-chol")
#         self.driver.find_element(By.CSS_SELECTOR, ".select2-search__field").send_keys(Keys.ENTER)

#         self.driver.find_element(By.ID, "btnAnalyze").click()
#         self.assertEqual(self.driver.current_url, f'{self.live_server_url}/analyzedProjects?project=TCGA-CHOL&data_type=miRNAs')

#     def test_api_tryouts(self):
#         self.driver.get(f'{self.live_server_url}/aboutApi')
#         self.driver.find_element(By.LINK_TEXT, "SWAGGER").click()
#         self.assertEqual(self.driver.current_url, f'{self.live_server_url}/swagger/')
#         self.driver.get(f'{self.live_server_url}/aboutApi')
#         self.driver.find_element(By.LINK_TEXT, "REDOC").click()
#         self.assertEqual(self.driver.current_url, f'{self.live_server_url}/redoc/')

#     def test_nav_results(self):
#         self.driver.get(f'{self.live_server_url}/results/'+str(self.StudyCase1.id)+'/metadata')
#         sleep(2)
#         color1 = self.driver.find_element(By.ID, "btn-metadata").value_of_css_property('background-color')
#         color2 = self.driver.find_element(By.ID, "btn-diffExpr").value_of_css_property('background-color')
#         self.assertEqual(self.driver.current_url, f'{self.live_server_url}/results/'+str(self.StudyCase1.id)+'/metadata')
#         self.assertEqual(color1, 'rgb(82, 53, 92)')
#         self.assertNotEqual(color2, 'rgb(82, 53, 92)')

#         self.driver.find_element(By.ID, "btn-diffExpr").click()
#         sleep(2)
#         color1 = self.driver.find_element(By.ID, "btn-diffExpr").value_of_css_property('background-color')
#         color2 = self.driver.find_element(By.ID, "btn-enrich").value_of_css_property('background-color')
#         self.assertEqual(self.driver.current_url, f'{self.live_server_url}/results/'+str(self.StudyCase1.id)+'/diffExpr')
#         self.assertEqual(color1, 'rgb(82, 53, 92)')
#         self.assertNotEqual(color2, 'rgb(82, 53, 92)')

#         self.driver.find_element(By.ID, "btn-enrich").click()
#         sleep(2)
#         color1 = self.driver.find_element(By.ID, "btn-enrich").value_of_css_property('background-color')
#         color2 = self.driver.find_element(By.ID, "btn-survival").value_of_css_property('background-color')
#         self.assertEqual(self.driver.current_url, f'{self.live_server_url}/results/'+str(self.StudyCase1.id)+'/enrichment')
#         self.assertEqual(color1, 'rgb(82, 53, 92)')
#         self.assertNotEqual(color2, 'rgb(82, 53, 92)')

#         self.driver.find_element(By.ID, "btn-survival").click()
#         sleep(2)
#         color1 = self.driver.find_element(By.ID, "btn-survival").value_of_css_property('background-color')
#         color2 = self.driver.find_element(By.ID, "btn-metadata").value_of_css_property('background-color')
#         self.assertEqual(self.driver.current_url, f'{self.live_server_url}/results/'+str(self.StudyCase1.id)+'/survivalAnalysis')
#         self.assertEqual(color1, 'rgb(82, 53, 92)')
#         self.assertNotEqual(color2, 'rgb(82, 53, 92)')

class SeleniumTestWithAnalisis(StaticLiveServerTestCase):

    def setUp(self):
        super().setUp()
        self.StudyCase1 = StudyCase(project="TCGA-CHOL", data_type="RNAseq")
        self.StudyCase1.save()
        options = webdriver.FirefoxOptions()
        options.headless = False  
        driver = webdriver.Firefox(options=options)
        self.driver = driver

    def tearDown(self):
        super().tearDown()
        self.StudyCase1 = None
        self.StudyCase2 = None
        self.driver.quit()

    def test_results(self):
        analisis(self.StudyCase1.project, self.StudyCase1.data_type, self.StudyCase1.id)
        self.driver.set_window_size(1080, 1600)

        ####################### Results metadata #############################
        
        self.driver.get(f'{self.live_server_url}/results/'+str(self.StudyCase1.id)+'/metadata')

        sleep(3.0) # wait for load scripts

        tabla = self.driver.find_element(By.ID, 'metadataDatatable')
        td_elements = tabla.find_elements(By.CSS_SELECTOR, 'tr')
        self.assertEqual(len(td_elements), 11) # 10 + header

        btn = self.driver.find_element(By.ID, "headingTwo").find_element(By.CSS_SELECTOR, "button")
        self.driver.execute_script("arguments[0].click();",btn)

        sleep(2) # wait for animation

        gender_card = self.driver.find_element(By.ID, "genderCard")
        gender_header = gender_card.find_element(By.CLASS_NAME, "card-title")
        gender_body = gender_card.find_element(By.CLASS_NAME, "card-body")

        self.assertEqual(gender_header.text, "Gender Counts")
        self.assertTrue("male: 22" in gender_body.text)
        self.assertTrue("female: 22" in gender_body.text)

        sample_type_card = self.driver.find_element(By.ID,'sampleTypeCard')
        sample_type_header = sample_type_card.find_element(By.CLASS_NAME,'card-title')
        sample_type_body = sample_type_card.find_element(By.CLASS_NAME,'card-body')

        self.assertEqual(sample_type_header.text, "Sample Type Counts")
        self.assertTrue("PrimaryTumor: 35" in sample_type_body.text)
        self.assertTrue("SolidTissueNormal: 9" in sample_type_body.text)

        vital_status_card = self.driver.find_element(By.ID,'vitalStatusCard')
        vital_status_header = vital_status_card.find_element(By.CLASS_NAME,'card-title')
        vital_status_body = vital_status_card.find_element(By.CLASS_NAME,'card-body')
        
        self.assertEqual(vital_status_header.text, "Vital Status Counts")
        self.assertTrue("Dead: 23" in vital_status_body.text)
        self.assertTrue("Alive: 21" in vital_status_body.text)

        age_at_diagnosis_card = self.driver.find_element(By.ID,'age_at_diagnosis_div')
        age_at_diagnosis_header = age_at_diagnosis_card.find_element(By.CLASS_NAME,'card-title')
        age_at_diagnosis_body = age_at_diagnosis_card.find_element(By.CLASS_NAME,'card-body')
        
        self.assertEqual(age_at_diagnosis_header.text, "Field: age_at_diagnosis")
        self.assertTrue("Min: 10659" in age_at_diagnosis_body.text)
        self.assertTrue("Max: 30039" in age_at_diagnosis_body.text)

        ###################### Results diffExpr #############################

        self.driver.get(f'{self.live_server_url}/results/'+str(self.StudyCase1.id)+'/diffExpr')
        sleep(6.0) # wait for load scripts

        tabla = self.driver.find_element(By.ID, 'diffExprDatatable')
        td_elements = tabla.find_elements(By.CSS_SELECTOR, 'tr')
        self.assertEqual(len(td_elements), 11) # 10 + header

        btn = self.driver.find_element(By.ID, "headingTwo").find_element(By.CSS_SELECTOR, "button")
        self.driver.execute_script("arguments[0].click();",btn)
        sleep(2)

        self.driver.execute_script("window.scrollBy(0, 500);")

        self.assertIsNotNone(self.driver.find_element(By.ID, "volcanoPlot").find_element(By.CLASS_NAME, "plot-container"))
        self.assertEqual(self.driver.find_element(By.ID, "popupVolcanoPlot").value_of_css_property('display'), 'none')
        self.driver.find_element(By.ID, "btnConfigureVolcanoPlot").click()
        self.assertEqual(self.driver.find_element(By.ID, "popupVolcanoPlot").value_of_css_property('display'), 'block')
        self.driver.find_element(By.ID, "closePopupVolcanoPlot").click()


        btn = self.driver.find_element(By.ID, "headingThree").find_element(By.CSS_SELECTOR, "button")
        self.driver.execute_script("arguments[0].click();", btn)
        sleep(2)
        self.driver.execute_script("window.scrollBy(0, 500);")

        self.assertIsNotNone(self.driver.find_element(By.ID, "bar-chart").find_element(By.CLASS_NAME, "plot-container"))

        btn = self.driver.find_element(By.ID, "headingFour").find_element(By.CSS_SELECTOR, "button")
        self.driver.execute_script("arguments[0].click();", btn)
        sleep(2)
        self.driver.execute_script("window.scrollBy(0, 500);")

        self.assertIsNotNone(self.driver.find_element(By.ID, "corr-plot").find_element(By.CLASS_NAME, "plot-container"))
        self.assertEqual(self.driver.find_element(By.ID, "corrPlotError").value_of_css_property('display'), 'none')
        
        self.assertEqual(self.driver.find_element(By.ID, "popupCorrPlot").value_of_css_property('display'), 'none')
        self.driver.find_element(By.ID, "btnConfigureCorrPlot").click()
        self.assertEqual(self.driver.find_element(By.ID, "popupCorrPlot").value_of_css_property('display'), 'block')
        self.driver.find_element(By.ID, "autocompleteInputGene1").click()
        self.driver.find_element(By.ID, "autocompleteInputGene1").send_keys("ENSG00000105")
        self.driver.find_element(By.ID, "btnCorrPlot").click()
        self.assertEqual(self.driver.find_element(By.ID, "corrPlotError").value_of_css_property('display'), 'none')

        ##################### Results Enrichment #############################

        self.driver.get(f'{self.live_server_url}/results/'+str(self.StudyCase1.id)+'/enrichment')
        sleep(6.0) # wait for load scripts

        tabla = self.driver.find_element(By.ID, 'diffExprDatatable')
        td_elements = tabla.find_elements(By.CSS_SELECTOR, 'tr')
        self.assertEqual(len(td_elements), 11) # 10 + header

        btn = self.driver.find_element(By.ID, "headingTwo").find_element(By.CSS_SELECTOR, "button")
        self.driver.execute_script("arguments[0].click();",btn)
        sleep(2)

        self.driver.execute_script("window.scrollBy(0, 500);")

        self.assertIsNotNone(self.driver.find_element(By.ID, "bar-plot").find_element(By.CLASS_NAME, "plot-container"))
        self.assertEqual(self.driver.find_element(By.ID, "popupBarPlot").value_of_css_property('display'), 'none')
        self.driver.find_element(By.ID, "btnConfigureBarPlot").click()
        self.assertEqual(self.driver.find_element(By.ID, "popupBarPlot").value_of_css_property('display'), 'block')
        self.driver.find_element(By.ID, "closePopupBarPlot").click()

        ######################### Resuslts Survival ##########################

        self.driver.get(f'{self.live_server_url}/results/'+str(self.StudyCase1.id)+'/survivalAnalysis')
        sleep(6.0)

        tabla = self.driver.find_element(By.ID, 'diffExprDatatable')
        td_elements = tabla.find_elements(By.CSS_SELECTOR, 'tr')
        self.assertEqual(len(td_elements), 11) # 10 + header

        btn = self.driver.find_element(By.ID, "headingTwo").find_element(By.CSS_SELECTOR, "button")
        self.driver.execute_script("arguments[0].click();",btn)
        sleep(2)

        self.driver.execute_script("window.scrollBy(0, 500);")

        self.assertIsNotNone(self.driver.find_element(By.ID, "km-plot").find_element(By.CLASS_NAME, "plot-container"))
        self.assertEqual(self.driver.find_element(By.ID, "popupSurvivalPlot").value_of_css_property('display'), 'none')
        self.driver.find_element(By.ID, "btnConfigureSurvivalPlot").click()
        self.assertEqual(self.driver.find_element(By.ID, "popupSurvivalPlot").value_of_css_property('display'), 'block')
        self.driver.find_element(By.ID, "closePopupSurvivalPlot").click()
















    





