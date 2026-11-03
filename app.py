import streamlit as st
import time
import base64
from io import BytesIO
from pathlib import Path
import sys
import zipfile
import matplotlib.pyplot as plt
import pandas as pd

# 1. Streamlit Application UI Layout Configurations
st.set_page_config(page_title="AI Timetable Matrix Engine", layout="wide")

st.title("📅 AI-Powered Timetable Matrix Optimizer")
st.markdown("Execute Google Colab constraint satisfaction algorithms directly inside an interactive web dashboard environment.")

# --- EMBEDDED PROJECT EXTRACTOR & FILE SYSTEM MANAGEMENT ---
PROJECT_ROOT = Path("./timetable_project")
PROJECT_ROOT.mkdir(parents=True, exist_ok=True)

# Encapsulated core assets mapped cleanly inside a singular formatted system string
SOURCE_ARCHIVE_B64 = (
    "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"
