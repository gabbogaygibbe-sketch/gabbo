from fastapi import FastAPI
from mediaflow_proxy.main import app as mediaflow_app

# --------------------------------------------------
# 1. CREAZIONE APP PRINCIPALE
# --------------------------------------------------
main_app = FastAPI(
    title="MediaFlow Proxy Wrapper",
    description="Wrapper che espone tutte le rotte di MediaFlow Proxy",
    version="1.0.0",
)

# --------------------------------------------------
# 2. COPIA DELLE ROTTE DAL PROXY ORIGINALE
#    (include anche la root "/")
# --------------------------------------------------
for route in mediaflow_app.routes:
    main_app.router.routes.append(route)

# --------------------------------------------------
# 3. ENDPOINT DI INFORMAZIONI
# --------------------------------------------------
@main_app.get("/info")
def proxy_info():
    return {
        "app_name": "MediaFlow Proxy Wrapped App",
        "version": "1.0.0",
        "routes": [
            {
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name
            }
            for route in main_app.routes
        ]
    }

# --------------------------------------------------
# 4. STAMPA INFO ALL’AVVIO
# --------------------------------------------------
print("\n===== MEDIAFLOW PROXY ROUTES LOADED =====")
for route in main_app.routes:
    print(f"PATH: {route.path:<25} | METHODS: {route.methods}")
print("==========================================\n")

# --------------------------------------------------
# 5. AVVIO DEL SERVER (solo da esecuzione diretta)
# --------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(main_app, host="0.0.0.0", port=8080)
