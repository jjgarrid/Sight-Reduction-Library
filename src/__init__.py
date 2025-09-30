"""
Sight Reduction Package for Celestial Navigation

This package provides tools for performing celestial navigation sight reductions.
"""

from .sight_reduction import (
    calculate_intercept,
    get_total_observation_correction,
    calculate_refraction_correction,
    apply_refraction_correction,
    calculate_dip_correction,
    calculate_limb_correction,
    calculate_bubble_sextant_correction,
    calculate_movement_correction,
    apply_time_interval_correction,
    get_celestial_body,
    format_position,
    visualize_sight_reduction,
    visualize_multiple_sights
)

from .aviation_almanac import (
    AviationAlmanacInterface,
    get_aviation_celestial_body_data,
    get_aviation_table_lookup
)

__all__ = [
    'calculate_intercept',
    'get_total_observation_correction',
    'calculate_refraction_correction',
    'apply_refraction_correction',
    'calculate_dip_correction',
    'calculate_limb_correction',
    'calculate_bubble_sextant_correction',
    'calculate_movement_correction',
    'apply_time_interval_correction',
    'get_celestial_body',
    'format_position',
    'visualize_sight_reduction',
    'visualize_multiple_sights',
    'AviationAlmanacInterface',
    'get_aviation_celestial_body_data',
    'get_aviation_table_lookup'
]