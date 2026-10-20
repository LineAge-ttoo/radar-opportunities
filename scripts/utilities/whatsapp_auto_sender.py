import os
import json
import subprocess
import urllib.parse
import requests
from datetime import datetime, timezone

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SENT_LOG_PATH = os.path.join(BASE_DIR, 'data', 'opportunities', 'whatsapp_sent_log_3222739034.json')
USER_PHONE = "573222739034"


def load_sent_log() -> dict:
    try:
        if os.path.exists(SENT_LOG_PATH):
            with open(SENT_LOG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {"sent_ids": [], "last_auto_dispatch": None}


def save_sent_log(data: dict):
    try:
        os.makedirs(os.path.dirname(SENT_LOG_PATH), exist_ok=True)
        with open(SENT_LOG_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def auto_dispatch_to_whatsapp_3222739034(scored_list: list, force: bool = False) -> dict:
    """
    Envía automáticamente las oportunidades nuevas de alto potencial al WhatsApp +57 3222739034
    sin requerir que el usuario redacte ni presione botones manualmente.
    """
    log = load_sent_log()
    sent_ids = set(log.get("sent_ids", []))

    high_pot = [
        o for o in scored_list
        if o.get('overall_score', 0) >= 88 or o.get('estimated_data', {}).get('is_huila_guadua')
    ]
    new_high_pot = [o for o in high_pot if o.get('opportunity_id') not in sent_ids]

    if not new_high_pot and not force:
        return {
            "dispatched": False,
            "reason": "Sin oportunidades nuevas pendientes por enviar",
            "target_phone": USER_PHONE
        }

    batch = (new_high_pot if new_high_pot else high_pot)[:6]
    lines = [
        "🔔 *QUE HAY PA´ HACER! — ALERTA AUTOMÁTICA*",
        "📍 *San Agustín, Huila · Guadua · Alcaldía · Estudiantes*",
        f"🕒 {datetime.now().strftime('%d/%m/%Y %I:%M %p')}",
        ""
    ]

    for idx, o in enumerate(batch, 1):
        sal = o.get('observed_data', {}).get('stated_salary') or 'Por cotizar'
        wa_client = o.get('observed_data', {}).get('whatsapp_phone') or ''
        contact_str = f"WhatsApp Solicitante: +{wa_client}" if wa_client else f"Circular/Enlace: {o.get('source_url', '')}"
        lines.append(
            f"*{idx}. {o.get('title', '')[:72]}*\n"
            f"💰 {sal}\n"
            f"📞 {contact_str}\n"
        )

    msg_text = "\n".join(lines)
    encoded_msg = urllib.parse.quote(msg_text)
    methods_used = []

    # 1. Envío vía API Cloud (CallMeBot / TextMeBot / Webhook si está activo)
    callmebot_key = os.environ.get("RADAR_CALLMEBOT_APIKEY", "").strip()
    if callmebot_key:
        try:
            r = requests.get(
                f"https://api.callmebot.com/whatsapp.php?phone={USER_PHONE}&text={encoded_msg}&apikey={callmebot_key}",
                timeout=8
            )
            if r.status_code == 200:
                methods_used.append("CallMeBot_API")
        except Exception:
            pass

    webhook_url = os.environ.get("RADAR_WA_WEBHOOK", "").strip()
    if webhook_url:
        try:
            requests.post(webhook_url, json={"phone": USER_PHONE, "message": msg_text, "opportunities": batch}, timeout=8)
            methods_used.append("Webhook_Push")
        except Exception:
            pass

    # 2. Despacho Automático en Windows (Abre el protocolo de WhatsApp y presiona ENTER automáticamente)
    is_github_actions = os.environ.get("GITHUB_ACTIONS", "").lower() == "true"
    if os.name == "nt" and not is_github_actions:
        try:
            wa_protocol_url = f"whatsapp://send?phone={USER_PHONE}&text={encoded_msg}"
            ps_script = (
                f"Start-Process '{wa_protocol_url}'; "
                f"Start-Sleep -Seconds 4; "
                f"$wshell = New-Object -ComObject wscript.shell; "
                f"$wshell.SendKeys('~')"
            )
            subprocess.Popen(
                ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps_script],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            methods_used.append("Windows_WhatsApp_AutoSend")
        except Exception:
            pass

    for o in batch:
        if o.get("opportunity_id"):
            sent_ids.add(o["opportunity_id"])

    log["sent_ids"] = list(sent_ids)[-300:]
    log["last_auto_dispatch"] = datetime.now(timezone.utc).isoformat()
    log["last_message"] = msg_text
    save_sent_log(log)

    return {
        "dispatched": True,
        "methods": methods_used or ["AutoQueue_Ready"],
        "target_phone": USER_PHONE,
        "count": len(batch),
        "message_text": msg_text,
        "wa_me_url": f"https://wa.me/{USER_PHONE}?text={encoded_msg}"
    }
