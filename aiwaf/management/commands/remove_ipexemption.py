from django.core.management.base import BaseCommand
from aiwaf.storage import get_exemption_store

class Command(BaseCommand):
    help = "Retirer une IP de la whitelist (exemptions) AIWAF"

    def add_arguments(self, parser):
        parser.add_argument("ip", type=str, help="Adresse IP à retirer")

    def handle(self, *args, **opts):
        ip = opts["ip"]
        try:
            store = get_exemption_store()
            store.remove_ip(ip)
            self.stdout.write(self.style.SUCCESS(f"✅ IP {ip} retirée des exemptions"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur en retirant {ip}: {e}"))