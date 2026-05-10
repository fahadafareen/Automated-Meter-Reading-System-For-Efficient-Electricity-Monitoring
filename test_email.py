import smtplib

EMAIL = 'fahadafareen2003@gmail.com'
PASSWORD_WITH_SPACES = 'qcdc hnbf ezuj pwru'
PASSWORD_NO_SPACES = 'qcdchnbfezujpwru'

# Test 1: TLS on port 587 with spaces
print("Test 1: SMTP + TLS (port 587) with spaces in password...")
try:
    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
    server.starttls()
    server.login(EMAIL, PASSWORD_WITH_SPACES)
    print("  SUCCESS!")
    server.quit()
except Exception as e:
    print(f"  FAILED: {e}")

# Test 2: TLS on port 587 without spaces
print("\nTest 2: SMTP + TLS (port 587) without spaces in password...")
try:
    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
    server.starttls()
    server.login(EMAIL, PASSWORD_NO_SPACES)
    print("  SUCCESS!")
    server.quit()
except Exception as e:
    print(f"  FAILED: {e}")

# Test 3: SSL on port 465 with spaces
print("\nTest 3: SMTP_SSL (port 465) with spaces in password...")
try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
    server.login(EMAIL, PASSWORD_WITH_SPACES)
    print("  SUCCESS!")
    server.quit()
except Exception as e:
    print(f"  FAILED: {e}")

# Test 4: SSL on port 465 without spaces
print("\nTest 4: SMTP_SSL (port 465) without spaces in password...")
try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
    server.login(EMAIL, PASSWORD_NO_SPACES)
    print("  SUCCESS!")
    server.quit()
except Exception as e:
    print(f"  FAILED: {e}")

print("\nDone. If ALL tests failed, your App Password is expired or invalid.")
print("Generate a new one at: https://myaccount.google.com/apppasswords")
