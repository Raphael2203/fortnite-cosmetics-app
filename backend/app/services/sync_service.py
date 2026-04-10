import httpx
from app.database.session import SessionLocal
from app.api.v1.cosmetics.models import Cosmetic
from app.api.v1.bundles.models import Bundle
from app.core.config import BASE_FORTNITE_URL, FORTNITE_HEADERS

def fetch_fortnite_data_sync(endpoint: str):
    with httpx.Client(headers=FORTNITE_HEADERS, timeout=60) as client:
        response = client.get(f"{BASE_FORTNITE_URL}{endpoint}")
        response.raise_for_status()
        return response.json()

def sync_cosmetics():
    db = SessionLocal()
    try:
        print("Buscando dados da API...")
        all_data = fetch_fortnite_data_sync("/cosmetics")
        new_data = fetch_fortnite_data_sync("/cosmetics/new")
        shop_data = fetch_fortnite_data_sync("/shop")

       
        all_items = all_data.get("data", {}).get("beans", [])
        new_ids = {c.get("id") for c in new_data.get("data", [])}
 
        shop_ids = set()
        for section in shop_data.get("data", {}).get("featured", {}).get("entries", []):
            for item in section.get("items", []):
                shop_ids.add(item.get("id"))

        print(f"Processando {len(all_items)} itens...")

        for item in all_items:
            api_id = item.get("id")
            if not api_id: continue

            existing = db.query(Cosmetic).filter_by(api_id=api_id).first()
            
            rarity_val = item.get("rarity", {}).get("value", "Common")
            
            if existing:
                existing.name = item.get("name", existing.name)
                existing.rarity = rarity_val
                existing.price = item.get("price", 0)
                existing.is_new = api_id in new_ids
                existing.is_on_sale = api_id in shop_ids
            else:
                new_cosmetic = Cosmetic(
                    api_id=api_id,
                    name=item.get("name", "Unknown"),
                    rarity=rarity_val,
                    price=item.get("price", 0),
                    is_new=api_id in new_ids,
                    is_on_sale=api_id in shop_ids
                )
                db.add(new_cosmetic)

        db.commit()
        print("Sincronização concluída!")
    except Exception as e:
        print(f"Erro fatal: {e}")
        db.rollback()
    finally:
        db.close()

def run_initial_sync():
    db = SessionLocal()
    count = db.query(Cosmetic).count()
    db.close()
    
    if count > 0:
        print(f"Banco já tem {count} itens. Pulando sincronização.")
        return
        
    print("🚀 Banco vazio! Iniciando carga inicial...")
    sync_cosmetics()
    print("✅ Carga finalizada!")

if __name__ == "__main__":
    run_initial_sync()