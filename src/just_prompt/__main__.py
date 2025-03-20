"""
Main entry point for just-prompt.
"""

import argparse
import logging
import os
import sys
from dotenv import load_dotenv
from .server import serve

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main entry point for just-prompt.
    """
    parser = argparse.ArgumentParser(description="just-prompt - A lightweight MCP server for various LLM providers")
    parser.add_argument(
        "--weak-model", 
        default="o:gpt-4o-mini",
        help="Weak model to use for model name correction, in format provider:model"
    )
    parser.add_argument(
        "--host", 
        default="0.0.0.0",
        help="Host to bind the server to"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port to bind the server to"
    )
    parser.add_argument(
        "--log-level", 
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level"
    )
    
    args = parser.parse_args()
    
    # Set logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Set environment variables
    os.environ["HOST"] = args.host
    os.environ["PORT"] = str(args.port)
    
    try:
        # Start server
        serve(args.weak_model)
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()