import re

def check_length(password):
    return 1 if 12 <= len(password) <= 128 else 0

def check_upper(password):
    return 2 if re.search(r"[A-Z]", password) else 0

def check_lower(password):
    return 2 if re.search(r"[a-z]", password) else 0

def check_digit(password):
    return 2 if re.search(r"\d", password) else 0

def check_special(password):
    return 2 if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) else 0

def check_sequence(password):
    sequences = ["0123", "1234", "2345", "3456", "4567",
                 "abcd", "bcde", "cdef", "defg", "efgh"]
    for seq in sequences:
        if seq in password.lower():
            return -2
    return 0

def check_repeats(password):
    if re.search(r"(.)\1{2,}", password):  # e.g., aaa, 111
        return -2
    return 0

def check_user_data(password, username="", email=""):
    user_related = []
    if username:
        user_related.append(username.lower())
    if email:
        email_user = email.split("@")[0].lower()
        user_related.append(email_user)

    for piece in user_related:
        if piece and piece in password.lower():
            return -5
    return 0

def evaluate_password(password, username="", email=""):
    score = 0
    feedback = []

    # Positive checks
    score += check_length(password)
    score += check_upper(password)
    score += check_lower(password)
    score += check_digit(password)
    score += check_special(password)

    # Negative checks
    score += check_sequence(password)
    score += check_repeats(password)
    score += check_user_data(password, username, email)

    # Feedback
    if check_length(password) == 0:
        feedback.append("❌ Password must be between 12 and 128 characters.")
    if check_upper(password) == 0:
        feedback.append("❌ Add at least one uppercase letter.")
    if check_lower(password) == 0:
        feedback.append("❌ Add at least one lowercase letter.")
    if check_digit(password) == 0:
        feedback.append("❌ Add at least one digit.")
    if check_special(password) == 0:
        feedback.append("❌ Add at least one special character.")
    if check_sequence(password) < 0:
        feedback.append("⚠️ Avoid using obvious sequences like '1234' or 'abcd'.")
    if check_repeats(password) < 0:
        feedback.append("⚠️ Avoid repeating the same character multiple times.")
    if check_user_data(password, username, email) < 0:
        feedback.append("⚠️ Do not include your name or email in your password.")

    # Score rating
    if score <= 5:
        strength = "🔴 Weak"
    elif score <= 10:
        strength = "🟠 Moderate"
    elif score <= 15:
        strength = "🟡 Strong"
    else:
        strength = "🟢 Very Strong"

    return score, strength, feedback


if __name__ == "__main__":
    print("\n🔐 GitHub Password Strength Checker")
    print("Evaluate your password against security best practices.\n")

    password = input("Enter your password: ")
    username = input("Enter your GitHub username (optional): ")
    email = input("Enter your email address (optional): ")

    score, strength, feedback = evaluate_password(password, username, email)

    print(f"\n🔎 Evaluation Result: {strength} (Score: {score}/20)")
    if feedback:
        print("📋 Feedback to improve:")
        for item in feedback:
            print(f"  - {item}")
    else:
        print("✅ Your password looks great! No issues found.")

