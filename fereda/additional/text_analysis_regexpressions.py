# -*- coding: utf-8 -*-
from fereda.extra import utils


TEXT_ANALYSIS_REGEXPRESSIONS = utils.get_compiled_regex(
    (
        # --- Coordinates ---
        '(\d{1,3}\.\d+),? ?(\d{1,3}\.\d+)',                # Decimal degrees.
        '(\d+ \d+\.\d+),? ?(\d+ \d+\.\d+)',                # Degrees and decimal minutes.
    )
)
