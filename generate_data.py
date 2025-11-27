import pandas as pd
import random
from faker import Faker

fake = Faker()

def create_fake_database():
    print("Generating synthetic bank data...")
    data = []
    
    for _ in range(50):
        # Generate generic profiles
        name = fake.name()
        income = random.randint(25000, 150000)
        debt = random.randint(0, 40000)
        credit_score = random.randint(300, 850)
        
        # Simple logic: High debt + Low Score = High Risk
        if credit_score < 580 or debt > (income * 0.6):
            risk_category = "High Risk"
        else:
            risk_category = "Low Risk"
            
        data.append([name, income, debt, credit_score, risk_category])

    # Save to CSV
    df = pd.DataFrame(data, columns=['Name', 'Income', 'Debt', 'Credit_Score', 'Historical_Risk'])
    df.to_csv("customer_database.csv", index=False)
    print("✅ Success! 'customer_database.csv' created.")

if __name__ == "__main__":
    create_fake_database()