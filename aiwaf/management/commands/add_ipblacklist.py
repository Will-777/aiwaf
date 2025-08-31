from django.core.management.base import BaseCommand
from aiwaf.storage import get_blacklist_store

class Command(BaseCommand):
    help = "Ajouter une IP à la blacklist AIWAF"

    def add_arguments(self, parser):
        parser.add_argument("ip", type=str, help="Adresse IP à bloquer")
        parser.add_argument(
            "--reason",
            type=str,
            default="Manual block",
            help="Raison du blocage"
        )

    def handle(self, *args, **options):
        ip = options["ip"]
        reason = options["reason"]
        try:
            store = get_blacklist_store()
            store.add_ip(ip, reason=reason)
            self.stdout.write(self.style.SUCCESS(
                f"✅ IP {ip} ajoutée à la blacklist (raison: {reason})"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur en ajoutant {ip}: {e}"))