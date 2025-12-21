import cv2
import numpy as np
import paddle
from paddleocr import PaddleOCR


class RecognizedResult:
    def __init__(self, image, processed_image, text, timestamp, seq_id):
        self.image = image
        self.processed_image = processed_image
        self.text = text
        self.timestamp = timestamp
        self.seq_id = seq_id


class CombatLogOCR:
    def __init__(
        self,
        ocr_engine,
        ocr_lang,
        ocr_version,
        det_model_dir,
        rec_model_dir,
        cls_model_dir,
        use_gpu,
        extract_color_ranges,
        resize_factor=2,
        resize_interpolation=cv2.INTER_NEAREST_EXACT,
    ):
        self.color_ranges = extract_color_ranges
        self.ocr_engine = ocr_engine
        self.ocr_lang = ocr_lang
        self.ocr_version = ocr_version
        self.det_model_dir = det_model_dir
        self.rec_model_dir = rec_model_dir
        self.cls_model_dir = cls_model_dir
        self.use_gpu = self._detect_gpu() if use_gpu is None else use_gpu
        self.resize_factor = resize_factor
        self.resize_interpolation = resize_interpolation

        if self.ocr_engine != "paddle":
            raise ValueError(f"Unsupported OCR engine: {self.ocr_engine}")

        self.ocr = self._init_paddle_ocr()


    def handle(self, image, timestamp, seq_id):
        processed = self._preprocess_image(image)
        text = self._paddle_to_text(processed)
        return RecognizedResult(image, processed, text, timestamp, seq_id)


    def _preprocess_image(self, image):
        resized = cv2.resize(image, None, fx=self.resize_factor, fy=self.resize_factor, interpolation=self.resize_interpolation)
        extracted = self._extract_multi_color_text(resized, self.color_ranges)
        return extracted


    def _extract_multi_color_text(self, image, color_ranges):
        combined_mask = np.zeros(image.shape[:2], dtype=np.uint8)
        for lower, upper in color_ranges:
            mask = cv2.inRange(image, np.array(lower), np.array(upper))
            combined_mask = cv2.bitwise_or(combined_mask, mask)
        result = cv2.bitwise_and(image, image, mask=combined_mask)
        return result


    def _detect_gpu(self):
        return paddle.device.is_compiled_with_cuda() and paddle.device.cuda.device_count() > 0


    def _init_paddle_ocr(self):
        options = {
            "lang": self.ocr_lang,
            "use_angle_cls": True,
            "show_log": False,
            "use_gpu": self.use_gpu,
        }
        if self.ocr_version:
            options["ocr_version"] = self.ocr_version
        if self.det_model_dir:
            options["det_model_dir"] = self.det_model_dir
        if self.rec_model_dir:
            options["rec_model_dir"] = self.rec_model_dir
        if self.cls_model_dir:
            options["cls_model_dir"] = self.cls_model_dir
        return PaddleOCR(**options)


    def _paddle_to_text(self, image):
        try:
            result = self.ocr.ocr(image, cls=True)
        except Exception as exc:
            print(f"OCR Error: {exc}")
            return ""
        lines = []
        for block in result or []:
            for line in block or []:
                if len(line) > 1 and line[1]:
                    lines.append(line[1][0])
        return "\n".join(lines)
