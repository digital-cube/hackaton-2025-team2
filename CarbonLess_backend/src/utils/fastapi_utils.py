import importlib

from fastapi import FastAPI, APIRouter
from src.utils.path import get_services


def load_services(app: FastAPI):
    src_path = get_services()
    routes = {}

    for service in src_path.iterdir():
        if service.is_dir() and service.name != "__pycache__":
            handlers_file = service / "api" / "__init__.py"
            if handlers_file.exists():
                try:
                    module_name = f"src.services.{service.name}.api"
                    module = importlib.import_module(module_name)
                    if hasattr(module, 'router') and isinstance(module.router, APIRouter):
                        app.include_router(
                            module.router,
                            prefix='/api'
                        )

                        routes[service.name] = []
                        for route in module.router.routes:
                            if hasattr(route, 'path') and hasattr(route, 'methods'):
                                methods = [m for m in route.methods if m != 'HEAD']
                                routes[service.name].append(f"  {', '.join(methods):8} {route.path}")
                        print(f"✅ {service.name} router loaded")
                    else:
                        print(f"  ❌ No 'router' variable found in {handlers_file}")
                except ImportError as e:
                    print(f"  ❌ Import error for {service.name}: {e}")
                except Exception as e:
                    print(f"  ❌ General error for {service.name}: {e}")

    print("\n📋 All routes by service:")
    for service_name, service_routes in routes.items():
        print(f"\n🔹 {service_name}:")
        for route in service_routes:
            print(route)