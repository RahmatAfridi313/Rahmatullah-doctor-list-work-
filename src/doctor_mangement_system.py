import json
import os #used to access operating system to check if json file exist or not

#optional used to indicate whether the funtion will return dictionary or none
#here list is used to show list to acsess the list of objects like list[dict] list of dictionaries
from typing import List, Optional

# Doctor class
class Doctor:
    def __init__(self, doctor_id: int, name: str, specialization: str, email: str, contact: str):
        """initializer for doctors info(data)"""
        self.id = doctor_id
        self.name = name
        self.specialization = specialization
        self.email = email
        self.contact = contact

    def to_dict(self):
        """"returns doctors data in the form of dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "specialization": self.specialization,
            "email": self.email,
            "contact": self.contact
        }

# Doctor Database
class DoctorDatabase:
    FILE = "doctors.json"

    def __init__(self):
        #"os.path" is an advanced method that check the existance of file in real time
        # through operating system
        #"exist" is used as a flag to show/indicate whether a file exists or not
        if not os.path.exists(self.FILE):
            with open(self.FILE, "w") as f:
                json.dump({"last_id": 0, "doctors": []}, f, indent=4)
        self.data = self._load()

    def _load(self):
        """loads the json file and the data in it, if exists otherwise throws error"""
        try:
            with open(self.FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"last_id": 0, "doctors": []}

    def _save(self):
        """saves the doctor's data to json file"""
        with open(self.FILE, "w") as f:
            #dump funtion writes data to our json file
            json.dump(self.data, f, indent=4)

    def generate_id(self):
        """Generates a unique id for a doctor that is added"""
        #As by default in above the id starts from 0 so we += 1 to start from 1
        self.data["last_id"] += 1
        self._save()
        return self.data["last_id"]

    # Add new doctor with email and contact
    def add_doctor(self, name: str, specialization: str, email: str, contact: str):
        #"any" used as flag returns true if the condition in box is true
        if any(d["name"].lower() == name.lower() for d in self.data["doctors"]):
            return False, "Doctor name already exists!"
        
        #if doctor info not exist, it takes info through "Doctor" class and saves it in json file
        doctor_id = self.generate_id()
        new_doctor = Doctor(doctor_id, name, specialization, email, contact).to_dict()
        self.data["doctors"].append(new_doctor)
        self._save()
        return True, "Doctor added successfully!"

    # List doctors with optional sorting
    def get_all_doctors(self, sort_by: str = "id") -> List[dict]:
    #"list[dict]" returns the list of dictionaries where doctors data is stored
        valid_keys = ["id", "name", "specialization"]
        if sort_by not in valid_keys:
            sort_by = "id"
        return sorted(
            self.data["doctors"],
            #here lambda holds the sort choice and isinstance defines both "name" and "specialization as strings"
            #if choice is something different then it sort is by "ID" which is default sorting choice 
            key=lambda x: x[sort_by].lower() if isinstance(x[sort_by], str) else x[sort_by]
        )

    # Search doctors by name or specialization
    def search_doctors(self, keyword: str) -> List[dict]:
        """search specific doctor on the basis of 'name' or 'specialization'"""
        keyword = keyword.lower()
        return [
            d for d in self.data["doctors"]
            if keyword in d["name"].lower() or keyword in d["specialization"].lower()
        ]

    # Get doctor by ID
    def get_doctor_by_id(self, doctor_id: int) -> Optional[dict]:
        return next((d for d in self.data["doctors"] if d["id"] == doctor_id), None)

    # Update doctor specialization, email, and contact
    def update_doctor(self, doctor_id: int, specialization: str = None, email: str = None, contact: str = None):
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor:
            if specialization:
                doctor["specialization"] = specialization
            if email:
                doctor["email"] = email
            if contact:
                doctor["contact"] = contact
            self._save()
            return True, "Doctor updated successfully!"
        return False, "Doctor not found."

    # Delete doctor
    def delete_doctor(self, doctor_id: int):
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor:
            self.data["doctors"].remove(doctor)
            self._save()
            return True, "Doctor deleted successfully!"
        return False, "Doctor not found."

#Doctor System 
#uses the functions of the "DoctorDatabase" class and make all fuctions like add, update etc
#that is required in a doctor class
class DoctorSystem:
    def __init__(self):
        self.db = DoctorDatabase()

    def menu(self):
        while True:
            print("\n=========== REAL-TIME DOCTOR MANAGEMENT ===========")
            print("1. Add Doctor")
            print("2. Show Doctors")
            print("3. Search Doctors")
            print("4. Update Doctor")
            print("5. Delete Doctor")
            print("6. Exit")
            print("===================================================")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.add()
            elif choice == "2":
                self.show()
            elif choice == "3":
                self.search()
            elif choice == "4":
                self.update()
            elif choice == "5":
                self.delete()
            elif choice == "6":
                print("Exiting system...")
                break
            else:
                print("Invalid choice!")

    def add(self):
        name = input("Enter doctor name: ").strip()
        specialization = input("Enter specialization: ").strip()
        email = input("Enter email: ").strip()
        contact = input("Enter contact number: ").strip()

        if not name or not specialization or not email or not contact:
            print("All fields are required!")
            return

        status, msg = self.db.add_doctor(name, specialization, email, contact)
        print(msg)

    def show(self):
        sort_choice = input("Sort doctors by (id/name/specialization) [default id]: ").strip().lower()
        doctors = self.db.get_all_doctors(sort_by=sort_choice)
        #if doctor is not present, it shows "No doctors found."
        if not doctors:
            print("No doctors found.")
            return

        print("\n----- Doctor List -----")
        print(f"{'ID':<5} {'Name':<20} {'Specialization':<20} {'Email':<30} {'Contact':<15}")
        print("-" * 95)
        for d in doctors:
            print(f"{d['id']:<5} {d['name']:<20} {d['specialization']:<20} {d['email']:<30} {d['contact']:<15}")
        print("-" * 95)

    def search(self):
        keyword = input("Enter name or specialization to search: ").strip()
        results = self.db.search_doctors(keyword)
        if not results:
            print("No doctors found matching your search.")
            return

        print("\n----- Search Results -----")
        print(f"{'ID':<5} {'Name':<20} {'Specialization':<20} {'Email':<30} {'Contact':<15}")
        print("-" * 95)
        for d in results:
            print(f"{d['id']:<5} {d['name']:<20} {d['specialization']:<20} {d['email']:<30} {d['contact']:<15}")
        print("-" * 95)

    def update(self):
        try:
            doctor_id = int(input("Enter doctor ID to update: "))
        except ValueError:
            print("Invalid ID!")
            return

        specialization = input("Enter new specialization (leave blank to keep current): ").strip()
        email = input("Enter new email (leave blank to keep current): ").strip()
        contact = input("Enter new contact (leave blank to keep current): ").strip()

        status, msg = self.db.update_doctor(
            doctor_id,
            specialization if specialization else None,
            email if email else None,
            contact if contact else None
        )
        print(msg)

    def delete(self):
        try:
            doctor_id = int(input("Enter doctor ID to delete: "))
        except ValueError:
            print("Invalid ID!")
            return

        confirm = input("Are you sure you want to delete this doctor? (y/n): ").lower()
        if confirm != "y":
            print("Deletion cancelled.")
            return

        status, msg = self.db.delete_doctor(doctor_id)
        print(msg)

#Program Start
if __name__ == "__main__":
    DoctorSystem().menu()
