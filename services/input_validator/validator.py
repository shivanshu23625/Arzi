import re
import unicodedata
from common.schemas import PipelineInput, ValidationResult
from common.logger import logger

class InputValidatorService:
    def __init__(self, max_length: int = 4096):
        self.max_length = max_length
        self.injection_pattern = re.compile(r"(union\s+select|drop\s+table|<script>|exec\s*\(|system\s*\()", re.IGNORECASE)

    def validate_and_normalize(self, payload: PipelineInput) -> ValidationResult:
        text = payload.raw_text

        if not text or len(text.strip()) == 0:
            return ValidationResult(
                valid=False,
                normalized_input="",
                request_id=payload.request_id,
                rejection_reason="Empty or whitespace-only text input."
            )

        if len(text) > self.max_length:
            return ValidationResult(
                valid=False,
                normalized_input="",
                request_id=payload.request_id,
                rejection_reason=f"Payload length exceeds maximum bound of {self.max_length} characters."
            )

        if self.injection_pattern.search(text):
            logger.warning("Potential injection pattern detected", extra={"request_id": payload.request_id})
            return ValidationResult(
                valid=False,
                normalized_input="",
                request_id=payload.request_id,
                rejection_reason="Malformed or suspicious payload characters detected."
            )

        normalized = unicodedata.normalize("NFKC", text)
        normalized = re.sub(r"\s+", " ", normalized).strip()

        return ValidationResult(
            valid=True,
            normalized_input=normalized,
            request_id=payload.request_id
        )