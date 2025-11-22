from pathlib import Path

# --- General Settings ---
# Default folder to organize if none provided
DEFAULT_TARGET_PATH = Path.home() / "Downloads"

# --- AI Categorization Settings ---

# 1. Extensions that require content-based categorization
DOCUMENT_EXTENSIONS = {
    '.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.md'
}

# 2. Labels for AI analysis of document content
DOCUMENT_CANDIDATE_LABELS = [
    "Research Paper", "Study Books or Materials", "Novel", "Template", 
    "Finance", "Letters", "Receipt", "Legal"
]

# 3. Labels for AI analysis of filenames
FILENAME_CANDIDATE_LABELS = ["Personal", "Work", "Projects", "Media", "System"]

# 4. Fallback category names
FALLBACK_CONTENT_CATEGORY = "Unsorted_Extraction_Failed"
FALLBACK_NAME_CATEGORY = "Unsorted_Name_Failed"

# 5. AI Model Settings
AI_CLASSIFIER_MODEL = "facebook/bart-large-mnli"  # Model for zero-shot classification
AI_MAX_TEXT_LENGTH = 512  # Max characters to send to the AI model