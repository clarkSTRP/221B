import uvicorn

def main():
    """
    Main entry point to launch the 221B web application server.
    """
    print("[*] Starting 221B Web Application server...")
    uvicorn.run(
        "web_host.app:app",  # Points to the 'app' instance in 'web_host/app.py'
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
