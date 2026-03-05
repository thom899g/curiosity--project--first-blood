"""
Genesis Stress Packet Telemetry Collector
Collects system telemetry over 60 seconds for minting.
Uses psutil for system metrics, implements rigorous error handling.
"""
import psutil
import time
import json
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import random  # For emotion simulation until ML model integrated

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelemetryCollector:
    def __init__(self, collection_duration: int = 60, sampling_interval: int = 1):
        """
        Initialize telemetry collector with duration and interval.
        
        Args:
            collection_duration: Total collection time in seconds (default: 60)
            sampling_interval: Time between samples in seconds (default: 1)
        """
        if collection_duration <= 0:
            raise ValueError("Collection duration must be positive")
        if sampling_interval <= 0:
            raise ValueError("Sampling interval must be positive")
        
        self.collection_duration = collection_duration
        self.sampling_interval = sampling_interval
        self.telemetry_data: Dict = {
            "timestamp_start": "",
            "timestamp_end": "",
            "cpu_percentages": [],
            "ram_percentages": [],
            "emotion_states": [],
            "adversarial_flags": [],
            "metadata": {
                "collection_version": "1.0.0",
                "system": "Evolution Ecosystem"
            }
        }
        self.is_collecting = False
        
    def _get_cpu_usage(self) -> float:
        """Get current CPU usage with error handling."""
        try:
            return psutil.cpu_percent(interval=0.1)
        except Exception as e:
            logger.error(f"Failed to get CPU usage: {e}")
            return 0.0  # Return safe default
    
    def _get_ram_usage(self) -> float:
        """Get current RAM usage with error handling."""
        try:
            return psutil.virtual_memory().percent