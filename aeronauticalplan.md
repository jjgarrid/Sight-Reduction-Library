# Aeronautical Sight Reduction Implementation Plan

Based on the analysis of the aeronautical.md document and the current codebase, this document outlines the comprehensive plan for implementing aeronautical sight reduction functionality in the existing nautical sight reduction library.

## Background
Celestial navigation from airplanes uses specialized procedures and tables distinct from typical marine navigation, adapting to the unique challenges posed by flight such as the absence of a natural horizon and constant aircraft movement. Aviators employed specific sight reduction tables—most famously, the Air Almanac and the Sight Reduction Tables for Air Navigation (e.g., Pub. No. 249)—and followed observation practices suited to fast-moving and pitching aircraft.

Key differences from marine navigation:
- Observations are made with a bubble sextant (not with the visible horizon)
- Time synchronization and adjustments for observer movement are critical, handled via specialized tables
- Position fixing procedures include corrections unique to the fast-changing position and attitude of aircraft as well as averaging techniques for multiple continuous sights

## Implementation Plan

### 1. Identify Navigation Modes
- Extend the current library to include an "aviation" mode in addition to the existing "marine" mode
- Add a navigation_mode parameter to sight reduction functions to differentiate between marine and aviation calculations
- Update the problem generator to support aviation-specific scenarios

### 2. Bubble Sextant Support
- Modify the existing dip correction function to accommodate artificial horizon observations
- Add new correction functions specific to bubble sextants that don't rely on a visible horizon
- Implement support for time-averaged sight measurements to account for turbulence and rapid movement
- Add input validation for bubble sextant readings (typically no dip correction needed)

### 3. Almanac and Table Selection
- Extend the almanac integration module to support both Air Almanac and Nautical Almanac formats
- Implement lookup functionality for Air Navigation reduction tables (e.g., Pub. No. 249)
- Add epoch management for aviation-specific tables
- Create a table selection interface to choose between marine and aviation tables

### 4. Observer Movement Correction
- Enhance algorithms to factor in observer movement during flight
- Implement elapsed time corrections for rapidly moving aircraft
- Add dead reckoning functionality to account for position shifts during observation
- Enable post-processing for averaging multiple rapid sights taken during turbulence
- Add parameters for aircraft speed, heading, and altitude changes

### 5. Exercise Generator Adaptation
- Expand practice exercises to include aviation-specific scenarios
- Add scenarios with absence of natural horizon 
- Create exercises with artificial horizon observations using bubble sextant
- Include simulated turbulence effects and variable sight intervals
- Add question sets testing proper aviation table selection and procedures

### 6. Enhanced atmospheric corrections for flight altitude
- Adjust refraction calculations for high-altitude observations
- Account for different atmospheric conditions at flight altitudes
- Update pressure and temperature correction models for aircraft altitudes
- Add aircraft altitude as a parameter in observation corrections

### 7. Validation and Testing
- Cross-check calculated aviation fixes against known aviation procedures
- Create aviation-specific test cases based on example problems from Air Navigation manuals
- Add comparison functions between marine and aviation methods

### 8. Documentation and User Interface Updates
- Update help documentation to cover aviation techniques
- Add tutorials for bubble sextant use and aviation-specific procedures
- Provide clear comparisons between air and marine navigation methods
- Update CLI interface to support aviation parameters

## Implementation Approach
1. **First Phase**: Add navigation mode support and modify core sight reduction functions
2. **Second Phase**: Implement bubble sextant corrections and aviation-specific atmospheric models
3. **Third Phase**: Update the problem generator and exercise creation
4. **Fourth Phase**: Add aviation almanac integration and table selection
5. **Fifth Phase**: Create comprehensive tests and update documentation

This plan builds upon the existing robust marine navigation foundation while adding the specific requirements for aeronautical celestial navigation, including the need for artificial horizon observations, aircraft movement corrections, and aviation-specific tables.