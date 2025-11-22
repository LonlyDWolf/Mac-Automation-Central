from pathlib import Path
from transformers import pipeline
# Imports for extracting text from documents
from pypdf import PdfReader
from docx import Document
from openpyxl import load_workbook
from pptx import Presentation

# Config settings
from config import setting

# Initialize the Zero-Shot Classifier
try:
    classifier = pipeline(
        "zero-shot-classification",
        model=setting.AI_CLASSIFIER_MODEL
    )
except Exception as e:
    print(f"CRITICAL ERROR: Failed to load AI pipeline. Check your internet connection and transformers install. Error: {e}")
    classifier = None  # Set to None so other functions can handle this gracefully


def categorize_by_content(file_path: Path) -> str:
    # This will read file content and call the AI API
    
    # 1. Extract text from the document
    document_text = extract_text_from_document(file_path)
    
    if not document_text:
        # Fallback category if extraction failed
        return setting.FALLBACK_CONTENT_CATEGORY
    
    # 2. Send the text to the AI model for categorization
    # Limit the text length to avoid exceeding model limits
    truncated_text = document_text[:512]  # Adjust as needed
    
    #2.1 Check if classifier is available
    if classifier is None:
        print("Warning: AI pipeline failed to load. Using fallback category.")
        return setting.FALLBACK_CONTENT_CATEGORY
      
    # 2.2 Run the classifier
    # The result is a list of dictionaries; we take the first one (most relevant)
    try: 
        result = classifier(truncated_text, setting.DOCUMENT_CANDIDATE_LABELS)
        # 2.3 Get the top category
        best_category = result['labels'][0]
    except Exception as e:
        # Fallback if the AI service fails for any reason
        print(f"Warning: AI classification failed for {file_path.name}. Error: {e}")
        best_category = setting.FALLBACK_CONTENT_CATEGORY
    
    # We replace spaces with underscores for folder naming
    return f"Documents/{best_category.replace(' ', '_')}"
    

def categorize_by_name(file_path: Path) -> str:
    # This will read filename/extension and call the AI API
    
    # 1. Determine the Extension_Category (e.g., Images, Videos, Archives)
    extension_category = file_path.suffix.lstrip('.').upper()
    
    # Simple mapping for common extensions
    if extension_category in {'JPG', 'JPEG', 'PNG', 'GIF', 'BMP', 'TIFF', 'SVG', 'RAW'}:
        extension_category = 'IMAGES'
    elif extension_category in {'MP4', 'MOV', 'AVI', 'MKV', 'WMV', 'FLV', 'MPEG'}:
        extension_category = 'VIDEOS'
    elif extension_category in {'MP3', 'WAV', 'FLAC', 'AAC', 'OGG'}:
        extension_category = 'AUDIO'
    elif extension_category in {'ZIP', 'RAR', '7Z', 'TAR', 'GZ'}:
        extension_category = 'ARCHIVES'
    elif extension_category in {'EXE', 'DMG', 'APP', 'BIN'}:
        extension_category = 'APPLICATIONS'
    elif extension_category in {'HTML', 'CSS', 'JS', 'JSON', 'XML', 'YAML', 'YML', 'PY', 'JAVA', 'C', 'CPP', 'RB', 'PHP', 'GO', 'RS', 'SH'}:
        extension_category = 'CODE'
    elif extension_category in {'CSV', 'LOG'}:
        extension_category = 'DATA'
    
    # 2. Analyze the filename using AI
    if classifier is None:
        print("Warning: AI pipeline failed to load. Using fallback category.")
        best_category = setting.FALLBACK_NAME_CATEGORY
    
    try:
        result = classifier(file_path.stem, setting.FILENAME_CANDIDATE_LABELS)
        best_category = result['labels'][0]
    except Exception as e:
        # Fallback if the AI service fails for any reason
        best_category = setting.FALLBACK_NAME_CATEGORY
    
    # 3. Combine both to form the final category
    return f"{extension_category}/{best_category.replace(' ', '_')}"

def get_destination_category(file_path: Path) -> str:
    """Determine the destination category based on file extension."""
    file_extension = file_path.suffix.lower()
    
    if file_extension in setting.DOCUMENT_EXTENSIONS:
        # for documents, use content-based categorization
        return categorize_by_content(file_path)
    else:
        # for non-documents, use name-based categorization
        return categorize_by_name(file_path)


def extract_text_from_document(file_path: Path) -> str:
    """Extracts text content from various document types using external libraries."""
    
    file_extension = file_path.suffix.lower()
    
    try:
        if file_extension == '.pdf':
            reader = PdfReader(file_path)
            text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
            return text
        
        elif file_extension in {'.doc', '.docx'}:
            doc = Document(file_path)
            text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
            return text
        
        # Add more document types as needed (e.g., .txt, .xls, .xlsx, .ppt, .pptx, .md)
        elif file_extension == '.txt':
            return file_path.read_text(encoding='utf-8')
        
        elif file_extension in {'.xls', '.xlsx'}:
            wb = load_workbook(filename=file_path, read_only=True)
            text = []
            for sheet in wb:
                for row in sheet.iter_rows(values_only=True):
                    text.append(" ".join(str(cell) for cell in row if cell is not None))
            return "\n".join(text)
          
        elif file_extension in {'.ppt', '.pptx'}:
            prs = Presentation(file_path)
            text = []
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text.append(shape.text)
            return "\n".join(text)
          
        elif file_extension == '.md':
            return file_path.read_text(encoding='utf-8')
        
        else:
            # Unsupported document type for text extraction
            return ""
        
          
    except Exception as e:
        print(f"Warning: Failed to extract text from {file_path.name}. Error: {e}")
        # For unsupported document types, return empty string or a message
        return ""
      
def generate_safe_path(target_path : Path) -> Path:
    """Generate a safe path by appending a number if the path already exists. (e.g., file.txt -> file_1.txt)"""
    
    if not target_path.exists():
        return target_path  # Path is safe
    
    current_path = target_path
    counter = 0
    
    # Loop until we find a non-existing path
    while current_path.exists():
        # 1. If the path exists, increment the counter and create a new path
        counter += 1
        # 2. Create a new path with the counter appended before the suffix
        if target_path.suffix:
            # Reconstruct: stem + _counter + suffix
            new_name = target_path.with_name(f"{target_path.stem}_{counter}{target_path.suffix}")
        else:
            # No suffix, just append the counter
            new_name = target_path.with_name(f"{target_path.name}_{counter}")
        
        # Update current_path to the new_name
        current_path = new_name
    
    return current_path
        