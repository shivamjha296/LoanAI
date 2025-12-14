
import os

# Paths
base_dir = r"d:\ey_techathon\LoanAI\loan_master_agent\sub_agents\sanction_letter_agent"
template_path = os.path.join(base_dir, "sanction_letter_template.html")
logo_base64_path = os.path.join(base_dir, "logo_base64.txt")

# Read Base64 Logo
with open(logo_base64_path, "r") as f:
    logo_src = f.read().strip()

# Read HTML Template
with open(template_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Replace Logo Placeholder
# We look for src="image.png" and replace it with the base64 data URI
updated_html = html_content.replace('src="image.png"', f'src="{logo_src}"')

# Verify replacement happened
if logo_src in updated_html:
    print("Logo embedded successfully.")
else:
    print("Warning: Logo placeholder 'src=\"image.png\"' not found or replacement failed.")

# Write Updated Template
with open(template_path, "w", encoding="utf-8") as f:
    f.write(updated_html)

print(f"Updated template saved to: {template_path}")
