import subprocess
import os
from pathlib import Path


class PDFConverter:
    """Convert Word documents to PDF format."""
    
    @staticmethod
    def docx_to_pdf(docx_path, pdf_path):
        """Convert DOCX file to PDF using LibreOffice.
        
        Args:
            docx_path: Path to the input DOCX file
            pdf_path: Path to save the output PDF file
            
        Returns:
            True if conversion is successful, False otherwise
        """
        try:
            # Use LibreOffice headless mode to convert
            output_dir = str(Path(pdf_path).parent)
            
            cmd = [
                'libreoffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', output_dir,
                str(docx_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Rename the generated PDF to the desired name
                generated_pdf = os.path.join(output_dir, Path(docx_path).stem + '.pdf')
                if os.path.exists(generated_pdf) and generated_pdf != pdf_path:
                    os.rename(generated_pdf, pdf_path)
                return True
            else:
                print(f"LibreOffice conversion failed: {result.stderr}")
                return False
                
        except FileNotFoundError:
            print("LibreOffice not found. Please install LibreOffice to convert DOCX to PDF.")
            print("macOS: brew install libreoffice")
            return False
        except subprocess.TimeoutExpired:
            print("LibreOffice conversion timed out.")
            return False
        except Exception as e:
            print(f"Error during conversion: {str(e)}")
            return False
    
    @staticmethod
    def convert_documents(question_paper_path, answer_key_path, output_dir):
        """Convert both Question Paper and Answer Key to PDF.
        
        Args:
            question_paper_path: Path to Question Paper DOCX
            answer_key_path: Path to Answer Key DOCX
            output_dir: Directory to save PDF files
            
        Returns:
            Tuple (question_paper_pdf_path, answer_key_pdf_path) or None if any conversion fails
        """
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate PDF paths
        question_paper_pdf = os.path.join(
            output_dir,
            Path(question_paper_path).stem + '.pdf'
        )
        answer_key_pdf = os.path.join(
            output_dir,
            Path(answer_key_path).stem + '.pdf'
        )
        
        # Convert Question Paper
        print("Converting Question Paper to PDF...")
        if not PDFConverter.docx_to_pdf(question_paper_path, question_paper_pdf):
            print("Failed to convert Question Paper to PDF")
            return None
        
        print(f"✓ Question Paper PDF created: {question_paper_pdf}")
        
        # Convert Answer Key
        print("Converting Answer Key to PDF...")
        if not PDFConverter.docx_to_pdf(answer_key_path, answer_key_pdf):
            print("Failed to convert Answer Key to PDF")
            return None
        
        print(f"✓ Answer Key PDF created: {answer_key_pdf}")
        
        return question_paper_pdf, answer_key_pdf
