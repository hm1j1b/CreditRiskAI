import pandas as pd
import random
from faker import Faker

fake = Faker()

# Lists of merchants for transaction simulation
safe_merchants = ['Uber', 'Tesco', 'Netflix', 'Spotify', 'Shell Station', 'Starbucks', 'Amazon']
risky_merchants = ['Bet365', 'PokerStars', 'CryptoBinance', 'LuxuryWatches', 'CasinoRoyal', 'Unknown Transfer']

def create_fake_database():
    print("Generating synthetic bank data...")
    data = []
    
    for _ in range(50):
        # Generate generic profiles
        name = fake.name()
        income = random.randint(25000, 150000)
        debt = random.randint(0, 40000)
        credit_score = random.randint(300, 850)
        transactions = random.choices(safe_merchants, k=5)
        
        # Simple logic: High debt + Low Score = High Risk
        if credit_score < 580 or debt > (income * 0.6):
            risk_category = "High Risk"
            transactions[random.randint(0, 4)] = random.choice(risky_merchants)
        else:
            risk_category = "Low Risk"
        
        transaction_str = ", ".join(transactions)
        data.append([name, income, debt, credit_score, risk_category, transaction_str])

    # Save to CSV
    df = pd.DataFrame(data, columns=['Name', 'Income', 'Debt', 'Credit_Score', 'Historical_Risk', 'Recent_Transactions'])
    df.to_csv("customer_database.csv", index=False)
    print("✅ Success! 'customer_database.csv' created.")

if __name__ == "__main__":
    create_fake_database()