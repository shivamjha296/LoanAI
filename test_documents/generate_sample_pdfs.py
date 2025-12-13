"""
Script to generate sample salary slip PDFs for testing
"""

import os


def text_to_pdf_simple(text_file, pdf_file):
    """Convert text file to simple PDF"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
        
        # Create PDF
        c = canvas.Canvas(pdf_file, pagesize=letter)
        width, height = letter
        
        # Read text file
        with open(text_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Write text to PDF
        y_position = height - 0.5 * inch
        c.setFont("Courier", 9)
        
        for line in lines:
            if y_position < 0.5 * inch:
                c.showPage()
                c.setFont("Courier", 9)
                y_position = height - 0.5 * inch
            
            # Replace rupee symbol if needed
            line = line.rstrip('\n')
            c.drawString(0.5 * inch, y_position, line)
            y_position -= 12
        
        c.save()
        print(f"✓ Created: {pdf_file}")
        return True
        
    except ImportError:
        print("⚠ reportlab not installed. Install with: pip install reportlab")
        return False
    except Exception as e:
        print(f"✗ Error creating PDF: {e}")
        return False


def main():
    """Generate sample salary slip PDFs"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Files to convert
    files = [
        ('sample_salary_slip_1.txt', 'sample_salary_slip_1.pdf'),
        ('sample_salary_slip_2.txt', 'sample_salary_slip_2.pdf'),
    ]
    
    print("Generating sample salary slip PDFs...\n")
    
    for txt_file, pdf_file in files:
        txt_path = os.path.join(script_dir, txt_file)
        pdf_path = os.path.join(script_dir, pdf_file)
        
        if os.path.exists(txt_path):
            text_to_pdf_simple(txt_path, pdf_path)
        else:
            print(f"⚠ Text file not found: {txt_file}")
    
    print("\n✓ Done! Sample salary slips are ready for testing.")
    print("\nTo test the salary slip upload functionality:")
    print("1. Run the main application: python main.py")
    print("2. Select a customer")
    print("3. Request a loan amount > pre-approved limit")
    print("4. When prompted for salary slip, use:")
    print(f"   - {os.path.join(script_dir, 'sample_salary_slip_1.pdf')}")
    print(f"   - {os.path.join(script_dir, 'sample_salary_slip_2.pdf')}")


if __name__ == "__main__":
    main()
