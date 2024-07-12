"""
Author: Chukwunazaekpere Emmanuel Obioma
Written for: DSS Project
Nationality: Biafran
Email-1: chukwunazaekpere.obioma@ue-germany.de 
Email-2: ceo.naza.tech@gmail.com
************************************************
Course: Software Optimisation
Written: July 12th 2024
Due: July 13th 2024
========================== Major Problem ==========================

"""

from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)
log_date = datetime.now()
logging.basicConfig(level=logging.INFO)

class ResourceAllocator():
    def __init__(self, project_category, estimated_budget=100000, number_of_developers=3):
        self.project_category = project_category
        self.estimated_budget = estimated_budget
        self.number_of_developers = number_of_developers
        self.cleaned_content = {}
        self.start_time = datetime.now()
        self.gathered_data_file = "./files/gathered_data.json" 

    def _file_helper(self, file_name:str, file_mode:str, content=""):
        """Read file containing message to be encrypted or decrypted"""
        if file_mode == "r":
            with open(file_name, "r")as file_content:
                content = file_content.read()
            return content
        elif file_mode == "rl":
            with open(file_name, "r")as file_content:
                file_content_list = file_content.readlines()
            return file_content_list
        elif file_mode == "w":
            with open(file_name, "w")as file_handle:
                file_handle.write(str(content))
        else:
            with open(file_name, "+a")as file_handle:
                file_handle.write(str(content))
    
    def _generate_cleaned_data(self, file_content):
        for data in file_content:
            try:
                # print("\n\t self.cleaned_content[data['category']]: ", self.cleaned_content[data['category']])
                # complexity = self.cleaned_content[data['category']]['complexity'] 
                complexity_upper = self.cleaned_content[data['category']]['complexity_upper'] 
                duration_lower = self.cleaned_content[data['category']]['duration_lower'] 
                duration_upper = self.cleaned_content[data['category']]['duration_upper'] 
                number_of_developers_lower = self.cleaned_content[data['category']]['number_of_developers_lower'] 
                number_of_developers_upper = self.cleaned_content[data['category']]['number_of_developers_upper'] 
                estimated_budget_lower = self.cleaned_content[data['category']]['estimated_budget_lower'] 
                estimated_budget_upper = self.cleaned_content[data['category']]['estimated_budget_upper'] 

                if duration_lower > int(data['duration_lower']):
                    self.cleaned_content[data["category"]]["duration_lower"] = int(data['duration_lower'])
                if duration_upper < int(data['duration_upper']):
                    self.cleaned_content[data["category"]]["duration_upper"] = int(data['duration_upper'])
                if number_of_developers_lower > int(data['number_of_developers_lower']):
                    self.cleaned_content[data["category"]]["number_of_developers_lower"] = int(data['number_of_developers_lower'])
                if number_of_developers_upper < int(data['number_of_developers_upper']):
                    self.cleaned_content[data["category"]]["number_of_developers_upper"] = int(data['number_of_developers_upper'])
                if estimated_budget_lower > int(data['estimated_budget_lower']):
                    self.cleaned_content[data["category"]]["estimated_budget_lower"] = int(data['estimated_budget_lower'])
                if estimated_budget_upper < int(data['estimated_budget_upper']):
                    self.cleaned_content[data["category"]]["estimated_budget_upper"] = int(data['estimated_budget_upper'])
                if int(data['complexity']) > complexity_upper:
                    self.cleaned_content[data["category"]]["complexity_upper"] = data['complexity']
            except Exception as err:
                # print("\n\t err: ", err)
                self.cleaned_content[data['category']] = {
                    "complexity": int(data["complexity"]),  
                    "duration_lower": int(data["duration_lower"]), 
                    "duration_upper": int(data["duration_upper"]), 
                    "number_of_developers_lower": int(data["number_of_developers_lower"]), 
                    "number_of_developers_upper": int(data["number_of_developers_upper"]), 
                    "estimated_budget_lower": int(data["estimated_budget_lower"]), 
                    "estimated_budget_upper": int(data["estimated_budget_upper"]), 
                    "complexity_upper": 1, # least complexity is 1
                }
                # print("\n\t self.cleaned_content: ", self.cleaned_content)

    def allocate_resource(self):
        try:
            result_path = "./files/allocation-result.txt"
            logging.info(msg=f"\n\t  {self.start_time.ctime()} Please wait, Resource Allocator is computing your request...")
            gathered_data_content = self._file_helper(self.gathered_data_file, "r")
            self._generate_cleaned_data(file_content=json.loads(gathered_data_content))
            project_category_details = self.cleaned_content[self.project_category]
            estimate_budg = self.budget_estimator(project_category_details)
            self._file_helper(file_mode="w", file_name=result_path, content="")
            self._file_helper(file_mode="w", file_name=result_path, content=estimate_budg)
            logging.info(msg=f"\n\t  {self.start_time.ctime()} {estimate_budg}")
            return estimate_budg
        except Exception as err:
            logging.info(msg=f"\n\t  {self.start_time.ctime()} {err}")


    def estimate_developer_size(self, estimated_budget, project_category_details):
        number_of_developers_lower = project_category_details["number_of_developers_lower"]
        estimated_budget_lower = project_category_details["estimated_budget_lower"]
        duration_lower = project_category_details["duration_lower"]
        duration_upper = project_category_details["duration_upper"]
        dev_size = ""
        duration = f"Estimated duration: {duration_lower} to {duration_lower+1}"
        logging.info(msg=f"\n\t {self.start_time.ctime()} Estimating project duration...")
        if number_of_developers_lower < number_of_developers_lower:
            dev_size = f"Developer size of {number_of_developers_lower} is unrealistic."
            duration = "Unrealistic range"
        elif estimated_budget >= estimated_budget_lower and estimated_budget <= (estimated_budget_lower*1.5):
            dev_size = f"Recommended developer size: {number_of_developers_lower} to {number_of_developers_lower+1}"
        elif estimated_budget >= estimated_budget_lower*1.5 and estimated_budget <= (estimated_budget_lower*3):
            dev_size = f"Recommended developer size: {number_of_developers_lower} to {number_of_developers_lower+2}"
        elif estimated_budget >= estimated_budget_lower*3.5 and estimated_budget <= (estimated_budget_lower*4):
            duration = f"Estimated duration: {duration_lower} to {duration_upper-1}"
            dev_size = f"Recommended developer size: {number_of_developers_lower} to {number_of_developers_lower+3}"
        elif estimated_budget >= estimated_budget_lower*4 and estimated_budget <= (estimated_budget_lower*4.5):
            duration = f"Estimated duration: {duration_lower} to {duration_upper-2}"
            dev_size = f"Recommended developer size: {number_of_developers_lower} to {number_of_developers_lower+4}"
        else:
            duration = f"Estimated duration: {duration_lower} to {duration_upper if duration_upper-4 <= duration_lower else duration_upper-4}"
            dev_size = f"Recommended developer size: {number_of_developers_lower} to {number_of_developers_lower+5}"
        return dev_size, duration

    def budget_estimator(self, project_category_details):
        # print("\n\t self.cleaned_content", self.cleaned_content)
        estimated_budget_lower = project_category_details["estimated_budget_lower"]
        complexity_upper = project_category_details["complexity_upper"]
        complexity = project_category_details["complexity"]
        if self.estimated_budget < estimated_budget_lower:
            return f"Your estimated budget of {self.estimated_budget} is less than the minimum budget of {estimated_budget_lower} for any {self.project_category} project"
        logging.info(msg=f"\n\t  {self.start_time.ctime()} Estimating developer size...")
        (dev_size, duration) = self.estimate_developer_size(estimated_budget=self.estimated_budget, project_category_details=project_category_details)
        logging.info(msg=f"\n\t  {self.start_time.ctime()} Estimating project complexity...")
        est_complexity = self.complexity(complexity, complexity_upper)
        return dev_size, duration, est_complexity

    def complexity(self, complexity, complexity_upper):
        comp_lower = complexity
        comp_higher = complexity_upper
        if complexity_upper < complexity:
            comp_lower = complexity_upper
            comp_higher = complexity
        return f"Expected complexity: {comp_lower} to {comp_higher}"
        


number_of_developers = 3
estimated_budget=180000
project_category="E-commerce"

RAL = ResourceAllocator(project_category, estimated_budget, number_of_developers)
RAL.allocate_resource()

# ('Recommended developer size: 2 to 5', 'Estimated duration: 2 to 12', 'Expected complexity: 13 to 18')