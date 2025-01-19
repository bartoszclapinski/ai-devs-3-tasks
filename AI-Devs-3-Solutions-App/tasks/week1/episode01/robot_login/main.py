import time
from models.robot import RobotLoginAutomation

def main():
    automation = RobotLoginAutomation()
    max_attempts = 5
    attempt = 0
    
    while attempt < max_attempts:
        print(f"\nPróba logowania {attempt + 1}/{max_attempts}")
        if automation.login():
            print("Logowanie zakończone sukcesem!")
            break
        else:
            print("Logowanie nie powiodło się, próbuję ponownie...")
            time.sleep(7)
        attempt += 1

if __name__ == "__main__":
    main() 