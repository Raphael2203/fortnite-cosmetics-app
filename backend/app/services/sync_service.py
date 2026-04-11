import httpx
import threading
from app.database.session import SessionLocal
from app.api.v1.cosmetics.models import Cosmetic
from app.api.v1.bundles.models import Bundle
from app.core.config import BASE_FORTNITE_URL, FORTNITE_HEADERS

def fetch_fortnite_data_sync(endpoint: str):
    with httpx.Client(headers=FORTNITE_HEADERS, timeout=60) as client:
        url = f"{BASE_FORTNITE_URL}{endpoint}"
        print(f"DEBUG: Tentando acessar URL: {url}")
        try:
            response = client.get(url)

            if response.status_code != 200:
                print(f"Erro na API: Status {response.status_code}")
                print(f"Resposta da API: {response.text}")
                return {}
            return response.json()
        except Exception as e:
            print(f"Erro na requisição: {e}")
            return {}

def sync_cosmetics():
    db = SessionLocal()
    try:
        print("Buscando dados oficiais da Fortnite-API...")
        
        all_data = fetch_fortnite_data_sync("/cosmetics/br")
        new_data = fetch_fortnite_data_sync("/cosmetics/new")
        shop_data = fetch_fortnite_data_sync("/shop")
        all_items = all_data.get("data", []) if isinstance(all_data, dict) else []
        
        new_items_list = []
        if isinstance(new_data, dict):
            new_items_list = new_data.get("data", {}).get("items", [])
        new_ids = {item.get("id") for item in new_items_list if isinstance(item, dict)}

        shop_ids = set()
        if isinstance(shop_data, dict):
            shop_entries = shop_data.get("data", {}).get("entries", [])
            for entry in shop_entries:
                for s_item in entry.get("items", []):
                    shop_ids.add(s_item.get("id"))

        print(f"Processando {len(all_items)} cosméticos encontrados...")

        for item in all_items:
            api_id = item.get("id")
            if not api_id: continue

            existing = db.query(Cosmetic).filter_by(api_id=api_id).first()
            rarity_data = item.get("rarity", {})
            rarity_val = rarity_data.get("value", "Common") if isinstance(rarity_data, dict) else "Common"
            
            if existing:
                existing.name = item.get("name", existing.name)
                existing.rarity = rarity_val
                existing.is_new = api_id in new_ids
                existing.is_on_sale = api_id in shop_ids
            else:
                new_cosmetic = Cosmetic(
                    api_id=api_id,
                    name=item.get("name", "Unknown"),
                    rarity=rarity_val,
                    price=0, 
                    is_new=api_id in new_ids,
                    is_on_sale=api_id in shop_ids
                )
                db.add(new_cosmetic)

        db.commit()
        print("Banco de dados sincronizado com sucesso!")

    except Exception as e:
        print(f"Erro fatal na sincronização: {e}")
        db.rollback()
    finally:
        db.close()

def sync_only_shop():
    db = SessionLocal()
    try:
        print("Atualizando apenas os preços da loja...")
        shop_data = fetch_fortnite_data_sync("/shop")

        if not isinstance(shop_data, dict) or "data" not in shop_data:
            print("Dados inválidos ou vazios.")
            return

        data_obj = shop_data.get("data", {})
        entries = data_obj.get("entries", [])

        if not entries:
            featured = data_obj.get("featured", {}).get("entries", []) if data_obj.get("featured") else []
            daily = data_obj.get("daily", {}).get("entries", []) if data_obj.get("daily") else []
            entries = featured + daily

        if not entries:
            print("Nenhuma entrada encontrada na loja")
            return

        db.query(Cosmetic).update({Cosmetic.is_on_sale: False})

        count = 0
        for entry in entries:
            price = entry.get("finalPrice", 0)
            for item in entry.get("items", []):
                api_id = item.get("id")
                if api_id:
                    db.query(Cosmetic).filter(Cosmetic.api_id == api_id).update({
                        "price": price,
                        "is_on_sale": True
                    })
                    count += 1

        db.commit()
        print(f"Loja atualizada: {count} itens com preços novos")
    except Exception as e:
        print(f"Erro ao sincronizar a loja: {e}")
        db.rollback()
    finally:
        db.close()

def schedule_shop_sync():
    print("Iniciando ciclo de atualização automática da loja...")
    try:
        sync_only_shop()
        print("Ciclo de atualização concluído com sucesso.")
    except Exception as e:
        print(f"Erro no ciclo de atualização: {e}")

    timer = threading.Timer(86400, schedule_shop_sync)
    timer.daemon = True
    timer.start()

def run_initial_sync():
    db = SessionLocal()
    count = db.query(Cosmetic).count()
    db.close()
    
    if count == 0:
        print("Banco vazio! Iniciando carga total em background...")
        threading.Thread(target=sync_cosmetics).start()
    else:
        print(f"Catálogo detectado ({count}) itens. Pulando Carga Pesada")

    schedule_shop_sync()

if __name__ == "__main__":
    run_initial_sync()