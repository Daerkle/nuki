import os
import time
import requests
import logging
import json
from typing import List, Optional
from langchain_core.documents import Document
from fastapi import HTTPException, status

log = logging.getLogger(__name__)


class LocalMarkerLoader:
    """
    Local Marker Loader - Native integration for Hive/OpenWebUI
    Replaces the Datalab cloud API with local Marker service
    """
    
    def __init__(
        self,
        file_path: str,
        # Compatibility parameters (matching Datalab interface)
        api_key: str = None,  # Ignored but kept for compatibility
        langs: Optional[str] = None,
        use_llm: bool = False,
        skip_cache: bool = False,
        force_ocr: bool = False,
        paginate: bool = False,
        strip_existing_ocr: bool = False,
        disable_image_extraction: bool = False,
        output_format: str = "markdown",
        # Local Marker specific parameters
        marker_url: str = None,
        timeout: int = None,
    ):
        self.file_path = file_path
        
        # Get marker URL from parameter or environment
        self.marker_url = (
            marker_url or 
            os.getenv("MARKER_SERVER_URL") or 
            os.getenv("MARKER_URL") or 
            "http://marker:8501"
        ).rstrip('/')
        
        # Get timeout from parameter or environment
        self.timeout = (
            timeout or 
            int(os.getenv("MARKER_TIMEOUT", "300"))
        )
        
        # Store parameters (keeping Datalab compatibility)
        self.langs = langs
        self.use_llm = use_llm
        self.skip_cache = skip_cache
        self.force_ocr = force_ocr
        self.paginate = paginate
        self.strip_existing_ocr = strip_existing_ocr
        self.disable_image_extraction = disable_image_extraction
        self.output_format = output_format or "markdown"
        
        # api_key is ignored for local implementation but kept for compatibility
        if api_key:
            log.info("API key provided but ignored for local Marker implementation")
        
        log.info(f"LocalMarkerLoader initialized: marker_url={self.marker_url}, timeout={self.timeout}s, output_format={self.output_format}")

    def _get_mime_type(self, filename: str) -> str:
        """Get MIME type from filename extension"""
        ext = filename.rsplit(".", 1)[-1].lower()
        mime_map = {
            "pdf": "application/pdf",
            "xls": "application/vnd.ms-excel",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "ods": "application/vnd.oasis.opendocument.spreadsheet",
            "doc": "application/msword",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "odt": "application/vnd.oasis.opendocument.text",
            "ppt": "application/vnd.ms-powerpoint",
            "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "odp": "application/vnd.oasis.opendocument.presentation",
            "html": "text/html",
            "epub": "application/epub+zip",
            "png": "image/png",
            "jpeg": "image/jpeg",
            "jpg": "image/jpeg",
            "webp": "image/webp",
            "gif": "image/gif",
            "tiff": "image/tiff",
        }
        return mime_map.get(ext, "application/octet-stream")

    def _check_marker_health(self) -> bool:
        """Check if local Marker service is available"""
        try:
            response = requests.get(f"{self.marker_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("converter_ready", False)
            return False
        except Exception as e:
            log.error(f"Marker health check failed: {e}")
            return False

    def check_marker_request_status(self, request_id: str) -> dict:
        """
        Compatibility method for the old interface
        For local implementation, this is not needed but kept for compatibility
        """
        log.warning("check_marker_request_status called on LocalMarkerLoader - this method is not applicable for local processing")
        return {"status": "complete", "success": True, "message": "Local processing does not use request IDs"}

    def _convert_with_local_marker(self) -> dict:
        """Convert file using local Marker service"""
        if not self._check_marker_health():
            raise HTTPException(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Local Marker service is not available or not ready"
            )

        filename = os.path.basename(self.file_path)
        mime_type = self._get_mime_type(filename)

        # Prepare form data for local Marker API
        form_data = {}
        
        # Add all supported parameters
        if self.output_format:
            form_data["output_format"] = self.output_format
        
        # Convert boolean values to strings as expected by the API
        if self.force_ocr is not None:
            form_data["force_ocr"] = str(self.force_ocr).lower()
        
        if self.use_llm is not None:
            form_data["use_llm"] = str(self.use_llm).lower()
            
        if self.skip_cache is not None:
            form_data["skip_cache"] = str(self.skip_cache).lower()
            
        if self.paginate is not None:
            form_data["paginate"] = str(self.paginate).lower()
            
        if self.strip_existing_ocr is not None:
            form_data["strip_existing_ocr"] = str(self.strip_existing_ocr).lower()
            
        if self.disable_image_extraction is not None:
            form_data["disable_image_extraction"] = str(self.disable_image_extraction).lower()
            
        # Add language parameter if specified
        if self.langs:
            form_data["langs"] = self.langs

        log.info(
            f"Local Marker request - URL: {self.marker_url}/convert, filename: {filename}, mime_type: {mime_type}, form_data: {form_data}"
        )

        try:
            with open(self.file_path, "rb") as f:
                files = {"file": (filename, f, mime_type)}
                
                # Try with form_data if we have any, otherwise just send the file
                if form_data:
                    response = requests.post(
                        f"{self.marker_url}/convert",
                        data=form_data,
                        files=files,
                        timeout=self.timeout
                    )
                else:
                    response = requests.post(
                        f"{self.marker_url}/convert",
                        files=files,
                        timeout=self.timeout
                    )
                
                log.info(f"Marker response status: {response.status_code}")
                
                if response.status_code != 200:
                    log.error(f"Marker error response: {response.text}")
                    
                response.raise_for_status()
                
                # Try to parse JSON response
                try:
                    result = response.json()
                except json.JSONDecodeError:
                    # If JSON parsing fails, treat the response as plain text
                    result = {"content": response.text}
                
                log.info(f"Local Marker conversion completed successfully")
                log.debug(f"Result type: {type(result)}")
                if isinstance(result, dict):
                    log.debug(f"Result keys: {list(result.keys())}")
                
                return result
                
        except FileNotFoundError:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, 
                detail=f"File not found: {self.file_path}"
            )
        except requests.exceptions.Timeout:
            raise HTTPException(
                status.HTTP_504_GATEWAY_TIMEOUT,
                detail=f"Marker conversion timed out after {self.timeout} seconds"
            )
        except requests.HTTPError as e:
            error_detail = f"Local Marker request failed: {e}"
            if hasattr(e.response, 'text'):
                try:
                    error_data = e.response.json()
                    error_detail = f"Marker error: {error_data.get('detail', str(e))}"
                except:
                    error_detail = f"Marker error: {e.response.text}"
            
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=error_detail
            )
        except Exception as e:
            log.error(f"Unexpected error in Marker conversion: {e}")
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Conversion error: {str(e)}"
            )

    def load(self) -> List[Document]:
        """
        Load and convert document using local Marker service
        Returns: List of Document objects compatible with LangChain
        """
        # Convert using local Marker service
        result = self._convert_with_local_marker()
        
        # Check if the result indicates failure (only if it's a dict with success field)
        if isinstance(result, dict) and "success" in result and not result.get("success"):
            error_msg = result.get("error", "Unknown conversion error")
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f"Local Marker conversion failed: {error_msg}"
            )

        # Extract content - the local Marker API might return content differently
        content = None
        
        log.debug(f"Marker response type: {type(result)}")
        log.debug(f"Marker response: {result}")
        
        # Try different possible response formats
        if isinstance(result, dict):
            # Check for different possible content keys
            content = (
                result.get("markdown") or
                result.get("text") or
                result.get("content") or
                result.get("output") or
                result.get("result") or
                result.get("data")
            )
            
            # If still no content, check if the result itself is the content
            if not content and len(result) == 1:
                content = list(result.values())[0]
                
            # Sometimes the content is nested in a success response
            if not content and result.get("success") and "data" in result:
                content = result["data"]
                
        elif isinstance(result, str):
            # The result might be the content directly
            content = result
        
        # Convert to string if needed
        if content and not isinstance(content, str):
            content = str(content)
        
        if not content or not content.strip():
            log.error(f"No content found in Marker response.")
            log.error(f"Response keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            log.error(f"Full response: {result}")
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f"Extracted content is not available for this file. Please ensure that the file is processed before proceeding."
            )

        # Save output to disk (matching Datalab behavior)
        filename = os.path.basename(self.file_path)
        marker_output_dir = os.path.join("/app/backend/data/uploads", "marker_output")
        os.makedirs(marker_output_dir, exist_ok=True)

        file_ext_map = {"markdown": "md", "json": "json", "html": "html"}
        file_ext = file_ext_map.get(self.output_format.lower(), "md")
        output_filename = f"{os.path.splitext(filename)[0]}.{file_ext}"
        output_path = os.path.join(marker_output_dir, output_filename)

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            log.info(f"Saved Local Marker output to: {output_path}")
        except Exception as e:
            log.warning(f"Failed to write marker output to disk: {e}")

        # Prepare metadata (matching Datalab format)
        metadata = {
            "source": filename,
            "output_format": self.output_format,
            "page_count": result.get("metadata", {}).get("page_count", 0),
            "processed_with_llm": self.use_llm,
            "request_id": f"local_{int(time.time())}",  # Local request ID
            "processing_method": "local_marker",
            "image_count": result.get("images", 0),
        }

        # Add any additional metadata from the conversion
        if "metadata" in result and isinstance(result["metadata"], dict):
            for key, value in result["metadata"].items():
                if key not in metadata:
                    metadata[f"marker_{key}"] = value

        # Ensure all metadata values are strings
        for k, v in metadata.items():
            if isinstance(v, (dict, list)):
                metadata[k] = json.dumps(v)
            elif v is None:
                metadata[k] = ""
            else:
                metadata[k] = str(v)

        log.info(f"Local Marker processing completed successfully for {filename}")
        return [Document(page_content=content, metadata=metadata)]


# Compatibility alias for easy replacement
DatalabMarkerLoader = LocalMarkerLoader
