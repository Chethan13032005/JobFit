"""Command-Line Interface for Batch Resume Analysis."""
import argparse

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="JobFit: Automated Resume & Skill Gap Analyzer")
    parser.add_argument("--resume", "-r", required=True, help="Path to resume file (.pdf, .docx, .txt)")
    parser.add_argument("--job", "-j", required=True, help="Path to job description text file")
    parser.add_argument("--format", "-f", choices=["markdown", "csv", "json", "html"], default="markdown")
    return parser
