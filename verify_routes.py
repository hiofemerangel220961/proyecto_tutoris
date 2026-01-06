import requests

BASE_URL = "http://127.0.0.1:8000"

def test_routes():
    # Note: This test assumes the server is running and no auth is required to just GET the html (for now)
    # If auth is required, this will fail with 401/403 which is also informative.
    
    routes = [
        "/admin/dashboard",
        "/tutor/dashboard"
    ]
    
    for route in routes:
        try:
            response = requests.get(f"{BASE_URL}{route}")
            print(f"Route: {route}")
            print(f"Status: {response.status_code}")
            # Check for specific strings in the response to verify content
            if route == "/admin/dashboard":
                if "Dashboard del Administrador" in response.text or "Tulio Tribiño" in response.text:
                    print("Result: OK (Found Admin content)")
                else:
                    print("Result: FAILED (Admin content not found)")
            elif route == "/tutor/dashboard":
                if "Dashboard del Tutor" in response.text or "tutor@tutorias.com" in response.text:
                    print("Result: OK (Found Tutor content)")
                else:
                    print("Result: FAILED (Tutor content not found)")
            print("-" * 20)
        except Exception as e:
            print(f"Error testing {route}: {e}")

if __name__ == "__main__":
    test_routes()
