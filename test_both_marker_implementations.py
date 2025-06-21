#!/usr/bin/env python3
"""
Test script to verify both Marker implementations:
1. Local Marker (datalab_marker)
2. Datalab Marker Cloud API (datalab_marker_api)
"""

import os
import sys
import json
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from open_webui.retrieval.loaders.datalab_marker import DatalabMarkerLoader
from open_webui.retrieval.loaders.datalab_marker_api import DatalabMarkerAPILoader

def test_local_marker():
    """Test the local Marker implementation"""
    print("\n=== Testing Local Marker Implementation ===")
    
    # Configuration for local Marker
    marker_url = os.getenv("MARKER_URL", "http://marker:8501")
    
    print(f"Using Marker URL: {marker_url}")
    
    try:
        loader = DatalabMarkerLoader(
            file_path="test.pdf",  # You'll need a test PDF
            api_key="dummy",  # Not used for local
            marker_url=marker_url,
            langs="en,de",
            use_llm=False,
            skip_cache=False,
            # These parameters are NOT supported by local Marker:
            # force_ocr=False,
            # paginate=False,
            # strip_existing_ocr=False,
            # disable_image_extraction=False,
            # output_format="markdown"
        )
        
        # Note: This would actually try to load the file
        # For testing, we just verify the loader was created
        print("✓ Local Marker loader created successfully")
        print(f"  - Marker URL: {loader.marker_url}")
        print(f"  - Languages: {loader.langs}")
        print(f"  - Use LLM: {loader.use_llm}")
        print(f"  - Skip Cache: {loader.skip_cache}")
        
    except Exception as e:
        print(f"✗ Error creating local Marker loader: {e}")
        return False
    
    return True

def test_cloud_api():
    """Test the Datalab Marker Cloud API implementation"""
    print("\n=== Testing Datalab Marker Cloud API Implementation ===")
    
    # Configuration for Cloud API
    api_key = os.getenv("DATALAB_API_KEY", "test-api-key")
    
    print(f"Using API Key: {api_key[:10]}..." if len(api_key) > 10 else api_key)
    
    try:
        loader = DatalabMarkerAPILoader(
            file_path="test.pdf",  # You'll need a test PDF
            api_key=api_key,
            langs="en,de",
            use_llm=True,
            skip_cache=False,
            force_ocr=True,
            paginate=True,
            strip_existing_ocr=False,
            disable_image_extraction=False,
            output_format="markdown"
        )
        
        # Note: This would actually try to load the file
        # For testing, we just verify the loader was created
        print("✓ Cloud API loader created successfully")
        print(f"  - API Key: {loader.api_key[:10]}...")
        print(f"  - Languages: {loader.langs}")
        print(f"  - Use LLM: {loader.use_llm}")
        print(f"  - Skip Cache: {loader.skip_cache}")
        print(f"  - Force OCR: {loader.force_ocr}")
        print(f"  - Paginate: {loader.paginate}")
        print(f"  - Strip Existing OCR: {loader.strip_existing_ocr}")
        print(f"  - Disable Image Extraction: {loader.disable_image_extraction}")
        print(f"  - Output Format: {loader.output_format}")
        
    except Exception as e:
        print(f"✗ Error creating Cloud API loader: {e}")
        return False
    
    return True

def test_main_loader():
    """Test the main loader that switches between implementations"""
    print("\n=== Testing Main Loader Implementation ===")
    
    from open_webui.retrieval.loaders.main import Loader
    
    # Test 1: Local Marker
    print("\nTest 1: Local Marker via main loader")
    try:
        loader = Loader(
            engine="datalab_marker",
            DATALAB_MARKER_API_KEY="http://marker:8501",  # URL for local
            DATALAB_MARKER_LANGS="en,de",
            DATALAB_MARKER_USE_LLM=False,
            DATALAB_MARKER_SKIP_CACHE=False
        )
        
        print("✓ Main loader configured for local Marker")
        print(f"  - Engine: {loader.engine}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 2: Cloud API
    print("\nTest 2: Cloud API via main loader")
    try:
        loader = Loader(
            engine="datalab_marker_api",
            DATALAB_MARKER_API_KEY="test-api-key-12345",  # API key for cloud
            DATALAB_MARKER_LANGS="en,de",
            DATALAB_MARKER_USE_LLM=True,
            DATALAB_MARKER_SKIP_CACHE=False,
            DATALAB_MARKER_FORCE_OCR=True,
            DATALAB_MARKER_PAGINATE=True,
            DATALAB_MARKER_OUTPUT_FORMAT="markdown"
        )
        
        print("✓ Main loader configured for Cloud API")
        print(f"  - Engine: {loader.engine}")
        
    except Exception as e:
        print(f"✗ Error: {e}")

def main():
    """Run all tests"""
    print("Datalab Marker Implementation Tests")
    print("===================================")
    
    # Test individual loaders
    local_ok = test_local_marker()
    cloud_ok = test_cloud_api()
    
    # Test main loader
    test_main_loader()
    
    print("\n=== Summary ===")
    print(f"Local Marker: {'✓ PASS' if local_ok else '✗ FAIL'}")
    print(f"Cloud API: {'✓ PASS' if cloud_ok else '✗ FAIL'}")
    
    print("\n=== Configuration Notes ===")
    print("1. For Local Marker:")
    print("   - Set Content Extraction Engine to 'datalab_marker'")
    print("   - Enter Marker Server URL (e.g., http://marker:8501)")
    print("   - Only basic parameters are supported")
    print("\n2. For Cloud API:")
    print("   - Set Content Extraction Engine to 'datalab_marker_api'")
    print("   - Enter your Datalab API Key")
    print("   - All parameters are supported")

if __name__ == "__main__":
    main()