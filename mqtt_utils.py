import time

import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
# Cámbialo por algo único tuyo (broker público = compartido) y usa el MISMO en sketch.ino
PREFIJO = "critico_cine_demo"


def veredicto(nota):
    """Devuelve (clave, texto, emoji) según la calificación 0-10."""
    if nota >= 7:
        return "ver", "Vale la pena verla", "🟢"
    if nota >= 5:
        return "regular", "Regular", "🟡"
    return "saltar", "Mejor sáltala", "🔴"


def _cliente():
    return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)


def publicar(subtema, mensaje):
    """Publica un mensaje retenido. Devuelve True si salió bien."""
    try:
        c = _cliente()
        c.connect(BROKER, PORT, 60)
        c.loop_start()
        info = c.publish(f"{PREFIJO}/{subtema}", str(mensaje), qos=1, retain=True)
        info.wait_for_publish(timeout=5)
        c.loop_stop()
        c.disconnect()
        return info.is_published()
    except Exception:
        return False


def leer_estado(espera=1.5):
    """Lee los últimos mensajes retenidos. Devuelve dict o None si falla."""
    datos = {}

    def on_connect(c, userdata, flags, reason_code, properties):
        c.subscribe(f"{PREFIJO}/#")

    def on_message(c, userdata, msg):
        datos[msg.topic.removeprefix(PREFIJO + "/")] = msg.payload.decode(errors="ignore")

    try:
        c = _cliente()
        c.on_connect = on_connect
        c.on_message = on_message
        c.connect(BROKER, PORT, 60)
        c.loop_start()
        time.sleep(espera)
        c.loop_stop()
        c.disconnect()
        return datos
    except Exception:
        return None
