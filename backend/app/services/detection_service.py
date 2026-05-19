"""
detection_service.py — Orchestrates the full scam detection pipeline.

This service is the single entry point for detection logic.
Routes call this service; the service calls the model and utilities.

Responsibilities (to be implemented):
  1. Accept raw user input
  2. Call text_preprocessor to clean/normalize the text
  3. Pass cleaned text to ScamDetectorModel for inference
  4. Map raw model output to a DetectionResponse schema
  5. Log the prediction for auditing / dataset collection

Keeping this layer separate from the route handlers means:
  - Routes stay thin (HTTP concerns only)
  - Models stay pure (no HTTP/business logic)
  - This service is unit-testable without an HTTP server
"""

from app.schemas.detection import DetectionRequest, DetectionResponse, ScamCategory


class DetectionService:
    """
    Wraps the full detection pipeline.
    Instantiated once at startup and injected into route handlers.
    """

    def __init__(self):
        # Future: accept ScamDetectorModel as a dependency
        pass

    async def analyze(self, request: DetectionRequest) -> DetectionResponse:
        """
        Run the scam detection pipeline on incoming text.
        Returns a DetectionResponse with prediction and confidence.
        """
        # TODO: integrate preprocessor → model → response mapping
        raise NotImplementedError("DetectionService.analyze() is not yet implemented")
