"""Resend email utility for sending transactional emails via the Resend SDK."""

from __future__ import annotations

import logging
from typing import Any

from django.conf import settings

import resend

logger = logging.getLogger(__name__)


def send_email(
    *,
    to: str | list[str],
    subject: str = "",
    html: str = "",
    text: str = "",
    template_id: str = "",
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Send an email using the Resend SDK.

    When *template_id* is provided, the Resend template API is used and
    *html* / *text* / *subject* are ignored.  Otherwise a standard
    transactional email is sent.

    Parameters
    ----------
    to:
        Recipient email address(es).
    subject:
        Email subject (ignored when *template_id* is used).
    html:
        HTML body (ignored when *template_id* is used).
    text:
        Plain-text body (ignored when *template_id* is used).
    template_id:
        Optional Resend template ID.
    data:
        Template variables when *template_id* is used.

    Returns
    -------
    dict
        The JSON response from the Resend API.
    """
    if not settings.RESEND_API_KEY:
        logger.warning("RESEND_API_KEY is not configured; email not sent.")
        return {"id": "mock-email-id", "warning": "No RESEND_API_KEY configured"}

    resend.api_key = settings.RESEND_API_KEY

    recipients: list[str] = [to] if isinstance(to, str) else list(to)

    params: dict[str, Any] = {
        "from": settings.EMAIL_FROM or "noreply@example.com",
        "to": recipients,
    }

    if template_id:
        params["template_id"] = template_id
        if data:
            params["data"] = data
    else:
        if subject:
            params["subject"] = subject
        if html:
            params["html"] = html
        if text:
            params["text"] = text

    try:
        response = resend.Emails.send(params)
        logger.info("Email sent to %s via Resend (id=%s)", recipients, response.get("id"))
        return response
    except Exception:
        logger.exception("Failed to send email to %s", recipients)
        raise
