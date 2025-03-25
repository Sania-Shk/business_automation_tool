import sys
import os

# ✅ Backend ka path manually add karo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../Backend(Flask API)")))

# ✅ Now Import Processing Function
from utils.processing import process_file

# ✅ Test Data (CSV)
sample_data = b"id,name,age,salary\n1,John,25,50000\n2,Jane,30,60000\n3,Bob,35,70000"
df, msg = process_file(sample_data, "csv")

print(df)
print(msg)
