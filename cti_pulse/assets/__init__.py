"""
Assets package for CyberPulse application
Contains styling and HTML templates
"""

from .styles import load_custom_css, get_severity_color_class, get_severity_emoji
from .templates import (
    get_header_template,
    get_ai_container_template,
    get_executive_summary_template,
    get_metric_card_template,
    get_alert_card_template,
    get_welcome_screen_template,
    get_threat_article_template,
    get_no_threats_message_template,
    get_ai_response_template
)

__all__ = [
    'load_custom_css',
    'get_severity_color_class',
    'get_severity_emoji',
    'get_header_template',
    'get_ai_container_template',
    'get_executive_summary_template',
    'get_metric_card_template',
    'get_alert_card_template',
    'get_welcome_screen_template',
    'get_threat_article_template',
    'get_no_threats_message_template',
    'get_ai_response_template'
]