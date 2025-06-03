# Missing Processor Wrappers

Based on your description, you have many processors but only 3 wrappers. Here are the missing processor wrappers needed:

## Existing Wrappers (you already have these):
- corpus_balancer_wrapper.py
- text_extractor_wrapper.py
- pdf_extractor_wrapper.py

## Missing Wrappers to Create:
Based on the processors you mentioned:

1. quality_control_wrapper.py
2. deduplicator_wrapper.py
3. domain_classifier_wrapper.py
4. language_confidence_detector_wrapper.py
5. machine_translation_detector_wrapper.py
6. financial_symbol_processor_wrapper.py
7. formula_extractor_wrapper.py
8. chart_image_extractor_wrapper.py (if exists)

Each wrapper should:
- Inherit from BaseWrapper and ProcessorWrapperMixin
- Provide start(), stop(), and get_status() methods
- Support batch processing and progress/error reporting via PyQt signals
- Be placed in shared_tools/ui_wrappers/processors/