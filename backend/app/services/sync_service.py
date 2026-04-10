import httpx
from app.database.session import SessionLocal
from app.api.v1.cosmetics.models import Cosmetic
from app.api.v1.bundles.models import Bundle
from app.core.config import BASE_FORTNITE_URL, FORTNITE_HEADERS

def fetch_fortnite_data_sync(endpoint: str):
    with httpx.Client(headers=FORTNITE_HEADERS, timeout=60) as client:
        url = f"{BASE_FORTNITE_URL}{endpoint}"
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
        print("🚀 Buscando dados oficiais da Fortnite-API...")
        
        # 1. Busca os dados (Usando a estrutura da Documentação)
        all_data = fetch_fortnite_data_sync("/v2/cosmetics/br")
        new_data = fetch_fortnite_data_sync("/v2/cosmetics/new")
        shop_data = fetch_fortnite_data_sync("/v2/shop/br")

        # 2. Extrai as listas com segurança
        # /v2/cosmetics/br retorna uma lista direto em 'data'
        all_items = all_data.get("data", []) 
        
        # /v2/cosmetics/new retorna os itens dentro de 'data' -> 'items'
        new_items = new_data.get("data", {}).get("items", [])
        new_ids = {item.get("id") for item in new_items if item.get("id")}
        
        # /v2/shop/br organiza por 'featured' e 'daily' (simplificando para pegar todos)
        shop_ids = set()
        shop_entries = shop_data.get("data", {}).get("featured", {}).get("entries", []) + \
                       shop_data.get("data", {}).get("daily", {}).get("entries", [])
        
        for entry in shop_entries:
            for item in entry.get("items", []):
                shop_ids.add(item.get("id"))

        print(f"📊 Processando {len(all_items)} cosméticos encontrados...")

        for item in all_items:
            api_id = item.get("id")
            if not api_id: continue

            existing = db.query(Cosmetic).filter_by(api_id=api_id).first()
            
            # Estrutura: item["rarity"]["value"]
            rarity_data = item.get("rarity", {})
            rarity_val = rarity_data.get("value", "Common") if isinstance(rarity_data, dict) else "Common"
            
            if existing:
                existing.name = item.get("name", existing.name)
                existing.rarity = rarity_val
                existing.is_new = api_id in new_ids
                existing.is_on_sale = api_id in shop_ids
                # O preço geralmente vem na 'entry' da loja, 
                # você pode atualizar o preço aqui se o item estiver no shop_ids
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
        print("✅ Banco de dados sincronizado com sucesso!")

    except Exception as e:
        print(f"💥 Erro fatal na sincronização: {e}")
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