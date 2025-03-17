import subprocess

# Run both scripts in parallel
process1 = subprocess.Popen(["python", "1_extract_all_pages.py"])
process2 = subprocess.Popen(["python", "2_extract data.py"])

# Wait for both scripts to finish
process1.wait()
process2.wait()

print("\n✅ Both scripts have completed successfully!")
